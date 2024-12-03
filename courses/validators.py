import re

from rest_framework.exceptions import ValidationError

# forbidden_words = ['ставки', 'крипта', 'продам', 'гараж', 'знакомства', 'порно', 'казино']
#
#
# def validate_forbidden_words(value):
#     if value.lower() in forbidden_words:
#         raise ValidationError(f'The value "{value}" contains forbidden words.')


class VideoUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # reg = re.compile('^[a-zA-Z0-9\.\-\ ]+$')
        reg = re.compile("\Byoutube.com\B")

        tmp_val = dict(value).get(self.field)
        if tmp_val is None:
            return

        # print(f"tmp_val {tmp_val} !!!")

        first_match = re.search("youtube.com", tmp_val)

        if not bool(first_match):
            raise ValidationError("Video_url must be only link to 'youtube'")
