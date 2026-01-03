import json


class RequestData:
    def __new__(cls, request):
        method = request.method.upper()
        content_type = request.content_type or ""

        if method == "GET":
            return request.GET.dict()

        if method in ("POST", "PUT", "PATCH"):
            return cls._parse_body(request, content_type)

        if method == "DELETE":
            return cls._parse_delete(request, content_type)

        return {}

    @staticmethod
    def _parse_body(request, content_type: str) -> dict:
        if "application/json" in content_type:
            try:
                return json.loads(request.body.decode("utf-8"))
            except Exception:
                return {}

        if (
            "multipart/form-data" in content_type
            or "application/x-www-form-urlencoded" in content_type
        ):
            data = request.POST.dict()
            if request.FILES:
                data["files"] = [
                    f for _, files in request.FILES.lists() for f in files
                ]
            return data

        return {}

    @staticmethod
    def _parse_delete(request, content_type: str) -> dict:
        if "application/json" in content_type and request.body:
            try:
                return json.loads(request.body.decode("utf-8"))
            except Exception:
                return {}
        return {}
