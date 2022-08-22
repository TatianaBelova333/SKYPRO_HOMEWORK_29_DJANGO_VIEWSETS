import json
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ads.models import Category


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

        categories = self.object_list.order_by('name')

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
                })
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
                "id": category.id,
                "name": category.name,
            }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        cat = Category.objects.create(
                name=cat_data["name"],
            )

        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)

        cat = self.object

        cat.name = cat_data["name"]
        cat.save()

        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        }, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=404)