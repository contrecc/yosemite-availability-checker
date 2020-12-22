#! python3
import certifi
import json
import urllib3
import requests
import smtplib
import datetime

date = "2020-09-18"
url = "https://www.recreation.gov/api/ticket/availability/facility/300015?date={}".format(
    date)

toAddress = ["first_email_address_to_send_message_to", "second_email_address_to_send_message_to"]

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
response = http.request('GET', url)
data = json.loads(response.data.decode('ISO-8859-1'))

spaces_taken = data[0]["reservation_count"]["ANY"]
spaces_available = 1400 - int(spaces_taken)

if spaces_available > 0:
    conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
    conn.ehlo()  # call this to start the connection
    # starts tls encryption. When we send our password it will be encrypted.
    conn.starttls()
    conn.login('email_address_to_send_email_from', 'password_for_email_to_send_email_from')
    conn.sendmail('email_address_to_send_email_from', toAddress,
                  'Subject: Yosemite Availability on {} is {} spaces available\n\nhttps://www.recreation.gov/ticket/facility/tour/3000'.format(
                      date, str(spaces_available)))
    conn.quit()
    print('Sent notificaton e-mails for the following recipients:\n')
    for i in range(len(toAddress)):
        print(toAddress[i])
    print('')
else:
    print("\nAt {}, for the date {}, there were {} spaces available".format(
        datetime.datetime.now().time(), date, str(spaces_available)))
