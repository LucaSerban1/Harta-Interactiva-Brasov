from app.database import SessionLocal
from app.models.location import Location
from app.models.reviews import Review
from app.models.user import User
from app.models.favorite import Favorite  # noqa: F401
from app.models.review_report import ReviewReport  # noqa: F401

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
    Location(name="Cărtureşti Brașov", lat=45.6433, lng=25.5891, category="cafe", is_verified=True, rating_avg=4.6, description="Librărie cu cafenea, ideal pentru citit.", tags=["carti", "linistit", "wifi"]),
    Location(name="Tipografia", lat=45.6418, lng=25.5908, category="cafe", is_verified=True, rating_avg=4.9, description="Ceainărie și cafenea cu aer hipsteresc, perfectă pentru discuții și studiu.", tags=["specialty-coffee", "ceai", "vibe-bun"]),
    Location(name="Sufra Coffee Shop", lat=45.64009646787187, lng=25.58825721044644, category="cafe", is_verified=True, rating_avg=4.7, description="Mic, intim, cafea excelentă chiar în centrul vechi.", tags=["specialty-coffee", "intim", "centru"]),
    Location(name="Shakespeare Coffee", lat=45.6407, lng=25.5899, category="cafe", is_verified=True, rating_avg=4.6, description="Decor clasic, cafea foarte bună și sandvișuri.", tags=["clasic", "mic-dejun", "wifi"]),
    Location(name="CH9 Specialty Coffee", lat=45.6409160, lng=25.5873689, category="cafe", is_verified=True, rating_avg=4.9, description="Aflat lângă Biserica Neagră, locul perfect pentru pasionații de cafea.", tags=["biserica-neagra", "specialty-coffee", "terasa"]),
    Location(name="Starbucks Piața Sfatului", lat=45.6415, lng=25.5887, category="cafe", is_verified=True, rating_avg=4.4, description="Clasicul Starbucks, aglomerat dar sigur, cu vedere la piață.", tags=["to-go", "vedete", "aglomerat"]),
    Location(name="Starbucks AFI", lat=45.6510, lng=25.6105, category="cafe", is_verified=True, rating_avg=4.5, description="La parterul mall-ului AFI, ideal pentru o pauză de la shopping.", tags=["mall", "to-go", "rapid"]),
    Location(name="Croitoria de Cafea", lat=45.648027045464985, lng=25.598341534556944, category="cafe", is_verified=True, rating_avg=4.8, description="Cafea prăjită local, atmosferă prietenoasă.", tags=["prajitorie", "local", "aroma"]),
    Location(name="Starbucks Coresi", lat=45.6727808, lng=25.6126953, category="cafe", is_verified=True, rating_avg=4.1, description="Starbucks în Coresi, atmosferă modernă.", tags=["starbucks", "mall"]),
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
    Location(name="Biblioteca Județeană G.Barițiu", lat=45.645859219323874, lng=25.58712639242329, category="library", is_verified=True, rating_avg=4.6, description="Sală de lectură mare, liniște garantată, acces studenți gratuit.", tags=["linistit", "gratuit", "studiu"]),
    Location(name="Biblioteca Universității Transilvania", lat=45.6509, lng=25.6030, category="library", is_verified=True, rating_avg=4.4, description="Acces cu legitimație student, resurse digitale, săli silențioase.", tags=["studiu", "digital", "linistit"]),
    Location(name="Deane's Irish Pub", lat=45.64324588377507, lng=25.591924580835492, category="restaurant", is_verified=True, rating_avg=4.7, description="Pub irlandez, muzică live, foarte popular printre studenți.", tags=["pub", "bere", "distractie"]),
    Location(name="Aftăr Stube", lat=45.64122099025954, lng=25.59117276549254, category="restaurant", is_verified=True, rating_avg=4.8, description="Craft beer, burgeri demențiali, curte interioară relaxantă.", tags=["craft-beer", "burgeri", "vibe"]),
    Location(name="Restaurantul Sergiana", lat=45.64529779354546, lng=25.58978509531678, category="restaurant", is_verified=True, rating_avg=4.7, description="Mâncare tradițională românească, prețuri accesibile pentru studenți.", tags=["traditional", "accesibil", "romanesc"]),
    Location(name="Piața Sfatului", lat=45.6422, lng=25.5892, category="landmark", is_verified=True, rating_avg=4.9, description="Centrul istoric al Brașovului, punct de întâlnire popular.", tags=["istoric", "central", "intalnire"]),
    Location(name="Strada Republicii", lat=45.64362059282203, lng=25.59271183850691, category="landmark", is_verified=True, rating_avg=4.5, description="Stradă pietonală cu cafenele și magazine, animată toată ziua.", tags=["pietonal", "shopping", "cafenele"]),
    Location(name="Turnul Negru", lat=45.6413, lng=25.5856, category="landmark", is_verified=True, rating_avg=4.8, description="Monument istoric medieval, vedere excelentă asupra orașului.", tags=["istoric", "vedere", "medieval"]),
    Location(name="Gara Brașov", lat=45.6612, lng=25.6136, category="transport", is_verified=True, rating_avg=4.5, description="Principala gară din Brașov, conexiuni naționale și internaționale.", tags=["mijloc-de-transport", "tren", "gara"]),
    Location(name="Aeroportul Internațional Brașov-Ghimbav", lat=45.7054, lng=25.5231, category="transport", is_verified=True, rating_avg=4.6, description="Aeroportul din zona Stupini, zboruri interne și europene.", tags=["mijloc-de-transport", "avion", "aeroport"]),
    Location(name="Muntele Tâmpa", lat=45.634842598486344, lng=25.59286140487929, category="landmark", is_verified=True, rating_avg=4.9, description="Muntele emblematic al Brașovului, cu trasee de drumeție și vedere panoramică.", tags=["natura", "drumetie", "panorama", "tampa"]),
    Location(name="Telecabina Tâmpa", lat=45.63906899058914, lng=25.593057621748446, category="landmark", is_verified=True, rating_avg=4.7, description="Telecabina care urcă pe Tâmpa, punct de plecare din Parcul Gheorghe Dima.", tags=["telecabina", "tampa", "atractie", "vedere"]),
    Location(name="Semnul Brașov", lat=45.634743441332176, lng=25.593177640068603, category="landmark", is_verified=True, rating_avg=4.8, description="Semnul Hollywood al Brașovului, vizibil din tot orașul, pe versantul Tâmpei.", tags=["iconic", "tampa", "vedere", "fotografie"]),
    Location(name="Poiana Brașov", lat=45.5967, lng=25.5562, category="landmark", is_verified=True, rating_avg=4.9, description="Stațiunea montană la poalele Postăvarului, cu pârtii de schi și pensiuni.", tags=["ski", "munte", "stațiune", "natura"]),
    Location(name="McDonald's Calea Bucuresti", lat=45.63406192679652, lng=25.634174663730377, category="restaurant", is_verified=True, rating_avg=4.0, description="McDonald's clasic pe Calea Bucuresti, drive-through disponibil, program 24/7, ideal pentru o masă rapidă.", tags=["fast-food", "24/7", "drive-through", "rapid"]),
    Location(name="McDonald's AFI", lat=45.6495860,lng= 25.6108813, category="restaurant", is_verified=True, rating_avg=4.1, description="McDonald's în complexul AFI, acces direct din mall, perfect după shopping.", tags=["fast-food", "mall", "afi", "rapid"]),
    Location(name="McDonald's Coresi", lat=45.672619054290955, lng=25.612057648925116, category="restaurant", is_verified=True, rating_avg=4.0, description="McDonald's în Coresi Shopping Resort, zonă modernă, parcare generoasă.", tags=["fast-food", "mall", "coresi", "parcare"]),
    Location(name="KFC Coresi", lat=45.6726607, lng=25.6134058, category="restaurant", is_verified=True, rating_avg=4.1, description="KFC în Coresi Shopping Resort, meniu complet, zona food court.", tags=["fast-food", "pui", "coresi", "food-court"]),
    Location(name="KFC AFI Brașov", lat=45.6497289, lng=25.6104909, category="restaurant", is_verified=True, rating_avg=4.2, description="KFC în AFI Brașov, unul dintre cele mai aglomerate fast-food-uri din oraș.", tags=["fast-food", "pui", "afi", "mall"]),
    Location(name="KFC Centru", lat=45.6426367, lng = 25.5894700, category="restaurant", is_verified=True, rating_avg=4.3, description="KFC în centrul Brașovului pe strada principală, cel mai accesibil fast-food din zonă.", tags=["fast-food", "pui", "central", "pietonal"]),
    Location(name="Casa Tudor", lat=45.6570359, lng= 25.5893298, category="restaurant", is_verified=True, rating_avg=4.7, description="Restaurant tradițional românesc cu specific ardelenesc, preparate din rețete vechi de familie, atmosferă caldă.", tags=["traditional", "ardelenesc", "familie", "romanesc"]),
    Location(name="Ceasu' Rău", lat=45.6500008, lng =25.6038664, category="restaurant", is_verified=True, rating_avg=4.6, description="Restaurant cu personalitate, meniu inventiv inspirat din bucătăria românească modernă, cocktailuri artizanale.", tags=["modern", "cocktailuri", "romanesc", "inventiv"]),
    Location(name="La Ceaun - Piața Sfatului", lat= 45.6432547, lng =25.5913944, category="restaurant", is_verified=True, rating_avg=4.8, description="Mâncare gătită la ceaun în inima Brașovului, porții generoase, specific montan autentic.", tags=["ceaun", "traditional", "montan", "portii-mari"]), 
    Location(name="AntreU Prosciutterie", lat=45.640824131104466, lng=25.586508933767178, category="restaurant", is_verified=True, rating_avg=4.8, description="Prosciutterie autentică pe Str. George Barițiu, mezeluri italiene fine, vinuri selecționate și antipasti.", tags=["italian", "prosciutto", "mezeluri", "vin", "antipasti"]),    
    Location(name="Vino e Sapori", lat=45.64067012434446, lng=25.586701875848078, category="restaurant", is_verified=True, rating_avg=4.7, description="Restaurant italian autentic cu accent pe vinuri și preparate toscane, carte de vinuri impresionantă.", tags=["italian", "vin", "toscan", "romantic", "premium"]),  
    Location(name="Cafenea Dallmayr Brașov", lat=45.640729913217314, lng=25.58682743674644, category="cafe", is_verified=True, rating_avg=4.6, description="Cafenea premium a brandului german Dallmayr, cafea de origine controlată, produse de patiserie fine.", tags=["premium", "german", "specialty-coffee", "patiserie"]),
    Location(name="5 to go - Str. Paul Richter", lat=45.64065042456457, lng=25.586879651004423, category="cafe", is_verified=True, rating_avg=4.2, description="Franciză 5 to go pe Paul Richter, prețuri mici, cafea rapidă, ideal pentru studenți cu buget limitat.", tags=["accesibil", "rapid", "studenti", "5togo"]),
    Location(name="Biserica Neagră", lat=45.641100683349535, lng=25.58816393372675, category="landmark", is_verified=True, rating_avg=4.9, description="Cea mai mare și impunătoare biserică gotică din România, construită în sec. XIV-XV, adăpostește colecția de covoare anatoliene unică în lume.", tags=["UNESCO", "gotic", "medieval", "covoare", "turistic", "biserica"]),
    Location(name="5 to go - Piața Sfatului", lat=45.641607200339685, lng=25.588420598718805, category="cafe", is_verified=True, rating_avg=4.3, description="5 to go în cea mai turistică locație din Brașov, cafea ieftină cu vedere la Piața Sfatului.", tags=["accesibil", "rapid", "5togo", "central", "turistic"]),
    Location(name="Terroirs Boutique du Vin", lat=45.6416888, lng =25.5908706, category="restaurant", is_verified=True, rating_avg=4.9, description="Cramă urbană și magazin de vinuri boutique, degustări ghidate, colecție de vinuri românești și internaționale de excepție.", tags=["vin", "degustare", "boutique", "premium", "romanesc", "international"]),
    Location(name="AntreU Focaccerie", lat=45.64026342257715, lng=25.58994973138341, category="restaurant", is_verified=True, rating_avg=4.7, description="Focaccerie italiană autentică, pâine focaccia proaspătă zilnic, ingrediente importate direct din Italia.", tags=["italian", "focaccia", "artizanal", "proaspat", "sandwich"]),
    Location(name="Strada Sforii", lat=45.63961869970867, lng=25.588563065807946, category="landmark", is_verified=True, rating_avg=4.8, description="Una dintre cele mai înguste străzi din Europa cu doar 111 cm lățime, fostă cale de acces pentru pompieri în sec. XVII.", tags=["turistic", "ingust", "istoric", "medieval", "unic", "foto"]),
    Location(name="Poarta Schei", lat=45.63920464497976, lng=25.586371648471648, category="landmark", is_verified=True, rating_avg=4.7, description="Poartă medievală din sec. XVIII prin care românii intrau în cetatea Brașovului, simbol al separației istorice dintre comunități.", tags=["medieval", "istoric", "poarta", "monument", "schei"]),
    Location(name="Poarta Ecaterinei", lat=45.6395389, lng=25.5860193, category="landmark", is_verified=True, rating_avg=4.8, description="Cel mai bine conservat turn de poartă medieval din Brașov, sec. XV, simbol al orașului alături de Turnul Negru.", tags=["medieval", "sec-XV", "turn", "conservat", "simbol", "turistic"]),
    Location(name="Panoramic Restaurant", lat=45.6358292846033, lng=25.59733386301749, category="restaurant", is_verified=True, rating_avg=4.5, description="Restaurant cu panoramă spectaculoasă asupra Brașovului, meniu internațional, perfect pentru ocazii speciale.", tags=["panorama", "vedere", "international", "romantic", "special"]),
    Location(name="Ando's", lat=45.645593491409954, lng=25.59941856725406, category="restaurant", is_verified=True, rating_avg=4.6, description="Restaurant fusion cu influențe asiatice și mediteraneene, sushi și preparate la grill, atmosferă modernă.", tags=["fusion", "sushi", "asian", "grill", "modern"]),
    Location(name="Star", lat=45.64363656711047, lng=25.597754007546875, category="restaurant", is_verified=True, rating_avg=4.4, description="Restaurant clasic cu meniu variat românesc și internațional, preferat de familii și grupuri mai mari.", tags=["clasic", "familie", "romanesc", "international", "grup"]),
    Location(name="Muzeul de Artă Brașov", lat=45.6450040, lng=25.5937880, category="landmark", is_verified=True, rating_avg=4.7, description="Muzeu găzduit în fosta reședință a guvernatorului, colecție impresionantă de artă românească și europeană din sec. XVII-XX.", tags=["muzeu", "arta", "cultura", "expozitie", "istoric", "european"]),
    Location(name="Panini", lat=45.6485493, lng=25.6046424, category="restaurant", is_verified=True, rating_avg=4.5, description="Sandwich bar italian specializat în panini proaspete cu ingrediente mediteraneene, ideal pentru prânz rapid.", tags=["italian", "panini", "sandwich", "rapid", "pranz", "mediteranean"]),
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