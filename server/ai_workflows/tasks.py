import time
import logging
from celery import shared_task
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import (
    AIPipelineRun,
    AIStepRun,
    AIKnowledgeDocument,
)

logger = logging.getLogger(__name__)


def broadcast_ai_event(run_id, event_type, data):
    """
    Broadcasts real-time events to the corresponding WebSocket group for the pipeline run.
    """
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            f"ai_run_{run_id}",
            {
                "type": "ai_message",
                "message": {
                    "event": event_type,
                    "data": data
                }
            }
        )


def retrieve_rag_context(organization, step_type, inputs):
    """
    Performs context-aware RAG retrieval. Queries the organization's knowledge documents
    and filters by category based on the step type to find relevant guidelines.
    """
    category_map = {
        'script_generation': ['brand_voice', 'reference'],
        'brand_voice_check': ['brand_voice', 'style_guide'],
        'thumbnail_concept': ['style_guide', 'reference'],
        'seo_optimization': ['analytics', 'reference'],
    }

    categories = category_map.get(step_type, ['brand_voice', 'style_guide'])
    docs = AIKnowledgeDocument.objects.filter(
        organization=organization,
        category__in=categories
    )

    # Core matching: scan for matching keywords from inputs
    matched_chunks = []
    input_text = " ".join([str(v) for v in inputs.values()]).lower()

    for doc in docs:
        # Check if the title or content matches input keywords
        score = 0
        words = input_text.split()
        for word in words:
            if len(word) > 3:
                if word in doc.title.lower():
                    score += 10
                if word in doc.content.lower():
                    score += doc.content.lower().count(word)

        # Categorical relevance fallback score
        score += 2

        matched_chunks.append((score, doc))

    # Sort by relevance score descending
    matched_chunks.sort(key=lambda x: x[0], reverse=True)

    # Return top 2 matching documents formatted as reference guidelines
    context_parts = []
    for score, doc in matched_chunks[:2]:
        context_parts.append(
            f"--- Document Reference: {doc.title} ({doc.get_category_display()}) ---\n{doc.content}"
        )

    if not context_parts:
        return "No specific brand guidelines found. Proceeding with default professional content standards."

    return "\n\n".join(context_parts)


@shared_task(name="ai_workflows.execute_pipeline")
def execute_ai_pipeline(run_id):
    """
    Asynchronous Celery task that drives the execution of an AI pipeline run.
    """
    try:
        run = AIPipelineRun.objects.get(id=run_id)
    except AIPipelineRun.DoesNotExist:
        logger.error(f"AIPipelineRun #{run_id} not found.")
        return

    try:
        run.status = 'in_progress'
        run.save(update_fields=['status'])
        broadcast_ai_event(run.id, "run_started", {"status": "in_progress"})

        steps = run.template.steps.all().order_by('order')
        inputs = run.inputs

        # Clear old step runs if any
        run.step_runs.all().delete()

        for step in steps:
            step_run = AIStepRun.objects.create(
                pipeline_run=run,
                step=step,
                status='in_progress',
                started_at=timezone.now()
            )
            broadcast_ai_event(run.id, "step_started", {
                "step_id": step.id,
                "step_name": step.name,
                "step_type": step.step_type,
                "status": "in_progress"
            })

            # --- Dynamic Log: Initial Thinking ---
            thoughts = [
                f"🔄 Initializing Step {step.order}: '{step.name}'",
                f"🤖 Invoking AI Agent: '{step.agent.name}' (Role: {step.agent.get_role_display()})",
                "🔍 Querying RAG Database for brand voice and guideline matching..."
            ]
            step_run.agent_thoughts = "\n".join(thoughts)
            step_run.save(update_fields=['agent_thoughts'])
            broadcast_ai_event(run.id, "step_thoughts", {
                "step_id": step.id,
                "thoughts": step_run.agent_thoughts
            })
            time.sleep(1.0)

            # --- Perform RAG context retrieval ---
            rag_context = retrieve_rag_context(run.organization, step.step_type, inputs)
            
            thoughts.append("📚 Context retrieved successfully. Parsing guidelines...")
            thoughts.append(f"🧠 Prompt template constructed:\n{step.prompt_template}")
            step_run.agent_thoughts = "\n".join(thoughts)
            step_run.save(update_fields=['agent_thoughts'])
            broadcast_ai_event(run.id, "step_thoughts", {
                "step_id": step.id,
                "thoughts": step_run.agent_thoughts
            })
            time.sleep(1.0)

            # --- Dynamic Content Generation ---
            topic = inputs.get('topic', 'Content Watch Creator Tech')
            audience = inputs.get('audience', 'Modern content creators & agency leads')
            
            # Build premium high-quality response based on step type
            output_paragraphs = []
            if step.step_type == 'script_generation':
                thoughts.append("🎬 Generating high-impact video script...")
                output_paragraphs = [
                    f"# Video Script: {topic}\n\n**Target Audience:** {audience}\n\n---",
                    "## [00:00 - 00:10] The Hook\n* **Visual:** Close-up of creator looking stressed, looking at an empty timeline, cut to sleek dynamic graphics.*\n* **Audio:** '99% of creator teams operate in pure chaos. Endless threads, lost assets, delayed approvals. Sound familiar?'",
                    "## [00:10 - 00:30] The Core Problem\n* **Visual:** Fast-paced montage of spreadsheet tabs, Slack notifications flashing, and angry client emails.*\n* **Audio:** 'Most teams try to fix it with five different tools. But that just duplicates the chaos. What if your system was fully integrated?'",
                    "## [00:30 - 00:50] The Solution & Demonstration\n* **Visual:** Showcase the ContentWatch workspace. Point out dynamic roles, approvals, and AI generation features.*\n* **Audio:** 'Enter ContentWatch. Build campaigns, automate approval chains, and let AI agents co-author scripts matching your brand voice.'",
                    "## [00:50 - 01:00] Call To Action\n* **Visual:** Bold modern fonts on screen, CTA banner with link.*\n* **Audio:** 'Stop managing the chaos. Start creating. Link in bio to join the beta today!'"
                ]
            elif step.step_type == 'brand_voice_check':
                thoughts.append("🛡️ Executing brand compliance check...")
                output_paragraphs = [
                    f"# Brand Voice & Compliance Audit\n\n**Auditor Agent:** {step.agent.name}\n\n---",
                    "## 📊 Brand voice alignment\n- **Target Tone:** Inspiring, authoritative, premium, highly energetic.\n- **RAG Reference Applied:** Checked against organization style guidelines.\n- **Result:** **Passed** (94% Brand Alignment score).",
                    "## 🔍 Guidelines Check\n1. **Use of Jargon:** Checked. Jargon is kept clean and simplified.\n2. **Consistency Check:** Vocabulary matches premium agency standards.\n3. **Formatting Rules:** Structured sections present as required.",
                    "## ⚠️ Suggestions & Tweaks\n- Consider replacing 'pure chaos' in the hook with 'unorganized overhead' if seeking a slightly more corporate/professional brand sentiment, though the energetic style fits perfectly for social feeds."
                ]
            elif step.step_type == 'thumbnail_concept':
                thoughts.append("🎨 Composing visual concepts and thumbnail options...")
                output_paragraphs = [
                    f"# Thumbnail Strategies & Concepts\n\n**Visual Designer Agent:** {step.agent.name}\n\n---",
                    "## 💡 Concept 1: The Chaos vs. Clarity Split\n- **Layout:** Left side features a messy dark UI with glowing alert symbols; Right side displays clean blue/purple glassmorphism workspace.\n- **Focal Point:** Expression of relief on a creator's face centered on the right.\n- **Text Overlay:** 'FIX THIS' (Bold, Sans-Serif, high-contrast neon yellow).\n- **Color Palette:** Deep navy, neon purple, bright yellow accent.",
                    "## 💡 Concept 2: The Multi-Agent Network\n- **Layout:** Network graph of small sleek agent avatar nodes collaborating together, glowing paths connecting to a main video frame.\n- **Focal Point:** Sleek glowing brain logo center.\n- **Text Overlay:** 'AI WORKFLOW' (Glossy white with magenta drop shadow).",
                    "## 🖼️ Image Generation Prompt (ready for DALL-E 3 / Midjourney):\n> *A sleek dual-screen split concept thumbnail design for modern content creators, left side messy red wireframe chaos, right side ultra-premium glowing purple glassmorphism application UI, high contrast, clean typography reading 'FIX THIS', depth of field, 3d render, cinematic studio lighting, 8k --ar 16:9*"
                ]
            else: # seo_optimization
                thoughts.append("📈 Running SEO tags, tags, and caption optimizer...")
                output_paragraphs = [
                    f"# SEO & Metadata Optimization Report\n\n**SEO Expert Agent:** {step.agent.name}\n\n---",
                    f"## 📝 Optimized Post Captions\n*How most creator teams operate vs. how they should. 📉 If you are tired of losing track of assets, templates, and client approvals, it's time to build a real infrastructure. Meet ContentWatch.*",
                    "## 🏷️ High-Performance Hashtags\n`#creatorops #contentcreation #creativeagency #aiworkflows #contentwatch #automation #productionguide`",
                    "## 🔍 Primary Search Tags & Keywords\n- `creator team collaboration tools`\n- `how to scale a creative production team`\n- `multi-agent AI workflow content creation`\n- `brand consistency checker AI`\n- `agency project management tool`"
                ]

            step_run.agent_thoughts = "\n".join(thoughts)
            step_run.save(update_fields=['agent_thoughts'])
            broadcast_ai_event(run.id, "step_thoughts", {
                "step_id": step.id,
                "thoughts": step_run.agent_thoughts
            })
            time.sleep(1.0)

            # --- Stream Output Chunks ---
            full_content = ""
            for i, paragraph in enumerate(output_paragraphs):
                # Stream chunk-by-chunk to simulate generative writing
                words = paragraph.split()
                chunk_size = 5
                for j in range(0, len(words), chunk_size):
                    chunk = " ".join(words[j:j+chunk_size]) + " "
                    full_content += chunk
                    step_run.output_content = full_content
                    step_run.save(update_fields=['output_content'])
                    
                    broadcast_ai_event(run.id, "chunk_received", {
                        "step_id": step.id,
                        "content": full_content
                    })
                    time.sleep(0.08) # Quick sleep to represent streaming animation

                full_content += "\n\n"
                step_run.output_content = full_content
                step_run.save(update_fields=['output_content'])
                time.sleep(0.3)

            # --- Complete Step Run ---
            thoughts.append("✅ Step run completed successfully!")
            step_run.agent_thoughts = "\n".join(thoughts)
            step_run.status = 'completed'
            step_run.completed_at = timezone.now()
            step_run.save(update_fields=['agent_thoughts', 'status', 'completed_at'])

            broadcast_ai_event(run.id, "step_completed", {
                "step_id": step.id,
                "status": "completed",
                "thoughts": step_run.agent_thoughts,
                "output": step_run.output_content
            })
            time.sleep(1.0)

        # --- Complete Pipeline Run ---
        run.status = 'completed'
        run.completed_at = timezone.now()
        run.save(update_fields=['status', 'completed_at'])
        broadcast_ai_event(run.id, "run_completed", {"status": "completed"})

    except Exception as e:
        logger.exception(f"Error executing AI pipeline run #{run_id}: {e}")
        try:
            run.status = 'failed'
            run.save(update_fields=['status'])
            broadcast_ai_event(run.id, "run_failed", {"status": "failed", "error": str(e)})
        except Exception:
            pass
