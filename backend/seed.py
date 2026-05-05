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
    Location(name="Cărtureşti Brașov", lat=45.6420, lng=25.5881, category="cafe", is_verified=True, rating_avg=4.6, description="Librărie cu cafenea, ideal pentru citit și lucrat.", tags=["carti", "linistit", "wifi"]),

    Location(name="Tipografia", lat=45.6418, lng=25.5908, category="cafe", is_verified=True, rating_avg=4.9, description="Ceainărie și cafenea cu aer hipsteresc, perfectă pentru discuții și studiu.", tags=["specialty-coffee", "ceai", "vibe-bun"]),
    Location(name="Sufra Coffee Shop", lat=45.64009646787187, lng=25.58825721044644, category="cafe", is_verified=True, rating_avg=4.7, description="Mic, intim, cafea excelentă chiar în centrul vechi.", tags=["specialty-coffee", "intim", "centru"]),
    Location(name="Shakespeare Coffee", lat=45.6407, lng=25.5899, category="cafe", is_verified=True, rating_avg=4.6, description="Decor clasic, cafea foarte bună și sandvișuri.", tags=["clasic", "mic-dejun", "wifi"]),
    Location(name="CH9 Specialty Coffee", lat=45.6409160, lng=25.5873689, category="cafe", is_verified=True, rating_avg=4.9, description="Aflat lângă Biserica Neagră, locul perfect pentru pasionații de cafea.", tags=["biserica-neagra", "specialty-coffee", "terasa"]),
    Location(name="Starbucks Piața Sfatului", lat=45.6415, lng=25.5887, category="cafe", is_verified=True, rating_avg=4.4, description="Clasicul Starbucks, aglomerat dar sigur, cu vedere la piață.", tags=["to-go", "vedete", "aglomerat"]),
    Location(name="Starbucks AFI", lat=45.6510, lng=25.6105, category="cafe", is_verified=True, rating_avg=4.5, description="La parterul mall-ului AFI, ideal pentru o pauză de la shopping.", tags=["mall", "to-go", "rapid"]),
    Location(name="5 to go 15 Noiembrie", lat=45.643199648902076, lng=25.595438546772765, category="cafe", is_verified=True, rating_avg=4.6, description="Perfect pentru studenții care merg spre centrul civic.", tags=["to-go", "ieftin", "studentesc"]),
    Location(name="Croitoria de Cafea", lat=45.648181274808486, lng=25.598328909671505, category="cafe", is_verified=True, rating_avg=4.8, description="Cafea prăjită local, atmosferă prietenoasă.", tags=["prajitorie", "local", "aroma"]),
    
    Location(name="Parcul Nicolae Titulescu (Central)", lat=45.6461, lng=25.5920, category="park", is_verified=True, rating_avg=4.6, description="Cel mai mare parc din centrul orașului, mereu animat.", tags=["central", "banci", "alei"]),
    Location(name="Parcul Livada Poștei", lat=45.64669067776435, lng=25.585210938595022, category="park", is_verified=True, rating_avg=4.3, description="Nod de transport, dar și o oază de verdeață la marginea centrului vechi.", tags=["tranzit", "verdeata", "relaxare"]),
    Location(name="Parcul Tractorul", lat=45.6632, lng=25.6127, category="park", is_verified=True, rating_avg=4.5, description="Parc imens cu facilități sportive și patinoar în zonă.", tags=["sport", "mare", "role"]),
    Location(name="Parcul Trandafirilor", lat=45.6407, lng=25.6139, category="park", is_verified=True, rating_avg=4.4, description="Un parc curat, perfect pentru plimbări scurte și citit.", tags=["flori", "linistit", "banci"]),
    Location(name="Parcul Gheorghe Dima (Sub Tâmpa)", lat=45.6393, lng=25.5842, category="park", is_verified=True, rating_avg=4.8, description="Alee pietonală de sub Tâmpa, cu terenuri de sport și multă natură.", tags=["padure", "sport", "panorama"]),
    Location(name="Parcul Cetățuii", lat=45.6494, lng=25.5917, category="park", is_verified=True, rating_avg=4.9, description="Vedere panoramică asupra orașului, ideal pentru pauze.", tags=["aer-liber", "vedere", "relaxare"]),

    Location(name="Colegiul Național Andrei Șaguna", lat=45.6385, lng=25.5842, category="study", is_verified=True, rating_avg=4.8, description="Unul dintre cele mai vechi și prestigioase licee, situat lângă Poarta Ecaterinei.", tags=["istoric", "prestigiu", "liceu"]),
    Location(name="Colegiul Național Dr. Ioan Meșotă", lat=45.65434835049377, lng=25.60911480967188, category="study", is_verified=True, rating_avg=4.7, description="Liceu de top în centrul civic, excelent la științe exacte.", tags=["matematica", "modern", "liceu"]),
    Location(name="Liceul de Informatică Grigore Moisil", lat=45.6443, lng=25.6254, category="study", is_verified=True, rating_avg=4.6, description="Hub-ul viitorilor programatori, foarte aproape de Universitate.", tags=["IT", "programare", "liceu"]),
    Location(name="Școala Gimnazială Nr. 6 Iacob Mureșianu", lat=45.64539358072022, lng=25.588477182685654, category="study", is_verified=True, rating_avg=4.2, description="Școală centrală cu tradiție.", tags=["scoala", "central", "elevi"]),
    Location(name="Școala Gimnazială Nr. 5", lat=45.65075959816187, lng=25.600152512446726, category="study", is_verified=True, rating_avg=4.3, description="Școală mare cu baze sportive.", tags=["scoala", "sport", "cartier"]),

    Location(name="AFI Brașov", lat=45.6499, lng=25.6104, category="landmark", is_verified=True, rating_avg=4.8, description="Mall modern în centrul civic, terasă imensă, food court variat.", tags=["shopping", "food-court", "cinema"]),
    Location(name="Coresi Shopping Resort", lat=45.6730, lng=25.6167, category="landmark", is_verified=True, rating_avg=4.7, description="Cel mai mare mall din Brașov, spații de recreere uriașe, fântâni arteziene.", tags=["shopping", "mare", "distractie"]),
    Location(name="Unirea Shopping Center", lat=45.6612, lng=25.6106, category="landmark", is_verified=True, rating_avg=3.9, description="Centru comercial clasic vis-a-vis de gară.", tags=["shopping", "gara", "accesibil"]),
    Location(name="Magnolia Shopping Center", lat=45.64100789077306, lng=25.616553738506788, category="landmark", is_verified=True, rating_avg=4.0, description="Mall de cartier în Valea Cetății (Răcădău).", tags=["shopping", "racadau", "cartier"]),

    Location(name="Biblioteca Județeană G.Barițiu", lat=45.64551618090913, lng=25.58795534035704, category="library", is_verified=True, rating_avg=4.6, description="Sală de lectură mare, liniște garantată, acces studenți gratuit.", tags=["linistit", "gratuit", "studiu"]),
    Location(name="Biblioteca Universității Transilvania", lat=45.6509, lng=25.6030, category="library", is_verified=True, rating_avg=4.4, description="Acces cu legitimație student, resurse digitale, săli silențioase.", tags=["studiu", "digital", "linistit"]),
    
    Location(name="Deane's Irish Pub", lat=45.64324588377507, lng=25.591924580835492, category="restaurant", is_verified=True, rating_avg=4.7, description="Pub irlandez, muzică live, foarte popular printre studenți.", tags=["pub", "bere", "distractie"]),
    Location(name="Aftăr Stube", lat=45.641205988144876, lng=25.59130151152112, category="restaurant", is_verified=True, rating_avg=4.8, description="Craft beer, burgeri demențiali, curte interioară relaxantă.", tags=["craft-beer", "burgeri", "vibe"]),
    Location(name="Restaurantul Sergiana", lat=45.64568740931375, lng=25.58991167041609, category="restaurant", is_verified=True, rating_avg=4.7, description="Mâncare tradițională românească, prețuri accesibile pentru studenți.", tags=["traditional", "accesibil", "romanesc"]),
    Location(name="Piața Sfatului", lat=45.6422, lng=25.5892, category="landmark", is_verified=True, rating_avg=4.9, description="Centrul istoric al Brașovului, punct de întâlnire popular.", tags=["istoric", "central", "intalnire"]),
    Location(name="Strada Republicii", lat=45.64362059282203, lng=25.59271183850691, category="landmark", is_verified=True, rating_avg=4.5, description="Stradă pietonală cu cafenele și magazine, animată toată ziua.", tags=["pietonal", "shopping", "cafenele"]),
    Location(name="Turnul Negru", lat=45.6413, lng=25.5856, category="landmark", is_verified=True, rating_avg=4.8, description="Monument istoric medieval, vedere excelentă asupra orașului.", tags=["istoric", "vedere", "medieval"]),
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