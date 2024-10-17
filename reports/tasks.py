from celery import shared_task
import requests
import zipfile
import pandas as pd
from datetime import datetime, timedelta
from reports.serializer import ReportDataSerializer



@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done...!!!"

    
@shared_task(bind=True)
def download_daily_report(*args, **kwargs):
        today = datetime.now()
        previous = today + timedelta(-1)
        required = previous.strftime("%Y-%m-%d")
        print(previous)
        print(required)
        download_url = f"https://dps.psx.com.pk/download/mkt_summary/{required}.Z"
        try:
            req = requests.get(download_url)
            file_name = req.url[download_url.rfind("/") + 1 :]
            print(file_name)
            if file_name:
                print("File Name: ", file_name)
                with open(file_name, "wb") as f:
                    f.write(req.content)
                    with zipfile.ZipFile(file_name) as myzip:
                        myzip.printdir()
                        data = myzip.read("closing11.lis")
                        decoded_data = data.decode("utf-8")
                        lines = decoded_data.strip().split("\r\n")
                        headers = [
                            "date",
                            "symbol_code",
                            "sector_code",
                            "company_short_name",
                            "opening_rate",
                            "highest_rate",
                            "lowest_rate",
                            "current_rate",
                            "current_turnover",
                            "lastday_closing_price",
                            "Extra-1",
                            "Extra-2",
                            "Extra-3",
                        ]
                        df = pd.DataFrame(
                            [line.split("|") for line in lines], columns=headers
                        )
                        print(df)
                        df = df.drop(['Extra-1', 'Extra-2', 'Extra-3'], axis=1)
                        df.to_csv(f"{today}.csv", index=False)

                        print("File downloaded successfully and converted to a csv file")

                        def date_format(date_str):
                            return datetime.strptime(date_str, '%d%b%Y').strftime('%Y-%m-%d')
                        
                        df['date'] = df['date'].apply(date_format)
                        print(df)

                        data_records = df.to_dict(orient='records')
                        for record in data_records:
                            serializer = ReportDataSerializer(data=record)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                return {'error': serializer.errors, 'status':'Failed'}
                return {'message':"Data saved succesfully.", 'status': 'success'}
                    

            else:
                return {'messgae':'Failed to download file from URL.', 'status': 'Failed'}
        except requests.exceptions.RequestException as e:
            return {'message':f'Error fetching file :{str(e)}', 'status': 'Failed'}

