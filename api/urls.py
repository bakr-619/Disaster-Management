from django.urls import path
from .views import RegisterVolunteerView, LoginView, TotalFundsView, CrisisListView, DonationView

urlpatterns = [
    path('register/', RegisterVolunteerView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('funds/', TotalFundsView.as_view(), name='funds'),
    path('crises/', CrisisListView.as_view(), name='crises'),
    path('donations/', DonationView.as_view(), name='donations'),
]
