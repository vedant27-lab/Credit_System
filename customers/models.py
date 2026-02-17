from django.db import models

class Customer(models.Model):
    # customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2)
    approved_limit= models.DecimalField(max_digits=12, decimal_places=2)
