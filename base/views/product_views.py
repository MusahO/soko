from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from base.serializers import *
from base.models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class GetProducts(APIView):

	def get(self, request):
		query = request.query_params.get('keyword')
		if query==None:
			query=''

		products = Product.objects.filter(name__icontains=query)

		page = request.query_params.get('page')
		paginator = Paginator(products, 5)

		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)

		if page==None:
			page=1

		serializer = ProductSerializer(products, many=True)

		return Response({'products':serializer.data, 'page':int(page), 'pages':paginator.num_pages})

class GetTopProducts(APIView):

	def get(self, request):
		products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)

class GetProductDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


class DeleteProduct(APIView):
	permission_classes = [IsAdminUser,]

	def delete(self, request, pk):
		product = Product.objects.get(_id=pk)
		product.delete()
		return Response('Product deleted')


class CreateProduct(APIView):
	permission_classes = [IsAdminUser,]

	def post(self, request):
		user = request.user
		product = Product.objects.create(
			user=user,
			name='Sample Name',
			price=0,
			brand='Sample Brand',
			countInStock=0,
			category='Sample Category',
			description=''
			)
		serializer = ProductSerializer(product, many=False)
		return Response(serializer.data)


class UpdateProduct(APIView):
	permission_classes = [IsAdminUser,]

	def put(self, request, pk):
		data = request.data
		product = Product.objects.get(_id=pk)

		product.name = data['name']
		product.price = data['price']
		product.brand = data['brand']
		product.countInStock = data['countInStock']
		product.category = data['category']
		product.description = data['description']

		product.save()
		serializer = ProductSerializer(product, many=False)
		return Response(serializer.data)


class UploadImage(APIView):
	# permission_classes = [IsAdminUser,]

	def post(self, request):
		data = request.data

		product_id = data['product_id']
		product = Product.objects.get(_id=product_id)
		product.image = request.FILES.get('image')
		product.save()
		return Response('Image Was Uploaded')


class CreateProductReview(APIView):
	permission_classes = [IsAuthenticated,]

	def post(self, request, pk):
		user = request.user
		product = Product.objects.get(_id=pk)
		data = request.data

		alreadyExists = product.review_set.filter(user=user).exists()
		if alreadyExists:
			content = {'detail': 'Product already reviewed'}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		elif data['rating'] == 0:
			content = {'detail': 'Please select a rating'}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)

		else:
			review = Review.objects.create(
				user=user,
				product=product,
				name=user.first_name,
				rating=data['rating'],
				comment=data['comment'],
				)

			reviews = product.review_set.all()
			product.numReviews = len(reviews)

			total = 0
			for i in reviews:
				total += i.rating

			product.rating = total / len(reviews)
			product.save()
			return Response('Review Added')