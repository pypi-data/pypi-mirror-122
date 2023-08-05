from django.apps import AppConfig


class DjangoAuthEssentialsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_auth_essentials'

    def ready(self):
        response = super().ready()
        from django.conf import settings
        from . import configs
        for attr in dir(configs):

            if not hasattr(settings, attr):
                setattr(settings, attr, getattr(configs, attr))
            elif type(getattr(configs, attr)) == list and hasattr(settings, attr):
                settings_attr = getattr(settings, attr)
                settings_attr += getattr(configs, attr)
                setattr(settings, attr, settings_attr)

        MIDDLEWARES = getattr(settings, 'MIDDLEWARE')
        MIDDLEWARES += [
            'django_auth_essentials.middleware.UnauthenticatedSpecificMiddleware',
        ]
        
        if settings.RESTRICT_UNAUTHENTICATED_USER_ACCESS:
            MIDDLEWARES += [
                'django_auth_essentials.middleware.LoginRequiredMiddleware',
            ]

        setattr(settings, 'MIDDLEWARE', MIDDLEWARES)

        return response