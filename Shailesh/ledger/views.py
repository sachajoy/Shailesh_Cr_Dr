from django.db.models import Sum
from django.shortcuts import redirect, render, reverse
from django.views.generic import (CreateView, UpdateView)

from . import forms, models


def index(request):
    pending_list = models.Client.objects.all()
    for client in pending_list:
        client.val = 0
        for tranction in client.trancation_set.all():
            client.val += tranction.amount
    # print(pending_list)
    return render(request, "ledger/dashboard.html", {
        'pending': pending_list
    })


class ClientCreateView(CreateView):
    model = models.Client
    form_class = forms.ClientForm

    def get_success_url(self):
        return reverse('add-trancation', kwargs={'id': self.object.id})


class TranctionCreateListView(CreateView):
    model = models.Trancation
    form_class = forms.TrancationForm

    def get_context_data(self, **kwargs):
        context = super(TranctionCreateListView, self).get_context_data(
            **kwargs)
        context['trancations'] = models.Client.objects.get(
            pk=self.kwargs.get('id'))
        return context

    def form_valid(self, form):
        pk = self.kwargs['id']
        form.instance.client = models.Client.objects.get(pk=pk)
        print(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add-trancation', kwargs={'id': self.kwargs['id']})


class TranctionUpadateListView(UpdateView):
    model = models.Trancation
    form_class = forms.TrancationForm

    def get_context_data(self, **kwargs):
        context = super(TranctionUpadateListView, self).get_context_data(
            **kwargs)
        context['trancations'] = models.Client.objects.get(
            pk=self.kwargs.get('client_id'))
        return context

    def form_valid(self, form):
        pk = self.kwargs['client_id']
        form.instance.client = models.Client.objects.get(pk=pk)
        print(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('add-trancation',
                       kwargs={'id': self.kwargs['client_id']})


def client_list_view(request):
    client_list = models.Client.objects.all()
    for client in client_list:
        val = 0
        for tranction in client.trancation_set.all():
            val += tranction.amount
        client.val = val
    return render(request, 'ledger/client_list.html',
                  {'client_list': client_list})


def client_detail_view(request, id):
    client_details = models.Trancation.objects.filter(client_id=id)
    print(client_details)
    return render(request, 'ledger/client_detail.html', {
        'client_details': client_details
    })


def update_entry_verified(request, client_id, id):
    trancation = models.Trancation.objects.get(pk=id)
    trancation.verifed = not trancation.verifed
    trancation.save()
    # print(client_id)
    return redirect('add-trancation', id=client_id)


def client_report(request, id, client_id):
    tran = models.Trancation.objects.get(pk=id)
    opening_bal = models.Trancation.objects.filter(client_id=client_id,
                                                   booking_date__lt=tran.booking_date).aggregate(
        sum=Sum('amount'))
    trancation = models.Trancation.objects.filter(client_id=client_id,
                                                  booking_date__gte=tran.booking_date)
    # print(opening_bal)
    total_due = 0
    total_rec = 0
    total = 0
    if opening_bal['sum'] != None:
        total_due += opening_bal['sum']
    for t in trancation:
        if t.amount > 0:
            total_due += t.amount
        else:
            total_rec += t.amount
    # print(total_due)
    # print(total_rec)
    client = models.Client.objects.get(pk=client_id)
    return render(request, 'ledger/client_print.html', {
        'open': opening_bal['sum'],
        'tran': trancation,
        'client': client,
        'total_due': total_due,
        'total_rec': total_due + total_rec
    })


def ledger_of_client(request, id):
    trancation = models.Trancation.objects.filter(client_id=id)
    client = models.Client.objects.get(pk=id)
    balance = 0
    for t in trancation:
        balance += t.amount
        t.bal = balance

    return render(request, 'ledger/ledger_report.html', {
        'tran': trancation,
        'client': client,
    })
