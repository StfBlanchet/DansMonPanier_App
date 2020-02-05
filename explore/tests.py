"""
dansMonPanier app
File to run tests.
"""


from .views import *
from .models import *
from .forms import UserForm
from datetime import datetime
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse


class SimpleViewTest(TestCase):
    """
    This class performs simple view tests
    through status code and pieces of content
    """
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Je sais ce que je mange !")

    def test_legal(self):
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Directeur de publication")

    def test_signin(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Créez votre espace")

    def test_user_login(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Accédez à votre espace")

    def test_user_logout(self):
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)

    def test_my_favorites(self):
        response = self.client.get(reverse('my_favorites'))
        self.assertEqual(response.status_code, 302)

    def test_save_favorites(self):
        response = self.client.get(reverse('save_favorites'))
        self.assertEqual(response.status_code, 302)

    def test_remove_favorites(self):
        response = self.client.get(reverse('remove_favorites'))
        self.assertEqual(response.status_code, 302)

    def test_my_profile(self):
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 302)


class AppDataTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        This method creates temporary data
        for the needs of tests.
        """
        Category.objects.create(
            id=0,
            category='Pains'
        )

        Category.objects.create(
            id=1,
            category='Beurres'
        )

        Category.objects.create(
            id=2,
            category='Choux'
        )

        Food.objects.create(
            id=0,
            category_group='Pains,Biscottes, Céréales',
            created=datetime.now(),
            code='0000000000000',
            name='Bread Test',
            brands='Fake Bread Brand',
            stores='Carrefour',
            bio=True,
            eco_packaging=True,
            fsc=True,
            utz=True,
            palm_oil_free=True,
            made_in_france=True,
            ingredients_text='blé, eau, sel...',
            additives=3,
            allergens_from_ingredients='',
            quantity=4,
            image_url='https://foo-foo.bar',
            packaging='papier',
            french_ingredients=True,
            fair_trade=True,
            vegan=True,
            vegetarian=True,
            gluten_free=True,
            iplc=True,
            nova=3,
            nutrition_grade='b',
            energy=258,
            energy_unit='kcal',
            fat=2.0,
            saturated_fat=0.1,
            sugars=20.0,
            salt=2.0,
            fiber=10.0,
            proteins=66.0
            )

        Food.objects.create(
            id=1,
            category_group='Beurres, Matières grasses',
            created=datetime.now(),
            code='0000000000000',
            name='Butter Test',
            brands='Fake Butter Brand',
            stores='Leclerc',
            bio=True,
            eco_packaging=True,
            fsc=True,
            utz=True,
            palm_oil_free=True,
            made_in_france=True,
            ingredients_text='lait, eau, sel...',
            additives=3,
            allergens_from_ingredients='',
            quantity=4,
            image_url='https://foo-foo.bar',
            packaging='papier',
            french_ingredients=True,
            fair_trade=True,
            vegan=True,
            vegetarian=True,
            gluten_free=True,
            iplc=True,
            nova=2,
            nutrition_grade='d',
            energy=788,
            energy_unit='kcal',
            fat=70.0,
            saturated_fat=35.0,
            sugars=1.0,
            salt=2.0,
            fiber=1.0,
            proteins=26.0
            )

        User.objects.create_user(
            id=0,
            username='testeur_monpanier@gmail.com',
            email='testeur_monpanier@gmail.com',
            password='!MonP@nier:159357$',
            first_name='Testeur@MonPanier')

        Favorite.objects.create(
            products=Food.objects.get(pk=0),
            user=User.objects.get(pk=0)
        )

    def setUp(self):
        """
        Set working variables
        """
        self.factory = RequestFactory()
        self.user = User.objects.get(username='testeur_monpanier@gmail.com')
        self.new_user = {
            'email': 'jeanpaul-dubuc@gmail.com',
            'username': 'jeanpaul-dubuc@gmail.com',
            'password1': '$123a456Cv789p!',
            'password2': '$123a456Cv789p!',
            'first_name': 'Je@anP@ul'
        }
        self.bad_user = {
            'email': 'toto@gmail.com',
            'username': 'toto@gmail.com',
            'password1': '1234',
            'password2': '1234',
            'first_name': 'Toto'
        }

    def test_food_str(self):
        food = Food(name="Fake Name", stores="Fake stores", category_group="Test")
        self.assertIs(food.__str__(), "Test")

    def test_cat_str(self):
        category = Category(category="Test")
        self.assertIs(category.__str__(), "Test")

    def test_item_count(self):
        """
        Verify the count of items
        """
        self.assertEqual(Food.objects.count(), 2)

    def test_item_name(self):
        """
        Verify that a new item was created
        """
        self.assertTrue(Food.objects.filter(name='Bread Test').exists())

    def test_item_nova(self):
        """
        Verify the value of a specific feature
        """
        product = Food.objects.get(name='Butter Test')
        self.assertIs(product.nova, 2)

    def test_item(self):
        """
        Test item view regarding
        status and returned data
        with auth user
        """
        request = self.factory.get('/item/1/')
        request.user = self.user
        response = item(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Butter Test")
        self.assertContains(response, "Fake Butter Brand")
        self.assertContains(response, "Leclerc")
        user_favorites = Favorite().ref_list(request)
        self.assertEqual(len(user_favorites), 1)

    def test_new_user_1(self):
        """
        Test signin
        for a valid user
        """
        response = self.client.post(reverse('signin'), data=self.new_user)
        self.assertEqual(response.status_code, 302)

    def test_new_user_2(self):
        """
        Test signin form and login
        for a valid user
        """
        initial_count = User.objects.count()

        form = UserForm(data=self.new_user)
        self.assertTrue(form.is_valid())
        form.save()

        update_count = User.objects.count()
        self.assertEqual(update_count, initial_count + 1)

        user = User.objects.get(first_name='Je@anP@ul')
        self.assertEqual(user.username, 'jeanpaul-dubuc@gmail.com')

        user_is_logged = self.client.login(username='jeanpaul-dubuc@gmail.com', password='$123a456Cv789p!')
        self.assertTrue(user_is_logged)

    def test_auth_nok(self):
        """
        Test signin form and login
        for a not valid user
        """
        form = UserForm(data=self.bad_user)
        self.assertFalse(form.is_valid())

        user_is_logged = self.client.login(username='toto@gmail.com', password='1234')
        self.assertFalse(user_is_logged)

    def test_auth_user_ok(self):
        """
        Test login
        for a valid user
        """
        response = self.client.post(reverse('user_login'), data=self.new_user)
        self.assertEqual(response.status_code, 200)

    def test_my_profile_auth(self):
        """
        Test the access to the profile page
        by an auth user and
        verify returned data
        """
        request = self.factory.get(reverse('my_profile'))
        request.user = self.user
        response = my_profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testeur_monpanier@gmail.com")

    def test_checking_user_favorites(self):
        """
        Check favorite list content
        """
        request = self.factory.get(reverse('my_favorites'))
        request.user = self.user
        favorites = Food.objects.filter(favorite__user=request.user)
        response = my_favorites(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(len(favorites), 0)

    def test_save_favorites_auth(self):
        """
        Test save_favorites
        response
        """
        product = Food.objects.get(pk=1)
        response = self.client.post(reverse('save_favorites'), {'products': product, 'user': self.user})
        self.assertEqual(response.status_code, 302)

    def test_favorites_count(self):
        """
        Test favorites count
        is incremented when a
        product was added
        """
        request = self.factory.get(reverse('save_favorites'))
        request.user = self.user
        initial_count = Favorite.objects.count()
        new = Food.objects.get(pk=1)
        Favorite(products=new, user=request.user).save()
        update_count = Favorite.objects.count()
        self.assertEqual(update_count, initial_count + 1)

    def test_remove_favorites_auth(self):
        request = self.factory.get(reverse('my_favorites'))
        request.user = self.user
        favorites = Food.objects.filter(favorite__user=request.user)
        Favorite.objects.filter(Q(products=1) & Q(user=request.user)).delete()
        self.assertIs(len(favorites), 1)

    def test_results_nutrition(self):
        request = self.factory.get('/results/?q=beurre&ranking=nutrition&filtering=none')
        request.user = self.user
        response = results(request)
        self.assertEqual(response.status_code, 200)

    def test_results_nova(self):
        request = self.factory.get('/results/?q=beurre&ranking=nova&filtering=none')
        data = Food.objects.filter(category_group__unaccent__contains='Beurre')
        request.user = self.user
        response = results(request)
        self.assertEqual(response.status_code, 200)
        self.assertIs(len(data), 1)

    def test_results_nova_bio(self):
        request = self.factory.get('/results/?q=beurre&ranking=nova&filtering=bio')
        data = Food.objects.filter(category_group__unaccent__contains='Beurre')
        request.user = self.user
        response = results(request)
        self.assertEqual(response.status_code, 200)
        self.assertIs(len(data), 1)

    def test_results_nova_fair(self):
        request = self.factory.get('/results/?q=pain&ranking=nova&filtering=fair-trade')
        data = Food.objects.filter(category_group__unaccent__contains='Pain')
        request.user = self.user
        response = results(request)
        self.assertEqual(response.status_code, 200)
        self.assertIs(len(data), 1)

    def test_results_nutrition_france(self):
        request = self.factory.get('/results/?q=pain&ranking=nutrition&filtering=made-in-france')
        data = Food.objects.filter(category_group__unaccent__icontains='Pain')
        request.user = self.user
        response = results(request)
        self.assertEqual(response.status_code, 200)
        self.assertIs(len(data), 1)

    def test_results_nutrition_palm(self):
        request = self.factory.get('/results/?q=pain&ranking=nutrition&filtering=palm-oil-free')
        data = Food.objects.filter(category_group__unaccent__icontains='Pain')
        request.user = self.user
        response = results(request)
        self.assertEqual(response.status_code, 200)
        self.assertIs(len(data), 1)

    def test_results_nutrition_fsc(self):
        request = self.factory.get('/results/?q=pain&ranking=nutrition&filtering=fsc')
        data = Food.objects.filter(category_group__unaccent__icontains='Pain')
        request.user = self.user
        response = results(request)
        self.assertEqual(response.status_code, 200)
        self.assertIs(len(data), 1)

    def test_results_not_in_cat_1(self):
        request = self.factory.get('/results/?q=chou&ranking=nutrition&filtering=none')
        request.user = self.user
        data = Food.objects.filter(category_group__unaccent__icontains='Chou')
        self.assertIs(len(data), 0)

    def test_results_not_in_cat_2(self):
        request = self.factory.get('/results/?q=gateau+au+chocolat&ranking=nutrition&filtering=none')
        request.user = self.user
        data = Food.objects.filter(category_group__unaccent__icontains='Gateau au chocolat')
        self.assertIs(len(data), 0)
