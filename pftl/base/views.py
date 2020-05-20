from django.views.generic import FormView

from pftl.base.froms import ContactUs
from pftl.base.models import Message


class ContactUsView(FormView):
    form_class = ContactUs
    template_name = 'base/contact.html'
    success_url = '/'

    def form_valid(self, form):
        fake_field_value = form.cleaned_data.get('honeypot', None)
        print(form)
        if not fake_field_value:
            from_email = form.cleaned_data.get('from_email')
            message = form.cleaned_data.get('message')
            Message.objects.create(from_email=from_email, text=message)
        return super(ContactUsView, self).form_valid(form)


