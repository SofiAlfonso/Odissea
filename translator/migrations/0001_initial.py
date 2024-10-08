# Generated by Django 4.0.4 on 2024-08-12 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('name', models.CharField(help_text='Ingrese su nombre completo', max_length=100)),
                ('email', models.EmailField(help_text='Ingrese su correo electrónico', max_length=254)),
                ('username', models.CharField(help_text='Ingrese un nombre de usuario', max_length=150, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(help_text='Ingrese su contraseña', max_length=128)),
                ('origin_country', models.CharField(choices=[('CO', 'Colombia'), ('PA', 'Panamá'), ('MX', 'México'), ('US', 'Estados Unidos'), ('CA', 'Canadá')], default='CO', max_length=2)),
            ],
        ),
    ]
