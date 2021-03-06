from django import forms
from .models import Product, Seller, Sale

class SaleForm(forms.Form):
    amount = forms.IntegerField(label='Кол-во', min_value=1)
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    sellers = forms.ModelChoiceField(label='Продавцы', queryset=Seller.objects.none())

    def save(self):
        data = self.cleaned_data
        product = Product.objects.get(pk=data['product_id'])
        product.amount -= data['amount']
        product.save()
        Sale.objects.create(seller=data['sellers'], product=product, amount_sold=data['amount'], purchase_amount=product.price * data['amount'])

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        product_id = cleaned_data.get("product_id")
        seller = cleaned_data.get("sellers")

        if amount < 1:
            raise forms.ValidationError(
                "Указано неверное количесто товара."
            )

        if not Product.objects.filter(pk=product_id):
            raise forms.ValidationError(
                "Товар не найден в базе данных."
            )
        if Product.objects.get(pk=product_id).amount < amount:
            raise forms.ValidationError(
                "На складе нет столько единиц товара, выберите другое количество."
            )
        if not Seller.objects.filter(name=seller):
            raise forms.ValidationError(
                "Продавец не найден в базе данных."
            )
        if not Seller.objects.filter(product=product_id):
            raise forms.ValidationError(
                "Продавец не продает данный товар."
            )

    def __init__(self, *args, **kwargs):
        # Устанавливаем в форме продавцов, которые были переданны и максимальное кол-во товара, которое можно выбрать в форме.
        qs = kwargs.pop('sellers_qs')
        max_amount = kwargs.pop('max_amount')
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['sellers'].queryset = qs
        self.fields['amount'].max_value = max_amount
        self.fields['amount'].widget.attrs['max'] = max_amount
