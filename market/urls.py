from django.conf.urls import url
from market.views import (
			main,
			cart
			)
urlpatterns = [
	url(r'^market/$',main, name = 'market'),
	url(r'^cart/$',cart, name = 'cart'),
]
