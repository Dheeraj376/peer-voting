from .models import ActivityLog

class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

       
        if request.user.is_authenticated:
            ActivityLog.objects.create(
                user=request.user,
                action=f"Visited {request.path}",
                path=request.path,
                method=request.method,
                ip_address=self.get_client_ip(request)
            )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
