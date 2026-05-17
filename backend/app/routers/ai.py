from fastapi import APIRouter, Depends
import logging
import json
import re
import httpx
from urllib.parse import unquote
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db
from app.crud import locations as crud_locations

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

router = APIRouter(prefix="/api/ai", tags=["AI Recommendations"])

try:
    from groq import Groq

    # PUNE CHEIA TA AICI:
    client = Groq(api_key="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")
except ImportError:
    client = None

def process_google_maps_link(url: str, db: Session, client) -> Optional[dict]:
    try:
        with httpx.Client(follow_redirects=True, timeout=10.0) as http_client:
            response = http_client.get(url)
            final_url = str(response.url)
            html_content = response.text
        
        coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', final_url)
        if not coord_match:
            return None
        lat = float(coord_match.group(1))
        lng = float(coord_match.group(2))
        
        name = "Locație Necunoscută"
        name_match = re.search(r'/place/([^/&?]+)', unquote(final_url))
        if name_match:
            name = name_match.group(1).replace('+', ' ')
        else:
            title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
            if title_match and "google" not in title_match.group(1).lower():
                full_title = title_match.group(1)
                name = full_title.split('- Google Maps')[0].strip()
        
        category = "Altele"
        description = "Locație adăugată din Google Maps."
        
        if client:
            prompt = f"Am extras locația cu numele '{name}' de pe Google Maps. Te rog să alegi cea mai potrivită categorie din: [Cafenele, Biblioteci, Parcuri, Study/Cowork, Restaurante, Obiective Turistice, Altele]. Formulează și o scurtă descriere de 1-2 propoziții în română. Răspunde STRICT cu un JSON: {{\"categorie\": \"...\", \"descriere\": \"...\"}}"
            try:
                comp = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    response_format={"type": "json_object"},
                    messages=[{"role": "user", "content": prompt}]
                )
                res_data = json.loads(comp.choices[0].message.content)
                category = res_data.get("categorie", category)
                description = res_data.get("descriere", description)
            except Exception as e:
                logging.error(f"Error classifying location: {e}")

        existing = crud_locations.search(db, keyword=name)
        if existing:
            return existing[0]
            
        new_loc = crud_locations.create(
            db=db, name=name, lat=lat, lng=lng, 
            category=category, description=description, tags=["google_maps"]
        )
        return new_loc
    except Exception as e:
        logging.error(f"Error processing maps link: {e}")
        return None

@router.post("/chat")
def ai_chat(request: ChatRequest, db: Session = Depends(get_db)):
    if client is None:
        return {"error": "Libraria groq nu este instalata! Ruleaza 'pip install groq' in terminal."}

    try:
        locatii = crud_locations.get_all(db)
        
        # Verificare linkuri Google Maps in ultimul mesaj
        refresh_locations = False
        new_location_msg = ""
        if request.messages:
            last_msg = request.messages[-1].content
            urls = re.findall(r'https?://(?:www\.)?google\.com/maps[^\s]+|https?://(?:maps\.)?app\.goo\.gl/[^\s]+', last_msg)
            for url in urls:
                new_loc = process_google_maps_link(url, db, client)
                if new_loc:
                    refresh_locations = True
                    new_location_msg += f"\nSISTEM: AI DETECTAT UN LINK GOOGLE MAPS. Locația '{new_loc.name}' a fost adăugată automat pe hartă cu ID-ul {new_loc.id}. Este OBLIGATORIU să îi confirmi utilizatorului că ai adăugat locația pe hartă, să îi prezinți descrierea ei și să o folosești ca 'location_id'."
                    # Re-preluam locatiile pentru a include pe cea noua
                    locatii = crud_locations.get_all(db)

        # Formatam locatiile pentru a fi compacte pentru prompt
        date_context = [
            {"id": loc.id, "nume": loc.name, "categorie": loc.category, "descriere": loc.description, "tags": loc.tags}
            for loc in locatii
        ]

        system_prompt = f"""
        Esti un ghid local din Brasov.
        Ai la dispozitie urmatoarele date extrase din baza noastra:
        {json.dumps(date_context, ensure_ascii=False)}

        Sarcina ta:
        Raspunde la intrebarile userului cat mai natural, pastrand contextul conversatiei.
        Daca userul vrea o recomandare de locatie, alege cea mai buna locatie si pune id-ul in 'location_id'.
        Daca userul cere un traseu intre doua locatii (ex: "drumul de la X la Y", "vreau sa merg de la X la Y"), identifica cu atentie 'start_location_id' (locatia X) si 'location_id' (destinatia Y).
        Daca ai primit o notificare de sistem că o locație nouă a fost adăugată, folosește 'location_id' cu ID-ul noii locații.
        Pentru a desena ruta pe harta, este OBLIGATORIU sa returnezi ambele ID-uri ca numere, daca le gasesti in lista de date.
        Raspunde STRICT intr-un obiect JSON valid, cu urmatoarea structura:
        {{"mesaj": "Raspunsul tau detaliat...", "location_id": id_ul_locatiei_destinatie_sau_null, "start_location_id": id_ul_locatiei_de_start_sau_null, "refresh_locations": {"true" if refresh_locations else "false"}}}
        NU folosi markdown, nu adauga alte texte pe langa JSON.
        """

        # Construim array-ul de mesaje pentru Groq
        messages = [{"role": "system", "content": system_prompt}]
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})
            
        if new_location_msg:
            messages.append({"role": "system", "content": new_location_msg})

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            messages=messages
        )
        response_content = completion.choices[0].message.content
        return json.loads(response_content)
    except Exception as e:
        return {"eroare_detaliata": str(e)}