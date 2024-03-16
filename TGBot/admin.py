from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ExportActionMixin
from nested_inline.admin import NestedModelAdmin
from django.conf import settings

from .models import TGUser, Slider, Specialty, TemplateBlock, Admins


# Register your models here.
class TGUserAdmin(ExportActionMixin, admin.ModelAdmin):
    list_filter = ["registered"]

    list_display = ('name', 'phone', 'registered')


class SliderAdmin(admin.ModelAdmin):
    list_filter = ["priority"]

    def image_tag(self, obj):
        print(obj.image.url)
        return format_html('<img src="{}" width="70" height="70"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ('priority', 'image_tag',)


class SpecialtyAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        print(obj.image.url)
        return format_html('<img src="{}" width="70" height="70"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'
    list_display = ('title', 'priority', 'image_tag')


class TemplateBlockAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" width="70" height="70"/>'.format(obj.image.url))
        except:
            pass

    def template_id(self, obj):
        try:
            return format_html('<p>Шаблон #{}</p>'.format(obj.id))
        except:
            pass

    image_tag.short_description = 'Image'
    list_display = ('template_id', 'description', 'template_type', 'image_tag')


class AdminForm(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')


admin.site.register(TGUser, TGUserAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(TemplateBlock, TemplateBlockAdmin)
admin.site.register(Admins, AdminForm)

