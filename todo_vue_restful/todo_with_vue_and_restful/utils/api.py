import functools
import json

from django.views.generic import View
from django.http import HttpResponse, QueryDict

class ContentType:
    json_request = "application/json"
    url_encoded_request = "application/x-www-form-urlencoded"

    json_response = "application/json;charset=UTF-8"
    binary_response = "application/octet-stream"

class JSONParser:
    content_type = ContentType.json_request

    @staticmethod
    def parse(body):
        return json.load(body.decode("utf-8"))


class JSONResponse:
    content_type = ContentType.json_response

    @classmethod
    def response(cls, data):
        resp = HttpResponse(
            json.dumps(data, indent=4),
            content_type=cls.content_type
        )
        return resp


class URLEncodedParser:
    content_type = ContentType.url_encoded_request

    @staticmethod
    def parse(body):
        return QueryDict(body)

class APIError(Exception):
    def __init__(self, msg, err=None):
        self.err = err
        self.msg = msg
        super().__init__(err, msg)

class APIView(View):
    request_parsers = [JSONParser, URLEncodedParser]
    response_class = JSONResponse

    def _get_request_data(self, request):
        # idempotent
        if request.method not in ['GET', 'DELETE']:
            body = request.body
            content_type = request.META.get('CONTENT_TYPE')
            if not content_type:
                raise ValueError("content type is required")

            for parser in type(self).request_parsers:
                if content_type.startswith(parser.content_type):
                    break
            # else means the for loop is not interrupted by break
            else:
                raise ValueError("unknown content_type {}".format(content_type))

            if body:
                return parser.parse(body)
            return {}
        return request.GET

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)