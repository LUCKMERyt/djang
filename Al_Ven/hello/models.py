from django.db import models


class Person(models.Model):
    name = models.CharField('Имя', max_length=20)
    fam = models.CharField('Фамилия', max_length=100, default='Не указана')
    oth = models.CharField('Отчество', max_length=20, blank=True, default='')
    age = models.IntegerField('Возраст')

    def __str__(self):
        return f'{self.fam} {self.name} {self.oth}'.strip()

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    coment = models.TextField('Описание', max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    name = models.CharField('Название товара', max_length=100)
    sale = models.IntegerField('Цена')
    material = models.CharField('Материал', max_length=100)
    date_prod = models.DateField('Дата производства')
    conter = models.IntegerField('Количество')
    cat_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class RegisteredUser(models.Model):
    name = models.CharField('Имя пользователя', max_length=100)
    email = models.EmailField('Электронная почта', unique=True)
    password = models.CharField('Пароль', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'