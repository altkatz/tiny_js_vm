from minijs.objspace import ObjectSpace


def pytest_funcarg__space(request):
    options = getattr(request.cls, "space_options", {})
    return ObjectSpace(**options)