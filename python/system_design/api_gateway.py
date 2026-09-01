"""An exact-path API gateway model for interview practice.

The gateway maps non-empty paths to named callable services. Registration is
explicit: an existing route can only be replaced with replace=True.
Routing invokes the selected service and propagates its return value and
exceptions.

Authentication, authorization, rate limiting, retries, load balancing, and
protocol translation are intentionally out of scope.
"""

from typing import Any, Callable, Dict, Optional


class Service:
    """A named callable backend service."""

    def __init__(self, name: str, handler: Optional[Callable] = None) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("service name must be a non-empty string")
        if not callable(handler):
            raise ValueError("service handler must be callable")
        self.name = name
        self.handler = handler

    def __call__(self, request: Any):
        return self.handler(request)


class Route:
    """A route record retained for callers that want to inspect a mapping."""

    def __init__(self, path: str, service: Service) -> None:
        self.path = path
        self.service = service


class APIGateway:
    """Route requests by exact path to in-memory service callables."""

    def __init__(self) -> None:
        self.routes: Dict[str, Service] = {}

    def register(self, path: str, service, replace: bool = False) -> Service:
        """Register a service and optionally explicitly replace a route."""

        self._validate_path(path)
        if not isinstance(replace, bool):
            raise ValueError("replace must be a boolean")
        normalized = self._coerce_service(service)
        if path in self.routes and not replace:
            raise ValueError("route already exists: %s" % path)
        self.routes[path] = normalized
        return normalized

    def replace(self, path: str, service) -> Service:
        """Explicit convenience method for route replacement."""

        return self.register(path, service, replace=True)

    def route(self, path: str, request: Any):
        """Invoke the service registered for path."""

        self._validate_path(path)
        try:
            service = self.routes[path]
        except KeyError:
            raise KeyError("unknown route: %s" % path)
        return service(request)

    @staticmethod
    def _validate_path(path: str) -> None:
        if not isinstance(path, str) or not path.strip():
            raise ValueError("path must be a non-empty string")

    @staticmethod
    def _coerce_service(service) -> Service:
        if isinstance(service, Service):
            return service
        if callable(service):
            name = getattr(service, "service_name", None) or getattr(service, "__name__", None)
            if not name:
                raise ValueError("callable service must have a name")
            return Service(name, service)
        raise ValueError("service must be a callable Service")


if __name__ == "__main__":
    gateway = APIGateway()
    gateway.register("/health", Service("health", lambda request: {"ok": True}))
    print(gateway.route("/health", None))
