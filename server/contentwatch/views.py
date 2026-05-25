from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model
from django.db.models import Avg, Sum
from django.db.models.functions import TruncDate

from .serializers import RegisterSerializer, UserMeSerializer
from .models import Insight, PostFeatures, Post, ContentDNA


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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch the absolute latest generated insight for the logged-in user
        latest_insight = Insight.objects.filter(user=request.user).order_by('-created_at').first()
        
        if not latest_insight:
            return Response({"detail": "No insights found for this user. Please run an analysis first."}, status=404)
            
        data = {
            "strategy_block": {
                "best_content_type": latest_insight.best_content_type,
                "best_topic": latest_insight.best_topic,
                "best_posting_time": latest_insight.best_posting_time,
                "best_duration": latest_insight.best_duration,
                "strategy": latest_insight.strategy
            }
        }
        return Response(data)
    

class ViewTimeSeries(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Truncate the datetime to day intervals and aggregate the total views per day
        time_series = (
            Post.objects.filter(user=request.user)
            .annotate(date=TruncDate('posted_at'))
            .values('date')
            .annotate(total_views=Sum('views'))
            .order_by('date')
        )
        
        data = {
            "dates": [entry['date'].strftime('%Y-%m-%d') for entry in time_series],
            "views": [entry['total_views'] for entry in time_series],
        }
        return Response(data)
    

class EngagementTimeSeries(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Truncate the datetime and pull the average calculated engagement rate from PostFeatures per day
        time_series = (
            PostFeatures.objects.filter(post__user=request.user)
            .annotate(date=TruncDate('post__posted_at'))
            .values('date')
            .annotate(avg_engagement=Avg('engagement_rate'))
            .order_by('date')
        )
        
        data = {
            "dates": [entry['date'].strftime('%Y-%m-%d') for entry in time_series],
            "views": [round(entry['avg_engagement'], 4) for entry in time_series], # Kept key as "views" to match your original schema
        }
        return Response(data)
    

class TimeBucketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Group by the time_bucket field on PostFeatures, aggregating metrics from both tables
        buckets = (
            PostFeatures.objects.filter(post__user=request.user)
            .values('time_bucket')
            .annotate(
                avg_views=Avg('post__views'),
                avg_engagement=Avg('engagement_rate')
            )
        )
        
        # Format names slightly to handle the 'night_reach' nuance from your schema
        by_time_list = []
        for b in buckets:
            bucket_data = {
                "time": b['time_bucket'],
                "avg_engagement": round(b['avg_engagement'], 4)
            }
            # Match your hardcoded key divergence ("avg_reach" vs "avg_views" for night)
            if b['time_bucket'] == 'night':
                bucket_data["avg_reach"] = round(b['avg_views'] or 0, 1)
            else:
                bucket_data["avg_views"] = round(b['avg_views'] or 0, 1)
                
            by_time_list.append(bucket_data)

        return Response({"by_time": by_time_list})


class ContentTypeBucketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Group posts using the 'is_short' boolean field flag
        buckets = (
            PostFeatures.objects.filter(post__user=request.user)
            .values('is_short')
            .annotate(
                avg_views=Avg('post__views'),
                avg_engagement=Avg('engagement_rate')
            )
        )
        
        by_content_type = []
        for b in buckets:
            label = "short_video" if b['is_short'] else "long_video"
            by_content_type.append({
                "type": label,
                "avg_views": round(b['avg_views'] or 0, 1),
                "avg_engagement": round(b['avg_engagement'], 4)
            })
            
        return Response({"by_content_type": by_content_type})


class DurationBucketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Calculate engagement rates based on custom video duration brackets
        posts = PostFeatures.objects.filter(post__user=request.user)
        
        # Django conditional aggregation or Python grouping. Since duration brackets aren't 
        # explicitly explicitly stored as a field, querying ranges directly is clean:
        ranges = [
            {"range": "0-60s", "query": posts.filter(post__duration__lte=60)},
            {"range": "60-120s", "query": posts.filter(post__duration__gt=60, post__duration__lte=120)},
            {"range": "120-180s", "query": posts.filter(post__duration__gt=120, post__duration__lte=180)},
        ]
        
        by_duration = []
        for r in ranges:
            avg_eng = r["query"].aggregate(Avg('engagement_rate'))['engagement_rate__avg']
            by_duration.append({
                "range": r["range"],
                "avg_engagement": round(avg_eng, 4) if avg_eng is not None else 0.0
            })
            
        return Response({"by_duration": by_duration})
    

class ContentDNAView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch the active profile matrix row 
        dna = ContentDNA.objects.filter(user=request.user).first()
        latest_insight = Insight.objects.filter(user=request.user).order_by('-created_at').first()
        
        if not dna:
            return Response({"detail": "ContentDNA matrix profile not generated yet."}, status=404)
            
        data = {
            "generated_at": dna.created_at.isoformat(),

            "dna": {
                "format_affinity": {
                    "short_form": dna.short_form_affinity,
                    "long_form": round(1.0 - dna.short_form_affinity, 2) # Inverse profile complement
                },

                "content_bias": {
                    "education": dna.education_score,
                    "entertainment": dna.entertainment_score,
                    "other": round(max(0.0, 1.0 - (dna.education_score + dna.entertainment_score)), 2)
                },

                "time_performance": {
                    "morning": dna.morning_performance,
                    "afternoon": round((dna.morning_performance + dna.evening_performance) / 2, 2), # proxy balance
                    "evening": dna.evening_performance,
                    "night": dna.night_performance
                },

                # Pull historical range fallback maps
                "length_preference": {
                    "0-60s": dna.short_form_affinity,
                    "1-3min": round(dna.short_form_affinity * 0.5, 2),
                    "3min+": round(1.0 - dna.short_form_affinity, 2)
                }
            },

            "summary": {
                "dominant_format": "short_form" if dna.short_form_affinity >= 0.5 else "long_form",
                "dominant_topic": latest_insight.best_topic if latest_insight else "education",
                "best_time": latest_insight.best_posting_time if latest_insight else "evening",
                "ideal_length": latest_insight.best_duration if latest_insight else "0-60s"
            }
        }

        return Response(data)