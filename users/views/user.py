from users.serializers import UserCreateSerializer, UserUpdateSerializer, UserDestroySerializer, UserListSerializer, \
    UserDetailSerializer
from users.models import User
from django.db.models import Count
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self,  request, *args, **kwargs):
        published_ads = Count('ad', filter=Q(ad__is_published=True))

        self.queryset = self.queryset.prefetch_related('locations').order_by('username').annotate(total_ads=published_ads)

        return super().get(request, *args, **kwargs)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer
