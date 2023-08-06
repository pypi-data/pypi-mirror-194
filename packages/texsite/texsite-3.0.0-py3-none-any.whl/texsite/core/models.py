from django.utils.translation import ugettext_lazy as _
from wagtail.core.models import Page


class BasePage(Page):
    is_creatable = False

    @property
    def next_sibling(self):
        return self.get_next_siblings().live().first()

    @property
    def previous_sibling(self):
        return self.get_prev_siblings().live().first()

    class Meta:
        verbose_name = _('Base Page') + ' (' + __package__ + ')'
