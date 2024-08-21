from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django import views
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.views.generic.list import ListView


# Registration view
class RegisterView(views.View):
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'authentication/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
        return render(request, 'authentication/register.html', {'form': form})

# Login view
class LoginView(views.View):
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'authentication/login1.html', {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        return render(request, 'authentication/login1.html', {'form': form})

# Logout view
class LogoutView(views.View):
    def post(self, request):
        auth_logout(request)
        return redirect('login')

# Ensure user-specific data
class TableView(views.View):
    def get(self, request):
        current_date = now().date()
        selected_date = request.COOKIES.get('selected_date', current_date)
        
        # Date-filtered transactions for the logged-in user
        expenses = Expense.objects.filter(user=request.user, date_created__date=selected_date)
        credits = Credit.objects.filter(user=request.user, date_created__date=selected_date)
        
        # Get overall balance for the user
        total_balance_overall = Balance.objects.filter(user=request.user).aggregate(total=models.Sum('money'))['total'] or 0
        
        # Calculate the total credits and expenses for the selected date
        total_credits_date = sum(credit.money for credit in credits)
        total_expenses_date = sum(expense.money for expense in expenses)
        
        # Calculate the total balance for the selected date
        total_balance_date = total_balance_overall + (total_credits_date - total_expenses_date)
        
        # Fetch balances by payment mode directly
        balances_by_mode = Balance.objects.filter(user=request.user).values('account__name').annotate(total=models.Sum('money'))
        balances_dict = {balance['account__name']: balance['total'] for balance in balances_by_mode}
        
        # Calculate total expenses for the current month
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month + relativedelta(months=1, days=-1)
        month_expenses = Expense.objects.filter(user=request.user, date_created__date__range=[start_of_month, end_of_month])
        total_expenses_month = sum(expense.money for expense in month_expenses)

        context = {
            'expenses': expenses,
            'credits': credits,
            'selected_date': selected_date,
            'total_balance_date': total_balance_date,
            'total_balance_overall': total_balance_overall,
            'balances_dict': balances_dict,
            'total_expenses_month': total_expenses_month,
        }
        return render(request, 'datalist/dashboard.html', context)



    
class PaymentTypeView(views.View):
    form_class = PaymentTypeForm

    
    def get(self, request):
        form = self.form_class()
        payments = PaymentType.objects.all()
    
        context = {
            'payments': payments,
            'form': form,
              }
        
        return render(request, 'payment.html', context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            payment_type = form.save(commit=False)
            payment_type.user = request.user
            payment_type.save()
            return redirect('accounts')
        else:
            # Add debug statement to check form errors
            print(form.errors)
            return render(request, 'payment.html', {'form': form})

class BalanceCreateView(views.View):
    form_class = BalanceForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, 'balance.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            money = form.cleaned_data['money']
            
            # Check if a Balance entry already exists for this user and account
            balance, created = Balance.objects.get_or_create(
                user=request.user,
                account=account,
                defaults={'money': money}  # Use this value if the record is created
            )
            
            if not created:
                # If the Balance entry already exists, update the money field
                balance.money = money
                balance.save()

            return redirect('balance')
        else:
            return render(request, 'balance.html', {"form": form})


class ExpenseCreateView(views.View):
    form_class = ExpenseForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, 'expenses.html', {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
        else:
            return render(request,'expenses.html', {"form": form})

class CreditCreateView(views.View):
    form_class = CreditForm

    def get(self, request):
        form = self.form_class()
        return render(request,'credit.html', {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            credit = form.save(commit=False)
            credit.user = request.user
            credit.save()
            return redirect('dashboard')
        else:
            return render(request,'credit.html', {"form": form})

class CategoryView(views.View):
    form_class = CategoryForm
    
    def get(self, request):
        form = self.form_class()
        return render(request,'category.html', {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category')
        else:
            return render(request,'category.html', {'form': form})

class DeleteCreditView(views.View):
    def post(self, request, pk):
        credit = get_object_or_404(Credit, pk=pk, user=request.user)
        credit.delete()
        return redirect('dashboard')

class DeleteExpenseView(views.View):
    def post(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk, user=request.user)
        expense.delete()
        return redirect('dashboard')

class DeletePaymentView(views.View):
    def post(self, request, pk):
        account = get_object_or_404(PaymentType, pk=pk, user=request.user)
        account.delete()
        return redirect('accounts')
    
    
    
    
    
    
    
    
    
################################################## visualizations ################################################## 

import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from django.views import View
from .models import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth



class SpendingsView(views.View):
    def get(self, request):
        return render(request,'spendings.html')
class ExpenseBreakdownPieChartView(views.View):
    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.values('category__name').annotate(total=Sum('money'))
        categories = [expense['category__name'] for expense in expenses]
        totals = [expense['total'] for expense in expenses]
        
        fig, ax = plt.subplots()
        ax.pie(totals, labels=categories, autopct='%1.1f%%')
        ax.set_title('Expense Breakdown')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        return HttpResponse(buffer, content_type='image/png')
    
    
class MonthlySpendingTrendsLineGraphView(views.View):
    def get(self, request, *args, **kwargs):
        # Fetch monthly expense data
        monthly_expenses = Expense.objects.annotate(month=TruncMonth('date_created')).values('month').annotate(total=Sum('money')).order_by('month')
        months = [expense['month'].strftime('%Y-%m') for expense in monthly_expenses]
        totals = [expense['total'] for expense in monthly_expenses]

        # Create a line graph
        fig, ax = plt.subplots()
        ax.plot(months, totals, marker='o')
        ax.set_title('Monthly Spending Trends')
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Spending')

        # Rotate date labels for better readability
        # plt.xticks(rotation=45)

        # Save to a BytesIO object and return it as an HttpResponse
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return HttpResponse(buf, content_type='image/png')
    
class BudgetVsActualBarChartView(views.View):
    def get(self, request, *args, **kwargs):
        # Define a static budget for each month
        monthly_budget = 9000  # Example budget for every month

        # Aggregate expenses by month
        expenses_by_month = (
            Expense.objects.annotate(month=TruncMonth('date_created'))
            .values('month')
            .annotate(total_expenses=Sum('money'))
            .order_by('month')
        )

        # Prepare data for the bar chart
        labels = [entry['month'].strftime('%B %Y') for entry in expenses_by_month]
        budget_values = [monthly_budget for _ in expenses_by_month]
        actual_values = [entry['total_expenses'] for entry in expenses_by_month]

        # Create a bar chart
        fig, ax = plt.subplots()
        bar_width = 0.35
        index = range(len(labels))

        bar1 = ax.bar(index, budget_values, bar_width, label='Budget', color='b')
        bar2 = ax.bar([i + bar_width for i in index], actual_values, bar_width, label='Actual', color='r')

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        ax.set_title('Budget vs Actual Spending by Month')
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(labels, ha="right")
        ax.legend()

        # Save to a BytesIO object and return it as an HttpResponse
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return HttpResponse(buf, content_type='image/png')


