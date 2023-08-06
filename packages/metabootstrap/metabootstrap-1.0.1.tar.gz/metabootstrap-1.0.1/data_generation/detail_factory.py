def generate_detail_data(*args, **kwargs):
    self = kwargs["self"]
    list_fields = kwargs["metabootstrap_parameters"]["list_fields"]
    field_list = []
    model = self.queryset.model
    database_object = model.objects.get(pk=self.kwargs["pk"])

    for field in list_fields:
        field_object = getattr(model, field)
        if field_object.__class__.__name__ == "DeferredAttribute":
            verbose_name = field_object.field.verbose_name or field
        else:
            verbose_name = field
        field_list.append(
            {
                "label": verbose_name,
                "type": "text",
                "id": field,
                "value": getattr(database_object, field),
            }
        )

    metabootstrap_data = {
        "elements": field_list,
        "view": "property",
        "id": f'{model.__name__}{self.kwargs["pk"]}',
    }
    return metabootstrap_data
