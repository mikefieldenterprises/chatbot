# MESSENGER MODULE
from email.mime.text import MIMEText    # For sending email
from subprocess import Popen, PIPE      # For sending email
import logging
import chatbot.config as config
import chatbot.daoclientconfig as daoclientconfig

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def isValidEmail( inputtext ):
    if inputtext.rfind( "." ) <= inputtext.find("@"):
        return False
    else:
        return True

def sendEmail( to, cc, subject, body ): 
    msg = MIMEText( str(body) )
    msg['From'] = config.EMAIL_FROM
    msg['To'] = to
    msg["Cc"] = cc
    msg["Bcc"] = daoclientconfig.getEmailBCC()
    msg['Subject'] = subject
    # p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    # p.communicate(msg.as_bytes())

    smtpObj = smtplib.SMTP( config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login( config.EMAIL_SMTP_USER, config.EMAIL_SMTP_PWD)
    text = msg.as_string()
    smtpObj.sendmail( config.EMAIL_FROM, to, text)
    smtpObj.quit()
    logging.debug("Sent email to "+to)