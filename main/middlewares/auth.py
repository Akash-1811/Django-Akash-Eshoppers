from django.shortcuts import redirect

def auth_middleware(get_response):
    def middleware(request):
        if not request.session.get('customer_id'):
            return redirect('login')

        print('middleware')
        response = get_response(request)
        return response

    return middleware
