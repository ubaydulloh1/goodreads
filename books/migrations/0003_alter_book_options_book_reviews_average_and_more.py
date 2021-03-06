# Generated by Django 4.0 on 2022-04-16 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ('reviews_average', 'reviews_count')},
        ),
        migrations.AddField(
            model_name='book',
            name='reviews_average',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='reviews_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
