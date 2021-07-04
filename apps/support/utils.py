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
    

def pretty_ticket(ticket):
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
        > Category : {ticket.get("CategoryName")[:35]}\n> 
        > User : {ticket.get("SubmitterUserInfo").get("FullName")}\n> 
        > Tech: {tech}\n 
        """,
        inline=False)
    embed.add_field(name='Body', value=clean_html(ticket.get('Body')), inline=False)
    return embed

support_dict = {
    'yes': '<:yes:852980400589766697>',
}
support_emoji_list = [k for k, v in support_dict.items()]


property_dict = {
    2: ['<:iphone:860220718440251454>', 'iphone'],
    4: ['<:laptop:860213753312575519>', 'laptop'],
    5: ['<:ipad:860220923827585074>', 'ipad'],
    9: ['<:mail:860220741966233630>', 'mail'],
    10: ['<:cards:860220653654376459>', 'cards'],
    70: ['<:docuware:860216636120629298>', 'docuware'],
    75: ['<:concur:860220678748635177>', 'concur']
}

property_emoji_names = [val[1] for k, val in property_dict.items()]

colors_dict = {
    'iphone': 0x00dc9e,
    'laptop': 0x00a3ec,
    'ipad': 0xf400ed,
    'mail': 0xff0909,
    'cards': 0x29e629,
    'docuware': 0x404dff,
    'concur': 0xfdb400,
}

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


