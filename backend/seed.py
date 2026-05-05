from app.database import SessionLocal
from app.models.location import Location
from app.models.reviews import Review
from app.models.user import User

def seed():
    db = SessionLocal()

    test_user = db.query(User).filter(User.username == "student_test").first()
    
    if not test_user:
        test_user = User(
            email="test@s.unibuc.ro",
            username="student_test",
            hashed_password="hashed_placeholder",
            is_active=True,
            is_admin=False
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print("User de test creat ✓")
    else:
        print("User de test există deja, skip ✓")

    locations = [
    Location(name="Café del Arte", lat=45.6427, lng=25.5887, category="cafe", is_verified=True, rating_avg=4.8, description="Atmosferă liniștită, wifi rapid, prize la fiecare masă.", tags=["wifi", "prize", "linistit"]),
    Location(name="Beans & Bytes", lat=45.6440, lng=25.5950, category="cafe", is_verified=True, rating_avg=4.7, description="Cafea specialty, muzică ambientală, open 07:00-22:00.", tags=["wifi", "specialty-coffee", "muzica"]),
    Location(name="Cărtureşti Brașov", lat=45.6433, lng=25.5891, category="cafe", is_verified=True, rating_avg=4.6, description="Librărie cu cafenea, ideal pentru citit și lucrat.", tags=["carti", "linistit", "wifi"]),

    Location(name="Tipografia", lat=45.6441, lng=25.5900, category="cafe", is_verified=True, rating_avg=4.9, description="Ceainărie și cafenea cu aer hipsteresc, perfectă pentru discuții și studiu.", tags=["specialty-coffee", "ceai", "vibe-bun"]),
    Location(name="Sufra Coffee Shop", lat=45.6432, lng=25.5895, category="cafe", is_verified=True, rating_avg=4.7, description="Mic, intim, cafea excelentă chiar în centrul vechi.", tags=["specialty-coffee", "intim", "centru"]),
    Location(name="Shakespeare Coffee", lat=45.6445, lng=25.5880, category="cafe", is_verified=True, rating_avg=4.6, description="Decor clasic, cafea foarte bună și sandvișuri.", tags=["clasic", "mic-dejun", "wifi"]),
    Location(name="CH9 Specialty Coffee", lat=45.6398, lng=25.5882, category="cafe", is_verified=True, rating_avg=4.9, description="Aflat lângă Biserica Neagră, locul perfect pentru pasionații de cafea.", tags=["biserica-neagra", "specialty-coffee", "terasa"]),
    Location(name="Starbucks Piața Sfatului", lat=45.6425, lng=25.5885, category="cafe", is_verified=True, rating_avg=4.4, description="Clasicul Starbucks, aglomerat dar sigur, cu vedere la piață.", tags=["to-go", "vedete", "aglomerat"]),
    Location(name="Starbucks AFI", lat=45.6513, lng=25.6105, category="cafe", is_verified=True, rating_avg=4.5, description="La parterul mall-ului AFI, ideal pentru o pauză de la shopping.", tags=["mall", "to-go", "rapid"]),
    Location(name="5 to go Republicii", lat=45.6438, lng=25.5883, category="cafe", is_verified=True, rating_avg=4.5, description="Cafea rapidă pe strada principală a orașului.", tags=["to-go", "ieftin", "rapid"]),
    Location(name="5 to go 15 Noiembrie", lat=45.6480, lng=25.6020, category="cafe", is_verified=True, rating_avg=4.6, description="Perfect pentru studenții care merg spre centrul civic.", tags=["to-go", "ieftin", "studentesc"]),
    Location(name="Croitoria de Cafea", lat=45.6461, lng=25.5940, category="cafe", is_verified=True, rating_avg=4.8, description="Cafea prăjită local, atmosferă prietenoasă.", tags=["prajitorie", "local", "aroma"]),
    Location(name="Nola Coffee Shop", lat=45.6420, lng=25.5890, category="cafe", is_verified=True, rating_avg=4.7, description="Design minimalist, matcha și cafea premium.", tags=["matcha", "minimalist", "specialty-coffee"]),

    Location(name="Parcul Nicolae Titulescu (Central)", lat=45.6460, lng=25.5940, category="park", is_verified=True, rating_avg=4.6, description="Cel mai mare parc din centrul orașului, mereu animat.", tags=["central", "banci", "alei"]),
    Location(name="Parcul Livada Poștei", lat=45.6468, lng=25.5880, category="park", is_verified=True, rating_avg=4.3, description="Nod de transport, dar și o oază de verdeață la marginea centrului vechi.", tags=["tranzit", "verdeata", "relaxare"]),
    Location(name="Parcul Tractorul", lat=45.6660, lng=25.6050, category="park", is_verified=True, rating_avg=4.5, description="Parc imens cu facilități sportive și patinoar în zonă.", tags=["sport", "mare", "role"]),
    Location(name="Parcul Trandafirilor", lat=45.6432, lng=25.6120, category="park", is_verified=True, rating_avg=4.4, description="Un parc curat, perfect pentru plimbări scurte și citit.", tags=["flori", "linistit", "banci"]),
    Location(name="Parcul Gheorghe Dima (Sub Tâmpa)", lat=45.6405, lng=25.5865, category="park", is_verified=True, rating_avg=4.8, description="Alee pietonală de sub Tâmpa, cu terenuri de sport și multă natură.", tags=["padure", "sport", "panorama"]),
    Location(name="Parcul Cetățuii", lat=45.6480, lng=25.5820, category="park", is_verified=True, rating_avg=4.9, description="Vedere panoramică asupra orașului, ideal pentru pauze.", tags=["aer-liber", "vedere", "relaxare"]),

    Location(name="Colegiul Național Andrei Șaguna", lat=45.6380, lng=25.5835, category="study", is_verified=True, rating_avg=4.8, description="Unul dintre cele mai vechi și prestigioase licee, situat lângă Poarta Ecaterinei.", tags=["istoric", "prestigiu", "liceu"]),
    Location(name="Colegiul Național Dr. Ioan Meșotă", lat=45.6520, lng=25.6125, category="study", is_verified=True, rating_avg=4.7, description="Liceu de top în centrul civic, excelent la științe exacte.", tags=["matematica", "modern", "liceu"]),
    Location(name="Liceul de Informatică Grigore Moisil", lat=45.6465, lng=25.6050, category="study", is_verified=True, rating_avg=4.6, description="Hub-ul viitorilor programatori, foarte aproape de Universitate.", tags=["IT", "programare", "liceu"]),
    Location(name="Școala Gimnazială Nr. 6 Iacob Mureșianu", lat=45.6450, lng=25.5920, category="study", is_verified=True, rating_avg=4.2, description="Școală centrală cu tradiție.", tags=["scoala", "central", "elevi"]),
    Location(name="Școala Gimnazială Nr. 5", lat=45.6540, lng=25.5880, category="study", is_verified=True, rating_avg=4.3, description="Școală mare cu baze sportive.", tags=["scoala", "sport", "cartier"]),

    Location(name="AFI Brașov", lat=45.6511, lng=25.6108, category="landmark", is_verified=True, rating_avg=4.8, description="Mall modern în centrul civic, terasă imensă, food court variat.", tags=["shopping", "food-court", "cinema"]),
    Location(name="Coresi Shopping Resort", lat=45.6710, lng=25.6150, category="landmark", is_verified=True, rating_avg=4.7, description="Cel mai mare mall din Brașov, spații de recreere uriașe, fântâni arteziene.", tags=["shopping", "mare", "distractie"]),
    Location(name="Unirea Shopping Center", lat=45.6530, lng=25.6115, category="landmark", is_verified=True, rating_avg=3.9, description="Centru comercial clasic vis-a-vis de gară.", tags=["shopping", "gara", "accesibil"]),
    Location(name="Magnolia Shopping Center", lat=45.6495, lng=25.5780, category="landmark", is_verified=True, rating_avg=4.0, description="Mall de cartier în Valea Cetății (Răcădău).", tags=["shopping", "racadau", "cartier"]),

    Location(name="Biblioteca Județeană G.Barițiu", lat=45.6455, lng=25.5910, category="library", is_verified=True, rating_avg=4.6, description="Sală de lectură mare, liniște garantată, acces studenți gratuit.", tags=["linistit", "gratuit", "studiu"]),
    Location(name="Biblioteca Universității Transilvania", lat=45.6395, lng=25.5890, category="library", is_verified=True, rating_avg=4.4, description="Acces cu legitimație student, resurse digitale, săli silențioase.", tags=["studiu", "digital", "linistit"]),
    Location(name="Hub Studențesc Astra", lat=45.6410, lng=25.5870, category="study", is_verified=True, rating_avg=4.5, description="Spații de coworking, camere de grup, proiector disponibil.", tags=["coworking", "grup", "proiector"]),
    Location(name="MindSpace Coworking", lat=45.6418, lng=25.5925, category="study", is_verified=True, rating_avg=4.6, description="Hot desks, săli meeting, cafea inclusă, 24/7.", tags=["24/7", "meeting", "cafea"]),

    Location(name="Deane's Irish Pub", lat=45.6436, lng=25.5881, category="restaurant", is_verified=True, rating_avg=4.7, description="Pub irlandez, muzică live, foarte popular printre studenți.", tags=["pub", "bere", "distractie"]),
    Location(name="Aftăr Stube", lat=45.6440, lng=25.5905, category="restaurant", is_verified=True, rating_avg=4.8, description="Craft beer, burgeri demențiali, curte interioară relaxantă.", tags=["craft-beer", "burgeri", "vibe"]),
    Location(name="Restaurantul Sergiana", lat=45.6442, lng=25.5897, category="restaurant", is_verified=True, rating_avg=4.7, description="Mâncare tradițională românească, prețuri accesibile pentru studenți.", tags=["traditional", "accesibil", "romanesc"]),
    Location(name="Berăria Ciucaș", lat=45.6433, lng=25.5888, category="restaurant", is_verified=True, rating_avg=4.3, description="Mici, bere la halbă, prețuri studențești direct în centru.", tags=["ieftin", "mici", "terasa"]),
    Location(name="Piața Sfatului", lat=45.6430, lng=25.5887, category="landmark", is_verified=True, rating_avg=4.9, description="Centrul istoric al Brașovului, punct de întâlnire popular.", tags=["istoric", "central", "intalnire"]),
    Location(name="Strada Republicii", lat=45.6435, lng=25.5878, category="landmark", is_verified=True, rating_avg=4.5, description="Stradă pietonală cu cafenele și magazine, animată toată ziua.", tags=["pietonal", "shopping", "cafenele"]),
    Location(name="Turnul Negru", lat=45.6448, lng=25.5862, category="landmark", is_verified=True, rating_avg=4.8, description="Monument istoric medieval, vedere excelentă asupra orașului.", tags=["istoric", "vedere", "medieval"]),
]

    existing_locations = db.query(Location.name).all()
    existing_names = {loc[0] for loc in existing_locations}
    new_locations_count = 0
    for loc in locations:
        if loc.name not in existing_names:
            db.add(loc)
            new_locations_count += 1

    if new_locations_count > 0:
        db.commit()
        print(f"{new_locations_count} locații NOI adăugate în baza de date ✓")
    else:
        print("Toate locațiile existau deja. Nu s-a adăugat nimic nou. ✓")

    db.close()

if __name__ == "__main__":
    seed()