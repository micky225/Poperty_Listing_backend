from django.db import models


def property_image_path(instance, filename):
    return f'properties/{filename}'


def property_gallery_path(instance, filename):
    return f'properties/gallery/{filename}'


def agent_image_path(instance, filename):
    return f'agents/{filename}'


def blog_image_path(instance, filename):
    return f'blog/{filename}'


def testimonial_image_path(instance, filename):
    return f'testimonials/{filename}'


class Agent(models.Model):
    name = models.CharField(max_length=120, verbose_name='Full name')
    phone = models.CharField(max_length=40, verbose_name='Phone number')
    email = models.EmailField()
    image = models.ImageField(
        upload_to=agent_image_path,
        blank=True,
        verbose_name='Photo',
        help_text='Click Choose file to upload a photo.',
    )
    properties_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Listed count (manual)',
        help_text='Optional display number. Active listings are counted automatically in admin.',
    )
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    bio = models.TextField(blank=True, verbose_name='Short bio')

    class Meta:
        ordering = ['name']
        verbose_name = 'agent'
        verbose_name_plural = 'agents'

    def __str__(self):
        return self.name


class Property(models.Model):
    class PropertyType(models.TextChoices):
        HOUSE = 'house', 'House'
        APARTMENT = 'apartment', 'Apartment'
        LAND = 'land', 'Land'
        COMMERCIAL = 'commercial', 'Commercial'
        OFFICE = 'office', 'Office'
        WAREHOUSE = 'warehouse', 'Warehouse'
        CAR = 'car', 'Car'

    title = models.CharField(max_length=200, help_text='Headline shown on cards and detail pages.')
    description = models.TextField(help_text='Full listing description for the detail page.')
    type = models.CharField(max_length=20, choices=PropertyType.choices, verbose_name='Category')
    price = models.PositiveIntegerField(
        verbose_name='Sale price (GHS)',
        help_text='Whole number in Ghana Cedis, no commas.',
    )
    location = models.CharField(max_length=200, help_text='Neighborhood or area, e.g. East Legon')
    city = models.CharField(max_length=100)
    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    bathrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    area = models.PositiveIntegerField(
        default=0,
        verbose_name='Size / area',
        help_text='Square meters for property, or leave 0 for cars.',
    )
    image = models.ImageField(
        upload_to=property_image_path,
        blank=True,
        verbose_name='Main photo',
        help_text='Click Choose file to upload the main listing photo.',
    )
    featured = models.BooleanField(
        default=False,
        help_text='Show this listing in the Featured section on the homepage.',
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='listings',
        verbose_name='Assigned agent',
    )
    posted_date = models.DateField(verbose_name='Date posted')
    for_sale = models.BooleanField(default=True, verbose_name='Available for sale')
    for_rent = models.BooleanField(default=False, verbose_name='Available for rent')
    rent_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Monthly rent (GHS)',
        help_text='Required if “Available for rent” is checked.',
    )
    features = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Amenities / features',
        help_text='JSON list of labels, e.g. ["Swimming pool", "24hr security"]',
    )

    class Meta:
        ordering = ['-posted_date', '-id']
        verbose_name = 'property listing'
        verbose_name_plural = 'property listings'

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='gallery_images',
    )
    image = models.ImageField(
        upload_to=property_gallery_path,
        verbose_name='Photo',
    )
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name='Order')

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'gallery photo'
        verbose_name_plural = 'gallery photos'

    def __str__(self):
        return f'{self.property_id} gallery #{self.pk}'


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField(help_text='Short preview shown in lists.')
    content = models.TextField(help_text='Full article body.')
    image = models.ImageField(
        upload_to=blog_image_path,
        blank=True,
        verbose_name='Cover image',
        help_text='Click Choose file to upload a cover image.',
    )
    date = models.DateField(verbose_name='Publish date')
    author = models.CharField(max_length=120)
    category = models.CharField(max_length=80)

    class Meta:
        ordering = ['-date', '-id']
        verbose_name = 'blog post'
        verbose_name_plural = 'blog posts'

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=120, verbose_name='Client name')
    role = models.CharField(max_length=120, help_text='e.g. Home buyer · Accra')
    content = models.TextField(verbose_name='Quote')
    image = models.ImageField(
        upload_to=testimonial_image_path,
        blank=True,
        verbose_name='Photo',
        help_text='Click Choose file to upload a photo.',
    )
    rating = models.PositiveSmallIntegerField(default=5, help_text='1–5 stars')

    class Meta:
        ordering = ['id']
        verbose_name = 'testimonial'
        verbose_name_plural = 'testimonials'

    def __str__(self):
        return self.name
