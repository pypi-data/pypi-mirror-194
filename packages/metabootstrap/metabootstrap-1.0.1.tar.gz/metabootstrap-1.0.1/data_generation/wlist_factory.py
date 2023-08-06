import os


def generate_wlist_data(*args, **kwargs):
    self = kwargs["self"]
    request = kwargs["request"]
    fields = kwargs["metabootstrap_parameters"]["list_fields"]

    query_parameters = format_query_parameters(request)
    objects_count = self.queryset.model.objects.all().count()
    url_previous, url_next = create_urls(query_parameters, request, objects_count)
    records = make_query(self, query_parameters)
    data = create_metabootstrap_list(self, records, fields)
    start = query_parameters.get("start")

    wlist = {
        "data": data,
        "count": len(data),
        "previous": url_previous,
        "next": url_next,
    }
    if start or start == 0:
        position = start - 1 if start > 1 else 1
        wlist.update({"position": position})

    return wlist


def format_query_parameters(request):
    """The query params are strings, so we convert them to ints for the queryset."""
    start = request.GET.get("start")
    count = request.GET.get("count")
    if start and int(start) == 1 or not start:
        start = 0
    query_parameters = {
        "start": int(start) if start else 0,
        "count": int(count) if count else 0,
        "order": request.GET.get("order"),
    }

    return query_parameters


def create_urls(query_parameters, request, objects_count):
    master_url = os.getenv("MASTER_URL", default="localhost:8000")
    order = query_parameters.get("order")
    count = query_parameters.get("count")
    start = query_parameters.get("start")

    previous_start = start - count if start and count else None
    next_start = start + count + 1 if start and count else None

    url_next = (
        f"{master_url}{request.path}?start={next_start}"
        f"&count={count}" if next_start <= objects_count
        else None
    )
    url_previous = (
        f"{master_url}{request.path}?start={previous_start}"
        f"&count={count}"
        if previous_start >= 0 else None
    )

    if url_next and order:
        url_next += f"&order={order}"
    if url_previous and order:
        url_previous += f"&order={order}"

    return url_previous, url_next


def make_query(self, query_params):
    """Makes the query based on the query parameters."""
    model = self.queryset.model
    start = query_params.get("start")
    count = query_params.get("count")
    order = query_params.get("order")

    if not count:
        less_than = model.objects.all().count()
    else:
        less_than = start + count
    queryset = model.objects.filter(id__gt=start, id__lt=less_than)
    if order:
        queryset = queryset.order_by(order)
    return queryset


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
