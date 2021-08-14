from numpy import ALLOW_THREADS
import pandas as pd 
import re

file = 'media/verizon/verizon.csv'


def verizon_csv():

    # Collect verizon header
    verizon_header_df = pd.read_csv(file, nrows=2, header=None)

    # Collect Verison Data
    columns = ['Account', 'Number', 'Charges', 'Monthly', 'Usage', 'Equipment', 'Surcharges', 'Taxes', 'ThirdParty', 'Total']
    verizon_data_df = pd.read_csv(file, skiprows=7, header=None)
    verizon_data_df.columns = columns

    # Clean Data
    verizon_data_df[verizon_data_df.columns[2:]] = verizon_data_df[verizon_data_df.columns[2:]].replace('[\$,]', '', regex=True).astype(float)

    # Remove subtotal and total
    verizon_data_df = verizon_data_df[~verizon_data_df['Account'].isin(["Subtotal", "Total Charges", ""])]

    # Clean divisions
    verizon_data_df['Account'] = verizon_data_df['Account'].apply(lambda x: re.match('="(.*)"', x) if x else '')
    verizon_data_df['Account'] = verizon_data_df['Account'].apply(lambda x: x.group(1) if x else '')

    # Veriify No Extra Cost Centers
    divisions = verizon_data_df[['Account']].drop_duplicates()
    extra_divivions = divisions[~divisions['Account'].isin(ALLOWED_DIVISIONS)]

    print("please correct your data")
    print(extra_divivions)

    # Seperate dataframes
    seperate_divivions = {
        divivions: verizon_data_df[verizon_data_df['Account'].isin([divivions])]
        for divivions in ALLOWED_DIVISIONS
    }

    for div, df in seperate_divivions.items():
        df = df.append(df.sum(numeric_only=True), ignore_index=True)
        print(df.tail())


       


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