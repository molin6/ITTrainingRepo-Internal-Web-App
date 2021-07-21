import re
from django import forms
from django.urls import resolve
from .models import Opportunity

class FormBase(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        view_name = resolve(self.request.path_info).url_name
        (view_verb, view_object_type) = view_name.split("_")
        self.view_verb = view_verb
        self.view_object_type = view_object_type
        post_data = self.request.POST or None
        super(FormBase, self).__init__(post_data, **kwargs)
        self.model_name = re.sub("\(.*$", "", type(self.instance).__doc__)
        self.page_title = ("%s %s" % (view_verb, view_object_type)).title()
        app_name = resolve(self.request.path).app_name
        self.edit_view = ("%s:%s_%s" % (app_name, "edit", view_object_type))
        self.delete_view = ("%s:%s_%s" % (app_name, "delete", view_object_type))
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['created_by'].initial = self.request.user
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class OpportunityForm(FormBase):
    class Meta:
        model = Opportunity
        fields = [
            "name",
            "description",
            "category",
            "type",
            "price_range",
            "level",
            "link",
            "created_by"
        ]

