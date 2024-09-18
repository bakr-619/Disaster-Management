from http.client import HTTPResponse
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .models import Volunteer, Donation, Crisis, Inventory
from .serializers import VolunteerSerializer, DonationSerializer, CrisisSerializer, InventorySerializer
from django.db.models import Sum
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed


class RegisterVolunteerView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        location = request.data.get('location')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        volunteer = Volunteer.objects.create(user=user, phone_number=phone_number, location=location)
        return Response(VolunteerSerializer(volunteer).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Creates a session
            token, created = Token.objects.get_or_create(user=user)  # Generate token
            return Response({
                "message": "Login successful",
                "token": token.key
            }, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed("Invalid credentials, unable to login")


class TotalFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_funds = Donation.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({"total": total_funds}, status=status.HTTP_200_OK)


class CrisisListView(APIView):
    def get(self, request):
        crises = Crisis.objects.filter(is_approved=True)
        return Response(CrisisSerializer(crises, many=True).data)


class DonationView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        Donation.objects.create(amount=amount)
        return Response({"message": "Donation received"}, status=status.HTTP_201_CREATED)


def home(request):
    return HTTPResponse("<h1>Welcome to Disaster Management Application</h1>")
