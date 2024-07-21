import os
import pandas as pd
from google.oauth2 import service_account

credential = 'bq_key.json'
credentials = service_account.Credentials.from_service_account_file(credential)

project_id = 'hybrid-essence-429900-j9'

def send_to_bq(arquivo):
    df=pd.read_csv(arquivo)

    destination_table=f"terraform.{arquivo.split('.')[0].replace('data/','')}"
    
    df.to_gbq(
        destination_table=destination_table,
        project_id=project_id,
        credentials=credentials,
        if_exists='replace'
    )

for arquivo in os.listdir('data/'):
    send_to_bq(f'data/{arquivo}')
