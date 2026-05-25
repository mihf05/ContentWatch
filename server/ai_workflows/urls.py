from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'agents', views.AIAgentProfileViewSet, basename='ai-agent')
router.register(r'knowledge', views.AIKnowledgeDocumentViewSet, basename='ai-knowledge')
router.register(r'templates', views.AIPipelineTemplateViewSet, basename='ai-template')
router.register(r'runs', views.AIPipelineRunViewSet, basename='ai-run')

urlpatterns = [
    path('organizations/<int:org_id>/ai/', include(router.urls)),
]
