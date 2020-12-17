import functools
from http import HTTPStatus

class BasePermissionDecorator(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        view_obj = args[0]
        self.request = args[1]

        if self.check_permission():
            return self.func(*args, **kwargs)
        else:
            return view_obj.error(self.status, err=self.error)

    def check_permission(self):
        raise NotImplementedError


class login_required(BasePermissionDecorator):
    status = HTTPStatus.UNAUTHORIZED
    error = "login required"
    def check_permission(self):
        return self.request.user.is_authenticated


def check_object_permission(obj, user):
    if obj.user == user:
        return True

    if user.is_superuser:
        return True

    return False