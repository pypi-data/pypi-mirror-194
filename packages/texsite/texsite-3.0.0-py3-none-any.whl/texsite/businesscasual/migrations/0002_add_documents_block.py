import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texsitebusinesscasual', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesscasualpage',
            name='body',
            field=wagtail.core.fields.StreamField(
                (
                    (
                        'content',
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    'heading',
                                    wagtail.core.blocks.CharBlock(
                                        required=True
                                    ),
                                ),
                                (
                                    'image',
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=False
                                    ),
                                ),
                                (
                                    'paragraph',
                                    wagtail.core.blocks.RichTextBlock(
                                        required=True
                                    ),
                                ),
                            )
                        ),
                    ),
                    (
                        'documents',
                        wagtail.core.blocks.StructBlock(
                            (
                                (
                                    'heading',
                                    wagtail.core.blocks.CharBlock(
                                        required=True
                                    ),
                                ),
                                (
                                    'paragraph',
                                    wagtail.core.blocks.RichTextBlock(
                                        required=False
                                    ),
                                ),
                                (
                                    'files',
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.documents.blocks.DocumentChooserBlock(),
                                        template='texsitebusinesscasual/blocks/documentlist.html',
                                    ),
                                ),
                            )
                        ),
                    ),
                )
            ),
        ),
    ]
