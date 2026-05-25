from celery import shared_task
from django.contrib.auth import get_user_model

from .models import AnalysisRun, PlatformIntegration, Post, PostFeatures

from cwfetcher.fetcher import CW_PlatformFetcher 
from cwfetcher.savedata import process_and_save_analysis_view 

User = get_user_model()

@shared_task
def run_full_analytics_pipeline(user_id, analysis_run_id):
    try:
        user = User.objects.get(id=user_id)
        analysis_run = AnalysisRun.objects.get(id=analysis_run_id)
        
        integrations = PlatformIntegration.objects.filter(user=user)
        
        fetcher = CW_PlatformFetcher()
        metric_payloads = []
        
        for integration in integrations:
            # Generate dummy video data items matching this platform
            for i in range(10): 
                fake_vid_id = f"vid_{i}983"
                video_metrics = fetcher.fetch_video_data(integration.platform, fake_vid_id)
                
                # Save the raw post to your DB so your TimeSeries charts work!
                post = Post.objects.create(
                    user=user,
                    platforms_used=integration,
                    platform=integration.platform,
                    title=f"Mock video about {video_metrics.content_label}",
                    views=video_metrics.views,
                    likes=video_metrics.likes,
                    comments=video_metrics.comments,
                    duration=video_metrics.duration_seconds,
                    posted_at=video_metrics.posted_at
                )
                
                # Save computed feature configurations 
                PostFeatures.objects.create(
                    post=post,
                    engagement_rate=video_metrics.engagement_rate,
                    like_ratio=video_metrics.like_ratio,
                    comment_ratio=video_metrics.comment_ratio,
                    is_short=video_metrics.duration_seconds <= 60,
                    time_bucket=video_metrics.time_bucket,
                    topic=video_metrics.content_label
                )
                
                # Format a payload string/dict layout for Gemini to read
                metric_payloads.append({
                    "platform": video_metrics.platform,
                    "topic": video_metrics.content_label,
                    "views": video_metrics.views,
                    "engagement": video_metrics.engagement_rate,
                    "time": video_metrics.time_bucket
                })

        process_and_save_analysis_view(user, analysis_run, metric_payloads)
        
        analysis_run.status = "completed"
        analysis_run.save()
        
    except Exception as e:
        if 'analysis_run' in locals():
            analysis_run.status = "failed"
            analysis_run.save()
        raise e