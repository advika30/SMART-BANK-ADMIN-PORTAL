from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'acctype': forms.Select(attrs={'class': 'form-select'}),
        }

from .models import Transaction

class DepositForm(forms.Form):
    accno = forms.CharField(label="Account Number")
    amount = forms.DecimalField(label="Amount", max_digits=12, decimal_places=2, min_value=0.01)
    month = forms.CharField(label="Month / Remark", max_length=20)

class WithdrawForm(forms.Form):
    accno = forms.CharField(label="Account Number")
    amount = forms.DecimalField(label="Amount", max_digits=12, decimal_places=2, min_value=0.01)
    remark = forms.CharField(label="Remark", max_length=100)

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)