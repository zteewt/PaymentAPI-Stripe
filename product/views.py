from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .models import Item
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import stripe


class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelView(TemplateView):
    template_name = 'cancel.html'
    

class ItemPage(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        item = get_object_or_404(Item, pk=pk)
        context =  super(ItemPage, self).get_context_data(**kwargs)
        context.update({
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })

        return context
    
@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def get(self, request, pk):
        stripe.api_key = settings.STRIPE_SECRET_KEY 
        item = get_object_or_404(Item, pk=pk)
        DOMAIN = 'http://127.0.0.1:8000'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{  
                "price_data": {
                    "currency": "usd",  
                    "product_data": {
                        "name": item.name,
                        "description": item.desсription,
                    },
                    "unit_amount": item.price,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=DOMAIN + '/success/',
            cancel_url=DOMAIN + '/cancel/',
        )
        return JsonResponse({"id": checkout_session.id})