# Generated by Django 3.2.4 on 2021-06-16 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_collection_title'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]
