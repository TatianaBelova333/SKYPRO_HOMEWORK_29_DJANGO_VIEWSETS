import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from SKYPRO_HOMEWORK_27 import settings
from ads.models import Ad, Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from users.models import User


def index(request):
    return HttpResponse(200, {"status": "ok"})


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)

        all_ads = self.object_list.select_related('author', 'category').order_by('-price')

        paginator = Paginator(all_ads, settings.TOTAL_ON_PAGE)
        page_num = int(request.GET.get('page', 1))
        page_obj = paginator.get_page(page_num)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "image": ad.image.url if ad.image else None,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "category": ad.category.name,
        })
        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "image": ad.image.url if ad.image else None,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "category": ad.category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "image", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, id=ad_data["author_id"])
        category = get_object_or_404(Category, id=ad_data["category_id"])

        ad = Ad.objects.create(
            name=ad_data["name"],
            author_id=author.id,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            category_id=category.id,
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "image": ad.image.url if ad.image else None,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "category": ad.category.name,
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "image", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        ad = self.get_object()

        ad.image = request.FILES.get("image", None)
        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "image": ad.image.url if ad.image else None,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "image", "is_published", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        author = get_object_or_404(User, id=ad_data["author_id"])
        category = get_object_or_404(Category, id=ad_data["category_id"])
        ad = self.object

        ad.name = ad_data["name"]
        ad.author_id = author.id
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.is_published = ad_data["is_published"]
        ad.category_id = category.id

        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "image": ad.image.url if ad.image else None,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
        }, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)