from report_designer.core.filters import StyledFilterSet, SearchBaseFilterSet
from report_designer.models import Pattern


class PatternFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Шаблоны
    """

    searching_fields = ('name',)
    searching_select = (
        'root',
        'author',
    )

    class Meta:
        model = Pattern
        fields = (
            'root',
            'author',
            'groups',
        )
