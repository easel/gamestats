from datetime import timedelta
from django.db import models

DEFAULT_TIMESTAMP_FUZZ = timedelta(hours=12)

class BaseManager(models.Manager):
    """
    Base manager class providing convenience routines for handling timestamp fuzzing, etc
    """
    pass

class AttendanceManager(BaseManager):
    """
    Custom manager to handle attendance additions safely from multiple sources
    """

    def add_or_extend(self, submitter, attendee, start_time, end_time):
        """
        Add or extend the existing attendance record for @attendee between @start_time
        and @end_time
        """
        self.filter(
            attendee=attendee,
            start__gte=start_time - DEFAULT_TIMESTAMP_FUZZ,
            end__lte=end_time + DEFAULT_TIMESTAMP_FUZZ,
        )

class KillManager(BaseManager):
    """
    Custom manager to handle kill additions safely from multiple sources
    """

    def add_if_new(self, submitter, timestamp, killer, killee):
        """
        only add new kills if they are really new (fuzz based on timestamp and submitter)
        """
        self.filter(
            killer=killer,
            killee=killee,
            timestamp__lte=timestamp - DEFAULT_TIMESTAMP_FUZZ,
            timestamp__gte=timestamp + DEFAULT_TIMESTAMP_FUZZ,
        )

class LootManager(BaseManager):
    """
    Custom manager to handle additions safely from multiple sources
    """

    def add_if_new(self, submitter, character, item, timestamp):
        """
        only add new loots if they are really new (fuzz based on timestamp and submitter
        """
        self.filter(
            character=character,
            item=item,
            timestamp__lte=timestamp - DEFAULT_TIMESTAMP_FUZZ,
            timestamp__gte=timestamp + DEFAULT_TIMESTAMP_FUZZ,
        )
