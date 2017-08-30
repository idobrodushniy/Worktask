from django.contrib import admin
from market.models import (
	Goods,
	Per_count,
	Per_kg,
	Smth_free
	)
# Register your models here.
admin.site.register(Goods)
admin.site.register(Per_count)
admin.site.register(Per_kg)
admin.site.register(Smth_free)
