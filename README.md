# DVLA Appointment Notifier

DVLA Appointment Notifier utalises Selenium to interact with Gov.uk's DVLA Driving Test Portal in order to find and notify clients of earlier appointment times upon cancellation.

## Prerequisites
* [Selenium](https://www.selenium.dev) - Browser Automation Framework
* [Google Chrome](https://www.google.com/intl/en_uk/chrome/) - Browser of choice

## Usage
To use the script, there's two things you need:
1. You must have the client's Driving License No. & Existing Test Booking No.
2. You must have an SMTP capable email address in order to receive notifications for earlier appointments

❗ **Please ensure never to leave any sensitive information present in Version Control!** ❗

To get started, at the top of the script make sure to replace all client placeholder values with appropriate substitutes

```python
"""
Replace below details with whatever client details you wish.
These will be used when searching for earlier bookings and
for contacting the client
"""
client_email = "*insert email where notification will be sent*"
client_license_no = "*insert 16 character DVLA standard driving license number*"
client_booking_no = "*insert existing driving test booking number*"
```

Then proceed by replacing all server placeholder values with appropriate substitutes
```python
"""
Replace below details with your chosen email details in order to 
utalise a Notification System for notifying your client regarding
earlier bookings.
"""
server_email = "*insert sender email where notification will be sent from"
server_password = "*insert sender email password for above email*"
server_smtp = "*insert sender email smtp address*" # e.g: Gmail = smtp.gmail.com
```
❗ **Again, please ensure not to include any sensitive information in Version Control!** ❗

Afterward, you should be good to go! Once the script is running, it will automatically check every ~16 minutes for any cancellations. The script will only run during 6AM - 11:30PM which is when the DVLA Driving Test Booking WebApp is accessible

*Pro tip: Feel free to run this script on an AWS Instance*

## Future Goals
* Implement headless browser automation to eliminate chrome GUI (so i can migrate script to home server)

* Add script argument parameters, so that client/server details can be adapted as needed

* Make a more kawaii email template

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Need Any Help?
Feel free to [contact me.](mailto:im@pengboi.com)

## License
[MIT](https://choosealicense.com/licenses/mit/)
