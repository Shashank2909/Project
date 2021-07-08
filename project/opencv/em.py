import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

EMAIL_LIST = []
file = open("mailbook.txt","r")
lines = file.readlines()
for line in lines:
    EMAIL_LIST.append(line.strip())

def SendMail():
    global EMAIL_LIST
    if len(EMAIL_LIST)<1:
        EMAIL_LIST.append('sajgaonkar007@gmail.com')
    
    #img_data = ImgFileName
    msg = MIMEMultipart()
    msg['Subject'] = 'Alert'
    msg['From'] = 'projectfinal009@gmail.com'
    msg['To'] = 'sajgaonkar007@gmail.com'

    text = MIMEText("test")
    msg.attach(text)
    #image = MIMEImage(img_data, name=ImgFileName)
    #msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 25)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('projectfinal009@gmail.com', 'ProjectFinal@009')
    s.sendmail('projectfinal009@gmail.com', EMAIL_LIST, msg.as_string())
    s.quit()


