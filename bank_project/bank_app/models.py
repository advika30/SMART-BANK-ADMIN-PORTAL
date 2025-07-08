from django.db import models

class Account(models.Model):
    accno = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    aadharno = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    acctype = models.CharField(max_length=20, choices=[
        ('Saving', 'Saving'),
        ('RD', 'RD'),
        ('PPF', 'PPF'),
        ('Current', 'Current')
    ])

    def __str__(self):
        return f"{self.accno} - {self.name}"


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.CharField(max_length=20)  # could be replaced with DateField
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.accno} - ₹{self.amount}"
