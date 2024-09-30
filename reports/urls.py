from django.urls import path
from .views import *

urlpatterns = [
    path('view/', StockDataUploadView.as_view()),
]
