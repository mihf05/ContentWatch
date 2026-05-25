from contentwatch.models import ContentDNA, Insight

from analyze import generate_analytics_report


def process_and_save_analysis_view(request, analysis_run_obj, metric_payload):
    
    # 1. Fire off to Gemini
    gemini_result = generate_analytics_report(metric_payload)
    
    # 2. Extract and create the Django Insight instance
    insight_data = gemini_result.insight.model_dump() # converts pydantic to native python dict
    insight_model = Insight.objects.create(
        user=request.user,
        analysis=analysis_run_obj,
        **insight_data # Unpacks best_content_type, best_topic, strategy, confidence_score, etc.
    )
    
    # 3. Extract and update/create the ContentDNA instance
    dna_data = gemini_result.content_dna.model_dump()
    content_dna_model, created = ContentDNA.objects.update_or_create(
        user=request.user,
        defaults=dna_data # Unpacks short_form_affinity, morning_performance, etc.
    )
    
    return insight_model, content_dna_model