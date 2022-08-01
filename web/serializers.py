from django.contrib.auth.models import User
from rest_framework import serializers
from web.models import Name

class NameSerializer(
    serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Name
        fields = ['text', 'prob_f', 
            'prob_m', 'gender']
        lookup_field = 'text'
        extra_kwargs = {
            'url': {'lookup_field': 'text'}
        }      

class UserSerializer(
    serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 
            'email', 'groups', 'last_login']