from bs4 import BeautifulSoup
import discord, re

import core.config

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, features="html.parser")
    cleantext = soup.get_text()
    cleantext = cleantext.replace('\n', '')
    cleantext = cleantext.replace('\t', '')
    cleantext = cleantext.replace('\r', '')
    cleantext = cleantext.replace("'", '')
    cleantext = cleantext.replace("\"", ' ')
    cleantext = cleantext.replace(":", ' ')
    cleantext = cleantext.replace("(", ' ')
    cleantext = cleantext.replace(")", ' ')
    cleantext = cleantext.replace("#", ' ')
    cleantext = cleantext.replace("-", ' ')
    cleantext = cleantext.replace(",", '  ')
    cleantext = cleantext.replace(u'\xa0', u' ')
    return cleantext
    

def pretty_ticket(message, ticket):
    """
    Returns an embed for tickets for a prettier discord format
    """
    tech = ticket.get('AssigneeUserInfo')
    if tech:
        tech = tech.get('Username')
    else:
        tech = 'None'

    embed = discord.Embed(
        title=f'**{ticket.get("Subject")}**',
        color=0x03f8fc,
        url=ticket.get("Url"),
        )
    embed.add_field(
        name=f'Employee',
        value=f"""
        > Status: {ticket.get("Status")}\n> 
        > User : {ticket.get("SubmitterUserInfo").get("FullName")}\n> 
        > Tech: {tech}\n 
        """,
        inline=False)
    embed.add_field(name='Body', value=clean_html(ticket.get('Body')), inline=False)
    embed.set_footer(text=f"Requested by {message.author.display_name}")
    return embed

    # {'SubmitterUserInfo': {
    #     'UserID': 5842245,
    #     'Username':
    #     'clg1',
    #     'Email':
    #     'cgarza@arizonapipeline.com',
    #     'IsAdmin': False,
    #     'Disabled': False,
    #     'FirstName':'Christina',
    #     'LastName': 'Garza', 
    #     'Notes': '', 
    #     'Location': 'Las Vegas', 
    #     'Phone': '7609531175', 
    #     'CompanyName': 'Arizonapipeline', 
    #     'DepartmentName': None, 
    #     'IPAddress': '68.224.89.250', 
    #     'HostName': '68.224.89.250', 
    #     'Lang': '', 
    #     'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
    #     'AvatarURL': None, 
    #     'Signature': None, 
    #     'Greeting': None, 
    #     'CompanyId': 1103650, 
    #     'DepartmentID': None, 
    #     'DarkMode': False, 
    #     'CompanyNotes': None, 
    #     'SendEmail': True, 
    #     'IsTech': False, 
    #     'LastSeen': '2021-06-28T21:57:00Z', 
    #     'RecentTickets': None, 
    #     'IsManager': False, 
    #     'IsDepartmentManager': False, 
    #     'TwoFactorAuthEnabled': False, 
    #     'OutOfOffice': False, 
    #     'LastPasswordChange': None, 
    #     'FullNameAndLogin': 'Christina Garza (clg1)', 
    #     'FullName': 'Christina Garza'}, 
    # 'CategoryName': 'iPads', 
    # 'AssigneeUserInfo': None, 
    # 'Url': 'https://support.arizonapipeline.com/helpdesk/Ticket/38615312', 
    # 'ViewingTechNames': [], 
    # 'Origin': 'WebApp', 
    # 'IsActiveChat': False, 
    # 'Tags': [], 
    # 'OnBehalfUserName': None, 
    # 'Integrations': {}, 
    # 'IssueDate': '2021-06-28T21:56:50.96Z', 
    # 'Subject': 'IPAD Request', 
    # 'Body': '<!--html-->Hello I would like to request an Ipad for - #10959 James Fleischhacker<div><br>\r\n</div>\r\n<div>Please ship to Carson City Division Attn - Amanda Patiga</div>\r\n<div><br>\r\n</div>\r\n<div>Thank you</div>', 
    # 'Priority': 0, 
    # 'DueDate': None, 
    # 'StartDate': None, 
    # 'TimeSpentInSeconds': 897, 
    # 'LastUpdated': '2021-06-28T21:56:50.96Z', 
    # 'UpdatedByUser': False, 
    # 'UpdatedByPerformer': False, 
    # 'UpdatedForTechView': False, 
    # 'Attachments': [], 
    # 'Status': 'New', 
    # 'StatusStopTimeSpent': False, 
    # 'StatusID': 1, 
    # 'TicketID': 38615312, 
    # 'UserID': 5842245, 
    # 'AssignedToUserID': None, 
    # 'CategoryID': 61358, 
    # 'ResolvedDate': None, 
    # 'IsCurrentUserTechInThisCategory': True, 
    # 'SubmittedByCurrentUser': False, 
    # 'IsShared': False
    # }


def pretty_comment(ctx, comment):
    """
    Returns an embed for ticket comments for a prettier discord format
    """
    embed = discord.Embed(
    author=comment[2],
    color=discord.Color.green()
    )
    embed.add_field(name='User', value=comment[2], inline=True)
    embed.add_field(name='Tech only', value=comment[3], inline=True)
    embed.add_field(name='Message', value=comment[4], inline=False)
    embed.add_field(name='\u2800', value=('\u2800' * 65), inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
    return embed


def extract_ticket_from_url(url_input):
    ticket_url = f'{core.config.HELPDESK_URL}/Ticket/'
    return re.sub(ticket_url,"", url_input)
