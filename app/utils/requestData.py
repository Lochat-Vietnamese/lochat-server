import json

class RequestData:
    def __new__(cls, request):
        content_type = request.content_type or ""
        if "application/json" in content_type:
            try:
                data = json.loads(request.body.decode("utf-8"))
            except Exception:
                data = {}
        elif "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
            data = request.POST.dict()
            if request.FILES:
                data["files"] = [f for _, files in request.FILES.lists() for f in files]
        else:
            data = {}
        return data