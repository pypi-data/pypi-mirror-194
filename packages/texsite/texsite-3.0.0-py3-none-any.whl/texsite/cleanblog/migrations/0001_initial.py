import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texsitecore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleanBlogArticlePage',
            fields=[
                (
                    'basepage_ptr',
                    models.OneToOneField(
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to='texsitecore.BasePage',
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    'body',
                    wagtail.core.fields.StreamField(
                        [
                            (
                                b'intro',
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            b'keyvisual',
                                            wagtail.images.blocks.ImageChooserBlock(
                                                required=False
                                            ),
                                        ),
                                        (
                                            b'slogan',
                                            wagtail.core.blocks.CharBlock(
                                                required=True
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                b'heading',
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            b'title',
                                            wagtail.core.blocks.CharBlock(
                                                required=True
                                            ),
                                        ),
                                        (
                                            b'subtitle',
                                            wagtail.core.blocks.CharBlock(
                                                required=False
                                            ),
                                        ),
                                    ],
                                    template=b'texsitecleanblog/blocks/heading.html',
                                ),
                            ),
                            (
                                b'paragraph',
                                wagtail.core.blocks.RichTextBlock(),
                            ),
                            (
                                b'image',
                                wagtail.images.blocks.ImageChooserBlock(
                                    template=b'texsitecleanblog/blocks/image.html'
                                ),
                            ),
                        ]
                    ),
                ),
            ],
            options={
                'verbose_name': 'Clean Blog Article Page (texsite.cleanblog)',
            },
            bases=('texsitecore.basepage',),
        ),
    ]
