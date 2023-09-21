import smtplib
import ssl
from email.message import EmailMessage
import random
import time
import socks
import urllib.parse

# Define email sender and receiver
email_sender = 'glory.am@proton.me'
email_password = '6MrLRmCEWBRE4810agS1LA'

# Set the subject and body of the email
subjects = ['Reservation at the hotel', 'Reservation at hotel', 'Reservation at your hotel', 'Reservation', 'Question from Neilsone Christian', 'Neilsone Christian: Reservation']
bodies = ["""
Hello!

I would like to make a reservation at your hotel for the following dates: September 3 to September 10. I need a room for two adults. Please specify the price and availability.

If it is possible I would like to continue communication in telegram chat. Here is the link to my account - https://t.me/mistor4e

Regards,
Neilsone Dane Christian
""",
"""
Hey! 
 
I would like to make a reservation at your hotel for the following dates: 3.9.2023 - 10.9.2023. I need a room for two adults. Please indicate price and availability. 
 
If possible, I would like to continue communication on Telegram. Here is the link to my account - https://t.me/mistor4e 
 
respectfully,
Neilson Dane Christian
""",
"""
Good morning! 
 
I would like to book your company hotel for the following dates: September 3-10. I need a room for two adults. Indicate price and availability. 
 
I would like to continue communication through Telegram chat if possible. Here is the link to my account: https://t.me/mistor4e 
 
with my best wishes,
Nelson Dean Christian
""",
"""
Hello!
 
I would like to book your hotel for the following dates: 3-10. September. I need a room for two adults. Provide price and availability.
 
I would like to continue to communicate via Telegram chat if possible. Here is the link to my account: https://t.me/mistor4e
 
With my best wishes,
Nelson Dean Christian
"""]

global email_receiver

with open('./hotelsList.txt') as f:
  email_receiver = f.read().splitlines()

with open('./hotelsUsed.txt') as f:
  usedHotels = f.read().splitlines()

res = list(set(email_receiver) & set(usedHotels))

if len(res) > 0:
    print('Already used email detected')
    for i in range(0, len(res)):
        print('Deleting email - ' + res[i])
        email_receiver.remove(res[i])

context = ssl.SSLContext(ssl.PROTOCOL_TLS)

connection = smtplib.SMTP('127.0.0.1', 1025)
connection.ehlo()
connection.starttls(context=context)
connection.ehlo()

with connection as smtp:
    smtp.login(email_sender, email_password)
    print('Logged in successfully.')
    for user in email_receiver:
        print('Waking up.')
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = user
        em['Subject'] = random.choice(subjects)
        em.set_content(random.choice(bodies))
        smtp.sendmail(email_sender, user, em.as_string())
        print('Message to ' + user + ' was successfully sent\nFalling asleep...')
        file = open('./hotelsUsed.txt', 'a', encoding='utf-8')
        file.write(user + '\n')
        if user != email_receiver[len(email_receiver) - 1]:
          time.sleep(60)

print('Program is shutting down.')