import json
from abc import abstractmethod

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import QueryDict

from rest_framework.views import APIView as _APIView
from rest_framework.response import Response

from .serializers import UserLoginSerializer


class ContentType(object):
    json_request = "application/json"
    json_response = "application/json;charset=UTF-8"
    url_encoded_request="application/x-www-form-urlencoded"

class RequestParser:
    @abstractmethod
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


class APIView(_APIView):
    request_parsers = (JsonParser(), URLEncodedParser())
    response_class = Response

    def response(self, data):
        return self.response_class(data)

    def error(self, err="err", msg="msg"):
        data = {
            'err': err,
            'msg': msg,
        }
        return Response(data)

    def success(self, data=None):
        return self.response({"error": None, "data": data})

    def _get_request_data(self, request):
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
                return self.error(err="invalid-request", msg=str(e))

        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self.error(err="api error", msg=str(e))

# Create your views here.
class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)

        if serializer.is_valid():
            vdata = serializer.validated_data
            credential = {
                'username': vdata.get('username'),
                'password': vdata.get('password')
            }
            user = authenticate(request, **credential)
            if user:
                login(request, user)
                return self.success("Succeeded")
            else:
                return self.error("Invalid username or password")
        else:
            return self.error("Invalid username or password")
