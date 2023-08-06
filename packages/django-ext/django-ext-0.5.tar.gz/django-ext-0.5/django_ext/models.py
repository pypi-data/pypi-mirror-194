from django.db import models
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField


class TimestampModel(models.Model):
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True


class TimeRangeModel(models.Model):
    started_at = models.DateTimeField(_('Started at'), null=True, blank=True)
    ended_at = models.DateTimeField(_('Ended at'), null=True, blank=True)

    class Meta:
        abstract = True


class UserTrackModel(models.Model):
    created_by = CurrentUserField(on_delete=models.PROTECT, related_name='+', verbose_name=_('Created by'))
    updated_by = CurrentUserField(on_delete=models.PROTECT, on_update=True, related_name='+', verbose_name=_('Updated by'))

    class Meta:
        abstract = True
