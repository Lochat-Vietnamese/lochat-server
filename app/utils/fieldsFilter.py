class FieldsFilter:
    def __new__(cls, data: dict, entity):
        allowed_fields = {field.name for field in entity._meta.get_fields() if hasattr(field, "attname")}
        return {key: value for key, value in data.items() if key in allowed_fields}
