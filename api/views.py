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
        if random_slug == i.url_tocken:  # хоть там 1,340,095,640,625 вариантов, но мало ли
            rand_slug(model)
    else:
        return random_slug

def get_link(tocken):
    try:
        return Link.objects.get(tocken__exact=tocken)
    except Link.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'DELETE'])
def link_list(request, tocken):

    link = get_link(tocken)

    if request.method == 'GET':
        serializer = LinkInfoSerializer(link, many=False)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_link(request, tocken):
    try:
        link = Link.objects.get(tocken__exact=tocken)
    except Link.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LinkInfoSerializer(link, data=request.data, many=False)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_link(request):
    slug = rand_slug(Link)
    data = {
        'tocken': uuid.uuid4(),
        'url_tocken': f'{slug}',
    }
    data.update(request.data)
    serializer = LinkInfoSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)


@api_view(['GET'])
def link_jump(request, slug):
    """api call, which is used inside"""
    try:
        link = Link.objects.get(url_tocken__exact=slug)
    except Link.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    obj = LinkUse.objects.create(link=link)
    obj.save()
    return Response({}, status=status.HTTP_200_OK)
