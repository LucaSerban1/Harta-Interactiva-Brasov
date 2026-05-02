from app.database import SessionLocal
from app.models.location import Location
from app.models.reviews import Review
from app.models.user import User

def seed():
    db = SessionLocal()

    if db.query(Location).count() > 0:
        print("Baza de date are deja date, skip seed.")
        db.close()
        return

    test_user = User(
        email="test@student.unitbv.ro",
        username="student_test",
        hashed_password="hashed_placeholder",
        is_active=True,
        is_admin=False
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print("User de test creat ✓")

    locations = [
        Location(name="Café del Arte", lat=45.6427, lng=25.5887,
                 category="cafe", is_verified=True, rating_avg=4.8,
                 description="Atmosferă liniștită, wifi rapid, prize la fiecare masă.",
                 tags=["wifi", "prize", "linistit"]),

        Location(name="Beans & Bytes", lat=45.6440, lng=25.5950,
                 category="cafe", is_verified=True, rating_avg=4.7,
                 description="Cafea specialty, muzică ambientală, open 07:00-22:00.",
                 tags=["wifi", "specialty-coffee", "muzica"]),

        Location(name="Cărtureşti Brașov", lat=45.6433, lng=25.5891,
                 category="cafe", is_verified=True, rating_avg=4.6,
                 description="Librărie cu cafenea, ideal pentru citit și lucrat.",
                 tags=["carti", "linistit", "wifi"]),

        Location(name="Biblioteca Județeană G.Barițiu", lat=45.6455, lng=25.5910,
                 category="library", is_verified=True, rating_avg=4.6,
                 description="Sală de lectură mare, liniște garantată, acces studenți gratuit.",
                 tags=["linistit", "gratuit", "studiu"]),

        Location(name="Biblioteca Universității Transilvania", lat=45.6395, lng=25.5890,
                 category="library", is_verified=True, rating_avg=4.4,
                 description="Acces cu legitimație student, resurse digitale, săli silențioase.",
                 tags=["studiu", "digital", "linistit"]),

        Location(name="Parcul Cetățuii", lat=45.6480, lng=25.5820,
                 category="park", is_verified=True, rating_avg=4.9,
                 description="Vedere panoramică asupra orașului, ideal pentru pauze.",
                 tags=["aer-liber", "vedere", "relaxare"]),

        Location(name="Grădina Publică Brașov", lat=45.6465, lng=25.5970,
                 category="park", is_verified=True, rating_avg=4.3,
                 description="Spațiu verde central, bănci, ideal pentru studiu în aer liber.",
                 tags=["aer-liber", "banci", "linistit"]),

        Location(name="Parcul Trandafirilor", lat=45.6510, lng=25.6020,
                 category="park", is_verified=True, rating_avg=4.5,
                 description="Parc liniștit în cartierul Astra, perfect pentru relaxare.",
                 tags=["aer-liber", "relaxare", "linistit"]),

        Location(name="Hub Studențesc Astra", lat=45.6410, lng=25.5870,
                 category="study", is_verified=True, rating_avg=4.5,
                 description="Spații de coworking, camere de grup, proiector disponibil.",
                 tags=["coworking", "grup", "proiector"]),

        Location(name="MindSpace Coworking", lat=45.6418, lng=25.5925,
                 category="study", is_verified=True, rating_avg=4.6,
                 description="Hot desks, săli meeting, cafea inclusă, 24/7.",
                 tags=["24/7", "meeting", "cafea"]),

        Location(name="Facultatea de Informatică UTB", lat=45.6400, lng=25.5880,
                 category="study", is_verified=True, rating_avg=4.2,
                 description="Laboratoare disponibile studenților în afara orelor.",
                 tags=["laboratoare", "studiu", "tehnic"]),

        Location(name="Restaurantul Sergiana", lat=45.6442, lng=25.5897,
                 category="restaurant", is_verified=True, rating_avg=4.7,
                 description="Mâncare tradițională românească, prețuri accesibile pentru studenți.",
                 tags=["traditional", "accesibil", "romanesc"]),

        Location(name="Piața Sfatului", lat=45.6430, lng=25.5887,
                 category="landmark", is_verified=True, rating_avg=4.9,
                 description="Centrul istoric al Brașovului, punct de întâlnire popular.",
                 tags=["istoric", "central", "intalnire"]),

        Location(name="Strada Republicii", lat=45.6435, lng=25.5878,
                 category="landmark", is_verified=True, rating_avg=4.5,
                 description="Stradă pietonală cu cafenele și magazine, animată toată ziua.",
                 tags=["pietonal", "shopping", "cafenele"]),

        Location(name="Turnul Negru", lat=45.6448, lng=25.5862,
                 category="landmark", is_verified=True, rating_avg=4.8,
                 description="Monument istoric medieval, vedere excelentă asupra orașului.",
                 tags=["istoric", "vedere", "medieval"]),
    ]

    for loc in locations:
        db.add(loc)

    db.commit()
    print(f"{len(locations)} locații adăugate în baza de date ✓")
    db.close()

if __name__ == "__main__":
    seed()