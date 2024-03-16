# Generated by Django 5.0.3 on 2024-03-15 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGBot', '0011_alter_templateblock_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='TGBot.tguser', verbose_name='Адміністратор')),
            ],
            options={
                'verbose_name': 'адміністратор',
                'verbose_name_plural': 'адміністратори',
            },
        ),
    ]