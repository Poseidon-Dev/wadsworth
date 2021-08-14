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

    # Test
    verizon_data_df = pd.to_numeric(verizon_data_df['Total'])



    # verizon_data_df['User'] = verizon_data_df['Number'].apply(lambda x: str(x).split(' / ') if x else '')
    # verizon_data_df['Phone'] = verizon_data_df['Number'].apply(lambda x: str(x).split(' / ')[0] if x else '')
    print(verizon_data_df.head())