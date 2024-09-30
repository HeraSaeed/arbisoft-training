from django.shortcuts import render
from reports.models import DailyReport
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DailyReport
from reports.serializer import ReportDataSerializer
import requests
import pandas as pd
import zipfile
from io import BytesIO
from datetime import datetime

# Create your views here.

class StockDataUploadView(APIView):
    def get(self, request, *args, **kwargs):
        today = datetime.now().strftime("%Y-%m-%d")
        download_url = f"https://dps.psx.com.pk/download/mkt_summary/{today}.Z"
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
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message':"Data saved succesfully."}, status=status.HTTP_201_CREATED)
                    

            else:
                return Response({'messgae':'Failed to download file from URL.'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            return Response({'message':f'Error fetching file :{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)





# @api_view(['GET'])
# def report_view(request):
#     report = DailyReport.objects.all()
#     serializer = ReportDataSerializer(report, many=True)
#     return Response(serializer.data)


