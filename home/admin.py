from django.contrib import admin
from .models import Insight
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class InsightResources(resources.ModelResource):
    class Meta:
        model=Insight

class InsightAdmin(ImportExportModelAdmin):
    list_display = ('title', 'topic', 'sector', 'region', 'country', 'relevance', 'impact', 'likelihood')
    search_fields = ('title', 'topic', 'sector', 'country')
    list_filter = ('end_year', 'topic', 'sector', 'region', 'pestle', 'source', 'country')


admin.site.register(Insight,InsightAdmin)