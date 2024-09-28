from django.db import models

# Create your models here.
class DailyReport(models.Model):
    date = models.DateField()
    symbol_code = models.CharField(max_length=15)
    sector_code = models.CharField(max_length=5)
    company_short_name = models.CharField(max_length=25)
    opening_rate = models.DecimalField(max_digits=7, decimal_places=2)
    highest_rate = models.DecimalField(max_digits=7, decimal_places=2)
    lowest_rate = models.DecimalField(max_digits=7, decimal_places=2)
    current_rate = models.DecimalField(max_digits=7, decimal_places=2)
    current_turnover = models.IntegerField()
    lastday_closing_price = models.DecimalField(max_digits=7, decimal_places=2)
    




