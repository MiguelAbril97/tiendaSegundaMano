# Generated by Django 5.1.2 on 2024-10-26 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='historial',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='reporte',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='descuentoTotal',
        ),
        migrations.RemoveField(
            model_name='valoracion',
            name='comentarioVerificado',
        ),
        migrations.AlterField(
            model_name='producto',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_vendedor', to='tienda.usuario'),
        ),
    ]
