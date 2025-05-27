from django.db import models


class ListField(models.TextField):
    """
    A custom Django model field for storing Python lists as comma-separated strings in the database.
    This field extends `models.TextField` and overrides methods to handle conversion
    between Python lists and their string representation for storage and retrieval.
    Methods:
        from_db_value(value, expression, connection):
            Converts the database value (a comma-separated string) to a Python list when loading from the database.
        to_python(value):
            Ensures the value is always returned as a Python list, converting from a comma-separated string if necessary.
        get_prep_value(value):
            Prepares the value for database storage by converting a Python list to a comma-separated string.
    """

    def from_db_value(self, value, expression, connection):
        if value is None or value == "":
            return []
        try:
            cleaned_value = value.strip()
            if not cleaned_value:
                return []
            return [item.strip() for item in cleaned_value.split(",") if item.strip()]
        except (AttributeError, TypeError):
            return []

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None or value == "":
            return []
        try:
            cleaned_value = str(value).strip()
            if not cleaned_value:
                return []
            return [item.strip() for item in cleaned_value.split(",") if item.strip()]
        except (AttributeError, TypeError):
            return []

    def get_prep_value(self, value):
        if not value:
            return ""
        if isinstance(value, list):
            # Filter out empty strings and None values
            filtered_values = [str(v).strip() for v in value if v is not None and str(v).strip()]
            return ",".join(filtered_values)
        return str(value).strip()

    def value_to_string(self, obj):
        """Used by serializers"""
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
