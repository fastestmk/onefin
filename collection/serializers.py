from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username',)




class MovieSerializer(serializers.ModelSerializer):

	class Meta:
		model = Movie
		fields = ('uuid', 'title', 'description', 'genre')


class CollectionSerializer(serializers.ModelSerializer):
	movie = MovieSerializer(many=True)
	class Meta:
		model = Collection
		fields = ('title', 'description', 'movie')

	def create(self, validated_data):
		collection = Collection(user=self.context.get("user"), title=validated_data.get("title"), description=validated_data.get("description"))

		collection.save()
		print(collection)
		movie_data = validated_data.get("movie")

		movie_data = [dict(t) for t in {tuple(d.items()) for d in movie_data}]

		for item in movie_data:
			try:
				movie = Movie.objects.get(title=item["title"]) # if already exists
			except Movie.DoesNotExist:
				movie = Movie.objects.create(**item)
			collection.movie.add(movie)

		return collection

class UpdateCollectionSerializer(serializers.ModelSerializer):
	movie = MovieSerializer(many=True, required=False)
	title = serializers.CharField(max_length=30, required=False)
	description = serializers.CharField(max_length=500, required=False)

	class Meta:
		model = Collection
		fields = ('title', 'description', 'movie')

	def update(self, instance, validated_data):
		instance.title = validated_data.get('title', instance.title)
		instance.description = validated_data.get('description', instance.description)

		instance.save()

		if 'movie' in validated_data.keys():
			instance.movie.clear()

			movie_data = validated_data.get("movie")

			movie_data = [dict(t) for t in {tuple(d.items()) for d in movie_data}]

			for item in movie_data:
				try:
					movie = Movie.objects.get(title=item["title"])
				except Movie.DoesNotExist:
					movie = Movie.objects.create(**item)
				instance.movie.add(movie)

		return instance


class GetCollectionSerializer(serializers.ModelSerializer):
	movie = MovieSerializer(many=True)
	class Meta:
		model = Collection
		fields = ('title', 'uuid', 'description', 'movie')


class AllCollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Collection
		fields = ('title', 'uuid', 'description')


