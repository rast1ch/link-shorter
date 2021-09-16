from rest_framework import serializers
from .models import Link, LinkUse


class LinkUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkUse
        fields = ['order', 'time']

    def update(self, instance, validated_data):
        pass


class LinkInfoSerializer(serializers.ModelSerializer):
    jumps = LinkUseSerializer(many=True,
                              read_only=True, )

    def update(self, instance, validated_data):
        instance.link_to = validated_data.get('link_to', instance.link_to)
        instance.save()
        return instance

    class Meta:
        model = Link
        fields = ['tocken', 'url_tocken', 'link_to', 'jumps', ]
