from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

template_router = DefaultRouter()
template_router.register(r'templates', views.WorkflowTemplateViewSet, basename='workflow-template')

instance_router = DefaultRouter()
instance_router.register(r'instances', views.WorkflowInstanceViewSet, basename='workflow-instance')

step_router = DefaultRouter()
step_router.register(r'steps', views.WorkflowStepViewSet, basename='workflow-step')

execution_router = DefaultRouter()
execution_router.register(r'executions', views.StepExecutionViewSet, basename='step-execution')

urlpatterns = [
    path('organizations/<int:org_id>/workflows/', include(template_router.urls)),
    path('organizations/<int:org_id>/workflows/', include(instance_router.urls)),
    path('organizations/<int:org_id>/workflows/templates/<int:template_id>/', include(step_router.urls)),
    path('organizations/<int:org_id>/workflows/instances/<int:instance_id>/', include(execution_router.urls)),
]
