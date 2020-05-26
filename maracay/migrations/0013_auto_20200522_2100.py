# Generated by Django 2.2.10 on 2020-05-22 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maracay', '0012_dolarbolivar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dolarbolivar',
            name='bolivar',
            field=models.DecimalField(decimal_places=2, help_text='Cambia el dolar al precio actual y todos los precios de los productos en bolivares cambiaran al instante', max_digits=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='cant',
            field=models.PositiveSmallIntegerField(default=1, help_text='Cantidad disponible el producto en el almacen'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Viveres'), (2, 'Frigorifico'), (3, 'Enlatados'), (4, 'Charcuteria'), (5, 'Carnes')], help_text='Seleccione una categoria del producto'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(help_text='Descripcion del producto', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Alias de la imagen', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_image',
            field=models.CharField(help_text='Debes colocar el nombre de la imagen con la extension por ejemplo: imagen.png ', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Precio en Dolares', max_digits=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='pricebs',
            field=models.DecimalField(decimal_places=2, default=1, help_text='Precion en Bolivares', max_digits=30),
        ),
    ]