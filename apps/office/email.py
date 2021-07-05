from core.shared.email import Email
import re


class OfficeEmail(Email):

    def __init__(self):
        super().__init__('office')

    def read_all(self):
        return self.email()

    def gather_keys(self):
        emails = self.read_all()
        for email in emails:
            email = str(email.get('body')).split()
            for word in email:
                if word.lower() == 'code:':
                    idx = email.index(word) + 1 
                    return email[idx]
