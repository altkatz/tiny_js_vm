def pytest_funcarg__space(request):
    # Import is inside the function so that it executes after coverage is setup,
    # if you're using pytest-cov.
    from minijs.objspace import ObjectSpace

    options = getattr(request.cls, "space_options", {})
    return ObjectSpace(**options)
