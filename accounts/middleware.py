class SessionVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and not request.session.session_key:
            print("\n!!! SESSION INCONSISTENCY DETECTED !!!")
            print(f"User {request.user.pk} authenticated but no session exists")
            from django.contrib.auth import logout
            logout(request)
            
        return response