from django.urls import path
from .views import AccountDetail, AccountApi


urlpatterns = [
    path('account/', AccountApi.as_view()),
    path('account-retrive/<int:pk>/',AccountDetail.as_view()),
]
