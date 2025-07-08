from django.shortcuts import render
from django.db.models import Q
from .models import Account
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm
from .forms import WithdrawForm
from django.contrib.auth.decorators import login_required


def add_customer(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'bank_app/success.html', {'message': 'Customer added successfully!'})
    else:
        form = AccountForm()
    return render(request, 'bank_app/add_customer.html', {'form': form})

def view_customers(request):
    query = request.GET.get("q")
    field = request.GET.get("field")
    
    if query and field:
        if field == "accno":
            customers = Account.objects.filter(accno__icontains=query)
        elif field == "name":
            customers = Account.objects.filter(name__icontains=query)
        elif field == "mobile":
            customers = Account.objects.filter(mobile__icontains=query)
        elif field == "aadharno":
            customers = Account.objects.filter(aadharno__icontains=query)
        else:
            customers = Account.objects.none()
    else:
        customers = Account.objects.all()
    
    return render(request, 'bank_app/view_customers.html', {'customers': customers})

from .models import Account, Transaction
from .forms import DepositForm

def deposit_money(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            accno = form.cleaned_data['accno']
            amount = form.cleaned_data['amount']
            month = form.cleaned_data['month']

            try:
                account = Account.objects.get(accno=accno)
                account.balance += amount
                account.save()

                # Create a transaction record
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    month=month
                )

                return render(request, 'bank_app/success.html', {
                    'message': f"₹{amount} deposited successfully to Account {accno}."
                })

            except Account.DoesNotExist:
                form.add_error('accno', 'Account does not exist.')
    else:
        form = DepositForm()

    return render(request, 'bank_app/deposit.html', {'form': form})


def withdraw_money(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            accno = form.cleaned_data['accno']
            amount = form.cleaned_data['amount']
            remark = form.cleaned_data['remark']

            try:
                account = Account.objects.get(accno=accno)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()

                    Transaction.objects.create(
                        account=account,
                        amount=-amount,
                        month=remark  # optional: treat as "reason"
                    )

                    return render(request, 'bank_app/success.html', {
                        'message': f"₹{amount} withdrawn from Account {accno}."
                    })
                else:
                    form.add_error('amount', 'Insufficient balance.')
            except Account.DoesNotExist:
                form.add_error('accno', 'Account not found.')
    else:
        form = WithdrawForm()

    return render(request, 'bank_app/withdraw.html', {'form': form})


def transaction_history(request):
    accno = request.GET.get("accno")
    transactions = []
    account = None

    if accno:
        try:
            account = Account.objects.get(accno=accno)
            transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
        except Account.DoesNotExist:
            account = None

    return render(request, 'bank_app/history.html', {
        'transactions': transactions,
        'accno': accno,
        'account': account,
    })

def edit_customer(request, pk):
    customer = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('view_customers')
    else:
        form = AccountForm(instance=customer)

    return render(request, 'bank_app/edit_customer.html', {'form': form})

def delete_customer(request, pk):
    customer = get_object_or_404(Account, pk=pk)
    customer.delete()
    return redirect('view_customers')

@login_required(login_url='/login/')
def home(request):
    return render(request, 'bank_app/home.html')


from urllib.parse import urlencode
from authlib.integrations.django_client import OAuth
from django.conf import settings

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    return oauth.auth0.authorize_redirect(request, settings.AUTH0_CALLBACK_URL)

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    user = oauth.auth0.parse_id_token(request, token)
    request.session["user"] = {
        "user_id": user["sub"],
        "name": user["name"],
        "email": user["email"],
        "picture": user["picture"],
    }
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?" + urlencode({
            "client_id": settings.AUTH0_CLIENT_ID,
            "returnTo": "http://localhost:8000"
        })
    )
