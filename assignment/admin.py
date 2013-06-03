from django.contrib import admin
from django.db.models.loading import get_models
from django.db import models
for m in get_models():
    exec "from %s import %s" % (m.__module__, m.__name__)


admin.site.register(Question)
admin.site.register(Assignment)
