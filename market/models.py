from django.db import models
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators


class Sell_types(models.Model):
	type = models.CharField(null=False, max_length=20)
	def __str__(self):
		return ' |<ID = {0};Type = {1}>| '.format(
			self.id,
			self.type
			)


class Goods(models.Model):
	name = models.CharField(primary_key=True, max_length=50)
	price = models.FloatField(null=False, validators=[validators.MinValueValidator(0.1)])
	sell_type = models.ForeignKey(Sell_types, on_delete=models.CASCADE)
	def __str__(self):
		return '<Name = {0}; Price = {1}; Sell_type = {2}>'.format(
			self.name,
			self.price,
			self.sell_type
			)


class Per_count(models.Model):
	good = models.OneToOneField(Goods,on_delete=models.CASCADE,primary_key=True)
	discount_quantity = models.IntegerField(null=False, validators=[validators.MinValueValidator(1)])
	price_quantity = models.FloatField(null=False, validators=[validators.MinValueValidator(0.1)])
	def __str__(self):
		return 'Good_name = {0};Discount_quantity = {1};Price_quantity = {2}'.format(
			self.good_id,
			self.discount_quantity,
			self.price_quantity
			)


class Per_kg(models.Model):
	good = models.OneToOneField(Goods,on_delete=models.CASCADE,primary_key=True)
	discount_kg  = models.FloatField(null=False, validators=[validators.MinValueValidator(0.1)])
	price_kg = models.FloatField(null=False, validators=[validators.MinValueValidator(0.1)])
	def __str__(self):
		return 'Good_name = {0};Discount_kg = {1};Price_kg = {2}'.format(
			self.good_id,
			self.discount_kg,
			self.price_kg
			)


class Smth_free(models.Model):
	good = models.OneToOneField(Goods,on_delete=models.CASCADE, related_name='smth_good', primary_key=True)
	quantity_to_get  = models.IntegerField(null=False, validators=[validators.MinValueValidator(1)])
	item = models.ForeignKey(Goods,null=True, on_delete = models.SET_NULL)
	item_quantity = models.IntegerField(null = False, validators=[validators.MinValueValidator(1)])
	def __str__(self):
		return 'Good_name = {0};Quantity_to_get = {1};free_item = {2}; free_item_quantity = {3};'.format(
			self.good_id,
			self.quantity_to_get,
			self.item_id,
			self.item_quantity
			)


class Checkout_accept(models.Model):
	name  = models.ForeignKey(Goods, on_delete = models.CASCADE)
	quantity = models.FloatField(null=False)
	def __str__(self):
		return 'Good name = {0}'.format(
			self.name_id
			)




def per_count_algorithm(object, count):
	try:
		good = Per_count.objects.get(pk=object.pk)
		if count >= good.discount_quantity:
			mod = count %  good.discount_quantity
			total_without_disc = mod * object.price
			total_with_disc = ( (count - mod) / good.discount_quantity ) * good.price_quantity
			total = total_without_disc + total_with_disc
			return (round(total,2),'')
		else:
			total = count * object.price
			return (round(total,2),'') 
	except ObjectDoesNotExist:
		total = count * object.price
		return (round(total,2),'')


def per_kg_algorithm(object,kg):
	try:
		good = Per_kg.objects.get(pk=object.pk)
		if kg >= good.discount_kg:
			mod = kg % good.discount_kg
			total_without_disc = mod * object.price
			total_with_disc = ( (kg - mod) / good.discount_kg) * good.price_kg
			total = total_without_disc + total_with_disc
			return (round(total,2),'')
		else: 
			total = kg * object.price
			return (round(total,2),'')
	except ObjectDoesNotExist:
		total = kg * object.price
		return (round(total,2),'')


def smth_free_algorithm(object,count):
	try:
		good = Smth_free.objects.get(pk = object.pk)
		if count >= good.quantity_to_get : 
			total = count * object.price
			mod = count % good.quantity_to_get 
			quantity_free_item = int((count - mod) / good.quantity_to_get) * good.item_quantity
			return (round(total,2), ' and also you will get {0} {1} for free'.format(
				quantity_free_item,
				good.item_id
				))
		else:
			total = count * object.price
			return (round(total,2),'')
	except ObjectDoesNotExist:
		total = count * object.price
		return (round(total,2),'') 


def get_all_name_goods():
	goods = Goods.objects.all().values()
	c = []
	for i in goods:
		c.append((i['name'],i['name']))
	return c
	if not goods :
		return 0 


def select_type(name):
	object = Goods.objects.get(pk=name)
	if object.sell_type_id == 1:
		return 'Per count'

	elif object.sell_type_id == 2:
		return 'Per kg'
	
	elif object.sell_type_id == 3:
		return 'Something free'


def add_to_bag(name,count):
	object = Goods.objects.get(pk=name)
	obj = Checkout_accept(name = object,
			quantity = count
			)
	obj.save()


def get_all_items_in_cart():
	object = Checkout_accept.objects.all().values()
	for i in object:
		obj = Goods.objects.get(pk=i['name_id'])
		if obj.sell_type_id == 1 or obj.sell_type_id == 3:
			i['quantity'] = int(i['quantity'])
	return object


def have_to_pay():
	object =  Checkout_accept.objects.distinct('name')
	names = [] 
	results = []
	for i in object:
		names.append(i.name_id)
	for i in names:
		dict1 = Checkout_accept.objects.filter(name_id=i).aggregate(totalquantity = Sum('quantity'))
		object = Goods.objects.get(pk=i)
		if object.sell_type_id == 1:
			result = per_count_algorithm(object, int(dict1['totalquantity']))
			results.append((i,result,int(dict1['totalquantity'])))
		elif object.sell_type_id == 2:
			result = per_kg_algorithm(object, dict1['totalquantity'])
			results.append((i,result,dict1['totalquantity']))
		elif object.sell_type_id == 3:
			result = smth_free_algorithm(object, int(dict1['totalquantity']))
			results.append((i,result,int(dict1['totalquantity'])))
	return results


def delete_from_cart(id):
	object = Checkout_accept.objects.get(pk=id)
	object.delete()


def pay_for_all_in_my_cart():
	object = Checkout_accept.objects.all()
	for i in object:
		i.delete()

