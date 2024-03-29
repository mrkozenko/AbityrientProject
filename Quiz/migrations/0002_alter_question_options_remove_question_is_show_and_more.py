# Generated by Django 5.0.3 on 2024-03-07 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Питання', 'verbose_name_plural': 'Питання'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_show',
        ),
        migrations.AddField(
            model_name='quiz',
            name='is_show',
            field=models.BooleanField(default=True, verbose_name='Відображати'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='Час створення'),
        ),
    ]
