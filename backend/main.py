from fastapi import FastAPI
import ollama

# Inițializăm aplicația backend-ului
app = FastAPI()


# ==========================================
# 1. BAZA DE DATE "FAKE" (Mock Data)
# Asta vei înlocui mai târziu cu funcția colegului tău
# ==========================================
def extrage_date_din_db_fake(categorie_cautata: str):
    if categorie_cautata == "cafenea":
        return [
            {
                "nume": "Hub Cafe",
                "adresa": "Piața Sfatului nr. 10",
                "reviewuri": ["Prize la fiecare masă, excelent pentru laptop.",
                              "Cafeaua e cam scumpă, dar atmosfera e super ok pt muncă."]
            },
            {
                "nume": "Liniște Coffee",
                "adresa": "Strada Mureșenilor nr. 5",
                "reviewuri": ["Cel mai bun cappuccino din Brașov!", "Nu au mese mari, e greu să vii cu echipa."]
            }
        ]
    return "Nu am găsit locații pentru această categorie."


# ==========================================
# 2. ENDPOINT-UL TĂU AI (Asta vei prezenta miercuri)
# ==========================================
@app.get("/api/ai-recommend")
def recomanda_locatie(prompt_user: str):
    # A. Extragem intenția foarte simplist pentru moment
    categorie = "cafenea" if "cafea" in prompt_user.lower() or "lucrez" in prompt_user.lower() else "alta_categorie"

    # B. Luăm datele fictive
    date_context = extrage_date_din_db_fake(categorie)

    # C. Construim promptul
    system_prompt = f"""
    Ești un ghid local prietenos din Brașov. Userul te întreabă: '{prompt_user}'.

    Ai la dispoziție următoarele date extrase din baza noastră:
    {date_context}

    Sarcina ta: 
    Alege cea mai bună locație din lista de mai sus pentru ce vrea userul. 
    Oferă un răspuns scurt (maxim 3 propoziții), menționează numele locației și folosește argumente din review-uri. NU inventa detalii!
    """

    # D. Apelăm modelul Ollama instalat la tine pe laptop
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': system_prompt}
        ])
        raspuns_ai = response['message']['content']
    except Exception as e:
        raspuns_ai = f"Eroare la conectarea cu Ollama: {str(e)}. Asigură-te că ai rulat 'ollama run llama3' în terminal."

    # E. Returnăm răspunsul
    return {"recomandare": raspuns_ai}