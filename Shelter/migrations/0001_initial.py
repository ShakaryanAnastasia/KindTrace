# Generated by Django 3.1 on 2021-04-10 20:30

import Shelter.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('surname', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=200, verbose_name='Электронная почта')),
                ('phoneNum', models.CharField(max_length=17, verbose_name='Номер телефона')),
                ('sex', models.CharField(choices=[('male', 'мужской'), ('female', 'женский')], default='женский', max_length=10, verbose_name='пол')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('phoneNum', models.CharField(blank=True, max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('type', models.CharField(choices=[('Moderator', 'Moderator'), ('Client', 'Client'), ('Owner', 'Owner')], default='Client', max_length=9)),
                ('sex', models.CharField(choices=[('male', 'мужской'), ('female', 'женский')], default='женский', max_length=10, verbose_name='пол')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shelter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shelter.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('body', models.TextField(null=True, verbose_name='Содержание')),
                ('dateCreate', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('dateExpiration', models.DateTimeField(verbose_name='Дата выполнения')),
                ('status', models.CharField(choices=[('free', 'свободная'), ('progress', 'выполняется')], max_length=15, verbose_name='Статус')),
                ('shelter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shelter.shelter')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('sex', models.CharField(choices=[('male', 'мальчик'), ('female', 'девочка')], max_length=10, verbose_name='Пол')),
                ('type', models.CharField(choices=[('cat', 'кошка'), ('dog', 'собака')], max_length=10, verbose_name='Тип')),
                ('color', models.CharField(choices=[('black', 'черный'), ('red', 'рыжий'), ('white', 'белый'), ('grey', 'серый'), ('brown', 'коричневый'), ('striped', 'полосатый'), ('turtle', 'черепаший')], max_length=11, verbose_name='Цвет')),
                ('wool', models.CharField(choices=[('bald', 'лысый'), ('longhaired', 'длинношерстный'), ('shorthaired', 'короткошерстный')], max_length=15, verbose_name='Шерсть')),
                ('character', models.CharField(choices=[('Sanguine', 'Сангвиник'), ('Melancholic', 'Меланхолик'), ('Choleric', 'Холерик'), ('Phlegmatic', 'Флегматик')], max_length=11, verbose_name='Характер')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Shelter.profile', verbose_name='Владелец')),
                ('shelter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shelter.shelter', verbose_name='Приют')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('anons', models.CharField(default='', max_length=200, null=True, verbose_name='Анонс')),
                ('body', models.TextField(null=True, verbose_name='Содержание')),
                ('shelter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shelter.shelter')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/profile_image.jpg', upload_to=Shelter.models.user_directory_path_image, verbose_name='Изображения')),
                ('news', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Shelter.news')),
                ('pet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Shelter.pet')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Shelter.task')),
            ],
            options={
                'verbose_name': 'Изображения',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default='files/profile_image.jpg', upload_to=Shelter.models.user_directory_path, verbose_name='Файлы')),
                ('o_application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Shelter.ownerapplication')),
            ],
            options={
                'verbose_name': 'Файлы',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заговолок')),
                ('body', models.TextField(verbose_name='Комментарий')),
                ('dateCreate', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
                ('news', models.ForeignKey(default='New', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Shelter.news', verbose_name='Новости')),
                ('pet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Shelter.pet', verbose_name='Питомец')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Shelter.task', verbose_name='Задача')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shelter.profile', verbose_name='Пользователь')),
            ],
        ),
    ]
