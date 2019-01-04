# Views determine what content is displayed on a given page while URLConfs determine where that content is going
from django.urls import path, include
from django.contrib.auth import views
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutCompanyView.as_view(), name='about'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('calculate/', views.CalculateView.as_view(), name='calculate'),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(), {'template_name': 'order/index.html'}, name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('sender/', views.SenderAddressView.as_view(), name='sender_address'),
    path('recipient/', views.RecipientAddressView.as_view(), name='recipient_address'),
    path('summary/', views.SummaryView.as_view(), name='summary'),
    path('courier/', views.CourierView.as_view(), name='courier'),
    path('pricing/<pk>/', views.PricingCompanyView.as_view(), name='pricing_company'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile_address/create/', views.ProfileAddressCreateView.as_view(), name='profile_address_create'),
    path('profile_address/<pk>/delete/', views.DeleteAddressProfileView.as_view(), name='profile_address_delete'),
    path('profile_address/<pk>/update/', views.UpdateAddressProfileView.as_view(), name='profile_address_update'),
    path('orders/', views.OrdersProfileView.as_view(), name='orders'),
    path('ranking/', views.CourierRankingView.as_view(), name='ranking'),
]
