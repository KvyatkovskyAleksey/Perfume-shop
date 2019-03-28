from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
	# Отправка уведомления при успешном создании заказа
	order = Order.objects.get(id=order_id)
	subject = 'Заказ №{}'.format(order_id)
	message = 'Здравствуйте, {}! Ваш заказ был успешно размещён, наш менеджер скоро свяжется с Вами для уточнения деталей заказа.'.format(order.first_name)
	print(order.first_name)
	mail_sent = send_mail(subject,
						  message,
						  'kvyatkovsky89@gmail.com',
						  [order.email])
	return mail_sent