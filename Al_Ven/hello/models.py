from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=20) #    verbose_name='Имя'
    fam = models.CharField(max_length=100, default='Не указана')
    oth = models.CharField(max_length=20, default='')
    age = models.IntegerField()



class Category(models.Model):
    name = models.CharField(max_length=100)
    coment = models.TextField(max_length=500)


class Products(models.Model):
    name = models.CharField(max_length=100)
    sale = models.IntegerField()
    material = models.CharField(max_length=100)
    date_prod = models.DateField()
    conter = models.IntegerField()
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name





class RegisteredUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)