from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SellingBooks, Books

@receiver(post_save, sender=SellingBooks)
def update_or_create_selling_book(sender, instance, created, **kwargs):
    selling_book = SellingBooks.objects.filter(book=instance.book).first()

    if selling_book:  
        selling_book.count += 1
        selling_book.save()
    else:  
        SellingBooks.objects.create(book=instance.book, count=1)
