from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

# User registration form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# User login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

# Expense form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('category', 'payment_mode', 'money', 'date_created')

# Credit form
class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ('payment_mode', 'money', 'date_created')

# Balance form
class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ('payment_mode', 'money', 'date_created')

# PaymentType form
class PaymentTypeForm(forms.ModelForm):
    class Meta:
        model = PaymentType
        fields = ('name',)

# Category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
