from django.urls import path, include
from django.contrib.auth import views
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('choose-courier/', views.ChooseCourierView.as_view(), name='choose_courier'),
    path('sender-address/', views.SenderAddressView.as_view(), name='sender_address'),
    path('recipient-address/', views.RecipientAddressView.as_view(), name='recipient_address'),
    path('order-summary/', views.SummaryView.as_view(), name='summary'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('pricing/<pk>/', views.PricingCompanyView.as_view(), name='pricing_company'),
    path('about-company/', views.AboutCompanyView.as_view(), name='about'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile-address/create/', views.ProfileAddressCreateView.as_view(), name='profile_address_create'),
    path('profile-address/<pk>/update/', views.ProfileAddressUpdateView.as_view(), name='profile_address_update'),
    path('profile-address/<pk>/delete/', views.ProfileAddressDeleteView.as_view(), name='profile_address_delete'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('courier-opinion-create/', views.OpinionCreateView.as_view(), name='opinion_create'),
    path('courier-ranking/', views.CourierRankingView.as_view(), name='ranking'),
    path('charts/', views.ChartsView.as_view(), name='charts'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(), {'template_name': 'order/index.html'}, name='logout'),
]
