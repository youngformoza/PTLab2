from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.db.models import Q

from .models import Product, Purchase, PromoCode


def index(request):
    promo_codes = PromoCode.objects.all()
    products_without_promo = Product.objects.filter(promo_codes__isnull=True).order_by('pk')

    context = {'products': products_without_promo, 'promo_codes': promo_codes}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')


def apply_promo_code(request):
    error_message = None
    success_message = None
    promo_codes = PromoCode.objects.all()

    if request.method == 'POST':
        promo_code_input = request.POST.get('promo_code')
        try:
            promo_code = PromoCode.objects.get(code=promo_code_input)
            request.session['active_promo_code'] = promo_code.code
            success_message = f"Promo code '{promo_code.code}' activated successfully!"
        except PromoCode.DoesNotExist:
            error_message = "Invalid promo code. Please try again."
            request.session['active_promo_code'] = ""

    active_promo_code = request.session.get('active_promo_code')
    if active_promo_code:
        products = Product.objects.filter(Q(promo_codes__code=active_promo_code) | Q(promo_codes__isnull=True)).order_by('pk')
    else:
        products = Product.objects.filter(promo_codes__isnull=True).order_by('pk')

    context = {'products': products, 'promo_codes': promo_codes, 'error_message': error_message, 'success_message': success_message}
    return render(request, 'shop/index.html', context)
