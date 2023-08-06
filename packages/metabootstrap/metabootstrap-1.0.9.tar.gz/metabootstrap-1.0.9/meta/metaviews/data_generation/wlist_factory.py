from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination


class WebixPagination(LimitOffsetPagination):
    limit_query_param = 'count'
    offset_query_param = 'start'
    max_limit = None
    default_limit = 10

    def get_paginated_response(self, data):
        return OrderedDict([
            ("total_count", self.count),
            ("next", self.get_next_link()),
            ("previous", self.get_previous_link()),
            ("pos", self.offset),
            ("data", data),
        ])


def generate_wlist_data(*args, **kwargs):
    self = kwargs["self"]
    request = kwargs["request"]
    queryset = self.get_queryset()
    fields = kwargs["metabootstrap_parameters"]["list_fields"]
    paginator = WebixPagination()
    queryset = paginator.paginate_queryset(queryset, request, self)
    wlist = create_metabootstrap_list(self, queryset, fields)
    return paginator.get_paginated_response(wlist)


def create_metabootstrap_list(self, records, fields):
    """Creates the list for the json."""
    metabootstrap_list = []
    for record in records:
        metabootstrap_object = {}
        for field in fields:
            field_choices = getattr(self.queryset.model, field).field.choices
            if field_choices:
                display = f"get_{field}_display"
                display_method = getattr(record, display)
                metabootstrap_object.update({field: display_method()})
            else:
                metabootstrap_object.update({field: getattr(record, field)})
        metabootstrap_list.append(metabootstrap_object)
    return metabootstrap_list
