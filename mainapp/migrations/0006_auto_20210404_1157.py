# Generated by Django 3.1 on 2021-04-04 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20210404_1128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartproduct',
            old_name='amount',
            new_name='qty',
        ),
    ]
