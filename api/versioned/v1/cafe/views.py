from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.bases.cafe.models import Cafe
from api.versioned.v1.cafe.serializers import CafeSerializer
from common.viewsets import MappingViewSetMixin
from rest_framework import viewsets

class CafeViewSet(MappingViewSetMixin,
                     viewsets.ModelViewSet):

    permission_classes = [AllowAny, ]
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
