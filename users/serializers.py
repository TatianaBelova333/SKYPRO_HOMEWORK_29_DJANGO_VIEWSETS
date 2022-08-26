from users.models import User, Location
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField(required=True)
    locations = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        many=True,
    )

    class Meta:
        model = User
        exclude = ['password']


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        many=True,
    )

    class Meta:
        model = User
        exclude = ['password']


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        slug_field='name',
        many=True,
        queryset=Location.objects.all(),
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_obj)

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        slug_field='name',
        many=True,
        queryset=Location.objects.all(),
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        if self._locations:
            user.locations.clear()
            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                user.locations.add(location_obj)

        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']