from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app.models import Survey, Imajen, Cliente, Contador, Selu, Munisipiu
from app.services.gemini_service import GeminiService
from django.db.models import Count, Sum
from django.utils import timezone
import logging
import os
import json

logger = logging.getLogger(__name__)

@login_required
def analyze_survey_api(request, survey_id):
    """
    API endpoint that triggers Gemini AI to analyze a specific survey's description.
    """
    try:
        # Check if survey exists
        survey = Survey.objects.get(id=survey_id)
        description = survey.deskrisaun_instalasaun
        
        if not description or len(description.strip()) < 5:
            return JsonResponse({
                "error": "Deskrisaun badak liu ka mamuk.",
                "summary": "Analiza labele halao (Deskrisaun mamuk).",
                "risks": "La hatene.",
                "recommendation": "Hakere deskrisaun ho detalladu."
            }, status=200)

        # Initialize and call AI service
        ai_service = GeminiService()
        analysis_result = ai_service.analyze_survey_description(description)
        
        return JsonResponse(analysis_result)

    except Survey.DoesNotExist:
        return JsonResponse({"error": "Survey la'o eziste."}, status=404)
    except Exception as e:
        logger.error(f"Survey AI Analysis Error: {e}")
        return JsonResponse({"error": "Error iha prosesu analiza AI."}, status=500)

@login_required
def analyze_survey_by_client_api(request, cliente_id):
    """
    Convenience endpoint to analyze survey based on client ID.
    Useful for popups in dashboard map.
    """
    try:
        survey = Survey.objects.filter(cliente_id=cliente_id).first()
        if not survey:
             return JsonResponse({
                "error": "Survey ba kliente ne'e seidauk iha.",
                "summary": "Survey seidauk halo.",
                "risks": "La hatene.",
                "recommendation": "Halo survey lai."
            }, status=200)
            
        return analyze_survey_api(request, survey.id)
        
    except Exception as e:
        logger.error(f"Survey AI Analysis Error (Client ID): {e}")
@login_required
def analyze_image_api(request, image_id):
    """
    API endpoint to analyze an installation photo using Gemini Vision.
    """
    try:
        imajen = Imajen.objects.get(id=image_id)
        if not imajen.foto:
            return JsonResponse({"error": "Imajen la iha arkivu."}, status=400)

        # Get absolute path for PIL
        image_path = imajen.foto.path
        if not os.path.exists(image_path):
             return JsonResponse({"error": "Arkivu imajen la iha sistema."}, status=404)

        ai_service = GeminiService()
        analysis = ai_service.analyze_image(image_path)
        return JsonResponse(analysis)

    except Imajen.DoesNotExist:
        return JsonResponse({"error": "Imajen la'o eziste."}, status=404)
    except Exception as e:
        logger.error(f"Image AI Analysis Error: {e}")
        return JsonResponse({"error": "Error iha prosesu analiza imajen AI."}, status=500)

@login_required
def executive_summary_api(request):
    """
    Generates a high-level executive summary of current business data.
    """
    try:
        now = timezone.now()
        
        # Gather context data
        total_kliente = Cliente.objects.count()
        this_month_installations = Contador.objects.filter(
            created_at__year=now.year, 
            created_at__month=now.month
        ).count()
        
        total_revenue = Selu.objects.aggregate(total=Sum('montante'))['total'] or 0
        
        # Get filter objects safely
        try:
            top_munisipiu = Munisipiu.objects.annotate(
                num_contadors=Count('feeder__trafo__contador')
            ).order_by('-num_contadors').first()
            munisipiu_name = top_munisipiu.munisipiu if top_munisipiu else 'N/A'
        except Exception as mun_err:
            logger.warning(f"Could not get top munisipiu: {mun_err}")
            munisipiu_name = 'N/A'

        context_str = f"""
        Total Kliente Registadu: {total_kliente}
        Instalasaun Fulan Ne'e: {this_month_installations}
        Total Pendapatan (Revenue): ${total_revenue:,.2f}
        Munisipiu ho Atividade barak liu: {munisipiu_name}
        Data Relatoriu: {now.strftime('%d/%m/%Y %H:%M')}
        """
        
        # Log context for debugging
        logger.info(f"AI Context Generated: {context_str}")
        
        ai_service = GeminiService()
        summary = ai_service.generate_executive_summary(context_str)
        
        if summary and "Error" in summary:
             return JsonResponse({"error": summary}, status=200)

        return JsonResponse({"summary": summary})

    except Exception as e:
        logger.error(f"Executive Summary AI Error: {e}")
        return JsonResponse({"error": f"Error interno: {str(e)}"}, status=200)

@login_required
def chat_api(request):
    """
    Stateful chat API for the Technical Assistant.
    Uses Django sessions to store history.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed."}, status=405)

    try:
        body = json.loads(request.body)
        message = body.get('message', '').strip()
        
        if not message:
            return JsonResponse({"error": "Messajen mamuk."}, status=400)

        # Get history from session
        history = request.session.get('ai_chat_history', [])
        
        # Limit history size (last 10 interactions = 20 messages)
        if len(history) > 20:
            history = history[-20:]

        ai_service = GeminiService()
        response_text = ai_service.get_chat_response(message, history)

        # Update history
        history.append({"role": "user", "parts": [message]})
        history.append({"role": "model", "parts": [response_text]})
        
        request.session['ai_chat_history'] = history
        
        return JsonResponse({
            "response": response_text
        })

    except Exception as e:
        logger.error(f"AI Chat Error: {e}")
        return JsonResponse({"error": "Error iha prosesu chat."}, status=500)

def public_chat_api(request):
    """
    Public stateful chat API for the Keixa Assistant.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed."}, status=405)

    try:
        body = json.loads(request.body)
        message = body.get('message', '').strip()
        
        if not message:
            return JsonResponse({"error": "Messajen mamuk."}, status=400)

        history = request.session.get('public_chat_history', [])
        
        if len(history) > 10:
            history = history[-10:]

        ai_service = GeminiService()
        response_text = ai_service.get_public_chat_response(message, history)

        history.append({"role": "user", "parts": [message]})
        history.append({"role": "model", "parts": [response_text]})
        
        request.session['public_chat_history'] = history
        
        return JsonResponse({
            "response": response_text
        })

    except Exception as e:
        logger.error(f"Public AI Chat Error: {e}")
        return JsonResponse({"error": "Error iha prosesu chat."}, status=500)
