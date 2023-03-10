# Generated by Django 3.2.16 on 2023-02-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_user_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('unknown', 'unknown')], default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='vehicle_type',
            field=models.CharField(choices=[('SUV', 'SUV'), ('Sports Car', 'Sports Car'), ('Sedan', 'Sedan')], default='Sedan', max_length=256),
        ),
    ]
