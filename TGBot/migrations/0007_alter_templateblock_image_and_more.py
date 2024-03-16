# Generated by Django 5.0.3 on 2024-03-10 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGBot', '0006_alter_templateblock_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateblock',
            name='image',
            field=models.ImageField(null=True, upload_to='tmp_blocks/', verbose_name='Рисунок'),
        ),
        migrations.AlterField(
            model_name='templateblock',
            name='template_type',
            field=models.CharField(choices=[('START', 'СТАРТ'), ('CONTACTS', 'КОНТАКТИ'), ('SPECIALTY', 'СПЕЦІАЛЬНОСТІ'), ('QUIZ', 'ВІКТОРИНИ')], max_length=20, verbose_name='Тип шаблону'),
        ),
    ]