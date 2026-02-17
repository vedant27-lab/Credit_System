from django.urls import path
from customers.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
]
