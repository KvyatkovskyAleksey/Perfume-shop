from django.db import models
from django.urls import reverse
from django.db.models import Q

#Определение пути и имени файла
def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{}/{}/{}".format(type(instance).__name__, instance.slug, filename)



class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                        args = [self.slug])

class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name = 'Бренд', unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', 
                              blank=True,
                              verbose_name='Изображение')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class AromaGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Группа ароматов'
        verbose_name_plural = 'Группа ароматов'

    def __str__(self):
        return self.name



class Notes(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название', unique=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Нота'
        verbose_name_plural = 'Ноты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_note',
                        args = [self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', 
                                 on_delete=models.CASCADE,
                                 verbose_name = 'Категория')
    brand = models.ForeignKey(Brand, related_name='products',
                                 on_delete=models.CASCADE,
                                 verbose_name = 'Бренд')
    aroma = models.ManyToManyField(AromaGroup, related_name='products', 
                                               verbose_name='Группа ароматов')
    high_notes = models.ManyToManyField(Notes, related_name='high',  )
    heart_level = models.ManyToManyField(Notes, related_name='heart',  )
    low_level = models.ManyToManyField(Notes, related_name='low', )
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название', unique=True)
    real_name = models.CharField(max_length=200, db_index=True, verbose_name='Настоящее название')
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to=image_folder, 
                                 blank=True,
                                 verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Остаток')
    available = models.BooleanField(default=True, verbose_name='Доступность')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = ('Товар')
        verbose_name_plural = ('Товары')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                        args=[self.id, self.slug])

    @property
    def all_notes(self):
        return Notes.objects.filter(Q(name = self.low_level) | Q(name = self.high_notes) | Q(name = self.heart_level)).all()


class CarouselImages(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Название', unique=True)
    slug = models.SlugField(max_length=70, db_index=True)
    image = models.ImageField(upload_to=image_folder, 
                             blank=True, verbose_name='Изображение')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Картинка начального экрана'
        verbose_name_plural = 'Картинки начального экрана'


    def __str__(self):
        return self.name



#adding catalog from xlsx
'''   
from openpyxl import load_workbook
from slugify import slugify



wb = load_workbook(filename="/home/aleksey/Документы/django/shop/myshop/shop/Каталог.xlsx")
catalog = wb['Сводная таблица']
print(catalog)
x = 0
for row in catalog.values:
    row=[value for value in row]
    name = row[1]
    if Brand.objects.filter(name=row[2]).first():
        brand = Brand.objects.filter(name=row[2]).first()
    else:
        brand = Brand(name=row[2], slug=slugify(row[2]))
        brand.save()
    if Category.objects.filter(name=row[8]).first():
        category = Category.objects.filter(name=row[8]).first()
    else:
        category = Category(name=row[8], slug=slugify(row[8]))
        category.save()
    groups = row[13].split(', ')
    aroma_group = []
    for aroma in groups:
        a = AromaGroup.objects.filter(name=aroma).first()
        if a:
            aroma_group.append(a)
        else:
            a = AromaGroup(name=aroma, slug=slugify(aroma))
            a.save()
            aroma_group.append(a)

    high = row[15].split(', ')
    high_n = []
    for note in high:
        n = Notes.objects.filter(name=note).first()
        if n:
            high_n.append(n)
        else:
            n = Notes(name=note, slug=slugify(name))
            n.save()
            high_n.append(n)

    heart = row[16].split(', ')
    heart_n = []
    for note in heart:
        n = Notes.objects.filter(name=note).first()
        if n:
            heart_n.append(n)
        else:
            n = Notes(name=note, slug=slugify(name))
            n.save()
            heart_n.append(n)
    low = row[17].split(', ')
    low_n = []
    for note in low:
        n = Notes.objects.filter(name=note).first()
        if n:
            low_n.append(n)
        else:
            n = Notes(name=note, slug=slugify(name))
            n.save()
            low_n.append(n)
    print(f"{name}\n{brand}\n{category}\n{groups}\n{high}\n{heart}\n{low}\n")
    if not Product.objects.filter(name=row[1]):
        try:
            prod = Product(name=name, slug=slugify(name), 
                           brand=brand, category=category,
                           price=900, stock=1
                           )
            prod.save()
            for a in aroma_group:
                prod.aroma.add(a)
            for n in high_n:
                prod.high_notes.add(n)
            for n in heart_n:
                prod.heart_level.add(n)
            for n in low_n:    
                prod.low_level.add(n)
        except:
            print('NNN')
'''
