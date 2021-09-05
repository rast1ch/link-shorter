import random
import string
import uuid
from .models import Link, LinkUse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LinkInfoSerializer


def rand_slug(model):
    """Формирования случайного url"""
    random_slug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    for i in model.objects.all():  # Перебор и рекурсия на случай совпадения,
        if random_slug == i.slug:  # хоть там 1,340,095,640,625 вариантов, но мало ли
            rand_slug(model)
    else:
        return random_slug



@api_view(['GET', 'DELETE'])
def link_list(request, tocken):
    try:
        link = Link.objects.get(tocken__exact=tocken)
    except Link.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LinkInfoSerializer(link,many=False)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_link(request,tocken):
    pass


@api_view(['POST'])
def create_link(request):
    slug = rand_slug(Link)
    data = {'url_tocken' : uuid.uuid4(),
            'link_use' : f'http://localhost:8000/{slug}'}
    data.update(request.data)
    serializer = LinkInfoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)