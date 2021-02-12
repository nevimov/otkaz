# Generated by Django 3.1 on 2021-02-02 12:39

import ckeditor.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('single', 'Одностворчатое окно'), ('double', 'Двухстворчатое окно'), ('triple', 'Трехстворчатое окно'), ('single_transom', 'Одностворчатое окно с фрамугой'), ('double_transom', 'Двухстворчатое окно с фрамугой'), ('triple_transom', 'Трехстворчатое окно с фрамугой')], max_length=20, verbose_name='Тип конструкции')),
                ('width', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(200), django.core.validators.MaxValueValidator(5000)], verbose_name='Ширина, мм')),
                ('height', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(200), django.core.validators.MaxValueValidator(5000)], verbose_name='Высота, мм')),
                ('color', models.CharField(choices=[('white', 'Белый'), ('wood_dark', 'Темное дерево '), ('wood_light', 'Светлое дерево'), ('other', 'Другой')], default='white', max_length=20, verbose_name='Цвет')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('description', ckeditor.fields.RichTextField(blank=True, verbose_name='Описание')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('datetime_changed', models.DateTimeField(auto_now=True, verbose_name='Время последнего редактирования')),
            ],
            options={
                'verbose_name': 'Окно',
                'verbose_name_plural': 'Окна',
            },
        ),
    ]
