from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import StreamField

from texsite.core.blocks import (
    HeadingBlock,
    ImageBlock,
    IntroBlock,
    QuoteBlock,
)
from texsite.core.models import BasePage


class CleanBlogArticlePage(BasePage):
    body = StreamField(
        [
            (
                'intro',
                IntroBlock(template='texsitecleanblog/blocks/intro.html'),
            ),
            (
                'heading',
                HeadingBlock(template='texsitecleanblog/blocks/heading.html'),
            ),
            ('paragraph', RichTextBlock()),
            (
                'image',
                ImageBlock(template='texsitecleanblog/blocks/image.html'),
            ),
            (
                'quote',
                QuoteBlock(template='texsitecleanblog/blocks/quote.html'),
            ),
        ]
    )

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = _('Clean Blog Article Page') + ' (' + __package__ + ')'


class CleanBlogArticleIndexPage(BasePage):
    body = StreamField(
        [
            (
                'intro',
                IntroBlock(template='texsitecleanblog/blocks/intro.html'),
            ),
        ]
    )

    @property
    def articles(self):
        return (
            CleanBlogArticlePage.objects.live()
            .descendant_of(self)
            .order_by('path')
        )

    def get_context(self, request):
        articles = self.articles
        page = request.GET.get('page')
        paginator = Paginator(articles, 4)

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context = super(CleanBlogArticleIndexPage, self).get_context(request)
        context['articles'] = articles

        return context

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body'),
    ]

    class Meta:
        verbose_name = (
            _('Clean Blog Article Index Page') + ' (' + __package__ + ')'
        )
