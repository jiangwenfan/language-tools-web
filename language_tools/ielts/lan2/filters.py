from django_filters import FilterSet, filters
from language.models import BookModel, PaperModel, WordModel, ResultModel


class BookFilter(FilterSet):
    search = filters.CharFilter(method='search_filter', help_text="name description")

    class Meta:
        model = BookModel
        fields = ['search']

    def search_filter(self, queryset, name, value):
        name_value = queryset.filter(name__contains=value)
        description_value = queryset.filter(description__contains=value)
        return name_value | description_value


class PaperFilter(FilterSet):
    bid = filters.CharFilter(field_name="bid__id", lookup_expr="exact", help_text="book id")
    search = filters.CharFilter(method='search_filter', help_text="name chapter")

    class Meta:
        model = PaperModel
        fields = ['bid', 'search']

    def search_filter(self, queryset, name, value):
        name_value = queryset.filter(name__contains=value)
        chapter_value = queryset.filter(chapter__contains=value)
        return name_value | chapter_value


class WordFilter(FilterSet):
    pid = filters.CharFilter(field_name="pid__id", lookup_expr="exact", help_text="paper id")
    search = filters.CharFilter(method="search_filter", help_text="name zh symbol")

    class Meta:
        model = WordModel
        fields = ['pid', 'search']

    def search_filter(self, queryset, name, value):
        name_value = queryset.filter(name__contains=value)
        zh_value = queryset.filter(zh__contains=value)
        symbol_value = queryset.filter(symbol__contains=value)
        return name_value | zh_value | symbol_value


class ResultFilter(FilterSet):
    uid = filters.CharFilter(field_name="uid__id", lookup_expr="exact", help_text="user id")
    rtype = filters.CharFilter(help_text="result type")
    bid = filters.CharFilter(field_name="bid__id", lookup_expr="exact", help_text="book id")
    pid = filters.CharFilter(field_name="pid_id", lookup_expr="exact", help_text="paper id")

    class Meta:
        model = ResultModel
        fields = ['uid', 'rtype', 'bid', 'pid']
