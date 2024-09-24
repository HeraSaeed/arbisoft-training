import requests
from pathlib import Path
import zipfile
import pandas as pd
from datetime import datetime, timedelta


def file_download():
    today = datetime.now()
    extracted_date = today + timedelta(-1)
    print(extracted_date)
    required_date = extracted_date.strftime('%Y-%m-%d')
    download_url = f'https://dps.psx.com.pk/download/mkt_summary/{required_date}.Z'
    try:
        req = requests.get(download_url)
        file_name = req.url[download_url.rfind('/')+1:]
        print(file_name)
        if file_name:
            print('File Name: ', file_name)
            with open(file_name, 'wb') as f:
                f.write(req.content)
                with zipfile.ZipFile(file_name) as myzip:
                    myzip.printdir()
                    data = myzip.read('closing11.lis')
                    decoded_data = data.decode('utf-8')
                    lines = decoded_data.strip().split('\r\n')
                    headers = ['Date', 'Symbol', 'Code', 'Company Name', 'Open Rate', 'Highest', 'Lowest', 'Closing Rate', 'Turn Over', 'Prev. Rate', 'Extra-1', 'Extra-2', 'Extra-3']
                    df = pd.DataFrame([line.split('|') for line in lines], columns=headers)
                    print(df)
                    df.to_csv(f'{required_date}.csv')

                    print('File downloaded successfully and converted to a csv file')

        else:
            print('File not Found')
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")



file_download()

