from django.conf import settings
from rest_framework import serializers
from wagtail.core import blocks
from django.utils.translation import gettext_lazy as _

rest_pack = getattr(settings, "REST_PACK", {})
icons = rest_pack.get('icons', [])

class LinkBlockSerializer(serializers.Serializer):
    block_name = 'linkblock'

    name = serializers.CharField(max_length=50)
    icon = serializers.CharField()
    page = serializers.SerializerMethodField('get_page_repre')

    @staticmethod
    def block_definition():
        return LinkBlockSerializer.block_name, blocks.StructBlock(local_blocks=[
            ('name', blocks.TextBlock(max_length=50, required=True, help_text=_('Name of the link'))),
            ('page', blocks.PageChooserBlock(label=_('A page to be opened'))),
            ('icon', blocks.ChoiceBlock(choices=[('none', _('None'))] + icons, default=['none'], label=_('The icon'))),
        ])

    def get_page_repre(self, value):
        page = value['page']
        return {
            'id': page.id,
            'url': page.url,
        }

    class Meta:
        fields = ['name', 'page', 'icon']