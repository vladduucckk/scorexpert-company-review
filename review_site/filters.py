import django_filters

from review_site.models import Review


class ReviewFilter(django_filters.FilterSet):
    comment = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Review
        fields = ["mark", "company__name", "comment"]
