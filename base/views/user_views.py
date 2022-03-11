from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from base.serializers import *
from base.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework import status
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super().validate(attrs)

		# data['username'] = self.user.username
		# data['email'] = self.user.email

		serializer = UserSerializerWithToken(self.user).data 
		for k, v in serializer.items():
			data[k] = v

		return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class GetUserProfile(APIView):
	authentication_classes = [JWTAuthentication,]
	permission_classes = [IsAuthenticated,]
	serializer_class = UserSerializer

	def get(self, request):
		serializer = self.serializer_class(request.user, many=False)
		return Response(serializer.data)

class UpdateUserProfile(APIView):
	authentication_classes = [JWTAuthentication,]
	permission_classes = [IsAuthenticated,]
	serializer_class = UserSerializerWithToken

	def put(self, request):
		user = request.user
		serializer = self.serializer_class(user, many=False)
		data = request.data
		user.first_name = data['name']
		user.username = data['email']
		user.email = data['email']

		if data['password']!='':
			user.password=make_password(data['password'])

		user.save()
		return Response(serializer.data)

class GetUsers(generics.ListAPIView):
	permission_classes = [IsAdminUser,]
	queryset = User.objects.all()
	serializer_class = UserSerializer

class GetUserById(APIView):
	permission_classes = [IsAdminUser,]

	def get(self, request, pk):
		user = User.objects.get(id=pk)
		serializer = UserSerializer(user, many=False)
		return Response(serializer.data)

class UpdateUser(APIView):
	permission_classes = [IsAuthenticated,]
	serializer_class = UserSerializer

	def put(self, request, pk):
		user = User.objects.get(id=pk)

		data = request.data

		user.first_name = data['name']
		user.username = data['email']
		user.email = data['email']
		user.is_staff = data['isAdmin']

		user.save()

		serializer = self.serializer_class(user, many=False)
		return Response(serializer.data)



class RegisterUser(APIView):
	def post(self, request):

		data = request.data 
		
		try:
			user = User.objects.create(
				first_name=data['name'],
				username=data['email'],
				email=data['email'],
				password=make_password(data['password'])
				)

			serializer = UserSerializerWithToken(user, many=False)
			return Response(serializer.data)
		except:
			message = {'detail': 'User with this email already exists'}
			return Response(message, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(APIView):
	permission_classes = [IsAdminUser,]

	def delete(self, request, pk):
		userForDeletion = User.objects.get(id=pk)
		userForDeletion.delete()
		return Response('User was deleted')
