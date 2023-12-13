from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field

class BaseResource(resources.ModelResource):
    title = Field(attribute='title')
    slug = Field(attribute='slug')
    description = Field(attribute='description')
    content = Field(attribute='content')

    