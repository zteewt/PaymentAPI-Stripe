from django.urls import path
from .views import (CreateCheckoutSessionView,
                    ItemPage,
                    SuccessView,
                    CancelView,
                     )

urlpatterns = [
    path('item/<int:pk>/', ItemPage.as_view(), name='item'),
    path('buy/<int:pk>/', CreateCheckoutSessionView.as_view(), name="buy"),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]
