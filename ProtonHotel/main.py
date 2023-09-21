import smtplib
import ssl
from email.message import EmailMessage
import random
import time
import vlc

# Define email sender and receiver
email_sender = 'glory.am@proton.me'
email_password = '6MrLRmCEWBRE4810agS1LA'

# Set the subject and body of the email
subjects = ['Reservation at the hotel', 'Reservation at hotel', 'Reservation at your hotel', 'Reservation', 'Question from Neilsone Christian', 'Neilsone Christian: Reservation']
bodies = []

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
        print('Message to ' + user + ' was sent\nFalling asleep...')
        file = open('./hotelsUsed.txt', 'a', encoding='utf-8')
        file.write(user + '\n')
        if user != email_receiver[len(email_receiver) - 1]:
          time.sleep(10)

p = vlc.MediaPlayer("./complete.mp3")
p.play()

print('Program is shutting down.')