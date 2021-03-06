import datetime

from django.db import transaction
from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from locations.serializers import LocationSerializer
from locations.tasks import get_geolocation

from .filters import TruckFilter
from .models import Truck
from .permissions import IsOwnerOrReadOnly
from .serializers import TruckImageSerializer, TruckSerializer
from .throttle import UserGetRateThrottle, UserPostRateThrottle


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.confirmed.all()
    serializer_class = TruckSerializer
    filterset_class = TruckFilter
    permission_classes = (
        permissions.DjangoModelPermissions,
        IsOwnerOrReadOnly,
    )
    throttle_classes = (UserGetRateThrottle, UserPostRateThrottle)

    def _get_images(self, request):
        for img in request.data.getlist("image"):
            image_serializer = TruckImageSerializer(data={"image": img})
            image_serializer.is_valid(raise_exception=True)

    def create(self, request, *args, **kwargs):
        if request.data.get("image"):
            self._get_images(request)
        return super(TruckViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        if request.data.get("image"):
            self._get_images(request)
        return super(TruckViewSet, self).update(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def mine(self, request):
        trucks = (
            self.filter_queryset(self.get_queryset())
            .filter(owner=request.user)
            .order_by("-updated")
        )
        page = self.paginate_queryset(trucks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(trucks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def opens(self, request):
        current_time = datetime.datetime.now().time()
        qs = self.filter_queryset(self.get_queryset()).filter(
            Q(location__open_from__lte=current_time)
            & Q(location__closed_at__gte=current_time)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def location(self, request, pk=None):
        truck = self.get_object()
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(city=truck.city, truck=truck)
            transaction.on_commit(lambda: get_geolocation.delay(truck.id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
