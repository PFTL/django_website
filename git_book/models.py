from django.db import models


class Subscription(models.Model):
    email = models.EmailField(blank=False, null=False)
    subscription_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Git Book {self.email}"