from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customers.models import Customer
from customers.serializers import RegisterSerializer

class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            data = serializer.validated_data

            approved_limit = data["monthly_salary"] * 36

            customer = Customer.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                age=data["age"],
                phone_number=data["phone_number"],
                monthly_salary=data["monthly_salary"],
                approved_limit=approved_limit
            )

            return Response({
                "customer_id": customer.customer_id,
                "name": f"{customer.first_name} {customer.last_name}",
                "approved_limit": approved_limit
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
