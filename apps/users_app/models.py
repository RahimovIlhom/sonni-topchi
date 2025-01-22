from django.db import models


LANGUAGES_CHOICES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
    ('en', 'English'),
)

class BotUser(models.Model):
    tg_id = models.CharField(max_length=50, null=False, primary_key=True)
    username = models.CharField(max_length=255, null=True)
    fullname = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    chat_lang = models.CharField(max_length=2, null=False, choices=LANGUAGES_CHOICES)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'bot_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-registered_at']


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address

    class Meta:
        db_table = 'locations'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
