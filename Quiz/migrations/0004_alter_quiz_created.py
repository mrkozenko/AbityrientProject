# Generated by Django 5.0.3 on 2024-03-07 10:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0003_alter_quiz_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='created',
            field=models.DateField(auto_created=True, default=datetime.datetime(2024, 3, 7, 12, 56, 38, 893689), verbose_name='Час створення'),
        ),
    ]