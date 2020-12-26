import functools
import json
from http import HTTPStatus

from django.views.generic import View as _APIView
from django.http import HttpResponse, QueryDict

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import serializers

#from rest_framework.views import APIView as _APIView
from rest_framework.response import Response

class ContentType(object):
    json_request = "application/json"
    json_response = "application/json;charset=UTF-8"
    url_encoded_request="application/x-www-form-urlencoded"

class RequestParser:
    def parse(self, body):
        raise NotImplementedError()

class JsonParser():
    content_type = ContentType.json_request

    def parse(self, body):
        return json.loads(body.decode("utf-8"))


class URLEncodedParser(RequestParser):
    content_type = ContentType.url_encoded_request

    def parse(self, body):
        return QueryDict(body)


class JsonResponse(object):
    content_type = ContentType.json_response
    
    @classmethod
    def response(cls, data):
        status = data.pop("status", HTTPStatus.OK)
        resp = HttpResponse(
            json.dumps(data, indent=4),
            content_type=cls.content_type,
            status=status)
        return resp


class APIError(Exception):
    def __init__(self, status, err="API error"):
        self.status = status
        self.err = err

    def __str__(self):
        return self.err

class APIView(_APIView):
    request_parsers = (JsonParser(), URLEncodedParser())
    response_class = JsonResponse

    def _response(self, data):
        return self.response_class.response(data)

    def error(self, status, err="error"):
        resp_data = {
            "error": err,
            "data": None,
            "status": status
        }
        return self._response(resp_data)

    def success(self, data=None, status=HTTPStatus.OK):
        resp_data = {
            "error": None,
            "data": data,
            "status": status
        }
        return self._response(resp_data)

    def server_error(self, err="server error"):
        return self.error(HTTPStatus.INTERNAL_SERVER_ERROR, err=err)

    def _extract_error(self, errors, key=""):
        if isinstance(errors, dict):
            key = list(errors.keys())[0]
            return self._extract_error(errors.pop(key), key)
        elif isinstance(errors, list):
            return self._extract_error(errors[0], key)
        
        return key, errors

    def invalid_serializer(self, serializer):
        key, error = self._extract_error(serializer.errors)
        err = f"invalid '{key}' : {error}"

        return self.error(HTTPStatus.BAD_REQUEST, err=err)

    def _get_request_data(self, request):
        #idempotent
        if request.method not in ["GET", "DELETE"]:
            body = request.body
            content_type = request.META.get("CONTENT_TYPE")
            if not content_type:
                raise ValueError("content_type is required")

            for parser in self.request_parsers:
                if content_type.startswith(parser.content_type):
                    break
            else:
                raise ValueError("unknown content type {}".format(content_type))

            if body:
                return parser.parse(body)
            return {}
        return request.GET

    def dispatch(self, request, *args, **kwargs):
        if self.request_parsers:
            try:
                request.data = self._get_request_data(request)
            except ValueError as e:
                return self.error(HTTPStatus.BAD_REQUEST, err=str(e))

        try:
            return super().dispatch(request, *args, **kwargs)
        except APIError as e:
            return self.error(status=e.status, err=str(e))
        except Exception as e:
            return self.server_error(err=str(e))


def validate_serializer(serializer):
    def validate(view_method):
        @functools.wraps(view_method)
        def handle(*args, **kwargs):
            self = args[0]
            request = args[1]

            s = serializer(data=request.data)
            if s.is_valid():
                request.data = s.validated_data
                return view_method(*args, **kwargs)
            else:
                return self.invalid_serializer(s)

        return handle
    return validate

def paginate_data(request, qs, serializer):
    try:
        limit = int(request.GET.get("limit", "10"))
    except ValueError:
        limit = 10
    if limit < 0 or limit > 50:
        limit = 10
    
    try:
        offset = int(request.GET.get("offset", "0"))
    except ValueError:
        offset = 0
    if offset < 0:
        offset = 0

    results = serializer(qs[offset:offset+limit], many=True).data
    count = qs.count()

    data = {
        "results": results,
        "count": count,
    }
    return data