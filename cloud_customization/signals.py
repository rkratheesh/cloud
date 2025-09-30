import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from horilla import horilla_middlewares
from django.contrib import messages


@receiver(pre_save, sender=User)
def customize_user_save(sender, instance, **kwargs):
    """
    This signal is used to limit the employee login access to the system based on the subscription plan.
    If the number of users exceeds the subscription limit, the user will be deactivated.
    """
    request = getattr(horilla_middlewares._thread_locals, "request", None)
        

    subscription_user_count =os.environ.get('SUBSCRIPTION_USER_COUNT')
    if subscription_user_count is not None:
        subscription_user_count = int(subscription_user_count)
        if User.objects.filter(is_active=True).count() >= subscription_user_count:
            instance.is_active = False  
            if instance.pk :
                if request:
                    messages.error(
                        request,
                        f"User limit exceeded. You can only have {subscription_user_count} active users.",
                    )
        
    else:
        instance.is_active = False

    

            