from rest_framework.views import APIView, Request, Response, status
from movies.permissions import IsLogged
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsEmployeeOnly
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOnly] 


    def get(self, request: Request) -> Response:
        movies = Movie.objects.all().order_by("id")
        
        result_page = self.paginate_queryset(movies, request, view=self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOnly]


    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        
        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK) 


    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT) 


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogged]

    def post(self, request: Request, movie_id: int) -> Response:
        movie_obj = get_object_or_404(Movie, pk=movie_id)

        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save(movie=movie_obj, order=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED) 