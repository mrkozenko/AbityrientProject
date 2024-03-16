# Generated by Django 5.0.3 on 2024-03-10 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGBot', '0003_slider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(verbose_name='Пріорітет відображення')),
                ('image', models.ImageField(upload_to='specialty/', verbose_name='Рисунок')),
                ('title', models.CharField(max_length=200, verbose_name='Підпис спеціальності')),
            ],
            options={
                'verbose_name': 'спеціальність',
                'verbose_name_plural': 'спеціальності',
            },
        ),
    ]
