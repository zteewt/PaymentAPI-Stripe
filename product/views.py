from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .models import Item, Order, OrderItem
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import stripe


class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelView(TemplateView):
    template_name = 'cancel.html'
    
class OrderDetail(TemplateView):
    template_name = 'order_detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        order = get_object_or_404(Order, pk=pk)
        context =  super(OrderDetail, self).get_context_data(**kwargs)
        context.update({
            "order": order,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })

        return context

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
        DOMAIN = settings.SITE_URL

        max_discount =  item.discount.order_by('-percentage').first()
        discount_id = [{"coupon": max_discount.stripe_coupon_id}] if max_discount else []

        tax_rates = [t.stripe_tax_rate_id for t in item.tax.all()]
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{  
                "price_data": {
                    "currency": "usd",  
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": item.price,
                },
                "tax_rates": tax_rates,
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{DOMAIN}/success/",
            cancel_url=f"{DOMAIN}/cancel/",
            discounts=discount_id,
        )
        return JsonResponse({"id": checkout_session.id})
    

@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutListSession(View):
    def get(self, request, pk):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(Order, pk=pk)

        if order.status == 'paid':
            return JsonResponse({"error": "Order already paid"}, status=400)
        if not order.order_items.exists():
            return JsonResponse({"error": "Empty cart"}, status=400)
        
        max_discount =  order.discount.order_by('-percentage').first()
        discount_id = [{"coupon": max_discount.stripe_coupon_id}] if max_discount else []
        
        tax_rates = [t.stripe_tax_rate_id for t in order.tax.all()]
        
        DOMAIN = 'http://127.0.0.1:8000'
        line_items = []
        for oi in order.order_items.all():
            line_item = {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": oi.item.name,
                        "description": oi.item.description,
                    },
                    "unit_amount": oi.snapshot_price
                },
                'tax_rates': tax_rates,
                "quantity": oi.quantity
            }
            line_items.append(line_item)
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=DOMAIN + '/success/',
            cancel_url=DOMAIN + '/cancel/',

            discounts=discount_id,
        )

        return JsonResponse({"id": checkout_session.id})