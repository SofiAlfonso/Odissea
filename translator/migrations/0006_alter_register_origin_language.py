# Generated by Django 4.0.4 on 2024-08-26 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0005_alter_register_origin_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='origin_language',
            field=models.CharField(choices=[('ES', 'Español'), ('EN', 'Inglés'), ('FR', 'Frances')], default='EN', max_length=2),
        ),
    ]
