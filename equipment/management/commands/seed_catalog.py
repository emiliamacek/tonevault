from django.core.management.base import BaseCommand
from equipment.models import Brand, Guitar, Amplifier, Pedal
from setups.models import Genre, Band, Song

class Command(BaseCommand):
    help = 'Populates the database with standard gear and music data'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding database...")

        # --- 1. BRANDS ---
        brands = [
            "Fender", "Gibson", "Ibanez", "PRS", "Epiphone", 
            "Marshall", "Vox", "Orange", "Mesa/Boogie", 
            "Boss", "Ibanez", "Dunlop", "Electro-Harmonix", "MXR"
        ]
        brand_objs = {}
        for b_name in brands:
            brand, _ = Brand.objects.get_or_create(name=b_name)
            brand_objs[b_name] = brand
        self.stdout.write(f"✅ Added {len(brands)} Brands")

        # --- 2. GUITARS ---
        guitars = [
            ("Stratocaster Standard", "Fender", "Solid Body"),
            ("Telecaster", "Fender", "Solid Body"),
            ("Les Paul Standard", "Gibson", "Solid Body"),
            ("SG Standard", "Gibson", "Solid Body"),
            ("ES-335", "Gibson", "Semi-Hollow"),
            ("RG550", "Ibanez", "Solid Body"),
            ("Custom 24", "PRS", "Solid Body"),
        ]
        for name, brand, shape in guitars:
            Guitar.objects.get_or_create(
                name=name, 
                brand=brand_objs[brand], 
                defaults={'body_shape': shape, 'num_strings': 6}
            )
        self.stdout.write(f"✅ Added {len(guitars)} Guitars")

        # --- 3. AMPLIFIERS ---
# --- 3. AMPLIFIERS ---
        # Format: (Name, Brand, Type, Wattage)
        amps = [
            ("JCM800", "Marshall", "Tube", 100),
            ("Twin Reverb", "Fender", "Tube", 85),
            ("AC30", "Vox", "Tube", 30),
            ("Dual Rectifier", "Mesa/Boogie", "Tube", 100),
            ("Rockerverb 50", "Orange", "Tube", 50),
            ("Katana 50", "Boss", "Digital/Modeling", 50),
        ]
        
        for name, brand, tech, watts in amps: # <--- Dodajemy watts tutaj
            Amplifier.objects.get_or_create(
                name=name, 
                brand=brand_objs[brand], 
                defaults={
                    'amp_type': tech,
                    'wattage': watts  # <--- I przekazujemy tutaj
                }
            )
        self.stdout.write(f"✅ Added {len(amps)} Amps")

        # --- 4. PEDALS ---
        pedals = [
            ("Tube Screamer TS9", "Ibanez", "Overdrive"),
            ("DS-1 Distortion", "Boss", "Distortion"),
            ("Cry Baby Wah", "Dunlop", "Wah"),
            ("Big Muff Pi", "Electro-Harmonix", "Fuzz"),
            ("Phase 90", "MXR", "Modulation"),
            ("DD-8 Digital Delay", "Boss", "Delay"),
        ]
        for name, brand, p_type in pedals:
            Pedal.objects.get_or_create(
                name=name, 
                brand=brand_objs[brand], 
                defaults={'pedal_type': p_type}
            )
        self.stdout.write(f"✅ Added {len(pedals)} Pedals")

        # --- 5. MUSIC (Genres, Bands, Songs) ---
        data = {
            "Rock": {
                "Jimi Hendrix Experience": ["Purple Haze", "Little Wing"],
                "Led Zeppelin": ["Whole Lotta Love", "Stairway to Heaven"],
            },
            "Metal": {
                "Metallica": ["Master of Puppets", "Enter Sandman"],
                "Iron Maiden": ["The Trooper", "Run to the Hills"],
            },
            "Blues": {
                "B.B. King": ["The Thrill Is Gone"],
                "Stevie Ray Vaughan": ["Pride and Joy"],
            }
        }

        for genre_name, bands in data.items():
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            for band_name, songs in bands.items():
                band, _ = Band.objects.get_or_create(name=band_name, genre=genre)
                for song_title in songs:
                    Song.objects.get_or_create(title=song_title, band=band)
        
        self.stdout.write("✅ Added Music Data (Genres, Bands, Songs)")
        self.stdout.write(self.style.SUCCESS('🎉 Database seeded successfully!'))
