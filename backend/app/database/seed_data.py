from sqlalchemy.orm import Session
from app.models.location import District, Taluk
from app.models.crop import Crop
from app.models.pattam import Pattam

TN_DISTRICTS_DATA = [
    {
        "name_en": "Ariyalur", "name_ta": "அரியலூர்", "lat": 11.1401, "lon": 79.0786,
        "taluks": [
            {"name_en": "Ariyalur", "name_ta": "அரியலூர்", "lat": 11.1401, "lon": 79.0786},
            {"name_en": "Udayarpalayam", "name_ta": "உடையார்பாளையம்", "lat": 11.1895, "lon": 79.2965},
            {"name_en": "Sendurai", "name_ta": "செந்துறை", "lat": 11.2721, "lon": 79.1764},
            {"name_en": "Andimadam", "name_ta": "ஆண்டிமடம்", "lat": 11.3364, "lon": 79.3789},
        ]
    },
    {
        "name_en": "Chengalpattu", "name_ta": "செங்கல்பட்டு", "lat": 12.6922, "lon": 79.9774,
        "taluks": [
            {"name_en": "Chengalpattu", "name_ta": "செங்கல்பட்டு", "lat": 12.6922, "lon": 79.9774},
            {"name_en": "Kancheepuram", "name_ta": "மதுராந்தகம்", "lat": 12.5097, "lon": 79.8821},
            {"name_en": "Cheyyur", "name_ta": "செய்யூர்", "lat": 12.3551, "lon": 80.0076},
            {"name_en": "Tiruporur", "name_ta": "திருப்போரூர்", "lat": 12.7247, "lon": 80.1873},
            {"name_en": "Tambaram", "name_ta": "தாம்பரம்", "lat": 12.9249, "lon": 80.1260},
            {"name_en": "Pallavaram", "name_ta": "பல்லாவரம்", "lat": 12.9675, "lon": 80.1491},
            {"name_en": "Vandalur", "name_ta": "வண்டலூர்", "lat": 12.8914, "lon": 80.0815},
            {"name_en": "Kundrathur", "name_ta": "குன்றத்தூர்", "lat": 12.9977, "lon": 80.0972},
        ]
    },
    {
        "name_en": "Chennai", "name_ta": "சென்னை", "lat": 13.0827, "lon": 80.2707,
        "taluks": [
            {"name_en": "Tondiarpet", "name_ta": "தண்டையார்பேட்டை", "lat": 13.1256, "lon": 80.2872},
            {"name_en": "Mylapore", "name_ta": "மயிலாப்பூர்", "lat": 13.0368, "lon": 80.2676},
            {"name_en": "Guindy", "name_ta": "கிண்டி", "lat": 13.0067, "lon": 80.2025},
            {"name_en": "Egmore", "name_ta": "எழும்பூர்", "lat": 13.0784, "lon": 80.2612},
            {"name_en": "Ambattur", "name_ta": "அம்பத்தூர்", "lat": 13.1143, "lon": 80.1548},
        ]
    },
    {
        "name_en": "Coimbatore", "name_ta": "கோயம்புத்தூர்", "lat": 11.0168, "lon": 76.9558,
        "taluks": [
            {"name_en": "Coimbatore North", "name_ta": "கோயம்புத்தூர் வடக்கு", "lat": 11.0350, "lon": 76.9550},
            {"name_en": "Coimbatore South", "name_ta": "கோயம்புத்தூர் தெற்கு", "lat": 10.9850, "lon": 76.9650},
            {"name_en": "Pollachi", "name_ta": "பொள்ளாச்சி", "lat": 10.6609, "lon": 77.0089},
            {"name_en": "Mettupalayam", "name_ta": "மேட்டுப்பாளையம்", "lat": 11.3000, "lon": 76.9500},
            {"name_en": "Sulur", "name_ta": "சூலூர்", "lat": 11.0242, "lon": 77.1264},
            {"name_en": "Annur", "name_ta": "அன்னூர்", "lat": 11.2333, "lon": 77.1333},
            {"name_en": "Kinathukadavu", "name_ta": "கிணத்துக்கடவு", "lat": 10.8222, "lon": 77.0194},
            {"name_en": "Valparai", "name_ta": "வால்பாறை", "lat": 10.3255, "lon": 76.9558},
            {"name_en": "Madukkarai", "name_ta": "மதுக்கரை", "lat": 10.9022, "lon": 76.9644},
            {"name_en": "Perur", "name_ta": "பேரூர்", "lat": 10.9700, "lon": 76.9100},
        ]
    },
    {
        "name_en": "Cuddalore", "name_ta": "கடலூர்", "lat": 11.7480, "lon": 79.7714,
        "taluks": [
            {"name_en": "Cuddalore", "name_ta": "கடலூர்", "lat": 11.7480, "lon": 79.7714},
            {"name_en": "Panruti", "name_ta": "பண்ருட்டி", "lat": 11.7700, "lon": 79.5500},
            {"name_en": "Chidambaram", "name_ta": "சிதம்பரம்", "lat": 11.3994, "lon": 79.6936},
            {"name_en": "Virudhachalam", "name_ta": "விருத்தாசலம்", "lat": 11.5000, "lon": 79.3300},
            {"name_en": "Tittakudi", "name_ta": "திட்டக்குடி", "lat": 11.4100, "lon": 79.1200},
            {"name_en": "Kattumannarkoil", "name_ta": "காட்டுமன்னார்கோயில்", "lat": 11.2750, "lon": 79.5550},
            {"name_en": "Kurinjipadi", "name_ta": "குறிஞ்சிப்பாடி", "lat": 11.5667, "lon": 79.5833},
            {"name_en": "Srimushnam", "name_ta": "ஸ்ரீமுஷ்ணம்", "lat": 11.4000, "lon": 79.4000},
            {"name_en": "Bhuvanagiri", "name_ta": "புவனகிரி", "lat": 11.4667, "lon": 79.6333},
            {"name_en": "Veppur", "name_ta": "வேப்பூர்", "lat": 11.5400, "lon": 79.0500},
        ]
    },
    {
        "name_en": "Dharmapuri", "name_ta": "தர்மபுரி", "lat": 12.1211, "lon": 78.1582,
        "taluks": [
            {"name_en": "Dharmapuri", "name_ta": "தர்மபுரி", "lat": 12.1211, "lon": 78.1582},
            {"name_en": "Harur", "name_ta": "அரூர்", "lat": 12.0600, "lon": 78.5000},
            {"name_en": "Palacode", "name_ta": "பாலக்கோடு", "lat": 12.3000, "lon": 78.0800},
            {"name_en": "Pennagaram", "name_ta": "பென்னாகரம்", "lat": 12.1300, "lon": 77.9000},
            {"name_en": "Pappireddipatti", "name_ta": "பாப்பிரெட்டிப்பட்டி", "lat": 11.9167, "lon": 78.3667},
            {"name_en": "Karimangalam", "name_ta": "காரிமங்கலம்", "lat": 12.3083, "lon": 78.2083},
            {"name_en": "Nallampalli", "name_ta": "நல்லம்பள்ளி", "lat": 12.0667, "lon": 78.1167},
        ]
    },
    {
        "name_en": "Dindigul", "name_ta": "திண்டுக்கல்", "lat": 10.3673, "lon": 77.9803,
        "taluks": [
            {"name_en": "Dindigul East", "name_ta": "திண்டுக்கல் கிழக்கு", "lat": 10.3673, "lon": 77.9803},
            {"name_en": "Dindigul West", "name_ta": "திண்டுக்கல் மேற்கு", "lat": 10.3700, "lon": 77.9500},
            {"name_en": "Palani", "name_ta": "பழனி", "lat": 10.4500, "lon": 77.5200},
            {"name_en": "Oddanchatram", "name_ta": "ஒட்டன்சத்திரம்", "lat": 10.4800, "lon": 77.7500},
            {"name_en": "Kodaikanal", "name_ta": "கொடைக்கானல்", "lat": 10.2381, "lon": 77.4892},
            {"name_en": "Natham", "name_ta": "நத்தம்", "lat": 10.2333, "lon": 78.2333},
            {"name_en": "Nilakottai", "name_ta": "நிலக்கோட்டை", "lat": 10.1667, "lon": 77.8667},
            {"name_en": "Vedasandur", "name_ta": "வேடசந்தூர்", "lat": 10.5333, "lon": 77.9500},
            {"name_en": "Gujiliamparai", "name_ta": "குஜிலியம்பாறை", "lat": 10.6667, "lon": 78.1333},
            {"name_en": "Authoor", "name_ta": "ஆத்தூர்", "lat": 10.2800, "lon": 77.8500},
        ]
    },
    {
        "name_en": "Erode", "name_ta": "ஈரோடு", "lat": 11.3410, "lon": 77.7172,
        "taluks": [
            {"name_en": "Erode", "name_ta": "ஈரோடு", "lat": 11.3410, "lon": 77.7172},
            {"name_en": "Bhavani", "name_ta": "பவானி", "lat": 11.4500, "lon": 77.6800},
            {"name_en": "Gobichettipalayam", "name_ta": "கோபிசெட்டிபாளையம்", "lat": 11.4550, "lon": 77.4380},
            {"name_en": "Sathyamangalam", "name_ta": "சத்தியமங்கலம்", "lat": 11.5039, "lon": 77.2405},
            {"name_en": "Perundurai", "name_ta": "பெருந்துறை", "lat": 11.2758, "lon": 77.5847},
            {"name_en": "Anthiyur", "name_ta": "அந்தியூர்", "lat": 11.5794, "lon": 77.5900},
            {"name_en": "Modakkurichi", "name_ta": "மொடக்குறிச்சி", "lat": 11.2400, "lon": 77.7700},
            {"name_en": "Kodumudi", "name_ta": "கொடுமுடி", "lat": 11.0800, "lon": 77.8800},
            {"name_en": "Thalavadi", "name_ta": "தாளவாடி", "lat": 11.7800, "lon": 77.0100},
            {"name_en": "Nambiyur", "name_ta": "நம்பியூர்", "lat": 11.3600, "lon": 77.3200},
        ]
    },
    {
        "name_en": "Kallakurichi", "name_ta": "கள்ளக்குறிச்சி", "lat": 11.7384, "lon": 78.9639,
        "taluks": [
            {"name_en": "Kallakurichi", "name_ta": "கள்ளக்குறிச்சி", "lat": 11.7384, "lon": 78.9639},
            {"name_en": "Sankarapuram", "name_ta": "சங்கராபுரம்", "lat": 11.8833, "lon": 78.9167},
            {"name_en": "Chinnasalem", "name_ta": "சின்னசேலம்", "lat": 11.6500, "lon": 78.8833},
            {"name_en": "Ulundurpet", "name_ta": "உளுந்தூர்பேட்டை", "lat": 11.6900, "lon": 79.2900},
            {"name_en": "Tirukoilur", "name_ta": "திருக்கோவிலூர்", "lat": 11.9667, "lon": 79.2000},
            {"name_en": "Kalvarayan Hills", "name_ta": "கல்வராயன் மலை", "lat": 11.8500, "lon": 78.7500},
        ]
    },
    {
        "name_en": "Kancheepuram", "name_ta": "காஞ்சிபுரம்", "lat": 12.8342, "lon": 79.7036,
        "taluks": [
            {"name_en": "Kancheepuram", "name_ta": "காஞ்சிபுரம்", "lat": 12.8342, "lon": 79.7036},
            {"name_en": "Sriperumbudur", "name_ta": "ஸ்ரீபெரும்புதூர்", "lat": 12.9667, "lon": 79.9500},
            {"name_en": "Uthiramerur", "name_ta": "உத்திரமேரூர்", "lat": 12.6167, "lon": 79.7667},
            {"name_en": "Walajabad", "name_ta": "வாலாஜாபாத்", "lat": 12.8000, "lon": 79.8167},
            {"name_en": "Kundrathur", "name_ta": "குன்றத்தூர்", "lat": 12.9977, "lon": 80.0972},
        ]
    },
    {
        "name_en": "Karur", "name_ta": "கரூர்", "lat": 10.9601, "lon": 78.0766,
        "taluks": [
            {"name_en": "Karur", "name_ta": "கரூர்", "lat": 10.9601, "lon": 78.0766},
            {"name_en": "Kulithalai", "name_ta": "குளித்தலை", "lat": 10.9333, "lon": 78.4167},
            {"name_en": "Aravakurichi", "name_ta": "அரவக்குறிச்சி", "lat": 10.7700, "lon": 77.9100},
            {"name_en": "Krishnarayapuram", "name_ta": "கிருஷ்ணராயபுரம்", "lat": 10.9600, "lon": 78.2800},
            {"name_en": "Manmangalam", "name_ta": "மண்மங்கலம்", "lat": 11.0200, "lon": 78.0900},
            {"name_en": "Kadavur", "name_ta": "கடவூர்", "lat": 10.6000, "lon": 78.2000},
            {"name_en": "Pugalur", "name_ta": "புகழூர்", "lat": 11.0700, "lon": 78.0100},
        ]
    },
    {
        "name_en": "Krishnagiri", "name_ta": "கிருஷ்ணகிரி", "lat": 12.5186, "lon": 78.2138,
        "taluks": [
            {"name_en": "Krishnagiri", "name_ta": "கிருஷ்ணகிரி", "lat": 12.5186, "lon": 78.2138},
            {"name_en": "Hosur", "name_ta": "ஓசூர்", "lat": 12.7409, "lon": 77.8253},
            {"name_en": "Pochampalli", "name_ta": "போச்சம்பள்ளி", "lat": 12.3333, "lon": 78.3667},
            {"name_en": "Uthangarai", "name_ta": "ஊத்தங்கரை", "lat": 12.2667, "lon": 78.5333},
            {"name_en": "Denkanikottai", "name_ta": "தேன்கனிக்கோட்டை", "lat": 12.5333, "lon": 77.7833},
            {"name_en": "Bargur", "name_ta": "பர்கூர்", "lat": 12.5500, "lon": 78.3600},
            {"name_en": "Shoolagiri", "name_ta": "சூளகிரி", "lat": 12.6700, "lon": 78.0100},
            {"name_en": "Anchetty", "name_ta": "அஞ்செட்டி", "lat": 12.3100, "lon": 77.7400},
        ]
    },
    {
        "name_en": "Madurai", "name_ta": "மதுரை", "lat": 9.9252, "lon": 78.1198,
        "taluks": [
            {"name_en": "Madurai North", "name_ta": "மதுரை வடக்கு", "lat": 9.9500, "lon": 78.1200},
            {"name_en": "Madurai South", "name_ta": "மதுரை தெற்கு", "lat": 9.9000, "lon": 78.1100},
            {"name_en": "Melur", "name_ta": "மேலூர்", "lat": 10.0333, "lon": 78.3333},
            {"name_en": "Usilampatti", "name_ta": "உசிலம்பட்டி", "lat": 9.9667, "lon": 77.8000},
            {"name_en": "Vadipatti", "name_ta": "வாடிப்பட்டி", "lat": 10.0833, "lon": 77.9667},
            {"name_en": "Thirumangalam", "name_ta": "திருமங்கலம்", "lat": 9.8167, "lon": 77.9833},
            {"name_en": "Peraiyur", "name_ta": "பேரையூர்", "lat": 9.7167, "lon": 77.7833},
            {"name_en": "Madurai East", "name_ta": "மதுரை கிழக்கு", "lat": 9.9300, "lon": 78.1800},
            {"name_en": "Madurai West", "name_ta": "மதுரை மேற்கு", "lat": 9.9200, "lon": 78.0500},
            {"name_en": "Tiruparankundram", "name_ta": "திருப்பரங்குன்றம்", "lat": 9.8800, "lon": 78.0700},
            {"name_en": "Kallikudi", "name_ta": "கள்ளிக்குடி", "lat": 9.6800, "lon": 77.9400},
        ]
    },
    {
        "name_en": "Mayiladuthurai", "name_ta": "மயிலாடுதுறை", "lat": 11.1075, "lon": 79.6524,
        "taluks": [
            {"name_en": "Mayiladuthurai", "name_ta": "மயிலாடுதுறை", "lat": 11.1075, "lon": 79.6524},
            {"name_en": "Sirkazhi", "name_ta": "சீர்காழி", "lat": 11.2333, "lon": 79.7333},
            {"name_en": "Tharangambadi", "name_ta": "தரங்கம்பாடி", "lat": 11.0333, "lon": 79.8500},
            {"name_en": "Kuthalam", "name_ta": "குத்தாலம்", "lat": 11.0800, "lon": 79.5500},
        ]
    },
    {
        "name_en": "Nagapattinam", "name_ta": "நாகப்பட்டினம்", "lat": 10.7672, "lon": 79.8449,
        "taluks": [
            {"name_en": "Nagapattinam", "name_ta": "நாகப்பட்டினம்", "lat": 10.7672, "lon": 79.8449},
            {"name_en": "Kilvelur", "name_ta": "கீழ்வேளூர்", "lat": 10.7000, "lon": 79.7500},
            {"name_en": "Vedaranyam", "name_ta": "வேதாரண்யம்", "lat": 10.3700, "lon": 79.8500},
            {"name_en": "Thirukkuvalai", "name_ta": "திருக்குவளை", "lat": 10.6000, "lon": 79.7167},
        ]
    },
    {
        "name_en": "Kanniyakumari", "name_ta": "கன்னியாகுமரி", "lat": 8.0883, "lon": 77.5385,
        "taluks": [
            {"name_en": "Agastheeswaram", "name_ta": "அகத்தீஸ்வரம்", "lat": 8.1667, "lon": 77.5167},
            {"name_en": "Thovalai", "name_ta": "தோவாளை", "lat": 8.2333, "lon": 77.5000},
            {"name_en": "Kalkulam", "name_ta": "கல்குளம்", "lat": 8.2667, "lon": 77.3167},
            {"name_en": "Vilavancode", "name_ta": "விளவங்கோடு", "lat": 8.3333, "lon": 77.2000},
            {"name_en": "Thiruvattar", "name_ta": "திருவட்டார்", "lat": 8.3300, "lon": 77.2700},
            {"name_en": "Killiyoor", "name_ta": "கிள்ளியூர்", "lat": 8.2400, "lon": 77.1900},
        ]
    },
    {
        "name_en": "Namakkal", "name_ta": "நாமக்கல்", "lat": 11.2189, "lon": 78.1674,
        "taluks": [
            {"name_en": "Namakkal", "name_ta": "நாமக்கல்", "lat": 11.2189, "lon": 78.1674},
            {"name_en": "Rasipuram", "name_ta": "ராசிபுரம்", "lat": 11.4667, "lon": 78.1833},
            {"name_en": "Tiruchengode", "name_ta": "திருச்செங்கோடு", "lat": 11.3800, "lon": 77.8900},
            {"name_en": "Paramathi Velur", "name_ta": "பரமத்தி வேலூர்", "lat": 11.1167, "lon": 78.0000},
            {"name_en": "Kolli Hills", "name_ta": "கொல்லிமலை", "lat": 11.2500, "lon": 78.3333},
            {"name_en": "Kumarapalayam", "name_ta": "குமாரபாளையம்", "lat": 11.4400, "lon": 77.7000},
            {"name_en": "Sendamangalam", "name_ta": "சேந்தமங்கலம்", "lat": 11.2800, "lon": 78.2400},
            {"name_en": "Mohanur", "name_ta": "மோகனூர்", "lat": 11.0600, "lon": 78.1400},
        ]
    },
    {
        "name_en": "Perambalur", "name_ta": "பெரம்பலூர்", "lat": 11.2342, "lon": 78.8820,
        "taluks": [
            {"name_en": "Perambalur", "name_ta": "பெரம்பலூர்", "lat": 11.2342, "lon": 78.8820},
            {"name_en": "Kunnam", "name_ta": "குன்னம்", "lat": 11.2833, "lon": 79.0167},
            {"name_en": "Veppanthattai", "name_ta": "வேப்பந்தட்டை", "lat": 11.3500, "lon": 78.7833},
            {"name_en": "Alathur", "name_ta": "ஆலத்தூர்", "lat": 11.1600, "lon": 78.8800},
        ]
    },
    {
        "name_en": "Pudukkottai", "name_ta": "புதுக்கோட்டை", "lat": 10.3797, "lon": 78.8208,
        "taluks": [
            {"name_en": "Pudukkottai", "name_ta": "புதுக்கோட்டை", "lat": 10.3797, "lon": 78.8208},
            {"name_en": "Alangudi", "name_ta": "ஆலங்குடி", "lat": 10.3500, "lon": 78.9833},
            {"name_en": "Aranthangi", "name_ta": "அறந்தாங்கி", "lat": 10.1667, "lon": 78.9833},
            {"name_en": "Gandarvakottai", "name_ta": "கந்தர்வக்கோட்டை", "lat": 10.5833, "lon": 79.0167},
            {"name_en": "Kulathur", "name_ta": "குளத்தூர்", "lat": 10.5500, "lon": 78.7667},
            {"name_en": "Thirumayam", "name_ta": "திருமயம்", "lat": 10.2500, "lon": 78.7500},
            {"name_en": "Avudaiyarkoil", "name_ta": "ஆவுடையார்கோவில்", "lat": 10.0800, "lon": 79.0300},
            {"name_en": "Manamelkudi", "name_ta": "மணமேல்குடி", "lat": 9.9600, "lon": 79.1300},
            {"name_en": "Illuppur", "name_ta": "இலுப்பூர்", "lat": 10.5100, "lon": 78.6300},
            {"name_en": "Ponnamaravathi", "name_ta": "பொன்னமராவதி", "lat": 10.2400, "lon": 78.5300},
            {"name_en": "Viralimalai", "name_ta": "விராலிமலை", "lat": 10.6000, "lon": 78.5400},
            {"name_en": "Karambakkudi", "name_ta": "கறம்பக்குடி", "lat": 10.4600, "lon": 79.1300},
        ]
    },
    {
        "name_en": "Ramanathapuram", "name_ta": "ராமநாதபுரம்", "lat": 9.3639, "lon": 78.8395,
        "taluks": [
            {"name_en": "Ramanathapuram", "name_ta": "ராமநாதபுரம்", "lat": 9.3639, "lon": 78.8395},
            {"name_en": "Paramakudi", "name_ta": "பரமக்குடி", "lat": 9.5333, "lon": 78.5833},
            {"name_en": "Tiruvadanai", "name_ta": "திருவாடானை", "lat": 9.7833, "lon": 78.9167},
            {"name_en": "Rameswaram", "name_ta": "ராமேஸ்வரம்", "lat": 9.2881, "lon": 79.3129},
            {"name_en": "Mudukulathur", "name_ta": "முதுகுளத்தூர்", "lat": 9.3333, "lon": 78.5000},
            {"name_en": "Kamuthi", "name_ta": "கமுதி", "lat": 9.4000, "lon": 78.3667},
            {"name_en": "Kadaladi", "name_ta": "கடலாடி", "lat": 9.2333, "lon": 78.5000},
            {"name_en": "Kilakarai", "name_ta": "கீழக்கரை", "lat": 9.2300, "lon": 78.7800},
            {"name_en": "RS Mangalam", "name_ta": "ஆர்.எஸ்.மங்கலம்", "lat": 9.8200, "lon": 78.7600},
        ]
    },
    {
        "name_en": "Ranipet", "name_ta": "ராணிப்பேட்டை", "lat": 12.9279, "lon": 79.3328,
        "taluks": [
            {"name_en": "Ranipet", "name_ta": "ராணிப்பேட்டை", "lat": 12.9279, "lon": 79.3328},
            {"name_en": "Walajah", "name_ta": "வாலாஜா", "lat": 12.9800, "lon": 79.3600},
            {"name_en": "Arcot", "name_ta": "ஆற்காடு", "lat": 12.9000, "lon": 79.3300},
            {"name_en": "Arakkonam", "name_ta": "அரக்கோணம்", "lat": 13.0800, "lon": 79.6700},
            {"name_en": "Nemili", "name_ta": "நெமிலி", "lat": 13.0200, "lon": 79.6000},
            {"name_en": "Kalavai", "name_ta": "கலவை", "lat": 12.7700, "lon": 79.2800},
        ]
    },
    {
        "name_en": "Salem", "name_ta": "சேலம்", "lat": 11.6643, "lon": 78.1460,
        "taluks": [
            {"name_en": "Salem", "name_ta": "சேலம்", "lat": 11.6643, "lon": 78.1460},
            {"name_en": "Attur", "name_ta": "ஆத்தூர்", "lat": 11.5900, "lon": 78.6000},
            {"name_en": "Mettur", "name_ta": "மேட்டூர்", "lat": 11.7900, "lon": 77.8000},
            {"name_en": "Omalur", "name_ta": "ஓமலூர்", "lat": 11.7400, "lon": 78.0400},
            {"name_en": "Sankari", "name_ta": "சங்ககிரி", "lat": 11.4800, "lon": 77.8700},
            {"name_en": "Valapady", "name_ta": "வாழப்பாடி", "lat": 11.6500, "lon": 78.4000},
            {"name_en": "Gangavalli", "name_ta": "கங்கவல்லி", "lat": 11.4800, "lon": 78.6500},
            {"name_en": "Edappadi", "name_ta": "எடப்பாடி", "lat": 11.5800, "lon": 77.8500},
            {"name_en": "Kadayampatti", "name_ta": "காடையாம்பட்டி", "lat": 11.8300, "lon": 78.1000},
            {"name_en": "Yercaud", "name_ta": "ஏற்காடு", "lat": 11.7800, "lon": 78.2100},
            {"name_en": "Pethanaickenpalayam", "name_ta": "பெத்தநாயக்கன்பாளையம்", "lat": 11.6300, "lon": 78.5200},
        ]
    },
    {
        "name_en": "Sivaganga", "name_ta": "சிவகங்கை", "lat": 9.8433, "lon": 78.4809,
        "taluks": [
            {"name_en": "Sivaganga", "name_ta": "சிவகங்கை", "lat": 9.8433, "lon": 78.4809},
            {"name_en": "Karaikudi", "name_ta": "காரைக்குடி", "lat": 10.0700, "lon": 78.7800},
            {"name_en": "Devakottai", "name_ta": "தேவகோட்டை", "lat": 9.9500, "lon": 78.8200},
            {"name_en": "Manamadurai", "name_ta": "மானாமதுரை", "lat": 9.7000, "lon": 78.4500},
            {"name_en": "Tirupathur", "name_ta": "திருப்பத்தூர்", "lat": 10.1100, "lon": 78.6200},
            {"name_en": "Ilayangudi", "name_ta": "இளையான்குடி", "lat": 9.6300, "lon": 78.6300},
            {"name_en": "Kalaiyarkoil", "name_ta": "காளையார்கோவில்", "lat": 9.8500, "lon": 78.6500},
            {"name_en": "Singampunari", "name_ta": "சிங்கம்புணரி", "lat": 10.1800, "lon": 78.4300},
            {"name_en": "Thirupuvanam", "name_ta": "திருப்புவனம்", "lat": 9.8600, "lon": 78.2700},
        ]
    },
    {
        "name_en": "Tenkasi", "name_ta": "தென்காசி", "lat": 8.9594, "lon": 77.3161,
        "taluks": [
            {"name_en": "Tenkasi", "name_ta": "தென்காசி", "lat": 8.9594, "lon": 77.3161},
            {"name_en": "Sankarankovil", "name_ta": "சங்கரன்கோவில்", "lat": 9.1700, "lon": 77.5300},
            {"name_en": "Shenkottai", "name_ta": "செங்கோட்டை", "lat": 8.9800, "lon": 77.2500},
            {"name_en": "Kadayanallur", "name_ta": "கடையநல்லூர்", "lat": 9.0700, "lon": 77.3500},
            {"name_en": "Sivagiri", "name_ta": "சிவகிரி", "lat": 9.3400, "lon": 77.4300},
            {"name_en": "Alangulam", "name_ta": "ஆலங்குளம்", "lat": 8.8700, "lon": 77.5000},
            {"name_en": "Thiruvengadam", "name_ta": "திருவேங்கடம்", "lat": 9.2700, "lon": 77.6700},
            {"name_en": "Veerakeralamputhur", "name_ta": "வீரகேரளம்புதூர்", "lat": 8.9400, "lon": 77.4300},
        ]
    },
    {
        "name_en": "Thanjavur", "name_ta": "தஞ்சாவூர்", "lat": 10.7870, "lon": 79.1378,
        "taluks": [
            {"name_en": "Thanjavur", "name_ta": "தஞ்சாவூர்", "lat": 10.7870, "lon": 79.1378},
            {"name_en": "Kumbakonam", "name_ta": "கும்பகோணம்", "lat": 10.9602, "lon": 79.3845},
            {"name_en": "Papanasam", "name_ta": "பாபநாசம்", "lat": 10.9300, "lon": 79.2800},
            {"name_en": "Pattukkottai", "name_ta": "பட்டுக்கோட்டை", "lat": 10.4300, "lon": 79.3200},
            {"name_en": "Peravurani", "name_ta": "பேராவூரணி", "lat": 10.2800, "lon": 79.1800},
            {"name_en": "Orathanadu", "name_ta": "ஒரத்தநாடு", "lat": 10.6300, "lon": 79.2500},
            {"name_en": "Thiruvaiyaru", "name_ta": "திருவையாறு", "lat": 10.8800, "lon": 79.1000},
            {"name_en": "Thiruvidaimarudur", "name_ta": "திருவிடைமருதூர்", "lat": 10.9900, "lon": 79.4600},
            {"name_en": "Budalur", "name_ta": "பூதலூர்", "lat": 10.8000, "lon": 78.9800},
        ]
    },
    {
        "name_en": "The Nilgiris", "name_ta": "நீலகிரி", "lat": 11.4916, "lon": 76.7337,
        "taluks": [
            {"name_en": "Udhagamandalam", "name_ta": "உதகமண்டலம்", "lat": 11.4102, "lon": 76.6950},
            {"name_en": "Coonoor", "name_ta": "குன்னூர்", "lat": 11.3500, "lon": 76.8000},
            {"name_en": "Kotagiri", "name_ta": "கோத்தகிரி", "lat": 11.4300, "lon": 76.8800},
            {"name_en": "Gudalur", "name_ta": "கூடலூர்", "lat": 11.5000, "lon": 76.5000},
            {"name_en": "Kundah", "name_ta": "குந்தா", "lat": 11.2800, "lon": 76.6500},
            {"name_en": "Pandalur", "name_ta": "பந்தலூர்", "lat": 11.4800, "lon": 76.3800},
        ]
    },
    {
        "name_en": "Theni", "name_ta": "தேனி", "lat": 10.0104, "lon": 77.4768,
        "taluks": [
            {"name_en": "Theni", "name_ta": "தேனி", "lat": 10.0104, "lon": 77.4768},
            {"name_en": "Periyakulam", "name_ta": "பெரியகுளம்", "lat": 10.1200, "lon": 77.5500},
            {"name_en": "Uthamapalayam", "name_ta": "உத்தமபாளையம்", "lat": 9.8100, "lon": 77.3300},
            {"name_en": "Bodinayakanur", "name_ta": "போடிநாயக்கனூர்", "lat": 10.0100, "lon": 77.3500},
            {"name_en": "Andipatti", "name_ta": "ஆண்டிபட்டி", "lat": 10.0000, "lon": 77.6200},
        ]
    },
    {
        "name_en": "Thoothukudi", "name_ta": "தூத்துக்குடி", "lat": 8.7642, "lon": 78.1348,
        "taluks": [
            {"name_en": "Thoothukudi", "name_ta": "தூத்துக்குடி", "lat": 8.7642, "lon": 78.1348},
            {"name_en": "Kovilpatti", "name_ta": "கோவில்பட்டி", "lat": 9.1700, "lon": 77.8700},
            {"name_en": "Tiruchendur", "name_ta": "திருச்செந்தூர்", "lat": 8.4900, "lon": 78.1200},
            {"name_en": "Srivaikuntam", "name_ta": "ஸ்ரீவைகுண்டம்", "lat": 8.6200, "lon": 77.9200},
            {"name_en": "Ottapidaram", "name_ta": "ஒட்டப்பிடாரம்", "lat": 8.9000, "lon": 78.0200},
            {"name_en": "Ettayapuram", "name_ta": "எட்டயபுரம்", "lat": 9.1500, "lon": 77.9900},
            {"name_en": "Vilathikulam", "name_ta": "விளாத்திகுளம்", "lat": 9.1300, "lon": 78.1700},
            {"name_en": "Sathankulam", "name_ta": "சாத்தான்குளம்", "lat": 8.4400, "lon": 77.9200},
            {"name_en": "Kayathar", "name_ta": "கயத்தாறு", "lat": 8.9500, "lon": 77.7800},
            {"name_en": "Eral", "name_ta": "ஏரல்", "lat": 8.6300, "lon": 78.0400},
        ]
    },
    {
        "name_en": "Tiruchirappalli", "name_ta": "திருச்சிராப்பள்ளி", "lat": 10.7905, "lon": 78.7047,
        "taluks": [
            {"name_en": "Tiruchirappalli East", "name_ta": "திருச்சிராப்பள்ளி கிழக்கு", "lat": 10.7905, "lon": 78.7047},
            {"name_en": "Tiruchirappalli West", "name_ta": "திருச்சிராப்பள்ளி மேற்கு", "lat": 10.8100, "lon": 78.6800},
            {"name_en": "Srirangam", "name_ta": "ஸ்ரீரங்கம்", "lat": 10.8600, "lon": 78.6900},
            {"name_en": "Lalgudi", "name_ta": "லால்குடி", "lat": 10.8700, "lon": 78.8200},
            {"name_en": "Manachanallur", "name_ta": "மண்ணச்சநல்லூர்", "lat": 10.9000, "lon": 78.7000},
            {"name_en": "Musiri", "name_ta": "முசிறி", "lat": 10.9400, "lon": 78.4500},
            {"name_en": "Thottiyam", "name_ta": "தொட்டியம்", "lat": 11.0000, "lon": 78.3300},
            {"name_en": "Thuraiyur", "name_ta": "துறையூர்", "lat": 11.1000, "lon": 78.6000},
            {"name_en": "Manapparai", "name_ta": "மணப்பாறை", "lat": 10.6000, "lon": 78.4200},
            {"name_en": "Marungapuri", "name_ta": "மருங்காபுரி", "lat": 10.4500, "lon": 78.3800},
            {"name_en": "Tiruverumbur", "name_ta": "திருவெறும்பூர்", "lat": 10.7800, "lon": 78.7800},
        ]
    },
    {
        "name_en": "Tirunelveli", "name_ta": "திருநெல்வேலி", "lat": 8.7139, "lon": 77.7567,
        "taluks": [
            {"name_en": "Tirunelveli", "name_ta": "திருநெல்வேலி", "lat": 8.7139, "lon": 77.7567},
            {"name_en": "Palayamkottai", "name_ta": "பாளையங்கோட்டை", "lat": 8.7100, "lon": 77.7300},
            {"name_en": "Ambasamudram", "name_ta": "அம்பாசமுத்திரம்", "lat": 8.7000, "lon": 77.4500},
            {"name_en": "Cheranmahadevi", "name_ta": "சேரன்மகாதேவி", "lat": 8.6800, "lon": 77.5600},
            {"name_en": "Nanguneri", "name_ta": "நாங்குநேரி", "lat": 8.4800, "lon": 77.6500},
            {"name_en": "Radhapuram", "name_ta": "ராதாபுரம்", "lat": 8.2700, "lon": 77.6800},
            {"name_en": "Tisayanvilai", "name_ta": "திசையன்விளை", "lat": 8.3300, "lon": 77.8700},
            {"name_en": "Manur", "name_ta": "மானூர்", "lat": 8.8500, "lon": 77.6700},
        ]
    },
    {
        "name_en": "Tirupathur", "name_ta": "திருப்பத்தூர்", "lat": 12.4958, "lon": 78.5678,
        "taluks": [
            {"name_en": "Tirupathur", "name_ta": "திருப்பத்தூர்", "lat": 12.4958, "lon": 78.5678},
            {"name_en": "Vaniyambadi", "name_ta": "வாணியம்பாடி", "lat": 12.6800, "lon": 78.6200},
            {"name_en": "Ambur", "name_ta": "ஆம்பூர்", "lat": 12.7900, "lon": 78.7100},
            {"name_en": "Natrampalli", "name_ta": "நாட்ராம்பள்ளி", "lat": 12.6200, "lon": 78.5300},
        ]
    },
    {
        "name_en": "Tiruppur", "name_ta": "திருப்பூர்", "lat": 11.1085, "lon": 77.3411,
        "taluks": [
            {"name_en": "Tiruppur North", "name_ta": "திருப்பூர் வடக்கு", "lat": 11.1200, "lon": 77.3400},
            {"name_en": "Tiruppur South", "name_ta": "திருப்பூர் தெற்கு", "lat": 11.0800, "lon": 77.3400},
            {"name_en": "Avinashi", "name_ta": "அவிநாசி", "lat": 11.1900, "lon": 77.2700},
            {"name_en": "Dharapuram", "name_ta": "தாராபுரம்", "lat": 10.7300, "lon": 77.5300},
            {"name_en": "Kangeyam", "name_ta": "காங்கேயம்", "lat": 11.0000, "lon": 77.5600},
            {"name_en": "Udumalaipettai", "name_ta": "உடுமலைப்பேட்டை", "lat": 10.5800, "lon": 77.2500},
            {"name_en": "Madathukulam", "name_ta": "மடத்துக்குளம்", "lat": 10.5500, "lon": 77.3800},
            {"name_en": "Uthukuli", "name_ta": "ஊத்துக்குளி", "lat": 11.1600, "lon": 77.4500},
        ]
    },
    {
        "name_en": "Tiruvallur", "name_ta": "திருவள்ளூர்", "lat": 13.1432, "lon": 79.9083,
        "taluks": [
            {"name_en": "Tiruvallur", "name_ta": "திருவள்ளூர்", "lat": 13.1432, "lon": 79.9083},
            {"name_en": "Ponneri", "name_ta": "பொன்னேரி", "lat": 13.3200, "lon": 80.1900},
            {"name_en": "Gummidipoondi", "name_ta": "கும்மிடிப்பூண்டி", "lat": 13.4100, "lon": 80.1300},
            {"name_en": "Uthukkottai", "name_ta": "ஊத்துக்கோட்டை", "lat": 13.3300, "lon": 79.9000},
            {"name_en": "Tiruttani", "name_ta": "திருத்தணி", "lat": 13.1800, "lon": 79.6300},
            {"name_en": "Pallipattu", "name_ta": "பள்ளிப்பட்டு", "lat": 13.3300, "lon": 79.4400},
            {"name_en": "Poonamallee", "name_ta": "பூந்தமல்லி", "lat": 13.0500, "lon": 80.1000},
            {"name_en": "Avadi", "name_ta": "ஆவடி", "lat": 13.1200, "lon": 80.1000},
            {"name_en": "R.K. Pet", "name_ta": "ஆர்.கே. பேட்டை", "lat": 13.2500, "lon": 79.5200},
        ]
    },
    {
        "name_en": "Tiruvannamalai", "name_ta": "திருவண்ணாமலை", "lat": 12.2253, "lon": 79.0747,
        "taluks": [
            {"name_en": "Tiruvannamalai", "name_ta": "திருவண்ணாமலை", "lat": 12.2253, "lon": 79.0747},
            {"name_en": "Arni", "name_ta": "ஆரணி", "lat": 12.6700, "lon": 79.2800},
            {"name_en": "Cheyyar", "name_ta": "செய்யாறு", "lat": 12.6600, "lon": 79.5400},
            {"name_en": "Polur", "name_ta": "போளூர்", "lat": 12.5000, "lon": 79.1300},
            {"name_en": "Chengam", "name_ta": "செங்கம்", "lat": 12.3000, "lon": 78.8000},
            {"name_en": "Vandavasi", "name_ta": "வந்தவாசி", "lat": 12.5000, "lon": 79.6100},
            {"name_en": "Kalasapakkam", "name_ta": "கலசப்பாக்கம்", "lat": 12.4000, "lon": 79.1000},
            {"name_en": "Kilpennathur", "name_ta": "கீழ்பென்னாத்தூர்", "lat": 12.2500, "lon": 79.2200},
            {"name_en": "Chetpet", "name_ta": "சேத்துப்பட்டு", "lat": 12.4700, "lon": 79.3500},
            {"name_en": "Jamunamarathur", "name_ta": "ஜமுனாமரத்தூர்", "lat": 12.5800, "lon": 78.9000},
            {"name_en": "Vembakkam", "name_ta": "வெம்பாக்கம்", "lat": 12.7800, "lon": 79.6300},
            {"name_en": "Thandarampattu", "name_ta": "தண்டராம்பட்டு", "lat": 12.0800, "lon": 78.9500},
        ]
    },
    {
        "name_en": "Tiruvarur", "name_ta": "திருவாரூர்", "lat": 10.7725, "lon": 79.6365,
        "taluks": [
            {"name_en": "Tiruvarur", "name_ta": "திருவாரூர்", "lat": 10.7725, "lon": 79.6365},
            {"name_en": "Mannargudi", "name_ta": "மன்னார்குடி", "lat": 10.6600, "lon": 79.4500},
            {"name_en": "Nannilam", "name_ta": "நன்னிலம்", "lat": 10.8800, "lon": 79.6200},
            {"name_en": "Thiruthuraipoondi", "name_ta": "திருத்துறைப்பூண்டி", "lat": 10.5300, "lon": 79.6500},
            {"name_en": "Valangaiman", "name_ta": "வலங்கைமான்", "lat": 10.8900, "lon": 79.3800},
            {"name_en": "Kodavasal", "name_ta": "குடவாசல்", "lat": 10.8600, "lon": 79.4800},
            {"name_en": "Needamangalam", "name_ta": "நீடாமங்கலம்", "lat": 10.7700, "lon": 79.4200},
            {"name_en": "Koothanallur", "name_ta": "கூத்தாநல்லூர்", "lat": 10.7200, "lon": 79.5200},
        ]
    },
    {
        "name_en": "Vellore", "name_ta": "வேலூர்", "lat": 12.9165, "lon": 79.1325,
        "taluks": [
            {"name_en": "Vellore", "name_ta": "வேலூர்", "lat": 12.9165, "lon": 79.1325},
            {"name_en": "Gudiyatham", "name_ta": "குடியாத்தம்", "lat": 12.9500, "lon": 78.8700},
            {"name_en": "Katpadi", "name_ta": "காட்பாடி", "lat": 12.9800, "lon": 79.1400},
            {"name_en": "Anaicut", "name_ta": "அணைக்கட்டு", "lat": 12.8700, "lon": 78.9800},
            {"name_en": "Pernambut", "name_ta": "பேரணாம்பட்டு", "lat": 12.9300, "lon": 78.7100},
            {"name_en": "K.V. Kuppam", "name_ta": "கே.வி. குப்பம்", "lat": 12.9900, "lon": 79.0300},
        ]
    },
    {
        "name_en": "Viluppuram", "name_ta": "விழுப்புரம்", "lat": 11.9401, "lon": 79.4861,
        "taluks": [
            {"name_en": "Viluppuram", "name_ta": "விழுப்புரம்", "lat": 11.9401, "lon": 79.4861},
            {"name_en": "Tindivanam", "name_ta": "திண்டிவனம்", "lat": 12.2300, "lon": 79.6500},
            {"name_en": "Gingee", "name_ta": "செஞ்சி", "lat": 12.2500, "lon": 79.4200},
            {"name_en": "Vanur", "name_ta": "வானூர்", "lat": 12.0200, "lon": 79.7300},
            {"name_en": "Vikkravandi", "name_ta": "விக்கிரவாண்டி", "lat": 12.0400, "lon": 79.5400},
            {"name_en": "Marakkanam", "name_ta": "மரக்காணம்", "lat": 12.2000, "lon": 79.9500},
            {"name_en": "Kandachipuram", "name_ta": "கண்டாச்சிபுரம்", "lat": 11.9800, "lon": 79.3100},
            {"name_en": "Thiruvennainallur", "name_ta": "திருவெண்ணெய்நல்லூர்", "lat": 11.8700, "lon": 79.4200},
            {"name_en": "Melmalayanur", "name_ta": "மேல்மலையனூர்", "lat": 12.3800, "lon": 79.3800},
        ]
    },
    {
        "name_en": "Virudhunagar", "name_ta": "விருதுநகர்", "lat": 9.5872, "lon": 77.9514,
        "taluks": [
            {"name_en": "Virudhunagar", "name_ta": "விருதுநகர்", "lat": 9.5872, "lon": 77.9514},
            {"name_en": "Sivakasi", "name_ta": "சிவகாசி", "lat": 9.4500, "lon": 77.8000},
            {"name_en": "Srivilliputhur", "name_ta": "ஸ்ரீவில்லிபுத்தூர்", "lat": 9.5100, "lon": 77.6300},
            {"name_en": "Rajapalayam", "name_ta": "ராஜபாளையம்", "lat": 9.4500, "lon": 77.5500},
            {"name_en": "Aruppukkottai", "name_ta": "அருப்புக்கோட்டை", "lat": 9.5100, "lon": 78.1000},
            {"name_en": "Sattur", "name_ta": "சாத்தூர்", "lat": 9.3600, "lon": 77.9300},
            {"name_en": "Kariapatti", "name_ta": "காரியாபட்டி", "lat": 9.6700, "lon": 78.1000},
            {"name_en": "Tiruchuli", "name_ta": "திருச்சுழி", "lat": 9.5300, "lon": 78.2000},
            {"name_en": "Watrap", "name_ta": "வத்திராயிருப்பு", "lat": 9.6300, "lon": 77.6300},
            {"name_en": "Vembakottai", "name_ta": "வெம்பக்கோட்டை", "lat": 9.3300, "lon": 77.7800},
        ]
    }
]

TN_PATTAMS_DATA = [
    {
        "name_en": "Chithirai Pattam (Summer)", "name_ta": "சித்திரை பட்டம் (கோடை)",
        "months_en": "April - May", "months_ta": "ஏப்ரல் - மே",
        "description_en": "Summer season suitable for short-duration pulses, sesame, watermelons, and irrigated vegetables.",
        "description_ta": "குறுகிய கால பயிர்கள், எள், தர்பூசணி, காய்கறிகள் பயிரிட ஏற்ற கோடைக்கால பட்டம்.",
        "recommended_crops_en": "Sesame, Green Gram, Black Gram, Watermelon, Muskmelon, Cucumber, Groundnut",
        "recommended_crops_ta": "எள், பாசிப்பயறு, உளுந்து, தர்பூசணி, முலாம்பழம், வெள்ளரி, நிலக்கடலை"
    },
    {
        "name_en": "Aadi Pattam (Monsoon Sowing)", "name_ta": "ஆடி பட்டம் (முன் பருவமழை)",
        "months_en": "July - August", "months_ta": "ஜூலை - ஆகஸ்ட்",
        "description_en": "The most vital agricultural sowing season in Tamil Nadu ('Aadi Pattam Thedi Vidhai'). Highest productivity for rainfed and irrigated crops.",
        "description_ta": "'ஆடி பட்டம் தேடி விதை' என்ற பழமொழிக்கேற்ப தமிழகத்தின் முதன்மை வேளாண் பருவம். அதிக விளைச்சல் தரும் பருவம்.",
        "recommended_crops_en": "Paddy, Maize, Sorghum, Pearl Millet, Finger Millet, Cotton, Groundnut, Red Gram, Tomato, Chilli, Brinjal, Okra, Turmeric",
        "recommended_crops_ta": "நெல், மக்காச்சோளம், சோளம், கம்பு, கேழ்வரகு, பருத்தி, நிலக்கடலை, துவரை, தக்காளி, மிளகாய், கத்தரி, வெண்டை, மஞ்சள்"
    },
    {
        "name_en": "Purattasi Pattam (Autumn)", "name_ta": "புரட்டாசி பட்டம் (பின் பருவமழை)",
        "months_en": "September - October", "months_ta": "செப்டம்பர் - அக்டோபர்",
        "description_en": "Northeast monsoon sowing season ideal for rainfed millets, pulses, and cotton across southern and central districts.",
        "description_ta": "வடகிழக்கு பருவமழையை நம்பி மானாவாரி சிறுதானியங்கள், பருப்பு வகைகள், பருத்தி பயிரிட உகந்த பருவம்.",
        "recommended_crops_en": "Cotton, Sorghum, Pearl Millet, Bengal Gram, Coriander, Sunflower, Chillies",
        "recommended_crops_ta": "பருத்தி, சோளம், கம்பு, கொண்டைக்கடலை, கொத்தமல்லி, சூரியகாந்தி, மிளகாய்"
    },
    {
        "name_en": "Thai Pattam (Winter / Post-Monsoon)", "name_ta": "தை பட்டம் (குளிர்காலம் / பின் பருவம்)",
        "months_en": "January - February", "months_ta": "ஜனவரி - பிப்ரவரி",
        "description_en": "Post-harvest winter season suitable for groundnut, pulses, sugarcane, vegetables, and sunflower.",
        "description_ta": "அறுவடைக்கு பின் நிலக்கடலை, பருப்பு வகைகள், கரும்பு, காய்கறிகள், சூரியகாந்தி பயிரிட சிறந்த பருவம்.",
        "recommended_crops_en": "Groundnut, Black Gram, Green Gram, Sugarcane, Sunflower, Sesame, Onion, Tomato, Bhendi",
        "recommended_crops_ta": "நிலக்கடலை, உளுந்து, பாசிப்பயறு, கரும்பு, சூரியகாந்தி, எள், வெங்காயம், தக்காளி, வெண்டை"
    },
    {
        "name_en": "Samba / Thaladi (Main Rice Season)", "name_ta": "சம்பா / தாளடி (முதன்மை நெல் பருவம்)",
        "months_en": "August - January", "months_ta": "ஆகஸ்ட் - ஜனவரி",
        "description_en": "The predominant single-crop and double-crop paddy season in the Cauvery Delta and coastal Tamil Nadu.",
        "description_ta": "காவிரி டெல்டா மற்றும் கடலோர மாவட்டங்களின் முதன்மை நெல் சாகுபடி பருவம்.",
        "recommended_crops_en": "Paddy (Medium & Long Duration: CR 1009, BPT 5204, ADT 46, TPS 5)",
        "recommended_crops_ta": "நெல் (மத்திய மற்றும் நீண்ட கால ரகங்கள்: சிஆர் 1009, பிபிடி 5204, ஏடிடி 46)"
    },
    {
        "name_en": "Navarai / Sornavari (Summer Rice & Pulses)", "name_ta": "நவரை / சொர்ணவாரி (கோடை நெல் & பயறு)",
        "months_en": "December - May", "months_ta": "டிசம்பர் - மே",
        "description_en": "Irrigated short-duration rice and pulse cultivation season in northern and central Tamil Nadu.",
        "description_ta": "வட மற்றும் மத்திய மாவட்டங்களில் குறுகிய கால நெல் மற்றும் பயறு சாகுபடி பருவம்.",
        "recommended_crops_en": "Paddy (Short Duration: ADT 37, ADT 43, ASD 16), Black Gram, Green Gram, Gingelly",
        "recommended_crops_ta": "நெல் (குறுகிய கால ரகங்கள்: ஏடிடி 37, ஏடிடி 43, ஏஎஸ்டி 16), உளுந்து, பாசிப்பயறு, எள்"
    },
    {
        "name_en": "Kar (Early Monsoon)", "name_ta": "கார் பருவம் (முன் பருவமழை)",
        "months_en": "May - June to September", "months_ta": "மே - ஜூன் முதல் செப்டம்பர்",
        "description_en": "Short-duration paddy season in Kanyakumari, Tirunelveli, and Tenkasi utilizing southwest monsoon showers.",
        "description_ta": "தென் மாவட்டங்களில் தென்மேற்கு பருவமழையை பயன்படுத்தி குறுகிய கால நெல் சாகுபடி பருவம்.",
        "recommended_crops_en": "Paddy (Short duration: ADT 36, ASD 16, TPS 3)",
        "recommended_crops_ta": "நெல் (குறுகிய கால ரகங்கள்: ஏடிடி 36, ஏஎஸ்டி 16, டிபிஎஸ் 3)"
    }
]

TN_CROPS_DATA = [
    # --- Cereals & Millets ---
    {
        "name_en": "Paddy", "name_ta": "நெல்", "category": "Cereals", "duration_days": 125,
        "ideal_soil": "Clay, Clay Loam, Alluvial", "ideal_soil_ta": "களிமண், வண்டல் மண், களிமண் கலந்த வண்டல்",
        "min_temp": 20.0, "max_temp": 38.0, "min_rainfall": 900.0, "max_rainfall": 1500.0,
        "water_req_level": "High", "water_req_level_ta": "அதிகம்",
        "n_req": 120.0, "p_req": 50.0, "k_req": 50.0, "ideal_ph_min": 5.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 2200.0, "typical_yield_max_acre": 3400.0,
        "harvest_indicators_en": "80% of grains in panicle turn golden yellow; moisture content drops to 20-22%.",
        "harvest_indicators_ta": "கதிர்களில் 80% மணிகள் பொன்னிறமாக மாறும்; தானிய ஈர்ப்பதம் 20-22% குறையும்.",
        "major_pests_en": "Stem borer, Brown planthopper (BPH), Leaf folder, Gall midge",
        "major_pests_ta": "தண்டு துளைப்பான், புகையான், இலை சுருட்டுப் புழு, ஆனைக் கொம்பன்",
        "major_diseases_en": "Blast, Bacterial leaf blight (BLB), Sheath blight, Tungro",
        "major_diseases_ta": "குலை நோய், பாக்டீரியா இலைக்கருகல், உறை அழுகல், துங்ரோ வைரஸ்"
    },
    {
        "name_en": "Maize", "name_ta": "மக்காச்சோளம்", "category": "Cereals", "duration_days": 105,
        "ideal_soil": "Sandy Loam, Red Loam, Deep Black Soil", "ideal_soil_ta": "மணல் கலந்த செம்மண், செம்மண், கரிசல் மண்",
        "min_temp": 18.0, "max_temp": 35.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 150.0, "p_req": 65.0, "k_req": 60.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 2400.0, "typical_yield_max_acre": 3800.0,
        "harvest_indicators_en": "Sheath turns brownish, silks dry up completely, black layer forms at base of grain kernel.",
        "harvest_indicators_ta": "மட்டைகள் காய்ந்து பழுப்பு நிறமாகும், தூவி காய்ந்துவிடும், தானியத்தின் அடிப்பகுதியில் கருப்பு வளையம் தோன்றும்.",
        "major_pests_en": "Fall armyworm (Spodoptera frugiperda), Stem borer",
        "major_pests_ta": "படைப்புழு (Fall Armyworm), தண்டு துளைப்பான்",
        "major_diseases_en": "Turcicum leaf blight, Banded leaf and sheath blight, Charcoal rot",
        "major_diseases_ta": "இலைக்கருகல் நோய், உறை கருகல், கரிக்காய் நோய்"
    },
    {
        "name_en": "Sorghum", "name_ta": "சோளம்", "category": "Millets", "duration_days": 100,
        "ideal_soil": "Clay Loam, Deep Black Soil, Red Loam", "ideal_soil_ta": "களிமண் கலந்த வண்டல், கரிசல் மண், செம்மண்",
        "min_temp": 24.0, "max_temp": 38.0, "min_rainfall": 400.0, "max_rainfall": 650.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 90.0, "p_req": 45.0, "k_req": 45.0, "ideal_ph_min": 6.0, "ideal_ph_max": 8.5,
        "typical_yield_min_acre": 1200.0, "typical_yield_max_acre": 2000.0,
        "harvest_indicators_en": "Ear heads turn light yellow or brown; grains become firm and crack when pressed with thumbnail.",
        "harvest_indicators_ta": "கதிர்கள் வெளிர் மஞ்சள் அல்லது பழுப்பு நிறமாக மாறும்; தானியங்கள் கடினமாக இருக்கும்.",
        "major_pests_en": "Shoot fly, Stem borer, Ear head bug",
        "major_pests_ta": "குருத்து ஈ, தண்டு துளைப்பான், கதிர் நாவாய்ப்பூச்சி",
        "major_diseases_en": "Grain mold, Downy mildew, Rust",
        "major_diseases_ta": "தானிய பூஞ்சான காளான், அடிச்சாம்பல் நோய், துரு நோய்"
    },
    {
        "name_en": "Pearl Millet", "name_ta": "கம்பு", "category": "Millets", "duration_days": 85,
        "ideal_soil": "Sandy Loam, Red Sandy Soil, Light Black Soil", "ideal_soil_ta": "மணல் கலந்த செம்மண், செம்மண், வெளிர் கரிசல் மண்",
        "min_temp": 25.0, "max_temp": 40.0, "min_rainfall": 350.0, "max_rainfall": 550.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 80.0, "p_req": 40.0, "k_req": 40.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 1000.0, "typical_yield_max_acre": 1600.0,
        "harvest_indicators_en": "Ear heads turn golden brown and stalks dry up.",
        "harvest_indicators_ta": "கதிர்கள் பொன்னிற பழுப்பு நிறமாக மாறி தாள்கள் காயும் போது.",
        "major_pests_en": "Shoot fly, Grasshoppers, Ear head midge",
        "major_pests_ta": "குருத்து ஈ, வெட்டுக்கிளி, கதிர் ஈ",
        "major_diseases_en": "Downy mildew (Green ear), Ergot, Smut",
        "major_diseases_ta": "அடிச்சாம்பல் நோய் (பச்சைக் கதிர்), தேன் ஒழுகல் நோய், கரிப்பூட்டை நோய்"
    },
    {
        "name_en": "Finger Millet", "name_ta": "கேழ்வரகு (ராகி)", "category": "Millets", "duration_days": 110,
        "ideal_soil": "Red Loam, Sandy Loam, Clay Loam", "ideal_soil_ta": "செம்மண், மணல் கலந்த செம்மண், வண்டல் மண்",
        "min_temp": 20.0, "max_temp": 34.0, "min_rainfall": 500.0, "max_rainfall": 900.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 60.0, "p_req": 30.0, "k_req": 30.0, "ideal_ph_min": 5.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 1200.0, "typical_yield_max_acre": 1900.0,
        "harvest_indicators_en": "Fingers turn characteristic golden brown color; seeds are firm.",
        "harvest_indicators_ta": "கதிர் விரல்கள் பொன்னிற பழுப்பு நிறமாக மாறி விதைகள் கடினமாகும்.",
        "major_pests_en": "Armyworm, Aphids, Stem borer",
        "major_pests_ta": "படைப்புழு, அசுவினி, தண்டு துளைப்பான்",
        "major_diseases_en": "Ragi blast, Foot rot, Mosaic virus",
        "major_diseases_ta": "ராகி குலை நோய், வேரழுகல், தேமல் நோய்"
    },
    {
        "name_en": "Barnyard Millet", "name_ta": "குதிரைவாலி", "category": "Millets", "duration_days": 80,
        "ideal_soil": "Red Sandy Loam, Gravelly Soil, Alluvial", "ideal_soil_ta": "செம்மண், சரளை மண், வண்டல் மண்",
        "min_temp": 18.0, "max_temp": 36.0, "min_rainfall": 300.0, "max_rainfall": 500.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 40.0, "p_req": 20.0, "k_req": 0.0, "ideal_ph_min": 5.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 700.0, "typical_yield_max_acre": 1100.0,
        "harvest_indicators_en": "Spikes turn straw yellow; seeds harden.",
        "harvest_indicators_ta": "கதிர்கள் வைக்கோல் மஞ்சள் நிறமாக மாறும்; விதைகள் கடினமாகும்.",
        "major_pests_en": "Shoot fly, Stem borer", "major_pests_ta": "குருத்து ஈ, தண்டு துளைப்பான்",
        "major_diseases_en": "Smut, Rust", "major_diseases_ta": "கரிப்பூட்டை நோய், துரு நோய்"
    },
    {
        "name_en": "Kodo Millet", "name_ta": "வரகு", "category": "Millets", "duration_days": 115,
        "ideal_soil": "Gravelly Red Soil, Sandy Loam", "ideal_soil_ta": "சரளை கலந்த செம்மண், மணல் கலந்த மண்",
        "min_temp": 22.0, "max_temp": 36.0, "min_rainfall": 400.0, "max_rainfall": 600.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 40.0, "p_req": 20.0, "k_req": 0.0, "ideal_ph_min": 5.5, "ideal_ph_max": 7.8,
        "typical_yield_min_acre": 650.0, "typical_yield_max_acre": 1050.0,
        "harvest_indicators_en": "Plants turn golden yellowish brown and seeds become dark brown.",
        "harvest_indicators_ta": "செடிகள் மஞ்சள் பழுப்பு நிறமாகி தானியங்கள் அடர் பழுப்பு நிறமாகும்.",
        "major_pests_en": "Shoot fly, Grasshoppers", "major_pests_ta": "குருத்து ஈ, வெட்டுக்கிளி",
        "major_diseases_en": "Head smut, Rust", "major_diseases_ta": "கதிர் கரிப்பூட்டை, துரு நோய்"
    },
    {
        "name_en": "Little Millet", "name_ta": "சாமை", "category": "Millets", "duration_days": 80,
        "ideal_soil": "Poor rocky soils, Sandy Loam, Red Loam", "ideal_soil_ta": "வளம் குறைந்த மண், மணல் கலந்த செம்மண்",
        "min_temp": 20.0, "max_temp": 35.0, "min_rainfall": 350.0, "max_rainfall": 550.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 40.0, "p_req": 20.0, "k_req": 0.0, "ideal_ph_min": 5.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 600.0, "typical_yield_max_acre": 950.0,
        "harvest_indicators_en": "Panicles dry up and turn pale yellow.",
        "harvest_indicators_ta": "கதிர்கள் காய்ந்து வெளிர் மஞ்சள் நிறமாகும் போது.",
        "major_pests_en": "Shoot fly", "major_pests_ta": "குருத்து ஈ",
        "major_diseases_en": "Grain smut", "major_diseases_ta": "தானிய கரிப்பூட்டை"
    },
    {
        "name_en": "Foxtail Millet", "name_ta": "தினை", "category": "Millets", "duration_days": 85,
        "ideal_soil": "Well drained Sandy Loam, Red Loam", "ideal_soil_ta": "நல்ல வடிகால் வசதியுள்ள மணல் கலந்த செம்மண்",
        "min_temp": 22.0, "max_temp": 36.0, "min_rainfall": 350.0, "max_rainfall": 500.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 40.0, "p_req": 20.0, "k_req": 0.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 700.0, "typical_yield_max_acre": 1100.0,
        "harvest_indicators_en": "Bristled panicle turns bright golden yellow.",
        "harvest_indicators_ta": "முட்கள் கொண்ட கதிர் பொன்னிறமாக மாறும்.",
        "major_pests_en": "Shoot fly, Stem borer", "major_pests_ta": "குருத்து ஈ, தண்டு துளைப்பான்",
        "major_diseases_en": "Blast, Rust", "major_diseases_ta": "குலை நோய், துரு நோய்"
    },

    # --- Pulses ---
    {
        "name_en": "Black Gram", "name_ta": "உளுந்து", "category": "Pulses", "duration_days": 70,
        "ideal_soil": "Loamy Soil, Clay Loam, Black Cotton Soil", "ideal_soil_ta": "வண்டல் மண், களிமண் கலந்த வண்டல், கரிசல் மண்",
        "min_temp": 25.0, "max_temp": 36.0, "min_rainfall": 400.0, "max_rainfall": 700.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 25.0, "p_req": 50.0, "k_req": 25.0, "ideal_ph_min": 6.5, "ideal_ph_max": 7.8,
        "typical_yield_min_acre": 350.0, "typical_yield_max_acre": 650.0,
        "harvest_indicators_en": "80% of pods turn blackish and become dry and crisp.",
        "harvest_indicators_ta": "80% காய்கள் கறுத்து காய்ந்து மொறுமொறுப்பாக மாறும் போது.",
        "major_pests_en": "Pod borer, Whitefly, Thrips, Aphids",
        "major_pests_ta": "காய் துளைப்பான், வெள்ளை ஈ, இலைப்பேன், அசுவினி",
        "major_diseases_en": "Yellow mosaic virus (YMV), Root rot, Powdery mildew",
        "major_diseases_ta": "மஞ்சள் தேமல் நோய் (YMV), வேரழுகல் நோய், சாம்பல் நோய்"
    },
    {
        "name_en": "Green Gram", "name_ta": "பாசிப்பயறு", "category": "Pulses", "duration_days": 65,
        "ideal_soil": "Well drained Sandy Loam, Red Loam, Alluvial", "ideal_soil_ta": "மணல் கலந்த செம்மண், செம்மண், வண்டல் மண்",
        "min_temp": 24.0, "max_temp": 35.0, "min_rainfall": 400.0, "max_rainfall": 650.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 25.0, "p_req": 50.0, "k_req": 25.0, "ideal_ph_min": 6.2, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 350.0, "typical_yield_max_acre": 600.0,
        "harvest_indicators_en": "Pods turn dark brown/black; leaves start shedding.",
        "harvest_indicators_ta": "காய்கள் அடர் பழுப்பு/கருப்பு நிறமாகும்; இலைகள் உதிரத் தொடங்கும்.",
        "major_pests_en": "Spotted pod borer, Whitefly, Blue butterfly caterpillar",
        "major_pests_ta": "புள்ளி காய் துளைப்பான், வெள்ளை ஈ, கம்பளிப் புழு",
        "major_diseases_en": "Yellow Mosaic Virus, Powdery Mildew, Cercospora leaf spot",
        "major_diseases_ta": "மஞ்சள் தேமல் வைரஸ், சாம்பல் நோய், செர்கோஸ்போரா இலைப்புள்ளி"
    },
    {
        "name_en": "Red Gram", "name_ta": "துவரை", "category": "Pulses", "duration_days": 160,
        "ideal_soil": "Deep Red Loam, Clay Loam, Black Cotton Soil", "ideal_soil_ta": "ஆழமான செம்மண், களிமண், கரிசல் மண்",
        "min_temp": 20.0, "max_temp": 35.0, "min_rainfall": 550.0, "max_rainfall": 900.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 25.0, "p_req": 50.0, "k_req": 25.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 500.0, "typical_yield_max_acre": 900.0,
        "harvest_indicators_en": "Pods turn brown and rattle when shaken.",
        "harvest_indicators_ta": "காய்கள் பழுப்பு நிறமாக மாறி அசைக்கும் போது சத்தம் வரும்.",
        "major_pests_en": "Gram pod borer (Helicoverpa armigera), Pod fly, Blister beetle",
        "major_pests_ta": "காய் துளைப்பான் (ஹெலிகோவெர்பா), காய் ஈ, வண்டு",
        "major_diseases_en": "Fusarium wilt, Sterility mosaic disease (SMD), Root rot",
        "major_diseases_ta": "வாடல் நோய், மலட்டுத் தேமல் நோய், வேரழுகல்"
    },
    {
        "name_en": "Bengal Gram", "name_ta": "கொண்டைக்கடலை", "category": "Pulses", "duration_days": 95,
        "ideal_soil": "Deep Black Cotton Soil, Clay Loam", "ideal_soil_ta": "ஆழமான கரிசல் மண், களிமண் கலந்த வண்டல்",
        "min_temp": 15.0, "max_temp": 28.0, "min_rainfall": 350.0, "max_rainfall": 500.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 20.0, "p_req": 40.0, "k_req": 20.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.5,
        "typical_yield_min_acre": 450.0, "typical_yield_max_acre": 800.0,
        "harvest_indicators_en": "Leaves turn yellowish brown and dry completely; pods become crisp.",
        "harvest_indicators_ta": "இலைகள் மஞ்சள் பழுப்பு நிறமாகி காயும்; காய்கள் மொறுமொறுப்பாகும்.",
        "major_pests_en": "Pod borer (Helicoverpa armigera), Cutworms",
        "major_pests_ta": "காய் துளைப்பான், வெட்டுப்புழு",
        "major_diseases_en": "Wilt, Ascochyta blight, Collar rot",
        "major_diseases_ta": "வாடல் நோய், அஸ்கோகைட்டா கருகல், தண்டு அழுகல்"
    },
    {
        "name_en": "Cowpea", "name_ta": "தட்டப்பயறு (காராமணி)", "category": "Pulses", "duration_days": 75,
        "ideal_soil": "Sandy Loam, Red Loam", "ideal_soil_ta": "மணல் கலந்த செம்மண், செம்மண்",
        "min_temp": 22.0, "max_temp": 35.0, "min_rainfall": 450.0, "max_rainfall": 700.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 25.0, "p_req": 50.0, "k_req": 25.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 400.0, "typical_yield_max_acre": 700.0,
        "harvest_indicators_en": "Pods become dry and turn light brown/straw color.",
        "harvest_indicators_ta": "காய்கள் காய்ந்து வெளிர் பழுப்பு நிறமாக மாறும்.",
        "major_pests_en": "Aphids, Pod borers, Leaf hoppers",
        "major_pests_ta": "அசுவினி, காய் துளைப்பான், இலைத்தத்துப்பூச்சி",
        "major_diseases_en": "Anthracnose, Powdery mildew, Cowpea mosaic",
        "major_diseases_ta": "ஆந்த்ராக்னோஸ், சாம்பல் நோய், காராமணி தேமல்"
    },
    {
        "name_en": "Horse Gram", "name_ta": "கொள்ளு", "category": "Pulses", "duration_days": 100,
        "ideal_soil": "Poor shallow Red soils, Gravelly soils", "ideal_soil_ta": "வளம் குறைந்த செம்மண், சரளை மண்",
        "min_temp": 20.0, "max_temp": 34.0, "min_rainfall": 300.0, "max_rainfall": 500.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 20.0, "p_req": 40.0, "k_req": 0.0, "ideal_ph_min": 5.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 300.0, "typical_yield_max_acre": 550.0,
        "harvest_indicators_en": "Foliage withers and pods turn light golden brown.",
        "harvest_indicators_ta": "இலைகள் உதிர்ந்து காய்கள் பொன்னிற பழுப்பு நிறமாகும்.",
        "major_pests_en": "Pod borer, Aphids", "major_pests_ta": "காய் துளைப்பான், அசுவினி",
        "major_diseases_en": "Dry root rot, Rust", "major_diseases_ta": "வேரழுகல், துரு நோய்"
    },

    # --- Oilseeds & Commercial ---
    {
        "name_en": "Groundnut", "name_ta": "நிலக்கடலை", "category": "Oilseeds", "duration_days": 110,
        "ideal_soil": "Sandy Loam, Red Sandy Loam, Well drained Light Soils", "ideal_soil_ta": "மணல் கலந்த செம்மண், இலகுவான மணல் மண்",
        "min_temp": 22.0, "max_temp": 34.0, "min_rainfall": 500.0, "max_rainfall": 750.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 25.0, "p_req": 50.0, "k_req": 75.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 900.0, "typical_yield_max_acre": 1600.0,
        "harvest_indicators_en": "Leaves turn yellow and shed; inner shell develops dark netting/black color.",
        "harvest_indicators_ta": "இலைகள் மஞ்சளாகி உதிரும்; கடலை ஓட்டின் உட்புறம் கருமை கலந்த நரம்பமைப்பாக மாறும்.",
        "major_pests_en": "Red hairy caterpillar, Leaf miner, Spodoptera litura, White grub",
        "major_pests_ta": "சிவப்பு கம்பளிப்புழு, சுருள் பூச்சி, புகையிலை வெட்டுப்புழு, வேர்ப்புழு",
        "major_diseases_en": "Tikka leaf spot, Rust, Collar rot, Stem rot",
        "major_diseases_ta": "டிக்கா இலைப்புள்ளி நோய், துரு நோய், தண்டு அழுகல் நோய்"
    },
    {
        "name_en": "Gingelly (Sesame)", "name_ta": "எள்", "category": "Oilseeds", "duration_days": 80,
        "ideal_soil": "Sandy Loam, Alluvial, Red Loam", "ideal_soil_ta": "மணல் கலந்த செம்மண், வண்டல் மண், செம்மண்",
        "min_temp": 25.0, "max_temp": 38.0, "min_rainfall": 350.0, "max_rainfall": 550.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 35.0, "p_req": 23.0, "k_req": 23.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.8,
        "typical_yield_min_acre": 250.0, "typical_yield_max_acre": 450.0,
        "harvest_indicators_en": "Bottom leaves and capsules turn yellow; bottom capsules start splitting at the tip.",
        "harvest_indicators_ta": "அடி இலைகள் மற்றும் காய்கள் மஞ்சளாக மாறும்; அடிப்பகுதி காய்கள் நுனியில் வெடிக்கத் தொடங்கும்.",
        "major_pests_en": "Shoot webber and pod borer, Gall fly, Sphinx moth",
        "major_pests_ta": "இலை மற்றும் காய் பிணைக்கும் புழு, காய் ஈ, அந்துப்பூச்சி",
        "major_diseases_en": "Phyllody (Mycoplasma), Root rot, Alternaria leaf blight",
        "major_diseases_ta": "இலை கொத்து நோய் (Phyllody), வேரழுகல், இலைக்கருகல்"
    },
    {
        "name_en": "Sunflower", "name_ta": "சூரியகாந்தி", "category": "Oilseeds", "duration_days": 90,
        "ideal_soil": "Deep Black Soil, Neutral Loamy Soil", "ideal_soil_ta": "கரிசல் மண், வண்டல் மண்",
        "min_temp": 20.0, "max_temp": 35.0, "min_rainfall": 500.0, "max_rainfall": 700.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 60.0, "p_req": 90.0, "k_req": 60.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 600.0, "typical_yield_max_acre": 1000.0,
        "harvest_indicators_en": "Back side of head turns golden lemon-yellow and bracts turn brown.",
        "harvest_indicators_ta": "பூவின் பின்புறம் எலுமிச்சை மஞ்சள் நிறமாக மாறும் மற்றும் இதழ்கள் பழுப்பாகும்.",
        "major_pests_en": "Head borer (Helicoverpa), Whitefly, Leaf hopper",
        "major_pests_ta": "பூ துளைப்பான், வெள்ளை ஈ, தத்துப்பூச்சி",
        "major_diseases_en": "Alternaria blight, Rust, Downy mildew",
        "major_diseases_ta": "ஆல்டர்னேரியா கருகல், துரு நோய், அடிச்சாம்பல் நோய்"
    },
    {
        "name_en": "Castor", "name_ta": "ஆமணக்கு", "category": "Oilseeds", "duration_days": 150,
        "ideal_soil": "Well drained Sandy Loam, Red Loam", "ideal_soil_ta": "மணல் கலந்த செம்மண், செம்மண்",
        "min_temp": 20.0, "max_temp": 38.0, "min_rainfall": 400.0, "max_rainfall": 600.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 45.0, "p_req": 30.0, "k_req": 30.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 500.0, "typical_yield_max_acre": 900.0,
        "harvest_indicators_en": "Capsules in spike turn yellowish-brown and dry up.",
        "harvest_indicators_ta": "கதிர் காய்கள் மஞ்சள்-பழுப்பு நிறமாகி காயும் போது.",
        "major_pests_en": "Semilooper, Capsule borer, Whitefly",
        "major_pests_ta": "கம்பளிப்புழு (Semilooper), காய் துளைப்பான், வெள்ளை ஈ",
        "major_diseases_en": "Fusarium wilt, Botrytis grey mold, Root rot",
        "major_diseases_ta": "வாடல் நோய், சாம்பல் நிற பூஞ்சை, வேரழுகல்"
    },
    {
        "name_en": "Cotton", "name_ta": "பருத்தி", "category": "Commercial", "duration_days": 160,
        "ideal_soil": "Deep Black Cotton Soil, Clay Loam, Alluvial", "ideal_soil_ta": "கரிசல் மண், களிமண், வண்டல் மண்",
        "min_temp": 22.0, "max_temp": 38.0, "min_rainfall": 600.0, "max_rainfall": 900.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 120.0, "p_req": 60.0, "k_req": 60.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.5,
        "typical_yield_min_acre": 800.0, "typical_yield_max_acre": 1400.0,
        "harvest_indicators_en": "Bolls burst open fully exposing fluffy white clean lint.",
        "harvest_indicators_ta": "பருத்தி காய்கள் முழுமையாக வெடித்து பஞ்சு வெளியே தெரியும் போது.",
        "major_pests_en": "Pink bollworm, American bollworm, Whitefly, Stem weevil",
        "major_pests_ta": "இளஞ்சிவப்பு காய்ப்புழு, அமெரிக்க காய்ப்புழு, வெள்ளை ஈ, தண்டு வண்டு",
        "major_diseases_en": "Bacterial blight (Black arm), Grey mildew, Root rot",
        "major_diseases_ta": "பாக்டீரியா கருகல் (கருப்பு கை), சாம்பல் பூஞ்சை, வேரழுகல்"
    },
    {
        "name_en": "Sugarcane", "name_ta": "கரும்பு", "category": "Commercial", "duration_days": 360,
        "ideal_soil": "Deep Loamy, Alluvial, Clay Loam with excellent drainage", "ideal_soil_ta": "ஆழமான வண்டல் மண், களிமண் கலந்த வண்டல்",
        "min_temp": 20.0, "max_temp": 38.0, "min_rainfall": 1200.0, "max_rainfall": 2000.0,
        "water_req_level": "High", "water_req_level_ta": "மிக அதிகம்",
        "n_req": 275.0, "p_req": 65.0, "k_req": 115.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 40000.0, "typical_yield_max_acre": 65000.0,
        "harvest_indicators_en": "Leaves turn yellow; canes produce metallic sound when tapped; hand refractometer Brix exceeds 18-20%.",
        "harvest_indicators_ta": "இலைகள் மஞ்சளாகும்; கரும்பை தட்டும்போது உலோகம் போன்ற ஒலி வரும்; பிரிக்ஸ் சர்க்கரை அளவு 18-20% தாண்டும்.",
        "major_pests_en": "Early shoot borer, Top borer, Internode borer, White grub, Woolly aphid",
        "major_pests_ta": "இளம் குருத்து துளைப்பான், நுனி துளைப்பான், இடைக்கணு துளைப்பான், வெள்ளை கம்பளி அசுவினி",
        "major_diseases_en": "Red rot, Smut, Grassy shoot, Sett rot",
        "major_diseases_ta": "செவ்வழுகல் நோய், கரிப்பூட்டை, புல் குருத்து நோய், கரணை அழுகல்"
    },
    {
        "name_en": "Banana", "name_ta": "வாழை", "category": "Fruits", "duration_days": 360,
        "ideal_soil": "Deep Fertile Loamy Soil, Clay Loam", "ideal_soil_ta": "ஆழமான வளமான வண்டல் மண், களிமண் வண்டல்",
        "min_temp": 15.0, "max_temp": 38.0, "min_rainfall": 1200.0, "max_rainfall": 2200.0,
        "water_req_level": "High", "water_req_level_ta": "அதிகம்",
        "n_req": 200.0, "p_req": 50.0, "k_req": 300.0, "ideal_ph_min": 6.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 18000.0, "typical_yield_max_acre": 30000.0,
        "harvest_indicators_en": "Angles of fruit disappear and become rounded; top floral remnants fall off easily.",
        "harvest_indicators_ta": "காயின் முக்கோண விளிம்புகள் மறைந்து உருண்டையாகும்; பூவின் நுனி காய்ந்து உதிரும்.",
        "major_pests_en": "Pseudostem weevil, Rhizome weevil, Banana aphid, Nematodes",
        "major_pests_ta": "தண்டு வண்டு, கிழங்கு வண்டு, அசுவினி, நூற்புழு",
        "major_diseases_en": "Panama wilt (Fusarium), Sigatoka leaf spot, Banana Bunchy Top Virus (BBTV)",
        "major_diseases_ta": "பனாமா வாடல் நோய், சிகடோகா இலைப்புள்ளி, முடிச்சு வைரஸ்"
    },
    {
        "name_en": "Coconut", "name_ta": "தென்னை", "category": "Commercial", "duration_days": 365,
        "ideal_soil": "Coastal Sand, Red Sandy Loam, Alluvial Soil", "ideal_soil_ta": "கடலோர மணல், செம்மண், வண்டல் மண்",
        "min_temp": 20.0, "max_temp": 36.0, "min_rainfall": 1000.0, "max_rainfall": 2500.0,
        "water_req_level": "High", "water_req_level_ta": "அதிகம்",
        "n_req": 560.0, "p_req": 320.0, "k_req": 1200.0, "ideal_ph_min": 5.2, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 6000.0, "typical_yield_max_acre": 12000.0,  # nuts/acre converted or kg
        "harvest_indicators_en": "Nuts turn brownish and sloshing sound of water is heard upon shaking (11-12 months old).",
        "harvest_indicators_ta": "தேங்காய் பழுப்பு நிறமாகும்; குலுக்கினால் தண்ணீர் சத்தம் கேட்கும் (11-12 மாத தேங்காய்).",
        "major_pests_en": "Rhinoceros beetle, Red palm weevil, Black headed caterpillar, Eriophyid mite",
        "major_pests_ta": "காண்டாமிருக வண்டு, சிவப்பு கூன் வண்டு, கருந்தலை புழு, மைட் பூச்சி",
        "major_diseases_en": "Bud rot, Basal stem rot (Thanjavur wilt), Leaf rot",
        "major_diseases_ta": "குருத்து அழுகல், தஞ்சாவூர் வாடல் நோய், இலை அழுகல்"
    },
    {
        "name_en": "Tapioca (Cassava)", "name_ta": "மரவள்ளிக்கிழங்கு", "category": "Commercial", "duration_days": 270,
        "ideal_soil": "Sandy Loam, Red Loam, Laterite Soil", "ideal_soil_ta": "மணல் கலந்த செம்மண், செம்மண், செம்பொறை மண்",
        "min_temp": 22.0, "max_temp": 38.0, "min_rainfall": 800.0, "max_rainfall": 1400.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 50.0, "p_req": 50.0, "k_req": 100.0, "ideal_ph_min": 5.5, "ideal_ph_max": 7.0,
        "typical_yield_min_acre": 12000.0, "typical_yield_max_acre": 18000.0,
        "harvest_indicators_en": "Leaves yellow and drop; soil cracks around root zone base.",
        "harvest_indicators_ta": "இலைகள் மஞ்சளாகி உதிரும்; செடியின் அடிப்பகுதியில் மண் வெடிக்கும்.",
        "major_pests_en": "Spiralling whitefly, Mealybug, Red spider mite",
        "major_pests_ta": "சுருள் வெள்ளை ஈ, மாவுப்பூச்சி, சிவப்பு சிலந்தி",
        "major_diseases_en": "Cassava Mosaic Virus (CMD), Brown leaf spot, Tuber rot",
        "major_diseases_ta": "மரவள்ளி தேமல் வைரஸ் (CMD), பழுப்பு இலைப்புள்ளி, கிழங்கு அழுகல்"
    },

    # --- Spices & Condiments ---
    {
        "name_en": "Turmeric", "name_ta": "மஞ்சள்", "category": "Spices", "duration_days": 270,
        "ideal_soil": "Well drained Sandy Loam, Clay Loam, Red Soil", "ideal_soil_ta": "மணல் கலந்த செம்மண், களிமண் வண்டல், செம்மண்",
        "min_temp": 20.0, "max_temp": 35.0, "min_rainfall": 1000.0, "max_rainfall": 1600.0,
        "water_req_level": "High", "water_req_level_ta": "அதிகம்",
        "n_req": 120.0, "p_req": 60.0, "k_req": 150.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 8000.0, "typical_yield_max_acre": 12000.0,
        "harvest_indicators_en": "Lower leaves turn yellow and pseudostem begins to dry completely.",
        "harvest_indicators_ta": "அடி இலைகள் மஞ்சளாகி தண்டு முழுமையாக காயத் தொடங்கும்.",
        "major_pests_en": "Shoot borer, Rhizome scale, Thrips",
        "major_pests_ta": "தண்டு துளைப்பான், கிழங்கு செதில் பூச்சி, இலைப்பேன்",
        "major_diseases_en": "Rhizome rot, Leaf spot (Colletotrichum), Leaf blotch (Taphrina)",
        "major_diseases_ta": "கிழங்கு அழுகல், இலைப்புள்ளி நோய், இலை கருகல்"
    },
    {
        "name_en": "Ginger", "name_ta": "இஞ்சி", "category": "Spices", "duration_days": 240,
        "ideal_soil": "Rich Sandy Loam, Red Loam with high organic matter", "ideal_soil_ta": "வளமான மணல் கலந்த செம்மண், அங்கக வளம் மிகுந்த மண்",
        "min_temp": 18.0, "max_temp": 32.0, "min_rainfall": 1200.0, "max_rainfall": 2000.0,
        "water_req_level": "High", "water_req_level_ta": "அதிகம்",
        "n_req": 75.0, "p_req": 50.0, "k_req": 50.0, "ideal_ph_min": 5.5, "ideal_ph_max": 6.8,
        "typical_yield_min_acre": 6000.0, "typical_yield_max_acre": 10000.0,
        "harvest_indicators_en": "Plants turn yellow and pseudo-stems dry and lodge on the ground.",
        "harvest_indicators_ta": "செடிகள் மஞ்சளாகி தண்டுகள் காய்ந்து தரையில் சாயும்.",
        "major_pests_en": "Shoot borer, Rhizome fly, Scale insects",
        "major_pests_ta": "தண்டு துளைப்பான், கிழங்கு ஈ, செதில் பூச்சி",
        "major_diseases_en": "Soft rot (Pythium), Bacterial wilt, Phyllosticta leaf spot",
        "major_diseases_ta": "மென் அழுகல் (சாஃப்ட் ராட்), பாக்டீரியா வாடல், இலைப்புள்ளி"
    },
    {
        "name_en": "Coriander", "name_ta": "கொத்தமல்லி", "category": "Spices", "duration_days": 90,
        "ideal_soil": "Deep Black Soil, Rich Loamy Soil", "ideal_soil_ta": "கரிசல் மண், வளமான வண்டல் மண்",
        "min_temp": 15.0, "max_temp": 28.0, "min_rainfall": 350.0, "max_rainfall": 500.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 30.0, "p_req": 40.0, "k_req": 20.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 300.0, "typical_yield_max_acre": 550.0,
        "harvest_indicators_en": "Umbels turn golden brown and seeds harden.",
        "harvest_indicators_ta": "பூங்கொத்துகள் பொன்னிற பழுப்பாகி விதைகள் கடினமாகும் போது.",
        "major_pests_en": "Aphids, Semilooper", "major_pests_ta": "அசுவினி, கம்பளிப்புழு",
        "major_diseases_en": "Powdery mildew, Wilt, Grain mold",
        "major_diseases_ta": "சாம்பல் நோய், வாடல் நோய், தானிய பூஞ்சை"
    },
    {
        "name_en": "Black Pepper", "name_ta": "மிளகு", "category": "Spices", "duration_days": 240,
        "ideal_soil": "Rich Forest Loam, Red Laterite Soils", "ideal_soil_ta": "காட்டு வண்டல் மண், செம்பொறை மண்",
        "min_temp": 15.0, "max_temp": 32.0, "min_rainfall": 1500.0, "max_rainfall": 3000.0,
        "water_req_level": "High", "water_req_level_ta": "அதிகம்",
        "n_req": 100.0, "p_req": 40.0, "k_req": 140.0, "ideal_ph_min": 5.0, "ideal_ph_max": 6.5,
        "typical_yield_min_acre": 800.0, "typical_yield_max_acre": 1500.0,
        "harvest_indicators_en": "One or two berries in the spike turn bright orange-red.",
        "harvest_indicators_ta": "சரத்திலுள்ள ஒன்று அல்லது இரண்டு மணிகள் ஆரஞ்சு-சிவப்பாக மாறும் போது.",
        "major_pests_en": "Pollu beetle, Top shoot borer, Scale insects",
        "major_pests_ta": "பொல்லு வண்டு, நுனி தண்டு துளைப்பான், செதில் பூச்சி",
        "major_diseases_en": "Quick wilt (Phytophthora foot rot), Slow decline, Pollu disease",
        "major_diseases_ta": "திடீர் வாடல் நோய் (ஃபைட்டோப்தோரா), மெதுவான வாடல் நோய்"
    },
    {
        "name_en": "Cardamom", "name_ta": "ஏலக்காய்", "category": "Spices", "duration_days": 300,
        "ideal_soil": "Humus rich Forest Loam, Clay Loam in hill slopes", "ideal_soil_ta": "மட்கு நிறைந்த மலைக்காட்டு வண்டல் மண்",
        "min_temp": 10.0, "max_temp": 28.0, "min_rainfall": 1800.0, "max_rainfall": 3500.0,
        "water_req_level": "High", "water_req_level_ta": "அதிகம்",
        "n_req": 75.0, "p_req": 75.0, "k_req": 150.0, "ideal_ph_min": 4.8, "ideal_ph_max": 6.2,
        "typical_yield_min_acre": 200.0, "typical_yield_max_acre": 450.0,
        "harvest_indicators_en": "Capsules reach physiological maturity and inner seeds turn black/brown.",
        "harvest_indicators_ta": "ஏலக்காயின் உட்புற விதைகள் கறுப்பாக மாறும் போது.",
        "major_pests_en": "Cardamom thrips, Shoot and capsule borer, Whitefly",
        "major_pests_ta": "ஏலக்காய் இலைப்பேன், தண்டு மற்றும் காய் துளைப்பான், வெள்ளை ஈ",
        "major_diseases_en": "Azhukal (Capsule rot), Katte virus (Mosaic), Clump rot",
        "major_diseases_ta": "அழுகல் நோய், கட்டே வைரஸ் நோய், தூரழுகல் நோய்"
    },

    # --- Vegetables ---
    {
        "name_en": "Tomato", "name_ta": "தக்காளி", "category": "Vegetables", "duration_days": 120,
        "ideal_soil": "Sandy Loam, Red Loam with good drainage", "ideal_soil_ta": "மணல் கலந்த செம்மண், செம்மண்",
        "min_temp": 18.0, "max_temp": 32.0, "min_rainfall": 600.0, "max_rainfall": 1000.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 150.0, "p_req": 100.0, "k_req": 100.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.0,
        "typical_yield_min_acre": 10000.0, "typical_yield_max_acre": 18000.0,
        "harvest_indicators_en": "Fruits turn pink to red (breaker/turning stage for transport; ripe red for local market).",
        "harvest_indicators_ta": "பழங்கள் இளஞ்சிவப்பு முதல் அடர் சிவப்பு நிறமாக மாறும் போது.",
        "major_pests_en": "Fruit borer (Helicoverpa), Whitefly, Leaf miner, Serpentine leaf miner",
        "major_pests_ta": "காய் துளைப்பான், வெள்ளை ஈ, இலை சுரங்கப் புழு",
        "major_diseases_en": "Early blight, Late blight, Tomato Leaf Curl Virus (ToLCV), Bacterial wilt",
        "major_diseases_ta": "முன் பருவ இலைக்கருகல், பின் பருவ இலைக்கருகல், இலைச்சுருட்டு வைரஸ், வாடல் நோய்"
    },
    {
        "name_en": "Onion", "name_ta": "வெங்காயம் (சின்ன வெங்காயம்)", "category": "Vegetables", "duration_days": 90,
        "ideal_soil": "Well drained Sandy Loam, Alluvial, Red Loam", "ideal_soil_ta": "மணல் கலந்த செம்மண், வண்டல் மண்",
        "min_temp": 15.0, "max_temp": 32.0, "min_rainfall": 500.0, "max_rainfall": 750.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 60.0, "p_req": 60.0, "k_req": 60.0, "ideal_ph_min": 6.2, "ideal_ph_max": 7.2,
        "typical_yield_min_acre": 5000.0, "typical_yield_max_acre": 8500.0,
        "harvest_indicators_en": "Tops fall over (neck fall) in 50-70% of plants and outer scale skin dries.",
        "harvest_indicators_ta": "50-70% செடிகளில் தாள்கள் தரையில் சாய்ந்து தோல் உலரும் போது.",
        "major_pests_en": "Thrips (Thrips tabaci), Cutworms",
        "major_pests_ta": "இலைப்பேன் (திரிப்ஸ்), வெட்டுப்புழு",
        "major_diseases_en": "Purple blotch (Alternaria porri), Basal rot, Stemphylium blight",
        "major_diseases_ta": "ஊதா இலைக்கருகல் நோய், அடி அழுகல் நோய்"
    },
    {
        "name_en": "Chilli", "name_ta": "மிளகாய்", "category": "Vegetables", "duration_days": 150,
        "ideal_soil": "Well drained Black Cotton Soil, Red Loam", "ideal_soil_ta": "கரிசல் மண், செம்மண்",
        "min_temp": 18.0, "max_temp": 35.0, "min_rainfall": 600.0, "max_rainfall": 900.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 120.0, "p_req": 60.0, "k_req": 60.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 4000.0, "typical_yield_max_acre": 7500.0,
        "harvest_indicators_en": "Green chillies when fully firm; dry chillies when bright red ripe.",
        "harvest_indicators_ta": "பச்சை மிளகாய் முற்றியவுடன்; காய்ந்த மிளகாய்க்கு பழங்கள் அடர் சிவப்பாக பழுத்த பின்.",
        "major_pests_en": "Thrips (Scirtothrips dorsalis), Yellow mite, Fruit borer, Aphids",
        "major_pests_ta": "இலைப்பேன் (முடக்கு நச்சு), மஞ்சள் சிலந்தி, காய் துளைப்பான்",
        "major_diseases_en": "Anthracnose / Fruit rot, Die-back, Chilli leaf curl virus (ChLCV), Powdery mildew",
        "major_diseases_ta": "ஆந்த்ராக்னோஸ் / பழ அழுகல், நுனிக் கருகல், இலைச்சுருட்டு வைரஸ், சாம்பல் நோய்"
    },
    {
        "name_en": "Brinjal", "name_ta": "கத்தரி", "category": "Vegetables", "duration_days": 140,
        "ideal_soil": "Rich Sandy Loam, Clay Loam with good drainage", "ideal_soil_ta": "வளமான மணல் கலந்த செம்மண், களிமண் வண்டல்",
        "min_temp": 20.0, "max_temp": 35.0, "min_rainfall": 600.0, "max_rainfall": 950.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 100.0, "p_req": 50.0, "k_req": 30.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 9000.0, "typical_yield_max_acre": 15000.0,
        "harvest_indicators_en": "Fruits become plump, glossy with bright color before seeds harden.",
        "harvest_indicators_ta": "விதைகள் முற்றுவதற்கு முன் பளபளப்பான நிறத்துடனும் மிருதுவாகவும் இருக்கும் போது.",
        "major_pests_en": "Shoot and fruit borer (Leucinodes orbonalis), Epilachna beetle, Whitefly",
        "major_pests_ta": "தண்டு மற்றும் காய் துளைப்பான், பொறி வண்டு, வெள்ளை ஈ",
        "major_diseases_en": "Little leaf of brinjal (Phytoplasma), Phomopsis blight, Bacterial wilt",
        "major_diseases_ta": "சிறு இலை நோய் (மைக்ரோபிளாஸ்மா), போமாப்சிஸ் கருகல், பாக்டீரியா வாடல்"
    },
    {
        "name_en": "Okra (Bhendi)", "name_ta": "வெண்டை", "category": "Vegetables", "duration_days": 90,
        "ideal_soil": "Sandy Loam, Clay Loam, Red Loam", "ideal_soil_ta": "மணல் கலந்த செம்மண், வண்டல் மண், செம்மண்",
        "min_temp": 22.0, "max_temp": 36.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 80.0, "p_req": 40.0, "k_req": 40.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 4500.0, "typical_yield_max_acre": 7500.0,
        "harvest_indicators_en": "Tender green pods snap easily at the tip (4-6 days after flowering).",
        "harvest_indicators_ta": "இளங்காய்கள் நுனியை ஒடித்தால் எளிதாக உடையும் போது.",
        "major_pests_en": "Fruit borer (Earias vittella), Leaf hopper, Whitefly",
        "major_pests_ta": "காய் துளைப்பான், தத்துப்பூச்சி, வெள்ளை ஈ",
        "major_diseases_en": "Yellow Vein Mosaic Virus (YVMV), Enation leaf curl, Powdery mildew",
        "major_diseases_ta": "மஞ்சள் நரம்பு தேமல் வைரஸ் (YVMV), சாம்பல் நோய்"
    },
    {
        "name_en": "Cabbage", "name_ta": "முட்டைக்கோஸ்", "category": "Vegetables", "duration_days": 100,
        "ideal_soil": "Sandy Loam, Clay Loam rich in humus", "ideal_soil_ta": "மணல் கலந்த வண்டல் மண், மட்கு நிறைந்த மண்",
        "min_temp": 12.0, "max_temp": 25.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 150.0, "p_req": 100.0, "k_req": 125.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.0,
        "typical_yield_min_acre": 12000.0, "typical_yield_max_acre": 20000.0,
        "harvest_indicators_en": "Heads are solid, compact, firm, and fully grown.",
        "harvest_indicators_ta": "கோஸ் தலைகள் கெட்டியாகவும் திடமாகவும் முழுமையாக வளர்ந்தவுடன்.",
        "major_pests_en": "Diamondback moth (DBM), Cabbage borer, Aphids",
        "major_pests_ta": "வைர முதுகு அந்துப்பூச்சி (DBM), புழு, அசுவினி",
        "major_diseases_en": "Black rot (Xanthomonas), Club root, Downy mildew",
        "major_diseases_ta": "கருப்பு அழுகல் நோய், வேர் வீக்க நோய், அடிச்சாம்பல்"
    },
    {
        "name_en": "Cauliflower", "name_ta": "காலிஃபிளவர்", "category": "Vegetables", "duration_days": 95,
        "ideal_soil": "Deep Rich Loamy Soil, Clay Loam", "ideal_soil_ta": "ஆழமான வளமான வண்டல் மண்",
        "min_temp": 12.0, "max_temp": 25.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 150.0, "p_req": 100.0, "k_req": 125.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.0,
        "typical_yield_min_acre": 10000.0, "typical_yield_max_acre": 16000.0,
        "harvest_indicators_en": "Curds are compact, pure white, and before buds begin to loosen.",
        "harvest_indicators_ta": "பூக்கள் தூய வெண்மையாகவும் தளர்வடையாமல் திடமாகவும் இருக்கும் போது.",
        "major_pests_en": "Diamondback moth, Tobacco caterpillar, Aphids",
        "major_pests_ta": "வைர முதுகு அந்துப்பூச்சி, புகையிலை புழு, அசுவினி",
        "major_diseases_en": "Black rot, Whiptail (Molybdenum deficiency), Downy mildew",
        "major_diseases_ta": "கருப்பு அழுகல், சாட்டைவால் நோய் (மாலிப்டினம் பற்றாக்குறை)"
    },
    {
        "name_en": "Carrot", "name_ta": "கேரட்", "category": "Vegetables", "duration_days": 100,
        "ideal_soil": "Deep Loose Sandy Loam with no stones", "ideal_soil_ta": "கற்களற்ற ஆழமான மணல் கலந்த வண்டல் மண்",
        "min_temp": 10.0, "max_temp": 24.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 50.0, "p_req": 50.0, "k_req": 90.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.0,
        "typical_yield_min_acre": 8000.0, "typical_yield_max_acre": 14000.0,
        "harvest_indicators_en": "Roots attain marketable diameter (2-3 cm) with bright orange coloration.",
        "harvest_indicators_ta": "கிழங்குகள் தகுந்த பருமனுடன் (2-3 செ.மீ) பிரகாசமான ஆரஞ்சு நிறம் அடையும் போது.",
        "major_pests_en": "Root knot nematodes, Carrot rust fly",
        "major_pests_ta": "வேர் முடிச்சு நூற்புழு, கேரட் துரு ஈ",
        "major_diseases_en": "Alternaria leaf blight, Cercospora leaf spot, Cavity spot",
        "major_diseases_ta": "ஆல்டர்னேரியா இலைக்கருகல், குழியமைப்பு நோய்"
    },
    {
        "name_en": "Radish", "name_ta": "முள்ளங்கி", "category": "Vegetables", "duration_days": 45,
        "ideal_soil": "Friable Sandy Loam rich in organic matter", "ideal_soil_ta": "மணல் கலந்த இலகுவான செம்மண்",
        "min_temp": 15.0, "max_temp": 30.0, "min_rainfall": 350.0, "max_rainfall": 600.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 50.0, "p_req": 25.0, "k_req": 40.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 6000.0, "typical_yield_max_acre": 10000.0,
        "harvest_indicators_en": "Roots reach tender edible size before becoming pithy and hollow.",
        "harvest_indicators_ta": "முள்ளங்கி நாறாகவும் பஞ்சாகவும் மாறுவதற்கு முன் இளம்பருவத்தில்.",
        "major_pests_en": "Flea beetle, Aphids", "major_pests_ta": "தெள்ளுப்பூச்சி, அசுவினி",
        "major_diseases_en": "Alternaria blight, White rust",
        "major_diseases_ta": "இலைக்கருகல், வெள்ளை துரு நோய்"
    },
    {
        "name_en": "Beetroot", "name_ta": "பீட்ரூட்", "category": "Vegetables", "duration_days": 80,
        "ideal_soil": "Sandy Loam, Loam with good organic content", "ideal_soil_ta": "மணல் கலந்த வண்டல் மண், செம்மண்",
        "min_temp": 15.0, "max_temp": 28.0, "min_rainfall": 450.0, "max_rainfall": 700.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 60.0, "p_req": 60.0, "k_req": 100.0, "ideal_ph_min": 6.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 8000.0, "typical_yield_max_acre": 13000.0,
        "harvest_indicators_en": "Roots develop to 5-7 cm diameter with deep crimson red flesh.",
        "harvest_indicators_ta": "கிழங்குகள் 5-7 செ.மீ விட்டம் மற்றும் அடர் சிவப்பு சதைப்பற்றுடன் இருக்கும் போது.",
        "major_pests_en": "Flea beetle, Leaf miner", "major_pests_ta": "தெள்ளுப்பூச்சி, இலை சுரங்கப் புழு",
        "major_diseases_en": "Cercospora leaf spot, Downy mildew, Heart rot (Boron deficiency)",
        "major_diseases_ta": "இலைப்புள்ளி, அடிச்சாம்பல், இதய அழுகல் (போரான் குறைபாடு)"
    },
    {
        "name_en": "French Beans", "name_ta": "பீன்ஸ்", "category": "Vegetables", "duration_days": 70,
        "ideal_soil": "Well drained Sandy Loam, Red Loam", "ideal_soil_ta": "மணல் கலந்த செம்மண், வண்டல் மண்",
        "min_temp": 15.0, "max_temp": 26.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 50.0, "p_req": 75.0, "k_req": 50.0, "ideal_ph_min": 5.5, "ideal_ph_max": 6.8,
        "typical_yield_min_acre": 3500.0, "typical_yield_max_acre": 6000.0,
        "harvest_indicators_en": "Tender crisp pods before seeds bulge prominently.",
        "harvest_indicators_ta": "விதைகள் பெருத்து முற்றுவதற்கு முன் மொறுமொறுப்பான இளங்காய்கள்.",
        "major_pests_en": "Stem fly, Pod borer, Aphids",
        "major_pests_ta": "தண்டு ஈ, காய் துளைப்பான், அசுவினி",
        "major_diseases_en": "Anthracnose, Rust, Bean common mosaic virus",
        "major_diseases_ta": "ஆந்த்ராக்னோஸ், துரு நோய், பீன்ஸ் தேமல் வைரஸ்"
    },
    {
        "name_en": "Green Peas", "name_ta": "பட்டாணி", "category": "Vegetables", "duration_days": 80,
        "ideal_soil": "Well drained Sandy Loam to Clay Loam", "ideal_soil_ta": "நல்ல வடிகால் வசதியுள்ள மணல் கலந்த வண்டல் மண்",
        "min_temp": 10.0, "max_temp": 22.0, "min_rainfall": 400.0, "max_rainfall": 650.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 40.0, "p_req": 60.0, "k_req": 50.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 2500.0, "typical_yield_max_acre": 4500.0,
        "harvest_indicators_en": "Pods are fully filled with sweet green tender seeds.",
        "harvest_indicators_ta": "காய்கள் இனிப்பான பசுமையான விதைகளால் நிரம்பியிருக்கும் போது.",
        "major_pests_en": "Pod borer, Leaf miner, Aphids",
        "major_pests_ta": "காய் துளைப்பான், இலை சுரங்கப் புழு, அசுவினி",
        "major_diseases_en": "Powdery mildew, Rust, Ascochyta blight",
        "major_diseases_ta": "சாம்பல் நோய், துரு நோய், அஸ்கோகைட்டா கருகல்"
    },
    {
        "name_en": "Pumpkin", "name_ta": "பூசணிக்காய் (பரங்கிக்காய்)", "category": "Vegetables", "duration_days": 110,
        "ideal_soil": "Sandy Loam rich in organic matter", "ideal_soil_ta": "அங்கக வளம் மிக்க மணல் கலந்த செம்மண்",
        "min_temp": 20.0, "max_temp": 36.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 60.0, "p_req": 50.0, "k_req": 50.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 8000.0, "typical_yield_max_acre": 15000.0,
        "harvest_indicators_en": "Rind hardens and rind color changes to yellow-orange; stem turns corky.",
        "harvest_indicators_ta": "தோல் கடினமாகி மஞ்சள்-ஆரஞ்சு நிறமாகும்; காம்பு மரக்கட்டை போல் மாறும்.",
        "major_pests_en": "Fruit fly (Bactrocera cucurbitae), Red pumpkin beetle",
        "major_pests_ta": "பழ ஈ, சிவப்பு பூசணி வண்டு",
        "major_diseases_en": "Downy mildew, Powdery mildew, Mosaic virus",
        "major_diseases_ta": "அடிச்சாம்பல், சாம்பல் நோய், தேமல் வைரஸ்"
    },
    {
        "name_en": "Bitter Gourd", "name_ta": "பாகற்காய்", "category": "Vegetables", "duration_days": 100,
        "ideal_soil": "Sandy Loam, Loam with good drainage", "ideal_soil_ta": "மணல் கலந்த வண்டல் மண், செம்மண்",
        "min_temp": 22.0, "max_temp": 36.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 60.0, "p_req": 40.0, "k_req": 40.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.0,
        "typical_yield_min_acre": 4000.0, "typical_yield_max_acre": 7500.0,
        "harvest_indicators_en": "Fruits reach full size and dark green/white color before turning yellowish orange.",
        "harvest_indicators_ta": "பழங்கள் மஞ்சளாவதற்கு முன் முழு அளவை அடைந்தவுடன்.",
        "major_pests_en": "Fruit fly, Epilachna beetle, Whitefly",
        "major_pests_ta": "பழ ஈ, பொறி வண்டு, வெள்ளை ஈ",
        "major_diseases_en": "Downy mildew, Powdery mildew, Mosaic virus",
        "major_diseases_ta": "அடிச்சாம்பல், சாம்பல் நோய், தேமல் வைரஸ்"
    },
    {
        "name_en": "Bottle Gourd", "name_ta": "சுரைக்காய்", "category": "Vegetables", "duration_days": 90,
        "ideal_soil": "Sandy Loam, Silt Loam rich in organic matter", "ideal_soil_ta": "மணல் கலந்த செம்மண், வண்டல் மண்",
        "min_temp": 20.0, "max_temp": 36.0, "min_rainfall": 450.0, "max_rainfall": 750.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 50.0, "p_req": 30.0, "k_req": 30.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 8000.0, "typical_yield_max_acre": 14000.0,
        "harvest_indicators_en": "Tender fruits whose rind can be pierced easily with fingernail.",
        "harvest_indicators_ta": "நகத்தால் அழுத்தினால் எளிதில் ஊடுருவக்கூடிய இளங்காய்கள்.",
        "major_pests_en": "Fruit fly, Red pumpkin beetle",
        "major_pests_ta": "பழ ஈ, சிவப்பு பூசணி வண்டு",
        "major_diseases_en": "Anthracnose, Downy mildew, Powdery mildew",
        "major_diseases_ta": "ஆந்த்ராக்னோஸ், அடிச்சாம்பல், சாம்பல் நோய்"
    },
    {
        "name_en": "Snake Gourd", "name_ta": "புடலங்காய்", "category": "Vegetables", "duration_days": 105,
        "ideal_soil": "Sandy Loam, Loamy Soil", "ideal_soil_ta": "மணல் கலந்த செம்மண், வண்டல் மண்",
        "min_temp": 22.0, "max_temp": 36.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 60.0, "p_req": 40.0, "k_req": 40.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.0,
        "typical_yield_min_acre": 6000.0, "typical_yield_max_acre": 11000.0,
        "harvest_indicators_en": "Tender long fruits before seeds turn hard and skin turns fibrous.",
        "harvest_indicators_ta": "தோல் கடினமாவதற்கு முன் நீண்ட இளங்காய்களாக இருக்கும் போது.",
        "major_pests_en": "Fruit fly, Plume moth", "major_pests_ta": "பழ ஈ, இறகு அந்துப்பூச்சி",
        "major_diseases_en": "Downy mildew, Powdery mildew",
        "major_diseases_ta": "அடிச்சாம்பல், சாம்பல் நோய்"
    },
    {
        "name_en": "Watermelon", "name_ta": "தர்பூசணி", "category": "Fruits", "duration_days": 85,
        "ideal_soil": "Sandy Loam, Riverbed Sandy Soils", "ideal_soil_ta": "ஆற்றுப்படுகை மணல் மண், மணல் கலந்த செம்மண்",
        "min_temp": 24.0, "max_temp": 38.0, "min_rainfall": 350.0, "max_rainfall": 600.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 60.0, "p_req": 40.0, "k_req": 60.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 12000.0, "typical_yield_max_acre": 22000.0,
        "harvest_indicators_en": "Tendril near fruit stalk dries up; ground spot turns creamy yellow; dull thud sound upon thumping.",
        "harvest_indicators_ta": "பழத்தின் அருகிலுள்ள பற்றுக்கம்பி காயும்; தரையில் படும் பகுதி வெளிர் மஞ்சளாகும்; தட்டினால் மந்தமான ஒலி வரும்.",
        "major_pests_en": "Fruit fly, Red spider mite, Aphids",
        "major_pests_ta": "பழ ஈ, சிவப்பு சிலந்தி, அசுவினி",
        "major_diseases_en": "Fusarium wilt, Downy mildew, Gummy stem blight",
        "major_diseases_ta": "வாடல் நோய், அடிச்சாம்பல், பிசின் தண்டு கருகல்"
    },
    {
        "name_en": "Muskmelon", "name_ta": "முலாம்பழம் (கீbreeding)", "category": "Fruits", "duration_days": 80,
        "ideal_soil": "Sandy Loam, Alluvial Soil", "ideal_soil_ta": "மணல் கலந்த வண்டல் மண், செம்மண்",
        "min_temp": 24.0, "max_temp": 38.0, "min_rainfall": 350.0, "max_rainfall": 550.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 50.0, "p_req": 30.0, "k_req": 50.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 7000.0, "typical_yield_max_acre": 12000.0,
        "harvest_indicators_en": "Fruit slips cleanly from the vine with gentle pressure ('full-slip' stage).",
        "harvest_indicators_ta": "கொடியிலிருந்து பழம் லேசான அழுத்தத்தில் எளிதாக பிரியும் போது.",
        "major_pests_en": "Fruit fly, Aphids", "major_pests_ta": "பழ ஈ, அசுவினி",
        "major_diseases_en": "Powdery mildew, Downy mildew",
        "major_diseases_ta": "சாம்பல் நோய், அடிச்சாம்பல்"
    },
    {
        "name_en": "Cucumber", "name_ta": "வெள்ளரி", "category": "Vegetables", "duration_days": 60,
        "ideal_soil": "Sandy Loam rich in organic matter", "ideal_soil_ta": "மணல் கலந்த செம்மண்",
        "min_temp": 20.0, "max_temp": 35.0, "min_rainfall": 400.0, "max_rainfall": 650.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 50.0, "p_req": 30.0, "k_req": 30.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.2,
        "typical_yield_min_acre": 5000.0, "typical_yield_max_acre": 9000.0,
        "harvest_indicators_en": "Crisp green fruits before spines turn yellow or seeds turn hard.",
        "harvest_indicators_ta": "விதைகள் முற்றுவதற்கு முன் முட்கள் உதிர்ந்து பசுமையாக இருக்கும் போது.",
        "major_pests_en": "Fruit fly, Red pumpkin beetle",
        "major_pests_ta": "பழ ஈ, சிவப்பு பூசணி வண்டு",
        "major_diseases_en": "Downy mildew, Powdery mildew, Cucumber mosaic virus",
        "major_diseases_ta": "அடிச்சாம்பல், சாம்பல் நோய், வெள்ளரி தேமல் வைரஸ்"
    },

    # --- Fruits & Plantation ---
    {
        "name_en": "Mango", "name_ta": "மாம்பழம்", "category": "Fruits", "duration_days": 365,
        "ideal_soil": "Deep Red Loamy Soil, Alluvial with deep subsoil", "ideal_soil_ta": "ஆழமான செம்மண், வண்டல் மண்",
        "min_temp": 20.0, "max_temp": 40.0, "min_rainfall": 700.0, "max_rainfall": 1500.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 400.0, "p_req": 200.0, "k_req": 400.0, "ideal_ph_min": 5.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 4000.0, "typical_yield_max_acre": 8500.0,
        "harvest_indicators_en": "Slight color break from green to yellowish-red at shoulders; specific gravity reaches 1.01-1.02.",
        "harvest_indicators_ta": "பழங்களின் தோள்பட்டை பகுதியில் லேசான மஞ்சள்-சிவப்பு நிறம் தோன்றும் போது.",
        "major_pests_en": "Mango hopper, Fruit fly, Stem borer, Nut weevil",
        "major_pests_ta": "மாந்தத்துப்பூச்சி, பழ ஈ, தண்டு துளைப்பான், மாங்கொட்டை வண்டு",
        "major_diseases_en": "Anthracnose, Powdery mildew, Die-back",
        "major_diseases_ta": "ஆந்த்ராக்னோஸ், சாம்பல் நோய், நுனிக்கருகல்"
    },
    {
        "name_en": "Guava", "name_ta": "கொய்யா", "category": "Fruits", "duration_days": 365,
        "ideal_soil": "Clay Loam, Sandy Loam with good drainage", "ideal_soil_ta": "களிமண் கலந்த வண்டல், மணல் கலந்த செம்மண்",
        "min_temp": 15.0, "max_temp": 38.0, "min_rainfall": 600.0, "max_rainfall": 1200.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 250.0, "p_req": 150.0, "k_req": 250.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 6000.0, "typical_yield_max_acre": 12000.0,
        "harvest_indicators_en": "Fruit skin changes from dark green to pale green/yellowish green.",
        "harvest_indicators_ta": "தோலின் நிறம் அடர் பச்சையிலிருந்து வெளிர் பச்சை/மஞ்சள் கலந்த பச்சையாக மாறும் போது.",
        "major_pests_en": "Fruit fly, Mealybug, Tea mosquito bug",
        "major_pests_ta": "பழ ஈ, மாவுப்பூச்சி, தேயிலை கொசு வண்டு",
        "major_diseases_en": "Guava wilt (Fusarium), Anthracnose, Canker",
        "major_diseases_ta": "கொய்யா வாடல் நோய், ஆந்த்ராக்னோஸ், புண் நோய்"
    },
    {
        "name_en": "Papaya", "name_ta": "பப்பாளி", "category": "Fruits", "duration_days": 270,
        "ideal_soil": "Well drained Deep Loamy Soil, Alluvial", "ideal_soil_ta": "நல்ல வடிகால் வசதியுள்ள ஆழமான வண்டல் மண்",
        "min_temp": 20.0, "max_temp": 36.0, "min_rainfall": 1000.0, "max_rainfall": 1800.0,
        "water_req_level": "High", "water_req_level_ta": "அதிகம்",
        "n_req": 200.0, "p_req": 200.0, "k_req": 250.0, "ideal_ph_min": 6.0, "ideal_ph_max": 7.0,
        "typical_yield_min_acre": 25000.0, "typical_yield_max_acre": 45000.0,
        "harvest_indicators_en": "One or two yellow streaks appear on the green skin near apex.",
        "harvest_indicators_ta": "பழத்தின் நுனிப்பகுதியில் ஒன்று அல்லது இரண்டு மஞ்சள் நிறக் கோடுகள் தோன்றும் போது.",
        "major_pests_en": "Papaya mealybug (Paracoccus marginatus), Whitefly, Aphids",
        "major_pests_ta": "பப்பாளி மாவுப்பூச்சி, வெள்ளை ஈ, அசுவினி",
        "major_diseases_en": "Papaya Ring Spot Virus (PRSV), Collar rot, Anthracnose",
        "major_diseases_ta": "பப்பாளி வளைய புள்ளி வைரஸ் (PRSV), தண்டு அழுகல், ஆந்த்ராக்னோஸ்"
    },
    {
        "name_en": "Pomegranate", "name_ta": "மாதுளை", "category": "Fruits", "duration_days": 365,
        "ideal_soil": "Deep Loamy to Light Sandy Loam", "ideal_soil_ta": "ஆழமான வண்டல் மண், மணல் கலந்த செம்மண்",
        "min_temp": 18.0, "max_temp": 38.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 250.0, "p_req": 125.0, "k_req": 250.0, "ideal_ph_min": 6.5, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 4500.0, "typical_yield_max_acre": 8500.0,
        "harvest_indicators_en": "Rind changes from green to yellowish-red and ridges become less prominent; metallic ring when tapped.",
        "harvest_indicators_ta": "தோலின் நிறம் மஞ்சள்-சிவப்பாக மாறும்; பழத்தின் முகடுகள் வட்டமாகும்; தட்டினால் உலோகம் போன்ற சத்தம் வரும்.",
        "major_pests_en": "Pomegranate butterfly (Deudorix isocrates), Thrips, Whitefly",
        "major_pests_ta": "மாதுளை பட்டாம்பூச்சி (காய் துளைப்பான்), இலைப்பேன்",
        "major_diseases_en": "Bacterial blight (Telya / Xanthomonas), Anthracnose, Wilt",
        "major_diseases_ta": "பாக்டீரியா கருகல் (டெல்யா நோய்), ஆந்த்ராக்னோஸ், வாடல்"
    },
    {
        "name_en": "Grapes", "name_ta": "திராட்சை", "category": "Fruits", "duration_days": 130,
        "ideal_soil": "Well drained Sandy Loam, Clay Loam", "ideal_soil_ta": "மணல் கலந்த வண்டல் மண், செம்மண்",
        "min_temp": 15.0, "max_temp": 35.0, "min_rainfall": 500.0, "max_rainfall": 800.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 200.0, "p_req": 150.0, "k_req": 300.0, "ideal_ph_min": 6.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 10000.0, "typical_yield_max_acre": 20000.0,
        "harvest_indicators_en": "Berries near cluster apex turn sweet; seed color turns brown; TSS exceeds 16-18°Brix.",
        "harvest_indicators_ta": "குலையின் நுனிப் பழங்கள் இனிப்பாகி விதைகள் பழுப்பாகும்; சர்க்கரை அளவு 16-18° பிரிக்ஸ் தாண்டும்.",
        "major_pests_en": "Thrips, Flea beetle, Mealybug",
        "major_pests_ta": "இலைப்பேன், தெள்ளுப்பூச்சி, மாவுப்பூச்சி",
        "major_diseases_en": "Downy mildew, Powdery mildew, Anthracnose",
        "major_diseases_ta": "அடிச்சாம்பல், சாம்பல் நோய், ஆந்த்ராக்னோஸ்"
    },
    {
        "name_en": "Cashew", "name_ta": "முந்திரி", "category": "Plantation", "duration_days": 365,
        "ideal_soil": "Red Sandy Loam, Laterite Soils, Coastal Sand", "ideal_soil_ta": "செம்மண், செம்பொறை மண், கடலோர மணல்",
        "min_temp": 20.0, "max_temp": 38.0, "min_rainfall": 800.0, "max_rainfall": 2000.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 200.0, "p_req": 100.0, "k_req": 100.0, "ideal_ph_min": 5.0, "ideal_ph_max": 6.5,
        "typical_yield_min_acre": 800.0, "typical_yield_max_acre": 1600.0,
        "harvest_indicators_en": "Cashew apple turns bright yellow/red and fruit drops naturally from tree.",
        "harvest_indicators_ta": "முந்திரிப் பழம் மஞ்சள்/சிவப்பாக மாறி மரத்திலிருந்து தானாக உதிரும் போது.",
        "major_pests_en": "Tea mosquito bug (Helopeltis antonii), Stem and root borer",
        "major_pests_ta": "தேயிலை கொசு வண்டு, தண்டு மற்றும் வேர் துளைப்பான்",
        "major_diseases_en": "Die-back / Anthracnose, Inflorescence blight",
        "major_diseases_ta": "நுனிக்கருகல் / ஆந்த்ராக்னோஸ், பூங்கொத்து கருகல்"
    },
    {
        "name_en": "Amla (Indian Gooseberry)", "name_ta": "நெல்லிக்காய்", "category": "Fruits", "duration_days": 365,
        "ideal_soil": "Light to Heavy Loam, Sodic & Saline tolerant", "ideal_soil_ta": "வண்டல் மண், உவர் மற்றும் களர் நிலங்களிலும் வளரும்",
        "min_temp": 15.0, "max_temp": 42.0, "min_rainfall": 500.0, "max_rainfall": 1000.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 200.0, "p_req": 150.0, "k_req": 200.0, "ideal_ph_min": 6.5, "ideal_ph_max": 9.0,
        "typical_yield_min_acre": 6000.0, "typical_yield_max_acre": 12000.0,
        "harvest_indicators_en": "Fruits turn greenish-yellow and seed color changes from light to dark brown.",
        "harvest_indicators_ta": "காய்கள் பச்சை-மஞ்சள் நிறமாக மாறி விதை அடர் பழுப்பாகும் போது.",
        "major_pests_en": "Bark eating caterpillar, Shoot gall maker",
        "major_pests_ta": "மட்டை தின்னும் புழு, குருத்து முடிச்சு வண்டு",
        "major_diseases_en": "Amla rust, Fruit rot",
        "major_diseases_ta": "நெல்லி துரு நோய், பழ அழுகல்"
    },
    {
        "name_en": "Drumstick (Moringa)", "name_ta": "முருங்கை", "category": "Vegetables", "duration_days": 180,
        "ideal_soil": "Sandy Loam, Red Loam, Well drained soils", "ideal_soil_ta": "மணல் கலந்த செம்மண், செம்மண்",
        "min_temp": 20.0, "max_temp": 40.0, "min_rainfall": 400.0, "max_rainfall": 800.0,
        "water_req_level": "Low", "water_req_level_ta": "குறைவு",
        "n_req": 75.0, "p_req": 50.0, "k_req": 75.0, "ideal_ph_min": 6.0, "ideal_ph_max": 8.0,
        "typical_yield_min_acre": 8000.0, "typical_yield_max_acre": 16000.0,
        "harvest_indicators_en": "Pods reach full length while remaining tender with soft seeds.",
        "harvest_indicators_ta": "காய்கள் முழு நீளத்தை அடைந்து விதைகள் மிருதுவாக இருக்கும் போது.",
        "major_pests_en": "Moringa fruit fly (Gitona distigma), Hairy caterpillar, Bark borer",
        "major_pests_ta": "முருங்கை காய் ஈ, கம்பளிப்புழு, மரப்பட்டை துளைப்பான்",
        "major_diseases_en": "Pod rot, Root rot",
        "major_diseases_ta": "காய் அழுகல், வேரழுகல்"
    },
    {
        "name_en": "Jasmine (Mullai / Madurai Malli)", "name_ta": "மல்லிகை (மல்லி / முல்லை)", "category": "Flowers", "duration_days": 365,
        "ideal_soil": "Well drained Sandy Loam, Red Loamy Soil", "ideal_soil_ta": "மணல் கலந்த செம்மண், வளமான வண்டல் மண்",
        "min_temp": 20.0, "max_temp": 38.0, "min_rainfall": 600.0, "max_rainfall": 1200.0,
        "water_req_level": "Medium", "water_req_level_ta": "நடுத்தரம்",
        "n_req": 120.0, "p_req": 240.0, "k_req": 240.0, "ideal_ph_min": 6.5, "ideal_ph_max": 7.5,
        "typical_yield_min_acre": 2500.0, "typical_yield_max_acre": 4500.0,
        "harvest_indicators_en": "Fully developed unopened white flower buds in early morning hours before sunrise.",
        "harvest_indicators_ta": "சூரிய உதயத்திற்கு முன் அதிகாலையில் விரிவடையாத வெண்மையான மொட்டுகள்.",
        "major_pests_en": "Bud worm (Hendecasis duplifascialis), Blossom midge, Red spider mite",
        "major_pests_ta": "மொட்டுப்புழு, பூ மொட்டு ஈ, சிவப்பு சிலந்தி",
        "major_diseases_en": "Leaf blight (Alternaria), Rust, Root rot",
        "major_diseases_ta": "இலைக்கருகல், துரு நோய், வேரழுகல்"
    }
]

def seed_database(db: Session):
    # Check if data already exists
    if db.query(District).first():
        return

    # 1. Seed Districts & Taluks
    for d_data in TN_DISTRICTS_DATA:
        district = District(
            name_en=d_data["name_en"],
            name_ta=d_data["name_ta"],
            latitude=d_data["lat"],
            longitude=d_data["lon"]
        )
        db.add(district)
        db.flush()

        for t_data in d_data.get("taluks", []):
            taluk = Taluk(
                district_id=district.id,
                name_en=t_data["name_en"],
                name_ta=t_data["name_ta"],
                latitude=t_data["lat"],
                longitude=t_data["lon"]
            )
            db.add(taluk)

    # 2. Seed Pattams
    for p_data in TN_PATTAMS_DATA:
        pattam = Pattam(
            name_en=p_data["name_en"],
            name_ta=p_data["name_ta"],
            months_en=p_data["months_en"],
            months_ta=p_data["months_ta"],
            description_en=p_data["description_en"],
            description_ta=p_data["description_ta"],
            recommended_crops_en=p_data["recommended_crops_en"],
            recommended_crops_ta=p_data["recommended_crops_ta"]
        )
        db.add(pattam)

    # 3. Seed 50+ Crops
    for c_data in TN_CROPS_DATA:
        crop = Crop(
            name_en=c_data["name_en"],
            name_ta=c_data["name_ta"],
            category=c_data["category"],
            duration_days=c_data["duration_days"],
            ideal_soil=c_data["ideal_soil"],
            ideal_soil_ta=c_data["ideal_soil_ta"],
            min_temp=c_data["min_temp"],
            max_temp=c_data["max_temp"],
            min_rainfall=c_data["min_rainfall"],
            max_rainfall=c_data["max_rainfall"],
            water_req_level=c_data["water_req_level"],
            water_req_level_ta=c_data["water_req_level_ta"],
            n_req=c_data["n_req"],
            p_req=c_data["p_req"],
            k_req=c_data["k_req"],
            ideal_ph_min=c_data["ideal_ph_min"],
            ideal_ph_max=c_data["ideal_ph_max"],
            typical_yield_min_acre=c_data["typical_yield_min_acre"],
            typical_yield_max_acre=c_data["typical_yield_max_acre"],
            harvest_indicators_en=c_data["harvest_indicators_en"],
            harvest_indicators_ta=c_data["harvest_indicators_ta"],
            major_pests_en=c_data["major_pests_en"],
            major_pests_ta=c_data["major_pests_ta"],
            major_diseases_en=c_data["major_diseases_en"],
            major_diseases_ta=c_data["major_diseases_ta"],
        )
        db.add(crop)

    db.commit()
    print("Database seeded with Tamil Nadu districts, taluks, pattams, and 50+ crops successfully.")
