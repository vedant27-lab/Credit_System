from rest_framework import serializers
from customers.models import Customer

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    age = serializers.IntegerField()
    phone_number = serializers.CharField()
    monthly_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
