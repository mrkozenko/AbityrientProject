# Generated by Django 5.0.3 on 2024-03-15 22:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0008_alter_result_unique_together'),
        ('TGBot', '0013_alter_admins_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.quiz', verbose_name='Вікторина'),
        ),
        migrations.AlterField(
            model_name='result',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='TGBot.tguser', verbose_name='Абітурієнт'),
        ),
    ]
