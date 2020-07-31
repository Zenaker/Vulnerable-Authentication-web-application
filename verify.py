import smtplib
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

def sendEmail(email, hash_link):
    fromaddr = config.get("smtp", "email")
    toaddrs  = email
    msg = '\nHello here is your password reset link: ' + hash_link
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(config.get("smtp", "email"),config.get("smtp", "password"))
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
