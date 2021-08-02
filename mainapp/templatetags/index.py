from django import template
from mainapp.models import Hospitaldata


register = template.Library()


@register.filter(name='hospital_name')
def hospital_name(id):
    h_name = Hospitaldata.objects.get(hospital_id=id)
    return h_name.hospital_name
