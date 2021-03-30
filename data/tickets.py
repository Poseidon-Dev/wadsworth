import json, os, sys, re, requests, sched, time
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from datetime import date

from data.base import DB

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

class TicketTable(DB):
    """
    Retrieves ticket data from JitBit API for a local store
    """
    
    def __init__(self):
        super(TicketTable, self).__init__()
        self.columns = '(tech, subject, status, body)'
        self.table = 'ticket_table'

    def create_table(self):
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id                  INT             PRIMARY KEY,
            tech                VARCHAR(100),
            subject             VARCHAR(256),
            status              VARCHAR(30),
            body                TEXT
        );
        """
        self.execute(command)

    def run(self):
        self.create_table()


class TicketCommentTable(DB):

    def __init__(self):
        super(TicketCommentTable, self).__init__()
        self.columns = ('ticket_id','user','type','body')
        self.table = 'ticket_comments'

    def create_table(self):
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id                 INT             PRIMARY KEY,
            ticket_id          INT,
            ticket_user        VARCHAR(100),
            type               BOOLEAN,
            body               TEXT,
            CONSTRAINT fk_ticket_table
                FOREIGN KEY(ticket_id) 
                REFERENCES ticket_table(ID)
                ON DELETE CASCADE
        );
        """
        self.execute(command)

    def run(self):
        self.create_table()

class JitBitAPI:

    def __init__(self):
        self.auth = HTTPBasicAuth(config.HELPDESK_USER, config.HELPDESK_PWD)

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
        url = f'{config.HELPDESK_URL}/api/{method}'
        print(url)
        return requests.get(url, auth=self.auth)


class JitBitTickets(JitBitAPI, TicketTable):

    def __init__(self):
        JitBitAPI.__init__(self)
        TicketTable.__init__(self)
        self.columns = '(id, tech, subject, status, body)'

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
            subject = clean_html(ticket['Subject']) if ticket['Subject'] else 'None'
            status = ticket['Status'] if ticket['Status'] else 'None'
            body = self.get_ticket_body(ticket['IssueID']) if ticket['IssueID'] else 'None'
            values = (str(issue_id), str(tech), str(subject), str(status), str(body))
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
                    tech = ticket['AssigneeUserInfo']['FirstName'] if ticket['AssigneeUserInfo']['FirstName'] else 'None'
                    subject = clean_html(ticket['Subject']) if ticket['Subject'] else 'None'
                    status = ticket['Status'] if ticket['Status'] else 'None'
                    body = clean_html(ticket['Body']) if ticket['Body'] else 'None'
                    values = (str(issue_id), str(tech), str(subject), str(status), str(body))
                    self.insert_or_replace(values) 
                    return issue_id
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



def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, features="html.parser")
    cleantext = soup.get_text()
    cleantext = cleantext.replace('\n', '')
    cleantext = cleantext.replace('\t', '')
    cleantext = cleantext.replace('\r', '')
    cleantext = cleantext.replace("'", '')
    cleantext = cleantext.replace("\"", ' ')
    cleantext = cleantext.replace(u'\xa0', u' ')
    return cleantext
