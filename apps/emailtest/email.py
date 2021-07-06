from imap_tools import mailbox
from core.shared.email import Email
import re


class TestEmail(Email):

    def __init__(self):
        super().__init__('emailtest')

    def read_all(self):
        return self.email()

    def gather_email(self):
        emails = self.read_all()
        tickets = [email.get('from') for email in emails]
        return tickets
