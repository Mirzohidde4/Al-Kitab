from django.db import models

# Create your models here.
class Categorys(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Books(models.Model):
    title = models.CharField(max_length=100, verbose_name='Kitob nomi')
    author = models.CharField(max_length=100, verbose_name='Muallif')
    genre = models.ForeignKey(Categorys, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Janri')
    price = models.PositiveIntegerField(verbose_name='Narxi')
    description = models.TextField(verbose_name='Tavsif')
    image = models.ImageField(upload_to='media/images/', verbose_name='Rasm', null=True, blank=True)

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'