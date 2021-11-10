from apps.erp import ErpApiConn

import re
command = f"""
SELECT 
    HRTCPRID,
    TRIM(CONTROLNO), CAST(PROPERTYNO AS INTEGER),
    TRIM(DESCRIPTION), ASGDATE
FROM CMSFIL.HRTCPR
WHERE COMPANYNO=1
AND STATUSCODE = 'A'
AND PROPERTYNO= 2
AND DESCRIPTION LIKE 'IPHONE - % - %'
"""

erp_connection = ErpApiConn()
iphone_data = erp_connection.erp_commmand(command)

property_breakdown = {}

property_breakdown = {
    device[0]: {
        'id': device[0],
        'control': device[1],
        'type': device[2],
        'description': device[3],
        'date' : device[4]
    }
    for device in iphone_data
}

# for device in iphone_data:
#     property_breakdown[device[0]] = device[0]
#     property_breakdown['control'] = device[1]
#     property_breakdown['type'] = device[2]
#     property_breakdown['description'] = device[3]
#     property_breakdown['assigned'] = device[4]

for k,v in property_breakdown.items():
    serial = v['description'].split('-')
    # serial = re.search(r'^IPHONE - ', v['description'])
    print(serial)
#    print(v['description'])