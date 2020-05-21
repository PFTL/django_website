import logging

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from pftl.git_book.models import Subscription


logger = logging.getLogger(__name__)
@method_decorator(csrf_exempt, name='dispatch')
class SubscribeGitView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        if email:
            if Subscription.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Already signed up'})
            Subscription.objects.create(email=email)
            return JsonResponse({'message': 'Thank you for signing up!'})
        return HttpResponse(status=400)

