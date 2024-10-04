from django.urls import path
from .views import *
from reports import views

urlpatterns = [
    # path('view/', StockDataUploadView.as_view()),
    path('', views.report_view,),
]
