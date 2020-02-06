"""
dansMonPanier app
File to run tests.
"""

from explore.views import *
from explore.models import *
from explore.forms import UserForm
from datetime import datetime
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse


class ViewTestNoRedir(TestCase):
    """
    This class performs view tests
    with status code 200 expected
    and pieces of content check
    """

    def test_index(self):
        """
        The user accesses the index page
        and sees the main headline
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Je sais ce que je mange !')

    def test_legal(self):
        """
        The user accesses the legal page
        and sees the main headline
        """
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Directeur de publication')

    def test_signin(self):
        """
        The user accesses the signin page
        and sees the main headline
        """
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Créez votre espace')

    def test_user_login(self):
        """
        The user accesses the signin page
        and sees the main headline
        """
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Accédez à votre espace')


class ViewTestRedir(TestCase):
    """
    This class performs view tests
    with status code 302 expected
    """

    def test_my_profile(self):
        """
        Unauthenticated user can't access
        profile page, hence the redirection
        """
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 302)

    def test_my_favorites(self):
        """
        Unauthenticated user can't access
        favorites page, hence the redirection
        """
        response = self.client.get(reverse('my_favorites'))
        self.assertEqual(response.status_code, 302)

    def test_save_favorites(self):
        """
        Unauthenticated user can't save
        products, hence the redirection
        """
        response = self.client.get(reverse('save_favorites'))
        self.assertEqual(response.status_code, 302)

    def test_remove_favorites(self):
        """
        Unauthenticated user can't remove
        products, hence the redirection
        """
        response = self.client.get(reverse('remove_favorites'))
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
            id=0,
            products=Food.objects.get(pk=0),
            user=User.objects.get(pk=0),
            meal='petit_dejeuner'
        )

    def setUp(self):
        """
        Set working variables
        """
        self.factory = RequestFactory()
        # Authenticated active user
        self.user = User.objects.get(username='testeur_monpanier@gmail.com')
        self.client.login(username='testeur_monpanier@gmail.com', password='!MonP@nier:159357$')
        # New users
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

    """
    Test auth scenarios
    """

    def test_user_login(self):
        """
        The user logs in
        """
        user_is_logged = self.client.login(username='testeur_monpanier@gmail.com', password='!MonP@nier:159357$')
        self.assertTrue(user_is_logged)

    def test_my_profile_auth(self):
        """
        Authenticated user accesses her profile
        which entails a specific context
        (user.username, user.first_name)
        """
        request = self.factory.get(reverse('my_profile'))
        request.user = self.user
        response = my_profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testeur_monpanier@gmail.com')
        self.assertContains(response, 'Testeur@MonPanier')

    def test_item(self):
        """
        The user accesses the page of
        a given product and sees its features
        """
        request = self.factory.get('/item/1/')
        request.user = self.user
        response = item(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Butter Test")
        self.assertContains(response, "Fake Butter Brand")
        self.assertContains(response, "Leclerc")

    def test_my_favorites_auth(self):
        """
        Authenticated user accesses her favorites
        and sees the headline, and the total of
        registered products
        """
        request = self.factory.get(reverse('my_favorites'))
        request.user = self.user
        response = my_favorites(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mes favoris')
        user_favorites = Favorite().ref_list(request)
        self.assertEqual(len(user_favorites), 1)

    def test_save_favorites_auth(self):
        """
        Authenticated user saves a new favorite
        and the total of registered products
        increases (1 -> 2)
        """
        request = self.factory.get(reverse('save_favorites'))
        request.user = self.user
        product = Food.objects.get(pk=1)
        m = 'petit_dejeuner'
        Favorite(id=1, user=request.user, products=product, meal=m).save()
        user_favorites = Favorite().ref_list(request)
        self.assertEqual(len(user_favorites), 2)

    def test_remove_favorites_auth(self):
        """
        Authenticated user saves a new favorite
        and the total of registered products
        decreases (2 -> 1)
        """
        request = self.factory.get(reverse('remove_favorites'))
        request.user = self.user
        Favorite(id=1, user=request.user).delete()
        user_favorites = Favorite().ref_list(request)
        self.assertEqual(len(user_favorites), 1)

    def test_user_logout(self):
        """
        The user logs out and is
        redirected to the index page
        """
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)

    """
    Test signin scenarios
    """

    def test_new_valid_user(self):
        """
        A new valid user signs in and
        the total of users increases
        """
        initial_count = User.objects.count()
        form = UserForm(data=self.new_user)
        self.assertTrue(form.is_valid())
        form.save()
        update_count = User.objects.count()
        self.assertEqual(update_count, initial_count + 1)

        # The new user can log in
        user = User.objects.get(first_name='Je@anP@ul')
        self.assertEqual(user.username, 'jeanpaul-dubuc@gmail.com')
        user_is_logged = self.client.login(username='jeanpaul-dubuc@gmail.com', password='$123a456Cv789p!')
        self.assertTrue(user_is_logged)

        # Expected status response is 200
        response = self.client.post(reverse('user_login'), data=self.new_user)
        self.assertEqual(response.status_code, 200)

    def test_new_bad_user(self):
        """
        A new user tries to register
        using non-compliant entries
        """
        form = UserForm(data=self.bad_user)
        self.assertFalse(form.is_valid())
        user_is_logged = self.client.login(username='toto@gmail.com', password='1234')
        self.assertFalse(user_is_logged)

    """
    Test search results
    """

    def test_results(self):
        """
        The user generates a query that
        combines ranking and filtering
        for an existing category
        """
        uris = ['/results/?q=beurre&ranking=nutrition&filtering=none',
                '/results/?q=beurre&ranking=nova&filtering=none',
                '/results/?q=beurre&ranking=nova&filtering=bio',
                '/results/?q=beurre&ranking=nova&filtering=fair-trade',
                '/results/?q=beurre&ranking=nutrition&filtering=made-in-france',
                '/results/?q=beurre&ranking=nutrition&filtering=palm-oil-free',
                '/results/?q=beurre&ranking=nutrition&filtering=fsc']
        data = Food.objects.filter(category_group__unaccent__contains='Beurre')
        for uri in uris:
            request = self.factory.get(uri)
            request.user = self.user
            response = results(request)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Faites le bon choix !')
            self.assertIs(len(data), 1)

    def test_no_results(self):
        """
        The user generates a query
        for a category that does not
        exist in the db
        """
        request = self.factory.get('/results/?q=chou&ranking=nutrition&filtering=none')
        request.user = self.user
        data = Food.objects.filter(category_group__unaccent__contains='Chou')
        self.assertIs(len(data), 0)

    def test_no_results_long_query(self):
        request = self.factory.get('/results/?q=gateau+au+chocolat&ranking=nutrition&filtering=none')
        request.user = self.user
        data = Food.objects.filter(category_group__unaccent__contains='Pain au chocolat')
        self.assertIs(len(data), 0)

    """
    Test models
    """

    def test_model_str(self):
        """
        Verify model strings
        """
        food = Food(name='Fake Name', stores='Fake stores', category_group='Test group')
        self.assertIs(food.__str__(), 'Test group')
        category = Category(category='Test category')
        self.assertIs(category.__str__(), 'Test category')

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
