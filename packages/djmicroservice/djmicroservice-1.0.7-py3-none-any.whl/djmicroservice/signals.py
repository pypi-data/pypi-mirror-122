from django.dispatch import Signal

post_install = Signal(providing_args=['djms_settings'])
post_upgrade = Signal(providing_args=['djms_settings']) 
post_register = Signal(providing_args=['djms_settings'])