from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from rest_framework import status
from datetime import datetime

class AddOrderItems(APIView):
	permission_classes = [IsAuthenticated,]

	def post(self, request):
		user = request.user
		data = request.data

		orderItems = data['orderItems']

		if orderItems and len(orderItems) == 0:
			return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			order = Order.objects.create(
	            user=user,
	            paymentMethod=data['paymentMethod'],
	            taxPrice=data['taxPrice'],
	            shippingPrice=data['shippingPrice'],
	            totalPrice=data['totalPrice']
	            )

			shipping = ShippingAddress.objects.create(
	            order=order,
	            address=data['shippingAddress']['address'],
	            city=data['shippingAddress']['city'],
	            postalCode=data['shippingAddress']['postalCode'],
	            country=data['shippingAddress']['country'],
	            )

			for i in orderItems:
				product = Product.objects.get(_id=i['product'])

				item = OrderItem.objects.create(
	                product=product,
	                order=order,
	                name=product.name,
	                qty=i['qty'],
	                price=i['price'],
	                image=product.image.url,
	                )

				product.countInStock -= int(item.qty)
				product.save()

		serializer = OrderSerializer(order, many=False)
		return Response(serializer.data)

class GetOrderById(APIView):
	permission_classes = [IsAuthenticated,]

	def get(self, request, pk):
		user = request.user

		try:
			order = Order.objects.get(_id=pk)

			if user.is_staff or order.user==user:
				serializer = OrderSerializer(order, many=False)
				return Response(serializer.data)

			else:
				Response({
					'detail': 'Not Authorized to view this Order'
					}, status=status.HTTP_400_BAD_REQUEST)

		except:
			Response({
					'detail': 'Order does not Exist'
					}, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderToPaid(APIView):
	permission_classes = [IsAuthenticated,]

	def put(self, request, pk):
		order = Order.objects.get(_id=pk)
		order.isPaid = True
		order.paidAt = datetime.now()
		order.save()

		return Response('Order Was Paid')


class GetMyOrders(APIView):
	permission_classes = [IsAuthenticated,]

	def get(self, request):
		orders = request.user.order_set.all()
		serializer = OrderSerializer(orders, many=True)
		return Response(serializer.data)

class GetOrders(generics.ListAPIView):
	permission_classes = [IsAdminUser,]

	queryset = Order.objects.all()
	serializer_class = OrderSerializer


class UpdateOrderToDelivered(APIView):
	permission_classes = [IsAdminUser,]

	def put(self, request, pk):
		order = Order.objects.get(_id=pk)
		order.isDelivered = True
		order.deliveredAt = datetime.now()
		order.save()

		return Response('Order Was Delivered')
