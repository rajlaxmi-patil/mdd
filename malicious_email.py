# -*- coding: utf-8 -*-
import smtplib
import imaplib, email 
from email.mime.text import MIMEText
from email.header import Header
import unicodedata
import re
import os
import time
import sys
import threading
import pdb

def sendMail(subject, message):

  # Python code to illustrate Sending mail from  
  # your Gmail account  
  
  # creates SMTP session 
  s = smtplib.SMTP('smtp.gmail.com', 587) 
  
  # start TLS for security 
  s.starttls() 
  
  # Authentication 
  s.login("oscmdreceiver@gmail.com","dsu@12345") 
  
  msg = MIMEText(message, _charset="UTF-8")
  msg['Subject'] = Header(subject, "utf-8")
  
  # sending the mail 
  s.sendmail("oscmdreceiver@gmail.com", "rajlaxmipatil92@gmail.com", msg.as_string()) 
  
  # terminating the session 
  s.quit() 
  
  
  
def receiveMail():
  #python code to receive a mail
  user = 'oscmdsender@gmail.com'
  password = 'dsu@12345'

  mail = imaplib.IMAP4_SSL('imap.gmail.com')
  mail.login(user, password)
  mail.list()
  # Out: list of "folders" aka labels in gmail.
  mail.select("inbox") # connect to inbox.
  result, data = mail.search(None, "(UNSEEN)",'(SUBJECT "mdd")')

  ids = data[0] # data is a list.
  id_list = ids.split() # ids is a space separated string
  latest_email_id = id_list[-1] # get the latest

  # fetch the email body (RFC822) for the given ID
  result, data = mail.fetch(latest_email_id, "(RFC822)") 

  raw_email = data[0][1] # here's the body, which is raw text of the whole email
  # including headers and alternate payloads

  email_message = email.message_from_string(str(raw_email))
  pdb.set_trace()

  print (email_message['To'])

  print (email.utils.parseaddr(email_message['From'])) # for parsing "Yuji Tomita" <yuji@grovemade.com>

  print (email_message.items()) # print all headers


  return 0


def main():
    #Daemon creation which checks mail
    print("Starting MDD assistant",len(sys.argv))
    while True:
        cmd = receiveMail()
        if cmd:

            os_cmd = "python mal_detect.py "+ cmd + " | tee cmd_output.txt"
            print('Command is:', os_cmd)
            os.system( os_cmd )
            # using decode() function to convert byte string to string
            f = open("cmd_output.txt","r")
            returned_output = f.read()
            print('Output to command:', returned_output)
            if "bad" in returned_output:
                message = "Domain: " + os_cmd + "Confidence level: " + returned_output.split("\n")[0]
                t1 = threading.Thread(target= sendMail, args=("Malicious Domain Detected",message,))
                t1.start()
                t1.join()
    #sendMail("oscmd",message)
    #time.sleep(5)

main()
