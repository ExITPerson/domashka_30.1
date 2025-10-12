from rest_framework.serializers import ValidationError


class URLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if bool('youtube.com' not in tmp_val):
            raise ValidationError('URL is not OK')