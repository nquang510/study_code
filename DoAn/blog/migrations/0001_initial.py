
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Mô tả ngắn / tóm tắt bài viết', null=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
                'ordering': ['-created_at'],
            },
        ),
    ]
