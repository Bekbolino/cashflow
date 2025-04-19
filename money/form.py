from django import forms
from django.utils import timezone
from .models import *



class CashFlowForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'value':timezone.now}),
        required=False,
         initial=timezone.now,
    )

    class Meta:
        model = CashFlow
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']


    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if not amount:
            self.add_error('amount', 'Поле "Сумма" обязательно.')
        if not type:
            self.add_error('type', 'Поле "Тип" обязательно.')
        if not category:
            self.add_error('category', 'Поле "Категория" обязательно.')
        if not subcategory:
            self.add_error('subcategory', 'Поле "Подкатегория" обязательно.')

        return cleaned_data

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ["name"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
