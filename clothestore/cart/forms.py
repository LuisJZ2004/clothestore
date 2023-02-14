from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card number', max_length=16)
    exp_month = forms.ChoiceField(label='Exp. month', choices=[(i, i) for i in range(1, 13)])
    exp_year = forms.ChoiceField(label='Exp. year', choices=[(i, i) for i in range(2022, 2032)])
    cvv = forms.CharField(label='CVV', max_length=3)