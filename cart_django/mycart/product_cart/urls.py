from django.urls import path
from .views import (index, add_to_cart, cart, delete_cart, estimation, comit,
                    answer_comit, calculation, download_file, ClickCounterView,
                    clic, PurchaseLevelView, AutoClick)


urlpatterns = [
    path('cnt/', clic, name='clic'),
    path('auto_click/', AutoClick.as_view(), name='auto_click'),
    path('purchase_level/', PurchaseLevelView.as_view(), name='purchase_level'),
    path('counter/', ClickCounterView.as_view(), name='click-counter'),
    path('download/', download_file, name='download_file'),
    path('calculation/', calculation, name='calculation'),
    path('answer_comit/', answer_comit, name='answer_comit'),
    path('comit/', comit, name='comit'),
    path('estimation/', estimation, name='estimation'),
    path('delete_cart/', delete_cart, name='delete_cart'),
    path('cart/', cart, name='cart'),
    path('', index, name='index'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
]
