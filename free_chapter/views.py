import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from free_chapter.models import People, FreeChapter


class RequestFreeChapter(View):
    """ This View is responsible for handling the form submitted when requesting a free chapter.
    """
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        person = People.objects.get_or_create(email=email)[0]
        if FreeChapter.objects.filter(user=person).count() > 0:
            return JsonResponse({'message': 'Already requested, check your e-mail'})
        s = FreeChapter(user=person)
        s.save()
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()
        s.send_confirmation_mail(user_ip)

        return JsonResponse({'message': 'Thanks! Check your e-mail'})


class ConfirmFreeChapter(View):
    """ This view is just for confirming that the user wants to receive the free chapter and avoids spam.
    """
    template_name = 'newsletter/confirm_subscription.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(People, secret_code=kwargs['secret_code'])
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()
        s = get_object_or_404(FreeChapter, user=user)
        if s.date_sent:
            return render(request, self.template_name)
        s.send_free_chapter(user_ip)
        return render(request, self.template_name)