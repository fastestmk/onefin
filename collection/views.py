from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
import requests
from requests.auth import HTTPBasicAuth
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from movies.settings import movies_url, username, password
from django.db.models import Count

class CreateGetCollection(APIView):
	def post(self, request):
		print(request.data)
		serializer = CollectionSerializer(data=request.data, context={"user": request.user})
		if serializer.is_valid():
			collection = serializer.save()
			return Response({"collection_uuid": collection.uuid}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		queryset = Collection.objects.filter(user=request.user)

		movie_set = set()
		for collection in queryset:
			movie_set.update(list(collection.movie.values_list('uuid', flat=True)))

		fav_genres = list(
			Movie.objects.filter(uuid__in=movie_set).values('genre').annotate(genre_count=Count('genre')).order_by(
				'-genre_count').values_list('genre', flat=True))

		if len(fav_genres) > 3:
			fav_genres = fav_genres[0:3]


		serializer = AllCollectionSerializer(queryset, many=True)

		response = {"is_success": True, 'data': {"collections": serializer.data}, "favourite_genres": ", ".join(fav_genres) }

		return Response(response, status=status.HTTP_200_OK)
	

class PutGetDeleteCollection(APIView):
	def getCollection(self, uuid, user):
		try:
			return Collection.objects.get(uuid=uuid, user=user)
		except Collection.DoesNotExist:
			raise Http404

	def get(self, request, uuid):
		collection = self.getCollection(uuid, request.user)
		collection_data = GetCollectionSerializer(collection).data
		return Response(collection_data,status=status.HTTP_200_OK)  

	def put(self, request, uuid):
		collection = self.getCollection(uuid, request.user)
		serializer = UpdateCollectionSerializer(collection, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"message": "Collection details updated"}, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	  

	def delete(self, request, uuid):
		print("in delete method")
		collection = self.getCollection(uuid, request.user)
		collection.delete()
		return Response({"message": "Collection deleted"}, status=status.HTTP_200_OK)

def prep_request():
	
	response = requests.get(movies_url, auth=HTTPBasicAuth(username,password))
	return response

	

class AllMovies(APIView):
	# pagination_class = CustomPagination
	def get(self, request):
		limit = self.request.query_params.get("limit", 10)
		offset = self.request.query_params.get("offset", 1)
		
		response = prep_request().json()	

		return Response(response, status=status.HTTP_200_OK)	  
	