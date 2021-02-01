from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-client/', views.ClientCreateView.as_view(), name='add-client'),
    path('add-tranction/', views.TranctionCreateView.as_view(), name='add-trancation'),
    path('client-list/', views.client_list_view, name='client-list'),
    path('client-detail/<int:id>', views.client_detail_view, name='client-detials')
]
