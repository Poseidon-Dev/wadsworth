from core.shared.email import Email
import re


class DirectoryEmail(Email):

    def __init__(self):
        super().__init__('LOA')

    def read_all(self):
        return self.email()

    def gather_employees(self):
        emails = self.read_all()
        ee_ids = [re.findall('\d{5}', email.get('body')) for email in emails][0]
        return ee_ids
