from rest_framework import serializers
from reports.models import DailyReport


class ReportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReport
        fields = '__all__'

# class ReportSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     symbol_code = serializers.CharField(max_length=15)
#     sector_code = serializers.CharField(max_length=5)
#     company_short_name = serializers.CharField(max_length=25)
#     opening_rate = serializers.DecimalField(max_digits=7, decimal_places=2)
#     highest_rate = serializers.DecimalField(max_digits=7, decimal_places=2)
#     lowest_rate = serializers.DecimalField(max_digits=7, decimal_places=2)
#     current_rate = serializers.DecimalField(max_digits=7, decimal_places=2)
#     current_turnover = serializers.IntegerField()
#     lastday_closing_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    

    

