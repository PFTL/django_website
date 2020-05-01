from django.http import JsonResponse
from django.views import View

from git_book.models import Subscription


class SubscribeGitView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        if email:
            if Subscription.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Already signed up'})
            Subscription.objects.create(email=email)
            return JsonResponse({'message': 'Thank you for signing up!'})