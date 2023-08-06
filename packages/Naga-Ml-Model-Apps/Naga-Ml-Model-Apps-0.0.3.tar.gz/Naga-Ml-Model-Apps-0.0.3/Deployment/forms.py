from  django.forms import ModelForm
from .models import  Deployed_data
class Deploy_form(ModelForm):
    class Meta:
        model=Deployed_data
        fields='__all__'
