# app/models.py
from django.db import models
from django_quill.fields import QuillField # Import QuillField
from .Utils.modelhelper import indexShifting
# --- Product Related Models ---

class ProductCategory(models.Model):
    """Model to store product categories."""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return self.label

class DietryNeeds(models.Model):
    """Model to store dietary needs/filters."""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return self.label

class Product(models.Model):
    """Main model for products."""
    image = models.ImageField(upload_to='products/images/') 
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    metaDescription = models.CharField(max_length=300)
    
    # QuillFields
    description = QuillField() # 5. description - quillfield
    ingredients = QuillField() # 6. ingredients - quillfield
    shippingAndDelivery = QuillField() # 7. shipping&delivery- quillfield (Standardized name)
    
    relatedProducts = models.ManyToManyField('self', blank=True)
    category = models.ManyToManyField(ProductCategory, related_name='products')
    dietryNeeds = models.ManyToManyField(DietryNeeds, related_name='products')

    def __str__(self):
        return self.title

# --- Blog Related Models ---

class BlogCategory(models.Model):
    """Model to store blog categories."""
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return self.label

class Blog(models.Model):
    """Main model for blog posts."""
    thumbnail = models.ImageField(upload_to='blogs/thumbnails/')
    image = models.ImageField(upload_to='blogs/images/')
    title = models.CharField(max_length=255)
    description = models.TextField() # This is a standard TextField, not QuillField
    
    # QuillField
    content = QuillField() # 5. content-quillfield
    
    category = models.ManyToManyField(BlogCategory, related_name='blogs')

    def __str__(self):
        return self.title
    

class Page(models.Model):
    title = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.title} page"

class HeroImages(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE,related_name='HeroImages')
    link = models.URLField()
    image = models.ImageField(upload_to='heroimages/')
    index = models.IntegerField()
    def __str__(self):
        return f"{self.page.title} page hero image"
    
    def save(self, *args, **kwargs):
        indexShifting(self)
        super().save(*args, **kwargs)
    