from celery import shared_task

import os
import redis

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import (
    EmailMessage,
    EmailMultiAlternatives,
    get_connection,
    send_mail,
)
from django.conf import settings
from .models import Alert


@shared_task(name='Alerter')
def alerter():
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    r = redis.Redis(host=REDIS_HOST, port=6379)
    price_dict = r.hgetall(':1:binance_data')
    if price_dict:
        price_dict = {k.decode('utf-8'): v.decode('utf-8') for k, v in price_dict.items()}
    else:
        price_dict = {}

    number_of_alerts = 0

    alerts = Alert.objects.all()
    active_alerts = Alert.objects.filter(status="Created")
    for alert in active_alerts:
        symbol = alert.symbol
        price = alert.price
        created_by = alert.created_by
        trigger = False
        if symbol in price_dict:
            if alert.price > alert.set_price:
                if float(price_dict[symbol]) > price or float(price_dict[symbol]) == price:
                    trigger = True
            elif alert.price < alert.set_price:
                if float(price_dict[symbol]) < price or float(price_dict[symbol]) == price:
                    trigger = True
        if trigger:
            mail_context = {"email": alert.created_by.email, "name": alert.created_by.username, "alert_name": alert.name, "symbol":alert.symbol, "target_price": alert.price}
            mailer.delay(mail_context)
            alert.status = "Triggered"
            alert.save()
            number_of_alerts += 1
    return number_of_alerts

@shared_task(name='Send Mail Function')
def mailer(mail_context):
    html_message = render_to_string("alert_mail.html", context=mail_context)
    plain_message = strip_tags(html_message)
    context = {
        "template": "alert_mail.html",
        "from_email": "Alert Notifier <alertnotifier@example.com>",
        "subject": f"Price Alert for {mail_context['alert_name']}",
        "message": plain_message,
        "html_message": html_message,
        "receiver": [mail_context["email"]],
    }
    try:
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        ) as connection:
            message = EmailMultiAlternatives(
                subject=context["subject"],
                body=context["message"],
                from_email=context["from_email"],
                to=context["receiver"],
            )
            message.attach_alternative(context["html_message"], "text/html")
            message.send()
            print("Mail Sent")
    except Exception as e:
        print("Mail Send Error",end=": ")
        print(e)