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
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Фото")
    description = models.TextField('Описание товара', max_length=1000, blank=True, default='')



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} ⭐") for i in range(1, 6)]
    
    name = models.CharField(max_length=100, verbose_name="Ваше имя")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        db_table = 'hello_reviews'
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at'] # Сортировка: новые сверху

    def __str__(self):
        return f"Отзыв от {self.name} ({self.rating}⭐)"
