from pyad import aduser
import pyad.adquery

import core.config

sAMAccountName = 'account name'
userAccountControl = {
    'active': 66048,
    'disabled': 66050,
}

def ad_query(first_name, last_name):

    q = pyad.adquery.ADQuery()
    q.execute_query(
        attributes = ['sAMAccountName', 'sn',  'givenName', 'cn', 'userAccountControl'],
        # where_clause= f"objectClass='user' and sn = '{last_name.capitalize()}*' and userAccountControl = {userAccountControl.get('active')}",
        where_clause= f"objectClass='user' and givenName='{first_name.capitalize()}*' and sn = '{last_name.capitalize()}*' and userAccountControl = {userAccountControl.get('active')}",
        base_dn="DC=azp, DC=local"
    )
    return [aduser.ADUser.from_cn(user['cn']) for user in q.get_results()]


