from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ads.models import Category
from ads.serializers import CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


"""
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

        categories = self.object_list.order_by('name')
        response = CategorySerializer(categories, many=True).data

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)
        response = CategorySerializer(category).data

        return JsonResponse(response, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        cat = Category.objects.create(
                name=cat_data["name"],
            )
        return JsonResponse(CategorySerializer(cat).data, status=201)



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
        return JsonResponse(CategorySerializer(cat).data, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=404)
"""