from numpy import ALLOW_THREADS
import pandas as pd 
import re
from csv import writer

file = 'media/verizon/verizon.csv'


def verizon_csv():

    # Collect verizon header
    verizon_header_df = pd.read_csv(file, nrows=2, header=None)

    # Collect Verison Data
    columns = ['Account', 'Number-User', 'Charges', 'Monthly', 'Usage', 'Equipment', 'Surcharges', 'Taxes', 'ThirdParty', 'Total']
    verizon_data_df = pd.read_csv(file, skiprows=7, header=None)
    verizon_data_df.columns = columns

    # Clean Data
    verizon_data_df[verizon_data_df.columns[2:]] = verizon_data_df[verizon_data_df.columns[2:]].replace('[\$,]', '', regex=True).astype(float)

    # Remove subtotal and total
    verizon_data_df = verizon_data_df[~verizon_data_df['Account'].isin(["Subtotal", "Total Charges", ""])]

    # Clean divisions
    verizon_data_df['Account'] = verizon_data_df['Account'].apply(lambda x: re.match('="(.*)"', x) if x else '')
    verizon_data_df['Account'] = verizon_data_df['Account'].apply(lambda x: x.group(1) if x else '')

    # Verify No Extra Cost Centers
    divisions = verizon_data_df[['Account']].drop_duplicates()
    extra_divivions = divisions[~divisions['Account'].isin(ALLOWED_DIVISIONS)]

    if not extra_divivions.empty and True == 0:
        print("please correct your data")
        print(extra_divivions)
    else:
        # Split Number and UserName
        verizon_data_df['Number'] = verizon_data_df['Number-User'].apply(lambda x: x.split('/')[0]).str.strip()
        verizon_data_df['User'] = verizon_data_df['Number-User'].apply(lambda x: x.split('/')[1]).str.strip()

        # Reorder Sheet
        columns = ['Account', 'Number', 'User', 'Charges', 'Monthly', 'Usage', 'Equipment', 'Surcharges', 'Taxes', 'ThirdParty', 'Total']
        verizon_data_df = verizon_data_df[columns]

        # Seperate dataframes
        seperate_divivions = {
            divivions: verizon_data_df[verizon_data_df['Account'].isin([divivions])]
            for divivions in ALLOWED_DIVISIONS
        }
        
        # Add header and total information
        for div, df in seperate_divivions.items():
            verizon_header_df.to_csv(f'media/verizon/{div}.csv', sep=',', encoding='utf-8', index=False)
            df = df.append(df.sum(numeric_only=True), ignore_index=True)
            df.to_csv(f'media/verizon/{div}.csv', mode='a', sep=',', encoding='utf-8', index=False)
            

ALLOWED_DIVISIONS = [
    'AVAILABLE',
    'BULLHEAD',
    'CARSON CITY',
    'CORONA',
    'CORPORATE',
    'HESPERIA',
    'LAS VEGAS',
    'N NEVADA',
    'PACIFIC',
    'PHOENIX',
    'PIPELINE',
    'SHOP',
    'TUCSON',
    ]
    



    # verizon_data_df['User'] = verizon_data_df['Number'].apply(lambda x: str(x).split(' / ') if x else '')
    # verizon_data_df['Phone'] = verizon_data_df['Number'].apply(lambda x: str(x).split(' / ')[0] if x else '')