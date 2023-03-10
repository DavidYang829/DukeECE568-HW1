# Generated by Django 4.1.6 on 2023-02-07 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_auto_20230205_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('male', 'male'), ('unknown', 'unknown'), ('female', 'female')], default='unknown', max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='vehicle_type',
            field=models.CharField(choices=[('SUV', 'SUV'), ('Sedan', 'Sedan'), ('Sports Car', 'Sports Car')], default='Sedan', max_length=64),
        ),
    ]
