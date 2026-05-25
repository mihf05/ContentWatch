from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserMeSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class UserMeView(APIView):
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)
    

class InsightsView(APIView):
    def get(self, request):
        data = {
            "strategy_block": {
                "best_content_type": "short tutorials",
                "best_topic": "tech tips",
                "best_posting_time": "20:00-22:00",
                "best_duration": "30-60 sec",
                "strategy": "Focus on short tech tutorials in evening slots"
            }
        }
        return Response(data)
    

class ViewTimeSeries(APIView):
    def get(self, request):
        data = {
            "dates": [
                "2026-05-01", "2026-05-02", "2026-05-03", 
                "2026-05-04", "2026-05-05", "2026-05-06",
                "2026-05-07", "2026-05-08", "2026-05-09", 
                "2026-05-10", "2026-05-11", "2026-05-12",
            ],
            "views": [
                1200, 1800, 1700,
                2504, 10230, 9009,
                1200, 1800, 1700,
                2504, 10230, 9009,
            ],
        }

        return Response(data)
    

class EngagementTimeSeries(APIView):
    def get(self, request):
        data = {
            "dates": [
                "2026-05-01", "2026-05-02", "2026-05-03", 
                "2026-05-04", "2026-05-05", "2026-05-06",
                "2026-05-07", "2026-05-08", "2026-05-09", 
                "2026-05-10", "2026-05-11", "2026-05-12",
            ],
            "views": [
                0.12, 0.18, 0.17,
                0.84, 0.23, 0.93,
                0.12, 0.18, 0.17,
                0.84, 0.23, 0.93,
            ],
        }

        return Response(data)