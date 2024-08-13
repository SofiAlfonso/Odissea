# Generated by Django 4.0.4 on 2024-08-13 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0002_register_origin_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='register',
            name='username',
            field=models.CharField(help_text='Ingrese un nombre de usuario', max_length=100, unique=True),
        ),
    ]
