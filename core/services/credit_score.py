from loans.models import Loan
from django.db.models import Sum
from django.utils import timezone

def calculate_credit_score(customer):
    loans = Loan.objects.filter(customer=customer)
    if not loans.exists():
        return 50
    total_loan_amount = loans.aggregate(
        Sum('loan_amount')
    )['loan_amount__sum'] or 0

    if total_loan_amount > customer.approved_limit:
        return 0
    
    total_emis_paid = loans.aggregate(
        Sum('emis_paid_on_time')
    )['emis_paid_on_time__sum'] or 0

    total_tenure = loans.aggregate(
        Sum('tenure')
    )['tenure__sum'] or 1

    repayment_ratio = total_emis_paid / total_tenure

    if repayment_ratio >= 0.9:
        repayment_score = 40
    elif repayment_ratio >= 0.7:
        repayment_score = 30
    elif repayment_ratio >= 0.5:
        repayment_score = 20
    else:
        repayment_score = 10

    total_loans = loans.count()

    if total_loans <= 2:
        loan_count_score = 20
    elif total_loans <= 4:
        loan_count_score = 10
    else:
        loan_count_score = 5

    current_year = timezone.now().year
    current_year_loans = loans.filter(
        date_of_approval__year=current_year
    ).count()

    if current_year_loans <= 1:
        activity_score = 15
    elif current_year_loans <=3:
        activity_score = 10
    else:
        activity_score = 5

    if customer.approved_limit > 0:
        ratio = total_loan_amount / customer.approved_limit
    else:
        ratio = 1
    if ratio < 0.5:
        volume_score = 25
    elif ratio < 0.8:
        volume_score = 15
    else:
        volume_score = 5
    
    final_score = (
        repayment_score +
        loan_count_score +
        activity_score +
        volume_score
    )

    return min(final_score, 100)