from django import forms

from service_list.models import Product


class StyleForMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class FindBadWord:

    def search_word(self, enter):
        for word in self.danger_words:
            if word in enter.lower():
                raise forms.ValidationError(f'Таким'
                                            f' "{word}", мы не занимаемся')


class ProductForm(StyleForMixin, FindBadWord, forms.ModelForm):
    danger_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                    'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name', 'overview', 'overview_big',
                  'category', 'picture', 'price')

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        self.search_word(cleaned_data)
        return cleaned_data

    def clean_overview(self):
        cleaned_data = self.cleaned_data.get('overview')
        self.search_word(cleaned_data)
        return cleaned_data
