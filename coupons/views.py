from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import MultiUseCoupon ,SingleUseCoupon
from .forms import CouponApplyForm

# Create your views here.

@require_POST

def coupon_Apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code= form.cleaned_data['code']
        try:
            try:
                coupons0 = MultiUseCoupon.objects.all()
                coupon = MultiUseCoupon.objects.get(code__iexact=code, valid_from__lte=now,valid_to__gte=now,active=True)
                
                if (coupon is not None):
                    request.session['coupon_id'] = coupon.id
            except MultiUseCoupon.DoesNotExist:
                coupons1 = SingleUseCoupon.objects.all()
                
                coupon = SingleUseCoupon.objects.get(code__iexact=code, valid_from__lte=now,valid_to__gte=now,active=True)
                if (coupon is not None):
                    request.session['coupon_id'] = coupon.id
                    coupon.deactivate_on_Use()
        except Exception as e:
            print(f"Error{e=} on applying coupon,{type(e)=}")
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')