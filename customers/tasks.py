import pandas as pd
from celery import shared_task
from customers.models import Customer
from loans.models import Loan
from django.db import transaction


@shared_task
def load_initial_data_task():

    customer_df = pd.read_excel("customer_data.xlsx")

    with transaction.atomic():
        for _, row in customer_df.iterrows():
            Customer.objects.update_or_create(
                customer_id=row["Customer ID"],
                defaults={
                    "first_name": row["First Name"],
                    "last_name": row["Last Name"],
                    "age": row["Age"],
                    "phone_number": str(row["Phone Number"]),
                    "monthly_salary": row["Monthly Salary"],
                    "approved_limit": row["Approved Limit"],
                }
            )

    loan_df = pd.read_excel("loan_data.xlsx")

    with transaction.atomic():
        for _, row in loan_df.iterrows():

            try:
                customer = Customer.objects.get(
                    customer_id=row["Customer ID"]
                )
            except Customer.DoesNotExist:
                continue

            Loan.objects.update_or_create(
                loan_id=row["Loan ID"],
                defaults={
                    "customer": customer,
                    "loan_amount": row["Loan Amount"],
                    "tenure": row["Tenure"],
                    "interest_rate": row["Interest Rate"],
                    "monthly_payment": row["Monthly payment"],
                    "emis_paid_on_time": row["EMIs paid on Time"],
                    "date_of_approval": row["Date of Approval"],
                    "end_date": row["End Date"],
                }
            )

    return "Data loaded successfully"
