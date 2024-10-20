# Generated by Django 5.1.1 on 2024-10-13 15:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LesProduits', '0002_productitem_quantité'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date création')),
                ('status', models.SmallIntegerField(choices=[(0, 'En preparation'), (1, 'Passée'), (2, 'Reçue')], default=0)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Commande',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Fournisseur',
            },
        ),
        migrations.RenameField(
            model_name='productitem',
            old_name='quantité',
            new_name='quantity',
        ),
        migrations.CreateModel(
            name='OrderProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantité')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LesProduits.order')),
                ('productItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LesProduits.productitem')),
            ],
            options={
                'verbose_name': 'Produit commandé',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LesProduits.provider'),
        ),
        migrations.CreateModel(
            name='ProviderProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Prix unitaire HT')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LesProduits.product')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LesProduits.provider')),
            ],
            options={
                'verbose_name': "Prix d'achat",
            },
        ),
    ]
