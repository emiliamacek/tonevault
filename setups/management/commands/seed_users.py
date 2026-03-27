import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Modele
from setups.models import Setup, SignalChainItem, Genre
from equipment.models import OwnedGear, Guitar, Amplifier, Pedal, Brand

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with a mix of Legends, Pros, and Regular Joes'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌍 Creating the ToneVault Community...")

        users_data = [
            # --- LEGENDY ---
            {
                'username': 'jimi_hendrix',
                'email': 'jimi@voodoo.com',
                'password': 'purplehaze',
                'bio': 'Electric Gypsy. Left-handed Strat master. I kiss the sky.',
                'skill_level': 'Virtuoso',
                'gear': [
                    {'type': 'guitar', 'model': 'Stratocaster Standard', 'brand': 'Fender', 'nick': 'Izabella', 'custom': False},
                    {'type': 'amp', 'model': 'Super Lead 100', 'brand': 'Marshall', 'nick': 'The Stack', 'custom': True}, # Custom bo nie ma w seedzie
                    {'type': 'pedal', 'model': 'Fuzz Face', 'brand': 'Dunlop', 'custom': True},
                    {'type': 'pedal', 'model': 'Cry Baby Wah', 'brand': 'Dunlop', 'custom': False},
                    {'type': 'pedal', 'model': 'Uni-Vibe', 'brand': 'MXR', 'custom': True},
                ],
                'setups': [
                    {
                        'name': 'Woodstock 1969',
                        'desc': 'The anthem destroyer tone. Fuzz fully cranked.',
                        'genre': 'Rock',
                        'band': 'Jimi Hendrix Experience',
                        'song': 'The Star Spangled Banner',
                        'public': True
                    }
                ]
            },
            {
                'username': 'srv_texas',
                'email': 'stevie@flood.com',
                'password': 'texasflood',
                'bio': 'Texas Blues. Heavy strings, high action. Soul to Squeeze.',
                'skill_level': 'Professional',
                'gear': [
                    {'type': 'guitar', 'model': 'Stratocaster Standard', 'brand': 'Fender', 'nick': 'Number One', 'custom': False},
                    {'type': 'amp', 'model': 'Super Reverb', 'brand': 'Fender', 'nick': 'Blackface', 'custom': True},
                    {'type': 'pedal', 'model': 'Tube Screamer TS9', 'brand': 'Ibanez', 'custom': False},
                ],
                'setups': [
                    {
                        'name': 'Pride and Joy Tone',
                        'desc': 'Clean but slightly broken up. Tube Screamer as a boost.',
                        'genre': 'Blues',
                        'band': 'Stevie Ray Vaughan',
                        'song': 'Pride and Joy',
                        'public': True
                    }
                ]
            },
            
            # --- LOKALNI UŻYTKOWNICY (POLSKA SPOŁECZNOŚĆ) ---
            {
                'username': 'jarek233',
                'email': 'jaroslaw@poczta.pl',
                'password': 'haslo123',
                'bio': 'Gram w garażu z chłopakami. Szukam taniego i dobrego brzmienia. Fan Dżemu.',
                'skill_level': 'Beginner',
                'gear': [
                    {'type': 'guitar', 'model': 'Squier Strat', 'brand': 'Fender', 'nick': 'Pierwsze wiosło', 'custom': True}, # Custom bo może nie być w katalogu
                    {'type': 'amp', 'model': 'Frontman 10G', 'brand': 'Fender', 'nick': 'Pierdzik', 'custom': True},
                    {'type': 'pedal', 'model': 'DS-1 Distortion', 'brand': 'Boss', 'custom': False},
                ],
                'setups': [
                    {
                        'name': 'Próba w garażu',
                        'desc': 'Ustawienia pod polski rock. Trochę siary na górze ale daje radę.',
                        'genre': 'Rock',
                        'public': True
                    }
                ]
            },
            {
                'username': 'metal_head_pl',
                'email': 'szatan666@buziaczek.pl',
                'password': '666',
                'bio': 'DJENT ONLY. 0-0-0-0-0. Kocham Meshuggah.',
                'skill_level': 'Intermediate',
                'gear': [
                    {'type': 'guitar', 'model': 'RG550', 'brand': 'Ibanez', 'nick': 'Wyścigówka', 'custom': False},
                    {'type': 'amp', 'model': '6505', 'brand': 'Peavey', 'nick': 'Bestia', 'custom': True},
                    {'type': 'pedal', 'model': 'Tube Screamer TS9', 'brand': 'Ibanez', 'nick': 'Boost', 'custom': False},
                    {'type': 'pedal', 'model': 'Noise Gate', 'brand': 'Boss', 'custom': True},
                ],
                'setups': [
                    {
                        'name': 'Djent Rhythm',
                        'desc': 'Mid boost, gain na 6, basy wycięte. Idealne do drop A.',
                        'genre': 'Metal',
                        'public': True
                    }
                ]
            },
            {
                'username': 'shoegaze_girl',
                'email': 'reverb@dreams.com',
                'password': 'loveless',
                'bio': 'I like making noises that sound like whales. Kevin Shields is god.',
                'skill_level': 'Intermediate',
                'gear': [
                    {'type': 'guitar', 'model': 'Jazzmaster', 'brand': 'Fender', 'nick': 'Pinky', 'custom': True},
                    {'type': 'amp', 'model': 'AC30', 'brand': 'Vox', 'nick': 'Chimey', 'custom': False},
                    {'type': 'pedal', 'model': 'Big Muff Pi', 'brand': 'Electro-Harmonix', 'custom': False},
                    {'type': 'pedal', 'model': 'DD-8 Digital Delay', 'brand': 'Boss', 'custom': False},
                    {'type': 'pedal', 'model': 'Hall of Fame', 'brand': 'TC Electronic', 'custom': True},
                ],
                'setups': [
                    {
                        'name': 'Wall of Sound',
                        'desc': 'Reverse reverb into fuzz. Dreamy and loud.',
                        'genre': 'Rock', # Alternative mapujemy na Rock bo nie ma w seedzie
                        'public': True
                    }
                ]
            },
            {
                'username': 'blues_dad_55',
                'email': 'lawyer@corp.com',
                'password': 'money',
                'bio': 'Playing for 40 years. Collecting boutique gear. Tone is in the fingers (and the wallet).',
                'skill_level': 'Advanced',
                'gear': [
                    {'type': 'guitar', 'model': 'Les Paul Standard', 'brand': 'Gibson', 'nick': 'The Burst', 'custom': False},
                    {'type': 'guitar', 'model': 'Custom 24', 'brand': 'PRS', 'nick': 'Birdie', 'custom': False},
                    {'type': 'amp', 'model': 'Twin Reverb', 'brand': 'Fender', 'nick': 'Clean Machine', 'custom': False},
                    {'type': 'pedal', 'model': 'Klon Centaur', 'brand': 'Unknown', 'nick': 'The Horse', 'custom': True}, # Custom bo rzadki
                ],
                'setups': [
                    {
                        'name': 'Sunday Blues Jam',
                        'desc': 'Just a bit of transparent overdrive.',
                        'genre': 'Blues',
                        'public': True
                    },
                     {
                        'name': 'Clapton Woman Tone',
                        'desc': 'Tone rolled off completely.',
                        'genre': 'Blues',
                        'public': False # Prywatny setup!
                    }
                ]
            },
            {
                'username': 'luthier_krzysztof',
                'email': 'krzysztof@warsztat.pl',
                'password': 'wood',
                'bio': 'Buduję gitary z drewna z odzysku. Ten setup to moje testowe brzmienie.',
                'skill_level': 'Professional',
                'gear': [
                    {'type': 'guitar', 'model': 'Telecaster Custom', 'brand': 'Unknown', 'nick': 'Projekt #1', 'custom': True},
                    {'type': 'amp', 'model': 'Katana 50', 'brand': 'Boss', 'nick': 'Roboczy', 'custom': False},
                ],
                'setups': [
                    {
                        'name': 'Test Clean',
                        'desc': 'Super czyste brzmienie do sprawdzania intonacji.',
                        'genre': 'Blues', # Jazz mapujemy na Blues
                        'public': True
                    }
                ]
            }
        ]

        # Słowniki pomocnicze do znajdowania ID gatunków
        genres_map = {g.name: g.id for g in Genre.objects.all()} 
        default_genre = Genre.objects.first()

        for user_data in users_data:
            # 1. Tworzenie usera
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                email=user_data['email']
            )
            
            # Aktualizacja pól Usera (hasło, bio, skill)
            user.set_password(user_data.get('password', 'password123'))
            
            # Sprawdźmy czy model User ma pola bio i skill_level (zgodnie z diagramem)
            if hasattr(user, 'bio'):
                user.bio = user_data.get('bio', '')
            if hasattr(user, 'skill_level'):
                user.skill_level = user_data.get('skill_level', 'Beginner')
            
            user.save()
            
            if created:
                self.stdout.write(f"👤 Created user: {user.username}")
            else:
                self.stdout.write(f"👤 Updated user: {user.username}")

            # 3. Dodawanie Sprzętu (Owned Gear)
            my_gear_map = {} # Do łączenia w setupach
            
            for item in user_data['gear']:
                gear_obj = None
                
                # A. Szukamy marki lub tworzymy
                brand_obj, _ = Brand.objects.get_or_create(name=item['brand'])

                # B. Szukamy lub tworzymy przedmiot w katalogu
                # Próbujemy znaleźć exact match, jak nie ma to tworzymy
                
                model_name = item['model']
                
                if item['type'] == 'guitar':
                    gear_obj = Guitar.objects.filter(name__iexact=model_name).first()
                    if not gear_obj:
                         defaults = {'body_shape': 'Custom', 'num_strings': 6}
                         gear_obj, _ = Guitar.objects.get_or_create(name=model_name, brand=brand_obj, defaults=defaults)
                
                elif item['type'] == 'amp':
                    gear_obj = Amplifier.objects.filter(name__iexact=model_name).first()
                    if not gear_obj:
                         defaults = {'amp_type': 'Custom', 'wattage': 50}
                         gear_obj, _ = Amplifier.objects.get_or_create(name=model_name, brand=brand_obj, defaults=defaults)

                elif item['type'] == 'pedal':
                    gear_obj = Pedal.objects.filter(name__iexact=model_name).first()
                    if not gear_obj:
                         defaults = {'pedal_type': 'Custom'}
                         gear_obj, _ = Pedal.objects.get_or_create(name=model_name, brand=brand_obj, defaults=defaults)

                # C. Tworzymy OwnedGear (Egzemplarz użytkownika)
                if gear_obj:
                    # ✅ POPRAWKA: Mapujemy 'amp' na 'amplifier', bo tak nazywa się pole w modelu
                    field_name = item['type']
                    if field_name == 'amp':
                        field_name = 'amplifier'
                        
                    owned_kwargs = {
                        'user': user,
                        field_name: gear_obj # Teraz będzie: guitar=obj, amplifier=obj lub pedal=obj
                    }
                    
                    owned, created_gear = OwnedGear.objects.get_or_create(
                        **owned_kwargs,
                        defaults={
                            'nickname': item.get('nick', ''),
                            'is_favorite': random.choice([True, False])
                        }
                    )
                    my_gear_map[item['model']] = owned

            # 4. Tworzenie Setupów
            if 'setups' in user_data:
                for setup_data in user_data['setups']:
                    
                    # Szukamy gatunku
                    g_id = genres_map.get(setup_data['genre'])
                    if not g_id and default_genre:
                        g_id = default_genre.id
                    
                    setup, created_setup = Setup.objects.get_or_create(
                        user=user,
                        name=setup_data['name'],
                        defaults={
                            'description': setup_data['desc'],
                            'genre_id': g_id,
                            'is_public': setup_data.get('public', True),
                            'views': random.randint(0, 1500)
                        }
                    )

                    # Jeśli setup został stworzony teraz (a nie istniał wcześniej), wypełnij go
                    if created_setup:
                        order_idx = 0
                        
                        # LOGIKA BUDOWANIA ŁAŃCUCHA
                        # 1. Najpierw Gitary (bierzemy pierwszą pasującą z ekwipunku)
                        for key, owned in my_gear_map.items():
                            if owned.guitar:
                                SignalChainItem.objects.create(setup=setup, owned_gear=owned, order=order_idx)
                                order_idx += 1
                                break # Tylko jedna gitara na setup
                        
                        # 2. Potem Pedały (Wszystkie jakie user ma w tym seedzie)
                        for key, owned in my_gear_map.items():
                            if owned.pedal:
                                SignalChainItem.objects.create(setup=setup, owned_gear=owned, order=order_idx)
                                order_idx += 1
                        
                        # 3. Na końcu Wzmacniacz
                        for key, owned in my_gear_map.items():
                            if owned.amplifier:
                                SignalChainItem.objects.create(setup=setup, owned_gear=owned, order=order_idx)
                                order_idx += 1
                                break # Tylko jeden wzmacniacz

        self.stdout.write(self.style.SUCCESS('🚀 Big Ass Seed Completed! Community is alive.'))
