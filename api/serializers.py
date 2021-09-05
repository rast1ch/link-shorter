from rest_framework import serializers
from .models import Link, LinkUse



class LinkUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkUse
        fields = ['order', 'time']

class LinkInfoSerializer(serializers.ModelSerializer):
    link_use = LinkUseSerializer(many = True,
                                 read_only = False)

    

    class Meta:
        model = Link
        fields = ['url_tocken','link_to' ,'link_use']
        extra_kwargs = {'link_use': {'read_only':True},}