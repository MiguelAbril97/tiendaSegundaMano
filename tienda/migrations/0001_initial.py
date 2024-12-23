# Generated by Django 5.1.2 on 2024-10-24 08:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=50)),
                ('existecias', models.IntegerField()),
                ('destacada', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_compra', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descuentoTotal', models.FloatField(blank=True)),
                ('garantia', models.CharField(choices=[('UNO', 'Un año'), ('DOS', 'Dos años')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('CN', 'Como nuevo'), ('U', 'Usado'), ('MU', 'Muy usado')], max_length=2)),
                ('fecha_de_publicacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('correo_electronico', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=9)),
                ('direccion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Muebles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=30)),
                ('ancho', models.FloatField()),
                ('alto', models.FloatField()),
                ('profundidad', models.FloatField()),
                ('peso', models.IntegerField()),
                ('producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tienda.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Consolas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=20)),
                ('memoria', models.CharField(max_length=20)),
                ('producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tienda.producto')),
            ],
        ),
        migrations.CreateModel(
            name='CompraProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=7)),
                ('subtotal', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('descuento', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.compra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Calzado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talla', models.CharField(max_length=2)),
                ('marca', models.CharField(choices=[('NIKE', 'Nike'), ('ADID', 'Adidas'), ('PUMA', 'Puma'), ('RBK', 'Reebok'), ('NB', 'New Balance'), ('CLRK', 'Clarks'), ('GUCCI', 'Gucci')], max_length=5)),
                ('color', models.CharField(blank=True, max_length=20)),
                ('material', models.CharField(max_length=30)),
                ('producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tienda.producto')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.categoria')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.producto')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='categorias',
            field=models.ManyToManyField(through='tienda.ProductoCategoria', to='tienda.categoria'),
        ),
        migrations.AddField(
            model_name='producto',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.usuario'),
        ),
        migrations.CreateModel(
            name='Envio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.TextField()),
                ('fecha_envio', models.DateTimeField()),
                ('fecha_recepcion', models.DateTimeField()),
                ('recepcionEstimada', models.DateTimeField()),
                ('compra', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tienda.compra')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='comprador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras_comprador', to='tienda.usuario'),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateTimeField(blank=True)),
                ('historial', models.TextField()),
                ('reporte', models.BooleanField(default=False)),
                ('usuario1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_usuario1', to='tienda.usuario')),
                ('usuario2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_usuario2', to='tienda.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField()),
                ('comentario', models.TextField(blank=True)),
                ('fecha_valoracion', models.DateTimeField(default=django.utils.timezone.now)),
                ('comentarioVerificado', models.BooleanField(default=False)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.compra')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tienda.usuario')),
            ],
        ),
    ]
