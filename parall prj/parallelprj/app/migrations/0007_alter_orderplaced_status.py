# Generated by Django 5.0.4 on 2024-05-05 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_orderplaced_status_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Packed', 'Packed'), ('Cancel', 'Cancel'), ('On The Way', 'On The Way')], default='Pending', max_length=50),
        ),
    ]
