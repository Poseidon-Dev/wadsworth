import json, os, requests
from requests.auth import HTTPBasicAuth

import core.config
from .models import TicketTable, TicketCommentTable
from .utils import clean_html

class JitBitAPI:

    def __init__(self):
        self.auth = HTTPBasicAuth(core.config.HELPDESK_USER, core.config.HELPDESK_PWD)

        if not self.test_creds():
            raise ValueError("Authorization failed, please check your credentials")
        else:
            print('Connection to Arizona Pipeline JitBit Established')

    def test_creds(self):
        """
        Ensure a connection to the JitBit API
        """
        response = self._make_request("Authorization")
        return response.status_code == 200

    def _make_request(self, method):
        """
        Default method for JitBit API calls
        """
        url = f'{core.config.HELPDESK_URL}/api/{method}'
        print(url)
        return requests.get(url, auth=self.auth)


class JitBitTickets(JitBitAPI, TicketTable):

    def __init__(self):
        JitBitAPI.__init__(self)
        TicketTable.__init__(self)
        self.columns = '(id, tech, submitter, subject, status, body)'

    def pull_ticket(self, ticket):
        """
        Retrieves individual ticket information
        """
        method = f'ticket?id={ticket}'
        response = self._make_request(method)
        ticket = json.loads(response.content)
        return ticket

    def pull_tickets(self):
        """
        Retrieves all unclosed tickets from JitBit API
        """
        method = 'Tickets/?mode=unclosed&count=50'
        response = self._make_request(method)
        tickets = json.loads(response.content)
        return tickets
            
    def push_tickets(self, tickets=None):
        """
        Pushes pulled tickets into tickets db
        """
        if not tickets:
            tickets = self.pull_tickets()
        for ticket in tickets:
            issue_id = ticket['IssueID']
            tech = ticket['TechFirstName'] if ticket['TechFirstName'] else 'None'
            submitter = ticket['UserName'] if ticket['UserName'] else 'None'
            submitter = submitter.replace('@arizonapipeline.com', '')
            subject = clean_html(ticket['Subject']) if ticket['Subject'] else 'None'
            status = ticket['Status'] if ticket['Status'] else 'None'
            body = self.get_ticket_body(ticket['IssueID']) if ticket['IssueID'] else 'None'
            values = (str(issue_id), str(tech), str(submitter), str(subject), str(status), str(body))
            self.insert_or_replace(values, self.columns)

    def check_ticket_differences(self):
        """
        Compare JitBit tickets with tickets in local db
        Update local db to match JitBit Current
        """        
        current_tickets = self.pull_tickets()
        jitbit_tickets = [ticket['IssueID'] for ticket in current_tickets]
        db_tickets = [ticket[0] for ticket in self.select_columns(columns='ID', table='ticket_table')]
        set_changes = set(jitbit_tickets).symmetric_difference(db_tickets)
        if set_changes:
            tickets = {'JitBit' : jitbit_tickets, 'db' : db_tickets, 'diff' : set_changes}
            for key in tickets['diff']:
                if key in tickets['db']:
                    self.delete_row_by_key(key)
                if key in tickets['JitBit']:
                    ticket = self.pull_ticket(key)
                    issue_id = ticket['TicketID']
                    tech = ticket['AssigneeUserInfo']['FirstName'] if ticket['AssigneeUserInfo'] else 'None'
                    submitter = ticket['UserName'] if ticket['UserName'] else 'None'
                    submitter = submitter.replace('@arizonapipeline.com', '')
                    subject = clean_html(ticket['Subject']) if ticket['Subject'] else 'None'
                    status = ticket['Status'] if ticket['Status'] else 'None'
                    body = clean_html(ticket['Body']) if ticket['Body'] else 'None'
                    values = (str(issue_id), str(tech), str(submitter), str(subject), str(status), str(body))
                    self.insert_or_replace(values, self.columns)
                else:
                    return None
        else:
            raise Exception('No changes found')
          

    def get_ticket_body(self, id):
        """
        Retrieves Body from ticket API
        """
        method = f'ticket?id={id}'
        response = self._make_request(method)
        ticket = json.loads(response.content)
        body = clean_html(ticket['Body'])
        return body


class JitBitTicketComments(JitBitAPI, TicketCommentTable):

    def __init__(self):
        JitBitAPI.__init__(self)
        TicketCommentTable.__init__(self)
        self.columns = '(id, ticket_id, ticket_user, type, body)'

    def pull_comment(self, ticket):
        """
        Pull comments for a select ticket
        """
        method = f'comments?id={ticket}'
        response = self._make_request(method)
        comments = json.loads(response.content)
        return comments

    def push_comment(self, ticket: str):
        """
        Push comment into local db
        """
        for comment in self.pull_comment(ticket):
            comment_id = comment['CommentID']
            ticket_id = comment['IssueID']
            ticket_user = comment['UserName'] if comment['UserName'] else 'None'
            comment_type = comment['ForTechsOnly']
            body = clean_html(comment['Body']) if clean_html(comment['Body']) else 'None'
            values = (str(comment_id), str(ticket_id), str(ticket_user), str(comment_type), str(body))
            self.insert_or_replace(values, self.columns)

    def push_comments(self):
        """
        Batch process push_comments to populate local db with all available tickets
        """
        tickets = self.select_columns(columns='id', table='ticket_table')
        for ticket in tickets:
            self.push_comment(ticket[0])
