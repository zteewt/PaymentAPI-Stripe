from django.urls import path
from .views import (CreateCheckoutSessionView,
                    ItemPage,
                    SuccessView,
                    CancelView,
                    CreateCheckoutListSession,
                    OrderDetail
                     )

urlpatterns = [
    path('item/<int:pk>/', ItemPage.as_view(), name='item'),
    path('buy/<int:pk>/', CreateCheckoutSessionView.as_view(), name="buy"),
    path('order/<int:pk>/', OrderDetail.as_view(), name="order-list"),
    path('order/<int:pk>/buy/', CreateCheckoutListSession.as_view(), name="order-buy"),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]
