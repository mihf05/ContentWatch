from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from teams.models import Organization
from .models import (
    AIAgentProfile,
    AIKnowledgeDocument,
    AIPipelineTemplate,
    AIPipelineStep,
    AIPipelineRun,
    AIStepRun,
)
from .tasks import retrieve_rag_context, execute_ai_pipeline

User = get_user_model()


class AIWorkflowTests(APITestCase):

    def setUp(self):
        # Create standard user, organization, and authenticate
        self.user = User.objects.create_user(
            username="testcreator", password="password123", email="creator@contentwatch.com"
        )
        self.organization = Organization.objects.create(
            name="Alpha Media Agency", slug="alpha-media", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

        # Create basic Agent Profiles
        self.writer_agent = AIAgentProfile.objects.create(
            organization=self.organization,
            name="Senior Scriptwriter",
            role="writer",
            system_prompt="You are a professional video scriptwriter with 10 years experience."
        )
        self.brand_agent = AIAgentProfile.objects.create(
            organization=self.organization,
            name="Brand Compliance Auditor",
            role="reviewer",
            system_prompt="You verify alignment with brand voice guidelines."
        )

        # Create RAG Knowledge Documents
        self.voice_doc = AIKnowledgeDocument.objects.create(
            organization=self.organization,
            title="Premium Visual Tone Rules",
            content="Brand tone must be energetic and premium. Avoid negative words like fail or boring.",
            category="brand_voice"
        )
        self.seo_doc = AIKnowledgeDocument.objects.create(
            organization=self.organization,
            title="TikTok Analytics Reference",
            content="Use modern creator tag sets like #creatorops and #automation. Focus on hooks.",
            category="analytics"
        )

        # Create AIPipelineTemplate
        self.template = AIPipelineTemplate.objects.create(
            organization=self.organization,
            name="Standard Video Workflow Blueprint",
            description="Generates premium script, checks voice compliance, and structures metadata."
        )

        # Create Steps
        self.step_1 = AIPipelineStep.objects.create(
            template=self.template,
            agent=self.writer_agent,
            name="Creative Script Generator",
            step_type="script_generation",
            order=1,
            prompt_template="Write a high impact script about {topic}."
        )
        self.step_2 = AIPipelineStep.objects.create(
            template=self.template,
            agent=self.brand_agent,
            name="Brand Compliance Audit",
            step_type="brand_voice_check",
            order=2,
            prompt_template="Audit this text to match style guidelines."
        )

    def test_rag_context_retrieval(self):
        """
        Verify that RAG category-based keyword lookup works correctly.
        """
        inputs = {"topic": "creator automation and scaling tools"}
        context = retrieve_rag_context(self.organization, "script_generation", inputs)
        
        # Verify that voice guidelines are retrieved
        self.assertIn("Premium Visual Tone Rules", context)
        self.assertIn("energetic and premium", context)

    def test_api_crud_operations(self):
        """
        Verify that our viewsets are functioning and support standard operations.
        """
        # 1. Get AI Agents
        url = reverse('ai-agent-list', kwargs={'org_id': self.organization.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        # 2. Get Knowledge Documents
        url = reverse('ai-knowledge-list', kwargs={'org_id': self.organization.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        # 3. Create a Pipeline Run
        url = reverse('ai-run-list', kwargs={'org_id': self.organization.id})
        run_data = {
            "template": self.template.id,
            "inputs": {
                "topic": "Scaling Content Production with AI",
                "audience": "Busy creators"
            }
        }
        response = self.client.post(url, run_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'idle')
        run_id = response.data['id']

        # 4. Trigger the run API endpoint
        trigger_url = reverse('ai-run-trigger', kwargs={'org_id': self.organization.id, 'pk': run_id})
        response = self.client.post(trigger_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_pipeline_task_execution(self):
        """
        Verify that synchronous execution of the Celery task processes all steps,
        applies RAG context, stores thoughts, and completes successfully.
        """
        run = AIPipelineRun.objects.create(
            organization=self.organization,
            template=self.template,
            triggered_by=self.user,
            inputs={
                "topic": "Building Creator Collaboration Infrastructure",
                "audience": "Creator teams"
            }
        )

        # Run task synchronously
        execute_ai_pipeline(run.id)

        # Refresh from database
        run.refresh_from_db()
        self.assertEqual(run.status, 'completed')

        # Check step runs
        step_runs = run.step_runs.all()
        self.assertEqual(step_runs.count(), 2)

        first_step = step_runs.get(step__order=1)
        self.assertEqual(first_step.status, 'completed')
        self.assertIn("Video Script", first_step.output_content)
        self.assertIn("📚 Context retrieved successfully", first_step.agent_thoughts)

        second_step = step_runs.get(step__order=2)
        self.assertEqual(second_step.status, 'completed')
        self.assertIn("Brand Voice & Compliance Audit", second_step.output_content)
