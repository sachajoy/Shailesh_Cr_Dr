from django.db import models
import datetime
from django.shortcuts import reverse
class Client(models.Model):
    name = models.CharField(null=False, max_length=56)
    mobno = models.CharField(max_length=11)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "{}, {}".format(self.name, self.mobno)


    def get_absolute_url(self):
        return reverse('add-trancation')


class Trancation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sector = models.CharField(null=False, max_length=100)
    amount = models.IntegerField(null=False)
    remarks = models.TextField()
    date = models.DateField(default=datetime.date.today)

    class Meta:
        ordering = ['client', '-date', 'amount']

    def __str__(self):
        return "{} - {}".format(self.client, self.date)

    def get_absolute_url(self):
        return reverse('add-trancation')