# Generated by Django 3.1 on 2021-04-14 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shelter', '0004_auto_20210413_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='color',
            field=models.CharField(choices=[('black', 'черный'), ('red', 'рыжий'), ('white', 'белый'), ('grey', 'серый'), ('brown', 'коричневый'), ('striped', 'полосатый'), ('turtle', 'черепаховый'), ('tricolor', 'трехцветный'), ('spotted', 'пятнистый'), ('blackwhite', 'черно-белый')], max_length=11, verbose_name='Цвет'),
        ),
    ]
