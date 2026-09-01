import pytest

from python.system_design.api_gateway import APIGateway, Service


def test_exact_path_routes_to_named_callable_service():
    gateway = APIGateway()
    seen = []
    service = Service("users", lambda request: seen.append(request) or {"ok": True})

    assert gateway.register("/users", service) is service
    assert gateway.route("/users", {"id": 7}) == {"ok": True}
    assert seen == [{"id": 7}]


def test_replacement_is_explicit_and_deterministic():
    gateway = APIGateway()
    first = Service("first", lambda request: "first")
    second = Service("second", lambda request: "second")
    gateway.register("/resource", first)

    with pytest.raises(ValueError):
        gateway.register("/resource", second)
    assert gateway.route("/resource", None) == "first"
    gateway.register("/resource", second, replace=True)
    assert gateway.route("/resource", None) == "second"
    assert gateway.replace("/resource", first) is first


def test_unknown_paths_and_service_errors_are_not_hidden():
    gateway = APIGateway()
    with pytest.raises(KeyError):
        gateway.route("/missing", None)
    gateway.register("/error", Service("error", lambda request: 1 / 0))
    with pytest.raises(ZeroDivisionError):
        gateway.route("/error", None)


@pytest.mark.parametrize("path", ["", "   ", None, 42])
def test_paths_must_be_non_empty_strings(path):
    with pytest.raises(ValueError):
        APIGateway().register(path, Service("service", lambda request: None))


def test_invalid_services_are_rejected():
    gateway = APIGateway()
    with pytest.raises(ValueError):
        gateway.register("/bad", object())
    with pytest.raises(ValueError):
        Service("", lambda request: None)
    with pytest.raises(ValueError):
        Service("missing-handler")
