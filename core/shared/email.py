import smtplib, imaplib, ssl, email
from imap_tools import MailBox, AND
from email.message import EmailMessage

import core.config

class Email:

    def __init__(self, folder='INBOX'):
        self.folder = folder

    def access_imap(self, folder=None):
        if not folder:
            folder = self.folder
        with MailBox(core.config.EMAIL_IMAP).login(core.config.EMAIL_UID, core.config.EMAIL_PWD, folder) as mailbox:
            access = mailbox
        return access

    def email(self, folder=None):
        if not folder:
            folder = self.folder
        with MailBox(core.config.EMAIL_IMAP).login(core.config.EMAIL_UID, core.config.EMAIL_PWD, folder) as mailbox:
            mail = [{
                    'from': msg.from_, 
                    'subject': msg.subject, 
                    'body': msg.text} 
                    for msg in mailbox.fetch(
                        AND(seen=False), 
                        mark_seen=True)]

            return mail