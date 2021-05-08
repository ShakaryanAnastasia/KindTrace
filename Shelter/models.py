from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class OwnerApplication(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    email = models.EmailField(max_length=200, verbose_name='Электронная почта')
    phoneNum = models.CharField(max_length=17, verbose_name='Номер телефона')
    SEX_CHOICES = (
        ('male', "мужской"),
        ('female', "женский"),
    )
    sex = models.CharField(max_length=10, verbose_name="пол", choices=SEX_CHOICES, default='женский')
    title_shelter = models.CharField(max_length=200, verbose_name='Название приюта', default='')
    address_shelter = models.CharField(max_length=200, verbose_name='Адрес приюта', default='')
    description_shelter = models.TextField(default='', blank=True, verbose_name='Описание приюта')
    STATUS_CHOICES = (
        ('accepted', "принята"),
        ('sent', "отправлена"),
    )
    status = models.CharField(max_length=15, verbose_name="Статус", choices=STATUS_CHOICES, default="sent")

    def __str__(self):
        return " ".join([self.name, self.surname])


def user_directory_path(instance, filename):
    return f'static/files/{instance.id}_{"".join(filename.split(".")[:-1])}.{filename.split(".")[-1]}'


class Files(models.Model):
    file = models.FileField(upload_to=user_directory_path, default='files/profile_image.jpg', verbose_name='Файлы')
    o_application = models.ForeignKey(OwnerApplication, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.file.name

    def get_name(self):
        return self.file.name.split("/")[-1].split("_")[-1]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    phoneNum = models.CharField(validators=[phone_regex], max_length=12, blank=True)

    class Type(models.TextChoices):
        MODERATOR = 'Moderator'
        CLIENT = 'Client'
        OWNER = 'Owner'

    type = models.CharField(
        max_length=9,
        choices=Type.choices,
        default='Client'
    )

    SEX_CHOICES = (
        ('male', "мужской"),
        ('female', "женский"),
    )
    sex = models.CharField(max_length=10, verbose_name="пол", choices=SEX_CHOICES, default='женский')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Shelter(models.Model):
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    description = models.TextField(default='', blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return " ".join([self.title])


class Pet(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=200)
    age = models.IntegerField(verbose_name="Возраст")
    SEX_CHOICES = (
        ('male', "мальчик"),
        ('female', "девочка"),
    )
    sex = models.CharField(max_length=10, verbose_name="Пол", choices=SEX_CHOICES)

    TYPE_CHOICES = (
        ('cat', "кошка"),
        ('dog', "собака"),
    )
    type = models.CharField(max_length=10, verbose_name="Тип", choices=TYPE_CHOICES)

    COLOR_CHOICES = (
        ('black', "черный"),
        ('red', "рыжий"),
        ('white', "белый"),
        ('grey', "серый"),
        ('brown', "коричневый"),
        ('striped', "полосатый"),
        ('turtle', "черепаховый"),
        ('tricolor', "трехцветный"),
        ('spotted', 'пятнистый'),
        ('blackwhite', "черно-белый")
    )
    color = models.CharField(max_length=11, verbose_name="Цвет", choices=COLOR_CHOICES)

    WOOL_CHOICES = (
        ('bald', "лысый"),
        ('longhaired', "длинношерстный"),
        ('shorthaired', "короткошерстный"),
    )
    wool = models.CharField(max_length=15, verbose_name="Шерсть", choices=WOOL_CHOICES)

    CHARACTER_CHOICES = (
        ('Sanguine', "Сангвиник"),
        ('Melancholic', "Меланхолик"),
        ('Choleric', "Холерик"),
        ('Phlegmatic', "Флегматик"),
    )
    character = models.CharField(max_length=11, verbose_name="Характер", choices=CHARACTER_CHOICES)

    objects = models.Manager()

    description = models.TextField(default='', verbose_name="Описание", blank=True)
    shelter = models.ForeignKey(Shelter, verbose_name="Приют", on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Владелец", blank=True, null=True)

    def __str__(self):
        return " ".join([self.name])

    def get_url(self):
        return reverse('post_detail',
                       args=[self.id])


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    anons = models.CharField(max_length=200, default="", null=True, verbose_name="Анонс")
    body = models.TextField(null=True, verbose_name="Содержание")
    objects = models.Manager()
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    def str(self):
        return " ".join([self.title])

    def got_url(self):
        return reverse('news_detail',
                       args=[self.id])


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    body = models.TextField(null=True, verbose_name="Содержание")
    dateCreate = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    dateExpiration = models.DateTimeField(verbose_name="Дата выполнения")
    objects = models.Manager()
    STATUS_CHOICES = (
        ('free', "свободная"),
        ('progress', "выполняется"),
    )
    status = models.CharField(max_length=15, verbose_name="Статус", choices=STATUS_CHOICES)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)

    def str(self):
        return " ".join([self.title])

    def get_url(self):
        return reverse('task_detail',
                       args=[self.id])


class Comment(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заговолок")
    body = models.TextField(verbose_name="Комментарий")
    dateCreate = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Пользователь")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="Питомец", related_name='comments', null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name="Новости", related_name='comments', null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Задача", related_name='comments', null=True)


def user_directory_path_image(instance, filename):
    return f'static/images/{instance.id}_{"".join(filename.split(".")[:-1])}.{filename.split(".")[-1]}'


class Image(models.Model):
    image = models.ImageField(upload_to=user_directory_path_image, default='images/profile_image.jpg',
                              verbose_name='Изображения')
    pet = models.ForeignKey(Pet, blank=True, null=True, on_delete=models.CASCADE)
    news = models.ForeignKey(News, blank=True, null=True, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Изображения"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.image.name


class Order(models.Model):
    pet = models.ForeignKey(Pet, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, blank=True, on_delete=models.CASCADE)
    dateCreate = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    datePickUp = models.DateField(null=True, verbose_name="Дата принятия", blank=True)
    dateViewing = models.DateTimeField(null=True, verbose_name="Дата просмотра животного", blank=True)
    STATUS_CHOICES = (
        ('sent', "отправлена"),
        ('accepted', "принята"),
        ('rejected', "отклонена"),
        ('confirmed', "подтверждена"),
    )
    status = models.CharField(max_length=15, verbose_name="Статус", choices=STATUS_CHOICES, default="sent")

    def __str__(self):
        return " ".join([self.dateCreate.strftime("%Y-%m-%d")])
