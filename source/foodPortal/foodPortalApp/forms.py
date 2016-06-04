from django.forms import ModelForm
from django import forms
from .models import *

class InitSelectMultiple(forms.SelectMultiple):
    allow_multiple_selected = True

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [forms.format_html('<select multiple="multiple"{}>', forms.flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        return forms.mark_safe('\n'.join(output))

class RegistrationForm(ModelForm):
    class Meta:
        model = Member
        fields = 'first_name','last_name','phoneNumber','room','bio','email','username','password'
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required=True
        self.fields['last_name'].required=True
        self.fields['phoneNumber'].required=True
        self.fields['phoneNumber'].label = "Phone Number"
        self.fields['email'].required=True
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})
            
            if field in ['username', 'password1', 'password2']:
                self.fields[field].help_text = None
                
class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ('restaurant', 'image')
    
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super(MenuForm, self).__init__(*args, **kwargs)

        self.fields['restaurant'].label = "Restaurant Name: "
        self.fields['image'].label = "Image URL: "
        for field in self.fields:
            try:
                self.fields[field].widget.attrs.update({'class' : 'form-control',
                                                    'value' : initial[field]})
            except:
                self.fields[field].widget.attrs.update({'class' : 'form-control'})

class SectionForm(ModelForm):
    class Meta:
        model = MenuSection
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super(SectionForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = "Section Name: "
        for field in self.fields:
            try:
                self.fields[field].widget.attrs.update({'class' : 'form-control',
                                                    'value' : initial[field]})
            except:
                self.fields[field].widget.attrs.update({'class' : 'form-control'})

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name','section','cost','description')
    optionField = forms.ModelMultipleChoiceField(queryset=Option.objects.all(), \
                                                 widget=forms.SelectMultiple())

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super(ItemForm, self).__init__(*args, **kwargs)

        self.fields['description'].required=False
        self.fields['optionField'].label = "Options: "
        self.fields['optionField'].required = True
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})


class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ('name','description')
    optionId = forms.CharField()

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        try:
            initial['name']
        except:
            initial['optionId'] = ''
        super(OptionForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = True
        self.fields['description'].required = False
        self.fields['optionId'].label = 'hidden'
        self.fields['optionId'].required = False
        for field in self.fields:
            if field == 'optionId':
                self.fields[field].widget.attrs.update({'class':'hidden',
                                                       'value':initial[field]})
            else:
                try:
                    self.fields[field].widget.attrs.update({'class' : 'form-control',
                                                            'value' : initial[field]})
                except:
                    self.fields[field].widget.attrs.update({'class' : 'form-control'})

class AddToForm(ModelForm):
    class Meta:
        model = Order
        fields = ()

    userId = forms.CharField()
    itemId = forms.CharField()
    optionId = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(AddToForm, self).__init__(*args, **kwargs)

        self.fields['name'].label = 'hidden'
        self.fields['description'].label = 'hidden'
        self.fields['userId'].label = 'hidden'
        self.fields['itemId'].label = 'hidden'
        self.fields['optionId'].label = 'hidden'
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control'})