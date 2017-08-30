from django.shortcuts import render,redirect
from market.forms import * 
from market.models import *
# Create your views here.

def first(request):
    return render(request, 'market/first.html')


def main(request):
	if request.method == 'POST':
			add_to_bag(request.GET['select'],request.POST['enter'])
			return redirect(main)
	select_form = Select_Form()
	if request.GET.get('select') != None:
		select_form = Select_Form({'select':request.GET['select']})
		if select_form.is_valid():
			s_type = select_type(select_form.cleaned_data['select'])
			
			if s_type == 'Per count':
				form = Int_Form()
				return render(request, 
					'market/goods.html',{
					'select_form':select_form,
					'pcount':s_type,
					'form':form
					})	
			
			elif s_type == 'Per kg':
				form = Float_Form()
				return render(request,
					'market/goods.html',{
					'select_form':select_form,
					'pkg':s_type,
					'form':form
					})	
			
			elif s_type == 'Something free':
				form = Int_Form()
				return render(request, 
					'market/goods.html',{
					'select_form':select_form,
					'pcount':s_type,
					'form':form
					})

	return render(request, 'market/goods.html', {
		'select_form':select_form
		})


def cart(request):
	items = get_all_items_in_cart()
	if request.POST.get('Paid out') != None:
		pay_for_all_in_my_cart()
		return redirect(main)
	if request.POST.get('Pay') != None:
		items = get_all_items_in_cart()
		results = have_to_pay()
		total_list = []
		total_price = 0
		for i in results:
			total_list.append('For {0} of  {1}: {2}${3}.'.format(
				i[2],i[0],i[1][0],i[1][1]
				))
			total_price += i[1][0]

		return render(request, 'market/cart.html',{
			'total_list':total_list,
			'total_price':round(total_price,3),
			'finally':1,
			'items':items
			})

	if request.POST.get('Delete') != None:
		delete_from_cart(request.POST.get('id'))
		return redirect(cart)
	
	return render(request, 'market/cart.html',{
		'items':items
		})