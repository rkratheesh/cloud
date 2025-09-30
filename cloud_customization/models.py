from django.db import models
from django.contrib.auth.models import User, UserManager

class CustomUserManager(UserManager):
    """restricting user login access on bulk create"""
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        for obj in objs:
            obj.is_active = False  
        return super().bulk_create(
            objs,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts
        )

