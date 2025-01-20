from django.core.validators import MinValueValidator
from django.db import models


class UserResult(models.Model):
    user = models.ForeignKey('users_app.BotUser', on_delete=models.CASCADE)
    number_of_attempts = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.fullname

    class Meta:
        ordering = ['number_of_attempts']
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
