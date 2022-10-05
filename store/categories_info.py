from .models import (
    OutWear, Shoes, Hat, Pants
)
product_models = (OutWear, Shoes, Hat, Pants)
product_creation_forms = {cls.__name__: cls.__name__ + 'CreationForm' for cls in product_models}
product_sizes_creation_formsets = {cls.__name__: cls.__name__ + 'SizesCreationFormSet' for cls in product_models}
product_sizes_inline_formsets = {cls.__name__: cls.__name__ + 'InlineFormSet' for cls in product_models}
product_sizes_models = (cls.__name__ + 'Sizes' for cls in product_models)
product_model_slugs = (cls.get_product_model_slug() for cls in product_models)
product_edit_models = (cls.__name__ + 'EditForm' for cls in product_models)


