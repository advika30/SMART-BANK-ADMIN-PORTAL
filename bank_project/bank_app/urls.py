from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('add/', views.add_customer, name='add_customer'),
    path('customers/', views.view_customers, name='view_customers'),
    path('deposit/', views.deposit_money, name='deposit_money'),
    path('withdraw/', views.withdraw_money, name='withdraw_money'),
    path('history/', views.transaction_history, name='transaction_history'),
    path('', views.home, name='home'),
    path('edit/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
]
