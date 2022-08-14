#!/usr/bin/python3

import sys
import smtplib
import argparse
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def main():
    parser = argparse.ArgumentParser(description="HTML mail sender.")
    parser.add_argument('-mf','--message_file', help="HTML mail template.")
    parser.add_argument('-r','--recipient', help="Recipient(s) emaill address. You can use comma (,) for multiple recipients.")
    parser.add_argument('-tm', '--test_mode', help="If you want to test script without any CC you can run test mode.", action='store_true')
    parser.add_argument('-img', '--image', help="Image(s) in HTML. You can use comma seperator. USAGE: -img image.png", )
    parser.add_argument('-t', '--type', help="Type of email. AVAIBLE: \{leak, ransom, vulnerability\}", required=True)
    args = parser.parse_args()

    recipients = args.recipient
    smtp = connect()

    msg = MIMEMultipart("alternative")
    subject = ""
    msg_from = ""

    if args.type == "leak":
        msg_from = "Example <example@example.com>"
        subject = "Report"

    elif args.type == "ransom":
        msg_from = "Example <example@example.com>"
        subject = "Report"

    elif args.type == "vulnerability":
        msg_from = "Example <example@example.com>"
        subject = "Report"
    
    else:
        print("Wrong type !!! Exiting.")
        return

    msg["Subject"] = subject
    msg["From"] = msg_from
    msg["To"] = recipients

    #Check is test mode?
    if args.test_mode is not None:
        print("Script running on test mode, there is no  user in CC.")
    else:    
        msg["CC"] = "examlecc@example.com"

    #Create Message body
    text = MIMEText(open(args.message_file, 'r', encoding='utf8').read(), 'html')
    #Attach text to msg
    msg.attach(text)

    #Check there is any image?
    if args.image is not None:
        img_part = MIMEImage(open(args.image, 'rb').read())
        img_part.add_header('Content-ID', "<{}>".format(args.image))
        #Attach img
        msg.attach(img_part)
    print("Mail sending...")
    smtp.sendmail(msg_from, recipients.split(","), msg.as_string())
    smtp.quit()
    print("Mail sended to {}.".format(recipients))


def connect():
    smtp_user = ""
    smtp_pass = ""

    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)
        print("Connected to smtp server...")
        return smtp
        

    except Exception as e:
        exc_type, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("!!!! ERROR !!!!")
        print(exc_type, fname, exc_tb.tb_lineno)
        print("There is an error occured: {0}".format(e))

   
if __name__ == "__main__":
    main()
