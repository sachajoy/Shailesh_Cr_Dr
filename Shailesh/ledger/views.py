from django.db.models import Sum, Count
from django.shortcuts import render
from django.views.generic import (CreateView)

from . import forms, models


def index(request):
    pending_list = models.Client.objects.all()
    for client in pending_list:
        client.val = 0
        for tranction in client.trancation_set.all():
            client.val += tranction.amount
    print(pending_list)
    return render(request, "ledger/dashboard.html", {
        'pending': pending_list
    })


class ClientCreateView(CreateView):
    model = models.Client
    form_class = forms.ClientForm


class TranctionCreateView(CreateView):
    model = models.Trancation
    form_class = forms.TrancationForm


def client_list_view(request):
    client_list = models.Client.objects.all()
    for client in client_list:
        val = 0
        for tranction in client.trancation_set.all():
            val += tranction.amount
        client.val = val
    return render(request, 'ledger/client_list.html', {'client_list': client_list})


def client_detail_view(request, id):
    client_details = models.Trancation.objects.filter(client_id=id)
    print(client_details)
    return render(request, 'ledger/client_detail.html', {
        'client_details': client_details
    })
