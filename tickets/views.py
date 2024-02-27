from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from tickets.serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from rest_framework import status,filters
from rest_framework import generics, mixins, viewsets
# 1 without Rest and without Model query 
def no_rest_no_model_query(request):
    guest = [
        {
            'id': 1,
            'name': 'John',
            'phone': 1234567890,
            'email': 'muhammedelsepa3y@gmail.com'
        },
        {
            'id': 2,
            'name': 'Jane',
            'phone': 1234567890,
            'email': 'muhammedelsepa3y@gmail.com'
        },
        {
            'id': 3,
            'name': 'Jack',
            'phone': 1234567890,
            'email': 'muhammedelsepa3y@gmail.com'
        }
    ]
    return JsonResponse(guest, safe=False)

# 2 without Rest and with Model query
def no_rest_with_model_query(request):
    guest = Guest.objects.all()
    response={
        "guests":list(guest.values('name','phone'))
    }
    return JsonResponse(response)


# List == GET
# Create == POST
# Retrieve == GET
# Update == PUT
# Delete == DELETE
# pk query == GET


# 3 Function Based View
# 3.1 GET POST 
@api_view(['GET','POST'])
def FBV_List(request):
    if request.method == 'GET':
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 3.2 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# 4 Class Based View
# 4.1 GET POST
class CBV_List(APIView):
    def get(self, request):
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 4.2 GET PUT DELETE
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# 5 Mixins
# 5.1 mixins List
class Mixins_List(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
# 5.2 mixins pk
class Mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)
    
# 6 Generic View
# 6.1 get and post
class Generic_List(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
# 6.2 get put delete
class Generic_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# 7 ViewSet
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
 
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


#8 find movie
@api_view(['GET'])
def find_movies(request):
    try:
        movie = Movie.objects.filter(
            hall__icontains=request.data.get('hall'),
            movie__icontains=request.data.get('movie')
            )
        serializer = MovieSerializer(movie, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# create reservation
@api_view(['POST'])
def create_reservation(request):
    try:
        movie=Movie.objects.get(
            hall=request.data.get('hall'),
            movie=request.data.get('movie')
        )
        guest=Guest()
        guest.name=request.data.get('name')
        guest.phone=request.data.get('phone')
        guest.email=request.data.get('email')
        guest.save()
        reservation = Reservation()
        reservation.movie = movie
        reservation.guest = guest
        reservation.seat = request.data.get('seat')
        reservation.save()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)




