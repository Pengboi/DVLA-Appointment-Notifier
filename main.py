#!/usr/bin/python
from selenium import webdriver
import os
import datetime as dt
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


"""
Replace below details with whatever client details you wish.
These will be used when searching for earlier bookings and
for contacting the client
"""
client_email = "*insert email where notification will be sent*"
client_license_no = "*insert 16 character DVLA standard driving license number*"
client_booking_no = "*insert existing driving test booking number*"

"""
Replace below details with your chosen email details in order to 
utalise a Notification System for notifying your client regarding
earlier bookings.
"""
server_email = "*insert sender email where notification will be sent from"
server_password = "*insert sender email password for above email*"
server_smtp = "*insert sender email smtp address*" # e.g: Gmail = smtp.gmail.com


def earlier_time_available():

    url = "https://driverpracticaltest.dvsa.gov.uk/login"
    webdriver_path = os.path.abspath("chromedriver")

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")

    browser = webdriver.Chrome(webdriver_path, options=options)
    browser.get(url)

    username_field = browser.find_elements_by_xpath("//input[@name='username' and @maxlength='16']")[0]
    username_field.send_keys(client_license_no)
    password_field = browser.find_element_by_id("application-reference-number")
    password_field.send_keys(client_booking_no)
    login_field = browser.find_element_by_id("booking-login")
    login_field.click()


    #   Post-Login Page
    change_booking_button = browser.find_element_by_xpath('//*[@id="date-time-change"]')
    change_booking_button.click()


    #   Change booking type Page
    change_type_button = browser.find_element_by_xpath('//*[@id="test-choice-earliest"]')
    change_type_button.click()

    change_submit_button = browser.find_element_by_xpath('//*[@id="driving-licence-submit"]')
    change_submit_button.click()

    #   Show all booking options Page

    existing_booking_option = browser.find_element_by_class_name('is-chosen')
    existing_booking_option_date = existing_booking_option.get_attribute('data-date')

    existing_date = dt.datetime.strptime(existing_booking_option_date, '%Y-%M-%d').date()
    earliest_date = dt.datetime.strptime(existing_booking_option_date, '%Y-%M-%d').date()

    booking_options = browser.find_elements_by_class_name('BookingCalendar-date--bookable')

    for option in booking_options:
        option_date = option.find_element_by_class_name('BookingCalendar-dateLink')
        option_date = option_date.get_attribute('data-date')
        curr_option_date = dt.datetime.strptime(option_date, '%Y-%M-%d').date()

        if curr_option_date < earliest_date:
            earliest_date = curr_option_date

        elif curr_option_date > earliest_date:
            break

    browser.close()

    if earliest_date < existing_date:
        return earliest_date
    else:
        return None


def notify_client(date):
    #   Email details and HTML. Feel free to use and adapt the template below as long as accreditation is contained
    #   in the footer
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Earlier Driving Test Date Available - Lidio"
    msg['From'] = server_email
    msg['To'] = client_email
    with open('mail-template.html', 'r') as file:
        html = file.read().replace('\n', '')
    html = html.replace('DATEPLACEHOLDER', date)

    content = MIMEText(html, 'html')
    msg.attach(content)

    server = smtplib.SMTP(server_smtp, 587)  # Port 587 works with most E-mail SMTP connections
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Input login credentials here! - Sensitive Data
    server.login(server_email, server_password)

    server.sendmail(server_email, client_email, msg.as_string())
    server.quit()


#   While time between 6:01AM - 11:38PM (Time the service is active)
#   search for earlier timeslots.
#   Program entry point.

curr_time = dt.datetime.now().replace(microsecond=0)
service_start_time = curr_time.replace(hour=6, minute=0, second=0, microsecond=0)
service_end_time = curr_time.replace(hour=23, minute=38, second=0, microsecond=0)


while True:
    while service_start_time < curr_time < service_end_time:
        #   Initiate check
        earlier_date = earlier_time_available()
        if earlier_date is not None:
            notify_client(earlier_date)
        #   Sleep for 2 minutes
        time.sleep(1000)