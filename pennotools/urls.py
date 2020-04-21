from django.urls import path

from pennotools.views import QrekeningView, get_debtor_creditor

app_name = 'pennotools'
urlpatterns = [
    path('Qrekening/', get_debtor_creditor, name='qrekening'),
]
