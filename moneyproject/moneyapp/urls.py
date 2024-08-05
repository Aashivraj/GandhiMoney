from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('table/', TableView.as_view(), name='table'),
    path('payment/', PaymentTypeView.as_view(), name='payment'),
    path('balance/', BalanceCreateView.as_view(), name='balance'),
    path('expense/', ExpenseCreateView.as_view(), name='expense'),
    path('credit/', CreditCreateView.as_view(), name='credit'),
    path('category/', CategoryView.as_view(), name='category'),
    path('delete_credit/<int:pk>/', DeleteCreditView.as_view(), name='delete_credit'),
    path('delete_expense/<int:pk>/', DeleteExpenseView.as_view(), name='delete_expense'),
]