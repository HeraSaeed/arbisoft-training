from django.http import HttpResponse
from django.shortcuts import render
from reports.models import DailyReport
# from rest_framework import status
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DailyReport
from reports.serializer import ReportDataSerializer
# import requests
# import pandas as pd
# import zipfile
# from io import BytesIO
# from datetime import datetime
from .tasks import test_func

# Create your views here.
# class DataViewSet()

def test(request):
    test_func.delay()
    return HttpResponse("Done")


@api_view(['GET'])
def report_view(request):
    report = DailyReport.objects.all()
    serializer = ReportDataSerializer(report, many=True)
    return Response(serializer.data)


