from django.forms import ModelForm
from .models import (
    Product,
    OutWear,
    Shoes,
    Hat,
    Pants,
    OutWearSizes,
    ShoesSizes,
    HatSizes,
    PantsSizes, Sizes
)
from django import forms
from users.models import StoreUser
from random import randint
from django.forms import (
    formset_factory,
    inlineformset_factory,
)

"""
    I must collect ModelCreationForm, ModelSizesCreationForm, ModelSizesCreationFormSet, ModelSizesInlineFormSet
"""


def get_engaged_product_codes_for_product(product_class, product_code='product_code'):
    data = list(product_class.objects.values_list(product_code))
    engaged_codes = [engaged_code[0] for engaged_code in data]
    return engaged_codes


def get_free_product_code():
    engaged_codes = get_engaged_product_codes_for_product(OutWear) + get_engaged_product_codes_for_product(Shoes) \
                    + get_engaged_product_codes_for_product(Hat)
    product_code = randint(100000, 999999)
    while product_code in engaged_codes:
        product_code = randint(100000, 999999)
    return product_code


class ProductCreationForm(ModelForm):
    seller = forms.ModelChoiceField(
        queryset=None,
        disabled=True,
    )
    product_code = forms.IntegerField(
        initial=get_free_product_code,
        disabled=True
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.category_slug = kwargs.pop('category_slug')
        super().__init__(*args, **kwargs)
        self.fields['seller'].initial = StoreUser.objects.get(pk=self.request.user.pk)
        self.fields['seller'].queryset = StoreUser.objects.filter(pk=self.request.user.pk)
        self.fields['category'].initial = self.category_slug.capitalize()
        self.fields['category'].disabled = True

    class Meta:
        model = Product
        exclude = ['seller', 'product_code']

    field_order = [
        'seller',
        'product_code',
        'category',
        'title',
        'product_description',
        'weight',
        'color',
        'additional_information',
        'image'
        'product_slug',
        'cost',
    ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.seller = self.cleaned_data['seller']
        instance.product_code = self.cleaned_data['product_code']
        if commit:
            instance.save(commit)
        return instance


class OutWearEditForm(ModelForm):
    class Meta:
        exclude = ('seller', 'product_code', 'category',)
        model = OutWear


class ShoesEditForm(ModelForm):
    class Meta:
        exclude = ('seller', 'product_code', 'category',)
        model = Shoes


class HatEditForm(ModelForm):
    class Meta:
        exclude = ('seller', 'product_code', 'category',)
        model = Hat


class PantsEditForm(ModelForm):
    class Meta:
        exclude = ('seller', 'product_code', 'category',)
        model = Pants


class OutWearCreationForm(ProductCreationForm):
    class Meta:
        model = OutWear
        exclude = ['seller', 'product_code']


class ShoesCreationForm(ProductCreationForm):
    class Meta:
        model = Shoes
        exclude = ['seller', 'product_code']


class HatCreationForm(ProductCreationForm):
    class Meta:
        model = Hat
        exclude = ['seller', 'product_code']


class PantsCreationForm(ProductCreationForm):
    class Meta:
        model = Pants
        exclude = ['seller', 'product_code']


class SizesCreationForm:  # Use this class to avoid code repetition
    pass


class OutWearSizesForm(ModelForm):
    class Meta:
        model = OutWearSizes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].disabled = True
        self.fields['size'].disabled = True
        self.fields['count'].required = False


class ShoesSizesForm(ModelForm):  # COLLECT_COLLECT_COLLECT_COLLECT_COLLECT_
    class Meta:
        model = ShoesSizes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].disabled = True
        self.fields['size'].disabled = True
        self.fields['count'].required = False


class HatSizesForm(ModelForm):  # COLLECT_COLLECT_COLLECT_COLLECT_COLLECT_
    class Meta:
        model = HatSizes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].disabled = True
        self.fields['size'].disabled = True
        self.fields['count'].required = False


class PantsSizesForm(ModelForm):
    class Meta:
        model = PantsSizes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].disabled = True
        self.fields['size'].disabled = True
        self.fields['count'].required = False


class SelectCategoryForm(ModelForm):  # COLLECT_COLLECT_COLLECT_COLLECT_COLLECT_
    class Meta:
        model = OutWear
        fields = ('category',)


OutWearSizesCreationFormSet = formset_factory(OutWearSizesForm, extra=0)
ShoesSizesCreationFormSet = formset_factory(ShoesSizesForm, extra=0)
HatSizesCreationFormSet = formset_factory(HatSizesForm, extra=0)
PantsSizesCreationFormSet = formset_factory(PantsSizesForm, extra=0)

OutWearSizesInlineFormSet = inlineformset_factory(
    OutWear,
    OutWearSizes,
    fields=('size', 'count'),
    extra=0,
    can_delete=False
)

ShoesSizesInlineFormSet = inlineformset_factory(
    Shoes,
    ShoesSizes,
    fields=('size', 'count'),
    extra=0,
    can_delete=False
)
HatSizesInlineFormSet = inlineformset_factory(
    Hat,
    HatSizes,
    fields=('size', 'count'),
    extra=0,
    can_delete=False
)
PantsSizesInlineFormSet = inlineformset_factory(
    Pants,
    PantsSizes,
    fields=('size', 'count'),
    extra=0,
    can_delete=False
)


class HatBuyForm(ModelForm):
    class Meta:
        model = HatSizes
        fields = '__all__'


class OutWearBuyForm(ModelForm):
    class Meta:
        model = OutWearSizes
        fields = '__all__'


class PantsBuyForm(ModelForm):
    class Meta:
        model = PantsSizes
        fields = '__all__'


class ShoesBuyForm(ModelForm):
    class Meta:
        model = ShoesSizes
        fields = '__all__'
