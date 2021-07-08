from core.shared.email import Email
import re


class DirectoryEmail(Email):

    def __init__(self):
        super().__init__('LOA')

    def read_all(self):
        return self.email()

    def gather_loa(self):
        emails = self.read_all()
        loa_data = []
        for email in emails:
            ee_id = re.findall('\d{5}', email.get('subject'))[0]
            command = email.get('body').split()[0]
            loa_data.append((ee_id, command))
        return loa_data
