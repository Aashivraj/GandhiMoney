from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Expense, Credit, Balance

@receiver(post_save, sender=Expense)
def update_balance_on_expense(sender, instance, **kwargs):
    try:
        balance = Balance.objects.get(user=instance.user, account=instance.account)
        balance.money -= instance.money  # Subtract the expense from balance
        balance.save()
    except Balance.DoesNotExist:
        pass

@receiver(post_delete, sender=Expense)
def restore_balance_on_expense_delete(sender, instance, **kwargs):
    try:
        balance = Balance.objects.get(user=instance.user, account=instance.account)
        balance.money += instance.money  # Restore the balance when an expense is deleted
        balance.save()
    except Balance.DoesNotExist:
        pass

@receiver(post_save, sender=Credit)
def update_balance_on_credit(sender, instance, **kwargs):
    try:
        balance = Balance.objects.get(user=instance.user, account=instance.account)
        balance.money += instance.money  # Add the credit to balance
        balance.save()
    except Balance.DoesNotExist:
        pass

@receiver(post_delete, sender=Credit)
def restore_balance_on_credit_delete(sender, instance, **kwargs):
    try:
        balance = Balance.objects.get(user=instance.user, account=instance.account)
        balance.money -= instance.money  # Restore the balance when a credit is deleted
        balance.save()
    except Balance.DoesNotExist:
        pass
