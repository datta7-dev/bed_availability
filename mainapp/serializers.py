from rest_framework import serializers
from mainapp.models import Facility, Hospitaldata


# facility serializer
class facilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


# hospitaldata serializer
class hospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospitaldata
        fields = '__all__'

    """ def validate(self, data):
        email = data.get('email')
        if Hospitaldata.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "hospital data with this email already exists")
        return data """
