from imap_tools import mailbox
from core.shared.email import Email
import re


class SupportEmail(Email):

    def __init__(self):
        super().__init__('support')

    def read_all(self):
        return self.email()

    def gather_tickets(self):
        emails = self.read_all()
        tickets = [re.findall('\d{8}', email.get('subject')) for email in emails]
        return tickets
