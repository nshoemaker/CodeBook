import django.dispatch

update_lang = django.dispatch.Signal(providing_args=["repo","gitobj"])
