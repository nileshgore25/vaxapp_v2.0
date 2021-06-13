# vaxapp_v2.0
Application to check vaccine slot availability

Description:

This application takes several inputs from the user and it will alert (bell sound) when the vaccine of the requested criteria is available for booking at any of the vaccination centers at the provided pin code locations.
As soon as the bell rings, user need to immediately login to COWIN application via browser (the normal vaccine slot booking procedure) and schedule the appointment via pin search method using the pin code (at which the slots are available) displayed in this application result.
It might be possible that by the time the user logs in and try to schedule the vaccination appointment at the pin code got from the application result, the slots get already booked.
The only thing that this application helps is to continuously check the vaccination slots availability without the need for user to keep checking the slots availability manually for long duration.
To abort the application at any time, press ctrl+c.

User should not pay anything to any one for using this application, it is available for free use. Please download from the following link
Application download Link:
https://github.com/nileshgore25/vaxapp_v2.0.git

This application will only work with windows operating system and tested only on windows 10 operating system.

How to use?
1.	Download the zip file from the application download link mentioned above.
2.	Unzip the file to any desired location on your windows computer.
3.	Navigate to this location: vaxapp_v2.0 > dist
4.	Under dist folder, you will see 2 files one is “bell.mp3” another is “vaxapp_v2.0.exe”
5.	Double click “vaxapp_v2.0.exe” which will open a terminal window and then follow the instructions there on.
6.	Maximize the terminal widow for better view and full information about the center when it is displayed. 


Application Inputs:
1)	Mobile number that was used for registration on COWIN app
2)	OPT received on mobile after entering the in this application
3)	List of pin codes of the desired locations
4)	List of dates for which slot availability need to be checked
5)	Age - slots to be checked for 18-44 years or 45+ years
6)	desired vaccine name that should be exactly matched with what mentioned on COWIN portal, input any if no preference for the vaccine
7)	dose number - slot checking for dose 1 or dose 2
8)	Search interval in seconds 

Important Information:
1)	The slot availability is checked once every 15 seconds by default if no input is provided.
2)	This application is prepared using the public APIs made available at the following website. Please visit the following link to understand the terms and conditions of usage as laid down by COWIN.
https://apisetu.gov.in/public/api/cowin/cowin-public-v2

3)	One important thing mentioned on the above link is - "The appointment availability data is cached and may be up to 5 minutes old. Further, these APIs are subject to a rate limit of 100 API calls per 5 minutes per IP"

The number of API calls this application will make
Generate OTP - 1
Confirm OTP - 1
Every 15 Secs - Number of pin codes provided in the user input

Example - In case you provide 10 pin codes and 3 dates then this application will make
30 API calls every 15 secs
120 API calls every 1 minute
600 API calls every 5 minutes – which is higher than the number specified on the “apisetu” url. 

However as per testing of this application the test account was not blocked even when it was running for more than 2 hours with 10 pin codes and 3 dates with 15 seconds’ search interval.

4)	The COWIN application when logged in via any browser logs out user after few minutes or even logs out the user when the user hit search for high number of times in short period.
This application does not face such issue; the session is not terminated for long hours and it worked as expected.

Disclaimer:

•	This application neither guarantee the slot availability nor guarantee that it is 100% error free.
•	It is prepared out of personal interest for personal use, and since it was found very useful the publisher has decided to make it publicly available.
•	Although the application uses public APIs, the publisher is not responsible for any legal consequences of using it.
•	The publisher is also not responsible in case the user account is blocked for any reason.

Application Input and output example:

Enter the mobile number that was used for registration on cowin : 98*******1
Enter OTP : 793767
COWIN Authentication Successful !

Enter pincodes separated by comma : 411035, 411033, 411017, 411018, 411044, 411057, 411039 ,411027, 411007, 412207

Enter dates separated by comma in DD-MM-YYYY format: 13-06-2021, 14-06-2021, 15-06-2021

Enter age as 18 for 18+ years and 45 for 45+ years : 18

Enter desired vaccine name COVISHIELD or COVAXIN or SPUTNIK V or any: any

Enter 1 for dose-1 or 2 fr dose-2 : 1

Enter search interval in seconds or hit enter for default 15 seconds :

Number of pincodes entered is 10
Number of dates entered is 3
Search frequency entered is 15

This will make 30 number of API calls every 15 seconds
Which is 600 number of API calls every 5 minutes

Press Enter to continue or ctrl+c to abort

=========================================================================================

Searching vaccination slots availability every 15 seconds for age 18+ years for ANY vaccine on dates and pincodes mentioned below :
['411035', '411033', '411017', '411018', '411044', '411057', '411039', '411027', '411007', '412207']
['13-06-2021', '14-06-2021', '15-06-2021']

18+ age group ANY dose-1 slots not yet available at the provided pincodes on provided dates !

18+ age group ANY dose-1 slots are now available at the following locations !

                   name  pincode fee_type        date  available_capacity_dose1  fee  min_age_limit     vaccine
1  S***a Hospital Wakad   411057     Paid  14-06-2021                         1  780             18  COVISHIELD
18+ age group ANY dose-1 slots not yet available at the provided pincodes on provided dates !
18+ age group ANY dose-1 slots not yet available at the provided pincodes on provided dates !
