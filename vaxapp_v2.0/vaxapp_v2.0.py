import requests
import json
import hashlib
from collections import defaultdict
import pandas as pd
import schedule
import time
import playsound
import datetime
import sys

def cowlogin():

    genotpurl = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"

    mobileno = input("\nEnter the mobile number that was used for registration on cowin : ")

    headers = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
    }
    
    payload = json.dumps({
    "mobile": mobileno
    })

    response = requests.request("POST", genotpurl, headers=headers, data=payload)
    if response.status_code == 200:
        txid = json.loads(response.text)['txnId']

        myotp = input('Enter OTP : ')
        otphash = hashlib.sha256(myotp.encode())
        otphashhex = otphash.hexdigest()
        otpdct = defaultdict(dict)
        otpdct["otp"] = otphashhex
        otpdct["txnId"] = txid
        otppayload = json.dumps(dict(otpdct))

        confotpurl = "https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP"

        sess = requests.session()
        responseotp = sess.post(confotpurl, headers=headers, data=otppayload)
        if responseotp.status_code == 200:
            print('COWIN Authentication Successful !')
            tokendata = json.loads(responseotp.text)['token']
            return sess
        else:
            print(responseotp.text)

    else:
        print(response.text)

def slotcheck(sess, datelist, age, vaccine, dose, pinlist):

    dataframelist = []

    for date in datelist:

        for pin in pinlist:

            pinurl = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={date}'

            headers = {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
            }
            pinresp = sess.get(pinurl, headers=headers)

            if pinresp.status_code == 200:
                slotdata = json.loads(pinresp.text)['sessions']
                if len(slotdata) != 0:
                    df = pd.DataFrame(slotdata)
                    df.drop(columns=['address','block_name', 'available_capacity', 'center_id', 'slots', 'district_name','lat','long','session_id','state_name','district_name', 'from', 'to'],inplace=True)
                    if dose == 1:
                        df.drop(columns=['available_capacity_dose2'],inplace=True)
                        if vaccine == 'ANY':
                            df = df[(df.min_age_limit == age)&(df.available_capacity_dose1 != 0)]
                        else:
                            df = df[(df.min_age_limit == age)&(df.vaccine == vaccine)&(df.available_capacity_dose1 != 0)]

                    elif dose == 2:
                        df.drop(columns=['available_capacity_dose1'],inplace=True)
                        if vaccine == 'ANY':
                            df = df[(df.min_age_limit == age)&(df.available_capacity_dose2 != 0)]
                        else:
                            df = df[(df.min_age_limit == age)&(df.vaccine == vaccine)&(df.available_capacity_dose2 != 0)]

                    dataframelist.append(df)
                else:
                    continue
            else:
                print(f'\nSession details request failed for pin {pin} !\n')
                print(pinresp.text)

    finaldf = pd.concat(dataframelist)
    finaldf.to_csv("10centerspmc.csv")

    if finaldf.empty != True:
        print(f"\n{age}+ age group {vaccine} dose-{dose} slots are now available at the following locations !\n")
        playsound.playsound("bell.mp3")
        print(finaldf)
    else:
        print(f"\n{age}+ age group {vaccine} dose-{dose} slots not yet available at the provided pincodes on provided dates !")

if __name__ == '__main__':
    logincowin = cowlogin()
    if logincowin != None:

        while True:
            pininput = input("\nEnter pincodes separated by comma : ")
            pininputlist = pininput.split(',')
            pinlist = []
            for i in pininputlist:
                try:
                    if len(i.strip()) == 6:
                        pinlist.append(str(int(i.strip())))
                    else:
                        print(f"Dropping invalid pin {i}")
                except ValueError:
                    print(f"Dropping invalid pin {i}")
            if len(pinlist) > 0:
                break

        while True:
            dateinput = input("\nEnter dates separated by comma in DD-MM-YYYY format: ")
            dateinputlist = dateinput.split(',')
            format = "%d-%m-%Y"
            datelist = []
            for j in dateinputlist:
                try:
                    datetime.datetime.strptime(j.strip(), format)
                    datelist.append(j.strip())
                except ValueError:
                    print(f"Dropping invalid Date {j}")
            if len(datelist) > 0:
                break
        
        while True:
            try:
                age = int(input("\nEnter age as 18 for 18+ years and 45 for 45+ years : "))
                if age == 18 or age == 45:
                    break
            except ValueError:
                print('Invalid Age input !')
                
        while True:
            try:
                vaccinelist = ['COVISHIELD', 'COVAXIN', 'SPUTNIK V', 'ANY']
                vaccine = input('\nEnter desired vaccine name COVISHIELD or COVAXIN or SPUTNIK V or any: ')
                vaccine = vaccine.upper().strip()
                if vaccine in vaccinelist:
                    break
            except ValueError:
                print('Invalid vaccine input !')

        while True:
            try:
                dose = int(input("\nEnter 1 for dose-1 or 2 fr dose-2 : "))
                if dose == 1 or dose == 2:
                    break
            except ValueError:
                print('Invalid dose input !')

        while True:
            try:
                frequency = int(input("\nEnter search interval in seconds or hit enter for default 15 seconds : ") or "15")
                if frequency == 15 or type(frequency) == int:
                    break
            except ValueError:
                print('Invalid frequency input !')

        print(f"\nNumber of pincodes entered is {len(pinlist)} ")
        print(f"Number of dates entered is {len(datelist)} ")
        print(f"Search frequency entered is {frequency}")
 
        print(f"\nThis will make {len(pinlist) * len(datelist)} number of API calls every {frequency} seconds")
        print(f"Which is {int(len(pinlist) * len(datelist) * (60/frequency) * 5)} number of API calls every 5 minutes")
        input('\nPress Enter to continue or ctrl+c to abort')
        print("\n=======================================================================================================")
        print(f"\nSearching vaccination slots availability every {frequency} seconds for age {age}+ years for {vaccine} vaccine on dates and pincodes mentioned below :")
        print(pinlist)
        print(datelist)

        # slotcheck(logincowin, datelist, age, vaccine, dose, pinlist)

        schedule.every(frequency).seconds.do(slotcheck, logincowin, datelist, age, vaccine, dose, pinlist)
        while True:
            schedule.run_pending()
            time.sleep(1)