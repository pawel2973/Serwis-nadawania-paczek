# Views determine what content is displayed on a given page while URLConfs determine where that content is going

from django.urls import path, include
from . import views


app_name = 'order'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutCompanyView.as_view(), name='about'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('calculate/', views.CalculateView.as_view(), name='calculate'),
    path('', include('django.contrib.auth.urls'),  name='login'),
    path('signup/', views.SignUpView.as_view(),  name='signup'),
    path('sender/', views.SenderAddressView.as_view(),  name='sender_address'),
    path('recipient/', views.RecipientAddressView.as_view(),  name='recipient_address'),
    path('summary/', views.SummaryView.as_view(),  name='summary'),
    path('courier/', views.CourierView.as_view(),  name='courier'),
    path('pricing/<pk>/', views.PricingCompanyView.as_view(), name='pricing_company'),
]