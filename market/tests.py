from django.test import TestCase
from market.models import * 


class Model_Algorithms_TestCase(TestCase):
	def setUp(self):
		"""Initialization"""

		#creating Sell_Types
		Sell_types.objects.create(type='Per Quantity')
		Sell_types.objects.create(type='Per kg')
		Sell_types.objects.create(type='Something free')
		
		#creating Goods
		Goods.objects.create(name='A',
			price = 0.5,
			sell_type = Sell_types.objects.get(pk=1)
			)
		Goods.objects.create(name='C',
			price = 1.99,
			sell_type = Sell_types.objects.get(pk=2)
			)
		Goods.objects.create(name='D',
			price = 1.20,
			sell_type = Sell_types.objects.get(pk=3)
			)

		#creating discounts
		Per_count.objects.create(good=Goods.objects.get(pk='A'),
			discount_quantity=3,
			price_quantity=1.30
			)
		Per_kg.objects.create(good=Goods.objects.get(pk='C'),
			discount_kg = 3,
			price_kg = 3.1
			)
		Smth_free.objects.create(good=Goods.objects.get(pk='D'),
			quantity_to_get = 2,
			item = Goods.objects.get(pk='A'),
			item_quantity=3
			)

		#creating items in user-cart
		Checkout_accept.objects.create(name=Goods.objects.get(pk='A'),quantity=7)
		Checkout_accept.objects.create(name=Goods.objects.get(pk='C'),quantity=14.9)
		Checkout_accept.objects.create(name=Goods.objects.get(pk='D'),quantity=4)

	
	def test_discount_algorithms(self):
		"""Testing algorithms of selling by selected type of discount"""
		#testing per_count
		self.assertEqual(per_count_algorithm(
			Goods.objects.get(pk='A'),3),
			(1.3,'')
		)
		#testing per_kg
		self.assertEqual(per_kg_algorithm(
			Goods.objects.get(pk='C'),4.1),
			(5.29,'')
		)
		#testing smth_free
		self.assertEqual(smth_free_algorithm(
			Goods.objects.get(pk='D'),4),
			(4.8,' and also you will get 6 A for free')
		)
		#testing payment algorithm
		self.assertEqual(have_to_pay(),[
			('A', (3.1, ''), 7),
			('C', (18.17, ''), 14.9),
			('D', (4.8, ' and also you will get 6 A for free'), 4)]
		)
	





















