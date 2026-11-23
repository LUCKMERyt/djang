from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


# ! Основная модель сотрудника. Фотографии хранятся в media/people/,
# ! а в базе данных сохраняется только относительный путь к файлу.
class Person(models.Model):
    name = models.CharField('Имя', max_length=20)
    fam = models.CharField('Фамилия', max_length=100, default='Не указана')
    oth = models.CharField('Отчество', max_length=20, blank=True, default='')
    age = models.IntegerField('Возраст')
    image = models.ImageField('Фото сотрудника', upload_to='people/', null=True, blank=True)
    description = models.TextField('Описание сотрудника', max_length=1000, blank=True, default='')
    position = models.CharField('Должность', max_length=100, blank=True, default='')
    email = models.EmailField('Рабочая почта', blank=True, default='')
    phone = models.CharField('Рабочий телефон', max_length=30, blank=True, default='')

    # NOTE: Это представление используется в админке и выпадающих списках Django.
    def __str__(self):
        return f'{self.fam} {self.name} {self.oth}'.strip()

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    coment = models.TextField('Описание', max_length=500)

    # NOTE: Название категории показывается вместо стандартного "Category object".
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class Products(models.Model):
    name = models.CharField('Название товара', max_length=100)
    sale = models.IntegerField('Цена', validators=[MinValueValidator(0)])
    material = models.CharField('Материал', max_length=100)
    date_prod = models.DateField('Дата производства')
    conter = models.IntegerField('Количество', validators=[MinValueValidator(0)])
    cat_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    # NOTE: ImageField хранит путь, а сами изображения находятся в MEDIA_ROOT/products/.
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Фото")
    description = models.TextField('Описание товара', max_length=1000, blank=True, default='')
    # NOTE: Slug для детальной страницы товара — дружелюбный URL для SEO.
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name='URL-пропуск')

    def save(self, *args, **kwargs):
        # NOTE: Генерируем уникальный slug из названия, если не задан.
        if not self.slug:
            # NOTE: allow_unicode=True сохраняет кириллицу в URL (встроенный slug-конвертер ASCII-only).
            base = slugify(self.name, allow_unicode=True) or 'product'
            slug = base
            n = 1
            while Products.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['sale'], name='products_sale_idx'),
            models.Index(fields=['conter'], name='products_conter_idx'),
            models.Index(fields=['date_prod'], name='products_date_prod_idx'),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    # NOTE: Отзывы выводятся на отдельной странице и сортируются от новых к старым.
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


class ProductInquiry(models.Model):
    """Отправка заявки на товар/цену — B2B-поток: заявка уходит на почту админов."""

    STATUS_CHOICES = [('new', 'Новая'), ('handled', 'Обработана')]

    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name='inquiries',
        verbose_name='Товар',
    )
    name = models.CharField('Ваше имя', max_length=150)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение (что и в какой цене нужно?)', max_length=2000)
    status = models.CharField(
        'Статус', choices=STATUS_CHOICES, default='new', max_length=10,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка на товар'
        verbose_name_plural = 'Заявки на товар'

    def __str__(self):
        return f'Заявка на «{self.product.name}» от {self.name}'
