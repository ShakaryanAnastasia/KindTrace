# Generated by Django 3.1 on 2021-05-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shelter', '0008_order_dateviewing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='dateViewing',
            field=models.DateField(blank=True, null=True, verbose_name='Дата просмотра животного'),
        ),
    ]
