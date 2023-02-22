from rest_framework import serializers
from users.models import User
from .models import Movie, RatingChoices, MovieOrder

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(choices=RatingChoices.choices, default=RatingChoices.DEFAULT)
    synopsis = serializers.CharField(allow_null=True, default=None)
    added_by = serializers.SerializerMethodField()

    def get_added_by(self, obj: User):
        return obj.user.email 


    def create(self, validated_data: dict) -> Movie:       
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) 
    title = serializers.SerializerMethodField()
    buyed_by = serializers.SerializerMethodField()
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)

    def get_title(self, obj: MovieOrder):
        return obj.movie.title 

    def get_buyed_by(self, obj: MovieOrder):
        return obj.order.email
    
    def create(self, validated_data: dict):
        return MovieOrder.objects.create(**validated_data)