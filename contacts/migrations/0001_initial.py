# Generated by Django 3.1 on 2021-02-02 12:39

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallbackRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, verbose_name='Имя')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время подачи заявки')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон')),
                ('comment', models.TextField(blank=True, max_length=500, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Запрос на обратный звонок',
                'verbose_name_plural': 'Запросы на обратный звонок',
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeedbackRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, verbose_name='Имя')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время подачи заявки')),
                ('msg_type', models.CharField(choices=[('ADV', 'Предложения по улучшению работы сайта'), ('BIZ', 'Вопросы и предложения о сотрудничестве'), ('OTR', 'Другое')], max_length=3, verbose_name='Тип сообщения')),
                ('msg', models.TextField(max_length=2500, verbose_name='Сообщение')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Запрос на обратный Email',
                'verbose_name_plural': 'Запросы на обратный Email',
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
    ]
