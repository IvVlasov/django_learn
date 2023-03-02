from django.contrib import admin
from django_celery_results.models import TaskResult, GroupResult
from django_celery_results.admin import TaskResultAdmin

from .models import Slider, IndexCats, Parser


class ParserAdmin(admin.ModelAdmin):
    model = Parser

    list_display = ('cat_name', 'site_name', 'is_active')


admin.site.register(Slider)
admin.site.register(IndexCats)
admin.site.register(Parser, ParserAdmin)


class CeleryTaskResultAdmin(TaskResultAdmin):
    """Change standart view table for TaskResult """
    model = TaskResult
    list_display = ('task_name', 'status', 'date_created',
                    'date_done', 'result')


admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.register(TaskResult, CeleryTaskResultAdmin)
