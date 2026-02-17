from django.db.models import Sum
from loans.models import Loan
from core.services.credit_score import calculate_credit_score
from core.services.emi import calculate_emi
from decimal import Decimal

def check_eligibility(customer, loan_amount, interest_rate, tenure):
    score = calculate_credit_score(customer=customer)
    if score > 50:
        min_rate = interest_rate
    elif score > 30 and score <= 50:
        min_rate = 12
    elif score > 10 and score <= 30:
        min_rate = 16
    else:
        return {
            "approved": False,
            "corrected_interest_rate": None,
            "monthly_installment": None,
            "message": "Credit score too low"
        }
    corrected_rate = max(interest_rate, min_rate)
    
    monthly_installment = calculate_emi(
        loan_amount,
        corrected_rate,
        tenure
    )

    existing_emis = Loan.objects.filter(customer=customer).aggregate(
        Sum('monthly_payment')
    )['monthly_payment__sum'] or 0

    total_emi_burden = existing_emis + monthly_installment

    if total_emi_burden > (customer.monthly_salary * Decimal("0.5")):
        return {
            "approved": False,
            "corrected_interest_rate": corrected_rate,
            "monthly_installment": monthly_installment,
            "message": "EMI exceeds 50% of monthly salary"
        }

    return {
    "approved": False,
    "corrected_interest_rate": None,
    "monthly_installment": None,
    "message": "Loan not approved"
}
