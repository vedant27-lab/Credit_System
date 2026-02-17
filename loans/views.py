from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customers.models import Customer
from loans.models import Loan
from loans.serializer import EligibilitySerializer, CreateLoanSerilizer
from core.services.eligibility import check_eligibility
from django.db.models import Max
from customers.tasks import load_initial_data_task


class CheckEligibilityView(APIView):
    def post(self, request):
        serilizer = EligibilitySerializer(data = request.data)
        if serilizer.is_valid():
            data = serilizer.validated_data

            try:
                customer = Customer.objects.get(
                    customer_id = data['customer_id']
                )
            except Customer.DoesNotExist:
                return Response(
                    {"error": "Customer not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            result = check_eligibility(
                customer,
                data['loan_amount'],
                data['interest_rate'],
                data['tenure']
            )

            return Response(result, status=status.HTTP_200_OK)
        
        return Response(
            serilizer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CreateLoanView(APIView):
    def post(self, request):
        serilizer = CreateLoanSerilizer(data = request.data)
        if serilizer.is_valid():
            data = serilizer.validated_data

            try:
                customer = Customer.objects.get(
                    customer_id = data['customer_id']
                )
            except Customer.DoesNotExist:
                return Response(
                    {"error": "Customer not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            result = check_eligibility(
                customer,
                data['loan_amount'],
                data['interest_rate'],
                data['tenure']
            )

            if not result["approved"]:
                return Response({
                    "loan_id": None,
                    "customer_id": data['customer_id'],
                    "loan_approved": False,
                    "message": result["message"],
                    "monthly_installment": result["monthly_installment"]
                }, status=status.HTTP_200_OK)
            
            last_id = Loan.objects.aggregate(
                Max('loan_id')
            )['loan_id_max'] or 0

            new_loan_id = last_id + 1

            Loan.objects.create(
                loan_id=new_loan_id,
                customer=customer,
                loan_amount=data['loan_amount'],
                interest_rate=result['corrected_interest_rate'],
                tenure=data['tenure'],
                monthly_payment=result['monthly_installment'],
                emis_paid_on_time=0,
                date_of_approval=timezone.now().data(),
                end_date=timezone.now().date()
            )

            result = {
                "loan_id": new_loan_id,
                "customer_id": data['customer_id'],
                "loan_approved": True,
                "message": "Loan approved",
                "monthly_installment": result["monthly_installment"],
            }

            return Response(result, status=status.HTTP_201_CREATED)
        
        return Response(
            serilizer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ViewLoanView(APIView):

    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response(
                {"error": "Loan not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "loan_id": loan.loan_id,
            "customer": {
                "customer_id": loan.customer.customer_id,
                "first_name": loan.customer.first_name,
                "last_name": loan.customer.last_name,
                "phone_number": loan.customer.phone_number,
                "age": loan.customer.age,
            },
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_payment,
            "tenure": loan.tenure
        })

class ViewCustomerLoansView(APIView):

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        loans = Loan.objects.filter(customer=customer)

        loan_list = []

        for loan in loans:
            repayments_left = loan.tenure - loan.emis_paid_on_time

            loan_list.append({
                "loan_id": loan.loan_id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_payment,
                "repayments_left": repayments_left
            })

        return Response(loan_list)

class LoadDataView(APIView):

    def post(self, request):
        load_initial_data_task.delay()
        return Response(
            {"message": "Data loading started in background"},
            status=status.HTTP_202_ACCEPTED
        )