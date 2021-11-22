from django.db import models
from common.models import AbstractTimeStampedModel

# Create your models here.
class Conversation(AbstractTimeStampedModel):
    """ Conversation Model Definition """

    participants = models.ManyToManyField(
        'users.User', related_name='conversations', blank=True)

    def __str__(self):
        return str(self.created)


class Message(AbstractTimeStampedModel):
    """ Message Model Definition """

    message = models.TextField()
    user = models.ForeignKey(
        'users.User', related_name='messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        'Conversation', related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} says: {self.message}'
