from django.core.exceptions import PermissionDenied

class StallOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'S':
            raise PermissionDenied("Only stall owners can access this page.")
        return super().dispatch(request, *args, **kwargs)