# from django.shortcuts import render
from datetime import datetime, timedelta
from django.conf import settings
import jwt
from rest_framework.views import APIView
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, APIException
from django.core.exceptions import ObjectDoesNotExist
from .serializers import CollectionDataSerializer, MovieDataSerializer, UserSerializer, CollectionSerializer, MovieSerializer
from .models import Collection, Movie, User


# Create your views here.
class RequestCountView(APIView):
    def get(self, request):
        res = settings.request_count
        return Response({
            "Request Count": res 
        })


class RequestCountResetView(APIView):
    def post(self, request):
        settings.request_count = 0
        return Response({
            "message": "Request Count has been reset!"
        })


class CollectionView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')

        username = payload['id']

        collection = request.data
        collection['username'] = username
        collection_movies = collection.pop('movies')
        
        collection_serializer = CollectionSerializer(data=collection)
        collection_serializer.is_valid(raise_exception=True)
        collection_serializer.save()

        collection_uuid = collection_serializer.data['uuid']

        for movie in collection_movies:
            movie['collection_uuid'] = collection_uuid
            movie['username'] = username
            movie_serializer = MovieSerializer(data=movie)
            movie_serializer.is_valid(raise_exception=True)
            movie_serializer.save()

        return Response({
            'collection_uuid': collection_uuid
        })
    
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')

        username = payload['id']

        fav_genres = {

        }
        genres = ""

        my_movies = Movie.objects.filter(username=username).only('genres')
        for movie in my_movies.iterator():
            genres = genres + ',' + movie.genres

        genres = genres[1:]

        genreList = genres.split(',')
        for genre in genreList:
            if genre in fav_genres:
                fav_genres[genre] += 1
            else:
                fav_genres[genre] = 1

        fav_sorted_genres = [k for k, v in sorted(fav_genres.items(), key=lambda item: item[1])]
        my_fav_genres = ",".join(fav_sorted_genres[-3:])

        my_collections = CollectionDataSerializer(Collection.objects.filter(username=username), many=True).data

        res = {
            "is_success": True,
            "data": {
                "collections": my_collections,
                "favourite_genres": my_fav_genres
            } 
        }
        return Response(res)

class ServiceUnavailableError(APIException):
    detail = None
    status_code = 503
    def __init__(self, status_code, message):
        #override public fields
        ServiceUnavailableError.status_code = status_code
        ServiceUnavailableError.detail = message


class CollectionEditView(APIView):
    def get(self, request, collection_uuid):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')
        
        try:
            collection = CollectionSerializer(Collection.objects.get(uuid=collection_uuid))
        except ObjectDoesNotExist:
            raise ServiceUnavailableError(message=f'Object <{collection_uuid}> does not exist!', status_code=503)
        
        collection_movies = MovieDataSerializer(Movie.objects.filter(collection_uuid=collection_uuid), many=True).data
        res = {
            "title": collection.data['title'],
            "description": collection.data['description'],
            "movies": collection_movies
        }
        return Response(res)


    def put(self, request, collection_uuid):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')
        
        try:
            collection_data = CollectionSerializer(Collection.objects.get(uuid=collection_uuid)).data
        except ObjectDoesNotExist:
            raise ServiceUnavailableError(message=f'Object <{collection_uuid}> does not exist!', status_code=503)
        
        update_data = request.data
        
        if 'movies' in update_data:
            movies_data = update_data.pop('movies')
            for movie in movies_data:
                movie_uuid = movie.pop('uuid')
                Movie.objects.filter(uuid=movie_uuid).update(**movie)
        
        for key in update_data:
            collection_data[key] = update_data[key]
        del collection_data['uuid']
        del collection_data['username']
        
        Collection.objects.filter(uuid=collection_uuid).update(**collection_data)

        return Response({
            'message': f'Successfully updated collection <{collection_uuid}>'
        })

    def delete(self, request, collection_uuid):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')

        try:
            collection = CollectionSerializer(Collection.objects.get(uuid=collection_uuid))
        except ObjectDoesNotExist:
            raise ServiceUnavailableError(message=f'Object <{collection_uuid}> does not exist!', status_code=503)

        collection.delete()
        return Response({
            'message': f'Successfully deleted collection <{collection_uuid}>'
        })


class MoviesView(APIView):
    def get(self, request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')

        movie_url = 'https://demo.credy.in/api/v1/maya/movies/'

        retry_strategy = Retry(
            total = 11,
            status_forcelist = [429, 500, 502, 503, 504],
            method_whitelist = ["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        movies = http.get(url=movie_url)
        resData = movies.json()
        resData['data'] = resData.pop('results')

        return Response(resData)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        payload = {
            'id': request.data['username'],
            'exp': datetime.now() + timedelta(minutes=60),
            'iat': datetime.now()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'access_token': token
        }
        return response
        

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User doesn't exist. Please register.")
        if not user.check_password(password):
            raise AuthenticationFailed("Password does not match. Please try again.")

        payload = {
            'id': username,
            'exp': datetime.now() + timedelta(minutes=60),
            'iat': datetime.now()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'access_token': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! Please register/login!')

        user = User.objects.filter(username=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully logged out!'
        }
        return response