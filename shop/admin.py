from django.contrib import admin
from .models import Category, Product, Brand, AromaGroup, Notes, CarouselImages


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'brand', 'get_aroma', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

    def get_aroma(self, obj):
    	return "\n".join([p.name for p in obj.aroma.all()])
    get_aroma.short_description = 'Группа ароматов'

admin.site.register(Product, ProductAdmin)


class BrandAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Brand, BrandAdmin)

class AromaGroupAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(AromaGroup, AromaGroupAdmin)

class NotesAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug',]
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Notes, NotesAdmin)

class CarouselImagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(CarouselImages, CarouselImagesAdmin)


