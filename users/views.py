import json
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from SKYPRO_HOMEWORK_27 import settings
from users.models import User, Location
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

        published_ads = Count('ad', filter=Q(ad__is_published=True))

        users = self.object_list.prefetch_related('locations').order_by('username').annotate(total_ads=published_ads)

        paginator = Paginator(users, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                # "locations": list(user.locations.all().values_list("name", flat=True)),
                "locations": list(map(str, user.locations.all())),
                "total_ads": user.total_ads,
                })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all())),
            }, status=200, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["last_name"],
            password=user_data['password'],
            role=user_data["role"],
            age=user_data["age"],
            )

        for location in user_data["locations"]:
            loc_obj, created = Location.objects.get_or_create(name=location)
            user.locations.add(loc_obj)

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all())),
        }, status=201, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        user = self.object

        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.username = user_data["username"]
        user.password = user_data["password"]
        user.role = user_data["role"]
        user.age = user_data["age"]

        if user_data["locations"]:
            user.locations.clear()
            for location in user_data["locations"]:
                loc_obj, created = Location.objects.get_or_create(name=location)
                user.locations.add(loc_obj)
        user.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all()))
        }, status=201, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=404)