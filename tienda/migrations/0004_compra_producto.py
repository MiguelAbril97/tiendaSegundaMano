# Generated by Django 5.1.2 on 2024-10-29 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0003_alter_producto_categorias'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='producto',
            field=models.ManyToManyField(related_name='producto_compra', through='tienda.CompraProducto', to='tienda.producto'),
        ),
    ]
