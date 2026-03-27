from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from equipment.models import OwnedGear, Guitar, Amplifier, Brand

User = get_user_model()


class EquipmentViewTests(TestCase):

    def setUp(self):
        # 1. Create user
        self.user = User.objects.create_user(username="rockstar", password="password")
        self.client.login(username="rockstar", password="password")

        # 2. Create brands
        fender = Brand.objects.create(name="Fender")
        marshall = Brand.objects.create(name="Marshall")

        # 3. Create gear
        strat = Guitar.objects.create(
            name="Stratocaster", brand=fender, guitar_type="STRAT"
        )
        jcm800 = Amplifier.objects.create(
            name="JCM800", brand=marshall, amp_type="TUBE", wattage=100
        )

        # 4. Add to OwnedGear
        self.g1 = OwnedGear.objects.create(
            user=self.user, guitar=strat, nickname="Moja Strzała", is_favorite=True
        )
        self.a1 = OwnedGear.objects.create(
            user=self.user, amplifier=jcm800, nickname="Głośny Potwór"
        )

    def test_list_view_displays_all_gear_by_default(self):
        response = self.client.get(reverse("equipment:list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["gear_list"]), 2)

    def test_list_view_filters_by_type_guitar(self):
        """Does ?type=guitar show only guitars"""
        response = self.client.get(reverse("equipment:list"), {"type": "guitar"})

        self.assertEqual(response.status_code, 200)
        gear_list = response.context["gear_list"]

        self.assertEqual(len(gear_list), 1)
        self.assertEqual(gear_list[0], self.g1)  # it has to be guitar
        self.assertIsNone(gear_list[0].amplifier)  # check if its not amplifier

    def test_list_view_search_query(self):
        # /equipment/?q=Potwór
        response = self.client.get(reverse("equipment:list"), {"q": "Potwór"})

        self.assertEqual(response.status_code, 200)
        gear_list = response.context["gear_list"]

        self.assertEqual(len(gear_list), 1)
        self.assertEqual(gear_list[0].nickname, "Głośny Potwór")

    def test_list_view_favorites_only(self):
        # ?favorites=true?
        response = self.client.get(reverse("equipment:list"), {"favorites": "true"})

        self.assertEqual(len(response.context["gear_list"]), 1)
        self.assertEqual(response.context["gear_list"][0], self.g1)

    def test_statistics_in_context(self):
        response = self.client.get(reverse("equipment:list"))

        stats = response.context["gear_stats"]
        self.assertEqual(stats["guitars"], 1)
        self.assertEqual(stats["amplifiers"], 1)
