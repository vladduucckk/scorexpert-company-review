from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    adress = models.TextField()
    url = models.URLField()
    image = models.ImageField(upload_to='company_images', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.email


class Review(models.Model):
    comment = models.TextField()
    mark = models.CharField(choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')), default="5",
                            max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
