from rest_framework import serializers

from .models import Agent, BlogPost, Property, Testimonial


def image_url(field, serializer):
    """Return an absolute media URL so a separately hosted frontend can load images."""
    if not field:
        return ''
    try:
        url = field.url
    except ValueError:
        return ''
    request = serializer.context.get('request')
    if request is not None:
        return request.build_absolute_uri(url)
    return url


class AgentSerializer(serializers.ModelSerializer):
    properties = serializers.IntegerField(source='properties_count')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'image',
            'properties',
            'rating',
            'bio',
        ]

    def get_image(self, obj):
        return image_url(obj.image, self)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['rating'] = float(instance.rating)
        return data


class PropertySerializer(serializers.ModelSerializer):
    agentId = serializers.SerializerMethodField()
    postedDate = serializers.DateField(source='posted_date')
    forSale = serializers.BooleanField(source='for_sale')
    forRent = serializers.BooleanField(source='for_rent')
    rentPrice = serializers.IntegerField(source='rent_price', allow_null=True)
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'description',
            'type',
            'price',
            'location',
            'city',
            'bedrooms',
            'bathrooms',
            'area',
            'image',
            'images',
            'featured',
            'agentId',
            'postedDate',
            'forSale',
            'forRent',
            'rentPrice',
            'features',
        ]

    def get_agentId(self, obj):
        return str(obj.agent_id) if obj.agent_id else None

    def get_image(self, obj):
        return image_url(obj.image, self)

    def get_images(self, obj):
        gallery = [
            image_url(item.image, self)
            for item in obj.gallery_images.all()
            if item.image
        ]
        main = image_url(obj.image, self)
        urls = []
        if main:
            urls.append(main)
        for url in gallery:
            if url and url not in urls:
                urls.append(url)
        return urls

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        if data.get('bedrooms') is None:
            data.pop('bedrooms', None)
        if data.get('bathrooms') is None:
            data.pop('bathrooms', None)
        if data.get('rentPrice') is None:
            data.pop('rentPrice', None)
        return data


class BlogPostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'excerpt',
            'content',
            'image',
            'date',
            'author',
            'category',
        ]

    def get_image(self, obj):
        return image_url(obj.image, self)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        return data


class TestimonialSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'role', 'content', 'image', 'rating']

    def get_image(self, obj):
        return image_url(obj.image, self)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        return data
