from google import genai
from google.genai import types
from PIL import Image
from decouple import config
import logging
import io

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = config('GOOGLE_API_KEY', default=None)
        self.model_name = config('GEMINI_MODEL', default='gemini-1.5-flash')
        
        if not self.api_key or self.api_key == 'PLACEHOLDER_KEY':
            self.client = None
            logger.warning("Gemini API Key is not set or is a placeholder.")
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self.client = None
                logger.error(f"Failed to initialize Gemini Client: {e}")

    def analyze_survey_description(self, description):
        """
        Analyzes the technician's survey description and returns a structured insight.
        """
        if not self.client:
            return {
                "error": "AI Service not configured. Please provide a valid GOOGLE_API_KEY in .env",
                "summary": "Analiza la'o nune (AI la konfiguradu)",
                "risks": "La hatene (AI la konfiguradu)",
                "recommendation": "Esperu fali (AI la konfiguradu)"
            }

        prompt = f"""
        Ita mak asisatente tékniku espesialista ba enerjia elétrika iha EDTL (Electricidade de Timor-Leste).
        Favor analiza deskrisaun survey husi tékniku tuir mai ne'e no fó komentáriu iha lian Tetum.
        
        Deskrisaun Tékniku: "{description}"
        
        Favor fó resposta ho formatu JSON hanesan ne'e:
        {{
            "summary": "Rezumu badak husi servisu ne'ebé halo",
            "risks": "Risku tékniku ka seguransa ne'ebé bele mosu (se iha)",
            "recommendation": "Rekomendasaun ba pasu tuir mai"
        }}
        
        Responde de'it ho formatu JSON, labele fó testu seluk.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            # The new SDK returns response.text
            # We should try to parse it as JSON
            import json
            import re
            
            # Clean the response text if there are markdown blocks
            text = response.text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "summary": text[:200],
                    "risks": "Error parsing AI response",
                    "recommendation": "Check AI logs"
                }

        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return {
                "error": str(e),
                "summary": "Error iha prosesu analiza.",
                "risks": "Indisponível",
                "recommendation": "Tenta fali fuan balun"
            }

    def analyze_image(self, image_path, prompt=None):
        """
        Analyzes an installation photo using Gemini Vision.
        """
        if not self.client:
             return {"error": "AI Service not configured."}

        if not prompt:
            prompt = """
            Ita mak inspektór elétrika espesialista. Analiza foto instalasaun ne'e no fó kometáriu iha lian Tetum.
            Identifika:
            1. Kondisaun meteran (nu-registu, klarak, ka aat).
            2. Qualidade kabu no liga-arde (grounding).
            3. Siguransa (iha risku ahi-han ka lae).
            
            Fó resposta ho formatu JSON:
            {
                "analysis": "Deskrisaun badak kona-ba saida mak ita haree iha foto",
                "status": "Di'ak / Atenção / Perigu",
                "findings": ["nu-meteran", "kabu kloose", "etc"],
                "recommendation": "Saida mak presiza hadi'a"
            }
            """

        try:
            img = Image.open(image_path)
            # Use the SDK's multimodal capabilities
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, img]
            )
            
            import json
            import re
            text = response.text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"analysis": text, "status": "Unknown"}

        except Exception as e:
            logger.error(f"Error calling Gemini Vision API: {e}")
            return {"error": str(e)}

    def generate_executive_summary(self, data_context):
        """
        Generates a business summary based on dashboard data.
        """
        if not self.client:
            return "AI Service not configured."

        prompt = f"""
        Ita mak Konsultór Estratėjiku ba EDTL. Analiza dadus operasionál fulan ne'e nian no fó 'Executive Summary' badak iha lian Tetum.
        Highlight trend, susesu, no área ne'ebé presiza atensaun.
        
        Dadus: {data_context}
        
        Uza lian ne'ebé profisional no fó pontu importante 3-4 de'it.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return f"Error: {str(e)}"

    def get_chat_response(self, message, history=None):
        """
        Handles conversational chat with history for the Technical Assistant.
        history format: [{"role": "user", "parts": ["..."]}, {"role": "model", "parts": ["..."]}]
        """
        if not self.client:
            return "AI Service not configured."

        system_instruction = """
        Ita mak 'Asistente Tékniku EDTL'. Ajuda utilizadór ho kestaun tékniku, prosedimentu, no informasaun husi sistema EDTL.
        Responde kestaun sira ne'e iha lian Tetum ho stilu ne'ebé profisionál, amigável, no badak (concise).
        Se utilizadór husu kona-ba buat ne'ebé la relasiona ho servisu EDTL, hatán ho respeitu keta kestaun ne'e la'o relasiona.
        """

        try:
            # Construct contents with history using explicit types
            contents = []
            if history:
                for entry in history:
                    role = entry.get('role', 'user')
                    parts_data = entry.get('parts', [])
                    # Convert parts to types.Part
                    parts = [types.Part(text=p) if isinstance(p, str) else p for p in parts_data]
                    contents.append(types.Content(role=role, parts=parts))
            
            # Add current message
            contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

            # Call SDK with system instruction
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7
                )
            )
            return response.text

        except Exception as e:
            logger.error(f"Error in chat response: {e}")
            return f"Deskulpa, hau labele hatán agora (Error: {str(e)})."

    def get_public_chat_response(self, message, history=None):
        """
        Handles conversational chat for the Public Keixa Assistant.
        """
        if not self.client:
            return "AI Service not configured."

        system_instruction = """
        Ita mak 'Asistente Atendimentu EDTL'. Ita-nia knaar mak ajuda kliente públiku atu hatene kona-ba oinsá halo reklamasaun (Keixa) kona-ba problema elétrika (hanesan mate lampu, trafo aat, metran aat, seluk-seluk).
        Responde kestaun sira ne'e iha lian Tetum ho lian ne'ebé amigável, di'ak, no badak.
        Sempre fó hatene ba sira katak sira bele prenxe formuláriu keixa iha link: http://127.0.0.1:8000/keixa/
        Se utilizadór husu buat seluk ne'ebé la relasiona ho keixa/reklamasaun EDTL, hatán ho respeitu katak ita foka liu ba ajuda reklamasaun EDTL.
        """

        try:
            contents = []
            if history:
                for entry in history:
                    role = entry.get('role', 'user')
                    parts_data = entry.get('parts', [])
                    parts = [types.Part(text=p) if isinstance(p, str) else p for p in parts_data]
                    contents.append(types.Content(role=role, parts=parts))
            
            contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7
                )
            )
            return response.text

        except Exception as e:
            logger.error(f"Error in public chat response: {e}")
            return "Deskulpa, hau labele hatán agora. Favor koko fali ba tempu oin."
