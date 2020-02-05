[![Build Status](https://travis-ci.org/StfBlanchet/DansMonPanier_App.svg?branch=master)](https://travis-ci.org/StfBlanchet/DansMonPanier_App)
<hr>

# dansMonPanier

* [Description](#description)
* [Releases](#releases)
* [User journey](#user-journey)
* [Data wrangling](#data-wrangling)
* [Technical requirements](#technical-requirements)
* [Test coverage](#test-coverage)
* [Status](#status)
* [Contributing](#contributing)
* [Authors](#authors)
* [License](#license) 
* [Appendix](#appendix)


## Description

dansMonPanier is a web application based on <a href="https://fr.openfoodfacts.org">Open Food Facts</a> data, aimed at leveraging its value regarding nutritional but also ethical and ecological concerns.

In line with nowadays growing willing to consume in a healthy and responsible way, this app allows the user to identify the products that best meet her requirements.

Intended for French users, the language communication of dansMonPanier is French. 


## Releases

The first release provided a list of products ordered by nutrition grade or by NOVA group, depending on the chosen ranking and the targeted category of food.

Since then, have been added multi-criteria classification and filtering of search results in the database and a feature to allow the user to remove products from her favorites.

Also the top navigation bar was replaced by a side navigation bar so to improve user experience and avoid conflicts with the virtual keyboard on mobiles.


## User journey

### Search & Save

The user enters a food name in the search field (from the home page or from the navbar) and chooses ranking (by nutrition grade or NOVA group) and filtering criteria (e.g. "bio", "fair trade", ...), according to her interest. If there is no corresponding category in the database, a message informs the user. Otherwise, a results page displays 18 products belonging to the targeted category, each being presented with a set of 12 features (e.g. the presence of allergens or palm oil, the origin of the ingredients, whether it is “bio” or not, etc. - see appendix) appearing when they are true or available. A button allows the user to save a product as a favorite. If she is not logged, a message prompts her to do so or to create an account. 

The user can learn more about a product by clicking on the image of the product (which is directly loaded from Open Food Facts database) or on the title of the card. The product page contains 12 criteria accompanied by information such as its nutritional formula per 100 g., composition, packaging, quantity, places of sale … Again, the user can add a product to her favorites if she is already connected. Each time a product is registered, a message confirms the operation.

When a product has already been selected by the user, the button “save” is not anymore active in any page but replaced by the mention “remove from my favorites”, which prevents duplicates. The user can retrieve all its favorites by clicking on the carrot icon in the top navbar (which appears only if the user is logged). If she has not saved any product yet, a message invites her to do so. The favorites page follows the same template as the results page.

### Sign in / up / out

The user accesses the login page by clicking on the user icon in the navbar to register or login, as appropriate. Whether or not she is a new user, she is greeted with a welcome message if all has gone well. Otherwise, an error message is displayed ("Incorrect credentials", "You must provide valid information to register"). When the user logs out, a good bye message appears.


## Data wrangling

Open Food Facts is a food products database made "by everyone, for everyone", which ensures its various and ever growing content. The drawback of this openness is the mixed quality of data. Any project aiming to use them should first carry out a detailed analysis of their overabundant and sometimes redundant facets, with the risk of delivering inaccurate or misleading results.

For this reason, a large part of the effort in building the application has been cleaning and reshaping the data, in order to make them correctly loadable in a postgres database but also readable by a user and actionable.

Two specific modules were built to achieve data wrangling and collection automation:

__cat_builder.py__ gets and stores in a csv file the food categories currently available in OFF database. It includes cleaning tasks such as dropping NaN, duplicated field labels and poor categories (i.e. containing less than 100 products). It also ensures the writing of the banner image paths for every category ;

__food_builder.py__ performs various operations on data to manage their collection and refinement:
<ul>
<li>automate URI generation based on the components of Open Food Facts Read/Search API and the data collected by the cat_loader module. The latter provides the total of products per food category and so enables to determine the number of pages (1000 items per page) to be loaded.</li>
<li>automate sending http requests and filter the data to be collected. Only some specific fields are taken into account (see appendix and details on the API/Read/Product page).</li>
<li>clean and refine data:</li>
<ul>
<li>drop products of which completeness is less than 90%</li>
<li>remove undesired tags that cause the creation of supernumerary lines in the csv file and/or hamper readability</li>
<li>remove duplicate words in textual columns</li>
<li>extract indicators from the fields 'labels', 'ingredients_analysis_tags' and 'nutriments'</li> 
</ul>
</li>
</ul>

Finally, it is built a food database that contains 32 variables including 25 criteria (see appendix) relevant regarding healthy, ethical and ecological concerns. Most of the Boolean variables were not given as such but extracted from text in the field 'labels', ‘ingredients_analysis_tags’ and ‘origins’ and then reshaped. 


## Technical requirements

The app is built with Django framework 2.2.9 and written in Python 3.7.

One can use the package manager [pip](https://pip.pypa.io/en/stable/) to install the whole required libraries.

```bash
pip install -r requirements.txt
```


## Test coverage

<table class="index">
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th class="name left headerSortDown shortkey_n">Module</th>
                <th class="shortkey_s">statements</th>
                <th class="shortkey_m">missing</th>
                <th class="shortkey_x">excluded</th>
                <th class="right shortkey_c">coverage</th>
            </tr>
        </thead>
        <tfoot>
            <tr class="total">
                <td class="name left"><b>Total</b></td>
                <td>424</td>
                <td>26</td>
                <td>0</td>
                <td class="right" data-ratio="398 424"><b>94%</b></td>
            </tr>
        </tfoot>
        <tbody>
            <tr class="file">
                <td class="name left"><a href="#">explore/__init__.py</a></td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="0 0">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/apps.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/forms.py</a></td>
                <td>10</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="10 10">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/migrations/0001_initial.py</a></td>
                <td>7</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="7 7">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/migrations/0002_auto_20200202_1454.py</a></td>
                <td>5</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="5 5">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/migrations/0003_favorite_meal.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/migrations/__init__.py</a></td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="0 0">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/models.py</a></td>
                <td>55</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="55 55">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/process.py</a></td>
                <td>13</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="11 13">85%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/tests.py</a></td>
                <td>186</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="186 186">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/urls.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="#">explore/views.py</a></td>
                <td>138</td>
                <td>24</td>
                <td>0</td>
                <td class="right" data-ratio="114 138">83%</td>
            </tr>
        </tbody>
    </table>
<p>
    <a class="nav" href="https://coverage.readthedocs.io">coverage.py v5.0.3</a>,
    created at 2020-02-05 10:16
</p>


## Status

This project is in progress.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Authors

- Initial work: Stephanie BLANCHET, Data and Application Pythonist.
- Contact: stephanie.blanchet.it@gmail.com


## License

This project is licensed under the MIT License - see [MIT](https://choosealicense.com/licenses/mit/) for details.


## Appendix

#### Fields collected from OFF API: 

<ul>
<li>category</li>
<li>code</li>
<li>name</li>
<li>brands</li>
<li>stores</li>
<li>completeness</li>
<li>origins</li>
<li>ingredients_text</li>
<li>additives</li>
<li>allergens_from_ingredients</li>
<li>quantity</li>
<li>image_url</li>
<li>packaging</li>
<li>labels</li>
<li>ingredients_analysis_tags</li>
<li>nova_group</li>
<li>nutrition_grades</li>
<li>energy_100g (from 'nutriments')</li>
<li>energy_unit (from 'nutriments')</li>
<li>fat (from 'nutriments')</li>
<li>saturated-fat (from 'nutriments')</li>
<li>sugars (from 'nutriments')</li>
<li>salt (from 'nutriments')</li>
<li>proteins (from 'nutriments')</li>
<li>fiber (from 'nutriments')</li>
</ul>

#### Additional data extracted from ‘origins’, ‘ingredients_analysis_tags’ and ‘labels’ fields (fr):

<ul>
<li>Agriculture biologique</li>
<li>Point Vert / Eco-emballages</li>
<li>Certifié FSC</li>
<li>Certifié UTZ (Chocolat)</li>
<li>Sans huile de palme</li>
<li>Fabriqué en France</li>
<li>Ingrédients d'origine française</li>
<li>Commerce équitable</li>
<li>Végétalien</li>
<li>Végétarien</li>
<li>Sans gluten</li>
<li>Garantie IPLC (lait)</li>
</ul>
