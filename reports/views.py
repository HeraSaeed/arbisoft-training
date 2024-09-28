from django.shortcuts import render
from reports.models import DailyReport
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reports.serializer import ReportSerializer

# Create your views here.
@api_view(['GET'])
def report_view(request):
    report = DailyReport.objects.all()
    serializer = ReportSerializer(report, many=True)
    return Response(serializer.data)


