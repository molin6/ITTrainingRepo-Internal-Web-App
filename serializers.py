from rest_framework import serializers
from .models import ( Opportunity )

class OpportunitySerializer(serializers.ModelSerializer):
    category__name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    created_by__username = serializers.CharField(source='created_by.username', read_only=True)
    type__name = serializers.CharField(source='type.name', read_only=True, allow_null=True)
    price_range__name = serializers.CharField(source='price_range.name', read_only=True, allow_null=True)
    level__name = serializers.CharField(source='level.name', read_only=True, allow_null=True)
    ratings__average = serializers.CharField(source='get_average_rating', read_only=True, allow_null=True)
    ratings__count = serializers.CharField(source='get_rating_count', read_only=True, allow_null=True)


    class Meta:
        model = Opportunity
        fields = [
            'id',
            'name',
            'description',
            'category__name',
            'type__name',
            'price_range__name',
            'level__name',
            'created_by__username',
            'ratings__average',
            'ratings__count',
            'link'
        ]

