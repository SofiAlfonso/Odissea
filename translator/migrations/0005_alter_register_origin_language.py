# Generated by Django 4.0.4 on 2024-08-26 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0004_alter_register_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='origin_language',
            field=models.CharField(choices=[('es', 'Español'), ('en', 'Inglés'), ('fr', 'Frances')], default='en', max_length=2),
        ),
    ]
