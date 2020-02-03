from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_group', models.CharField(max_length=800)),
                ('created', models.DateField()),
                ('code', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=350, null=True)),
                ('brands', models.CharField(max_length=250, null=True)),
                ('stores', models.CharField(max_length=800, null=True)),
                ('bio', models.CharField(max_length=5, null=True)),
                ('eco_packaging', models.CharField(max_length=5, null=True)),
                ('fsc', models.CharField(max_length=5, null=True)),
                ('utz', models.CharField(max_length=5, null=True)),
                ('palm_oil_free', models.CharField(max_length=5, null=True)),
                ('made_in_france', models.CharField(max_length=5, null=True)),
                ('ingredients_text', models.TextField(max_length=800, null=True)),
                ('additives', models.IntegerField(null=True)),
                ('allergens_from_ingredients', models.CharField(max_length=800, null=True)),
                ('quantity', models.CharField(max_length=250, null=True)),
                ('image_url', models.URLField(max_length=450, null=True)),
                ('packaging', models.CharField(max_length=250, null=True)),
                ('french_ingredients', models.CharField(max_length=5, null=True)),
                ('fair_trade', models.CharField(max_length=5, null=True)),
                ('vegan', models.CharField(max_length=5, null=True)),
                ('vegetarian', models.CharField(max_length=5, null=True)),
                ('gluten_free', models.CharField(max_length=5, null=True)),
                ('iplc', models.CharField(max_length=5, null=True)),
                ('nova', models.IntegerField(null=True)),
                ('nutrition_grade', models.CharField(max_length=1, null=True)),
                ('energy', models.FloatField(null=True)),
                ('energy_unit', models.CharField(max_length=5, null=True)),
                ('fat', models.FloatField(null=True)),
                ('saturated_fat', models.FloatField(null=True)),
                ('sugars', models.FloatField(null=True)),
                ('salt', models.FloatField(null=True)),
                ('fiber', models.FloatField(null=True)),
                ('proteins', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explore.Food')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
