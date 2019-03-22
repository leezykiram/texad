import math

from rest_framework import serializers

from light_jets.models import Product, Tracking


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('product_id','description')

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class TrackingSerializer(serializers.ModelSerializer):
    """
    Assumption made is ONLY one product(jet) can be at a Point(latitude,longitude) on a specific datetime.
    """
    product = ProductSerializer() # not many due to the assumption
    class Meta:
        model = Tracking
        fields = '__all__' 

    def validate_latitude(self, value):
        """
        Check if latitude is under the expected range.
        """
        _,lat = math.modf(value)
        lat = int(lat)
        if lat > 90 or lat < -90:
            raise serializers.ValidationError("Latitude values are not in the range of -90 to +90")
        return value

    def validate_longitude(self, value):
        """
        Check if longitude is under the expected range.
        """
        _,lon = math.modf(value)
        lon = int(lon)
        if lon > 180 or lon < -180:
            raise serializers.ValidationError("Longitude values are not in the range of -180 to +180")
        return value


    def create(self, validated_data):
        # Validate if product array is expected
        product_data = validated_data.pop('product')
        if product_data['product_id'] is None or product_data['product_id'] == "":
            raise serializers.ValidationError("product_id field cannot be NULL")
        if product_data['description'] is None or product_data['description'] == "":
            raise serializers.ValidationError("description field cannot be NULL")    
        product_obj, created = Product.objects.get_or_create(**product_data)
        return Tracking.objects.get_or_create(product=product_obj,**validated_data)

    def update(self, instance, validated_data):
        # Validate if product array is expected
        product_data = validated_data.pop('product')
        if product_data['product_id'] is None or product_data['product_id'] == "":
            raise serializers.ValidationError("product_id field cannot be NULL")
        if product_data['description'] is None or product_data['description'] == "":
            raise serializers.ValidationError("description field cannot be NULL")    
        # Check if the product object exists already
        product_obj, created = Product.objects.update_or_create(**product_data)

        instance.product = product_obj
        instance.track_datetime = validated_data.get('track_datetime', instance.track_datetime)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude =  validated_data.get('longitude', instance.longitude)
        instance.elevation = validated_data.get('elevation', instance.elevation)
        instance.save()
        return instance
