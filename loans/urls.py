from django.urls import path
from loans.views import (
    CheckEligibilityView,
    CreateLoanView,
    ViewLoanView,
    ViewCustomerLoansView,
    LoadDataView,
)

urlpatterns = [
    path('check-eligibility/', CheckEligibilityView.as_view()),
    path('create-loan/', CreateLoanView.as_view()),
    path('view-loan/<int:loan_id>/', ViewLoanView.as_view()),
    path('view-loans/<int:customer_id>/', ViewCustomerLoansView.as_view()),
    path('load-data/', LoadDataView.as_view()),

]
