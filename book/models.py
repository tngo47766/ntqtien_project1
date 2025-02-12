from django.db import models

class Book(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Book title
    author = models.CharField(max_length=100)  # Author name
    price = models.IntegerField(default=0)  # Book price
    description = models.TextField(blank=True, null=True)  # Book description
    image = models.ImageField(upload_to='uploads/books/', blank=True, null=True)  # Book cover image

    @staticmethod
    def get_books_by_id(ids): 
        return Book.objects.filter(id__in=ids) 

    @staticmethod
    def get_all_books(): 
        return Book.objects.all() 

    def __str__(self):
        return f"{self.name} - {self.author}"  # Show title & author in admin panel
