# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from xutils import (handle_exception,
                    CustomLogger)


EmailLogger = CustomLogger('EmailLogger')


@handle_exception(EmailLogger)
def send(subject, text, sender, username, password, host, receiver):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = subject
    smtp = smtplib.SMTP()
    smtp.connect(host)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
