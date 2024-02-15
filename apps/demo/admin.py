from fastapi_amis_admin import amis, admin
from fastapi_amis_admin.admin import AdminApp

# from .models import Category


class DemoApp(admin.AdminApp):
    page_schema = amis.PageSchema(label='Demo', icon='fa fa-bolt')
    router_prefix = '/demo'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        # self.register_admin(CategoryAdmin)


# Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     page_schema = amis.PageSchema(label='Category', icon='fa fa-folder')
#     model = Category
#     search_fields = [Category.name]
