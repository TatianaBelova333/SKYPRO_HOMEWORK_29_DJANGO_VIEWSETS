from django.http import HttpResponse, JsonResponse
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ads.models import Ad
from ads.serializers import AdListSerializer, AdCreateSerializer, AdUpdateSerializer, AdDestroySerializer, \
    AdDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView


def index(request):
    return HttpResponse(200, {"status": "ok"})


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat', None)
        text = request.GET.get('text', None)
        locations = request.GET.getlist('location', None)
        locations_q = None
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')

        if categories:
            self.queryset = self.queryset.filter(category__id__in=categories)

        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        if locations:
            for location in locations:
                if not locations_q:
                    locations_q = Q(author_id__locations__name__icontains=location)
                else:
                    locations_q |= Q(author_id__locations__name__icontains=location)
            if locations_q:
                self.queryset = self.queryset.filter(locations_q)

        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "image", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        ad = self.get_object()

        ad.image = request.FILES.get("image", None)
        ad.save()
        response = AdDetailSerializer(ad).data

        return JsonResponse(response)
