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
    #path('', include('django.contrib.auth.urls'), {'redirect_if_logged_in': '/about/'},  name='login'),
    #path('login/', views.login_view, name='login'),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True),name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('logout/', views.LogoutView.as_view(), {'template_name':'order/index.html'}, name='logout'),
    #path('logout/', views.logout_view(request), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('sender/', views.SenderAddressView.as_view(),  name='sender_address'),
    path('recipient/', views.RecipientAddressView.as_view(),  name='recipient_address'),
    path('summary/', views.SummaryView.as_view(),  name='summary'),
    path('courier/', views.CourierView.as_view(),  name='courier'),
    path('pricing/<pk>/', views.PricingCompanyView.as_view(), name='pricing_company'),
]