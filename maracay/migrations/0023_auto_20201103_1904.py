# Generated by Django 3.1 on 2020-11-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maracay', '0022_auto_20201009_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Viveres'), (2, 'Frigorifico'), (3, 'Enlatados'), (4, 'Charcuteria'), (5, 'Carnes'), (6, 'Personales'), (7, 'Chucherias')], help_text='Seleccione una categoria del producto'),
        ),
    ]
