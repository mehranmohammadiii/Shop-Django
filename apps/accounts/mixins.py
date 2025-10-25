from django.shortcuts import redirect
class RedirectLoggedInUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index') 
        return super().dispatch(request, *args, **kwargs)