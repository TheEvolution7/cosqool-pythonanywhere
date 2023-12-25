# Generated by Django 3.2.18 on 2023-04-29 03:22

from django.db import migrations, models
import django.db.models.deletion
import polymorphic_tree.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Field',
                'verbose_name_plural': 'Fields',
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('field_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='contents.field')),
                ('opening_title', models.CharField(max_length=200, verbose_name='Opening title')),
                ('opening_image', models.ImageField(upload_to='images', verbose_name='Opening image')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=('contents.field',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('field_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='contents.field')),
                ('images', models.ImageField(upload_to='images', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
            bases=('contents.field',),
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('field_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='contents.field')),
                ('extra_text', models.TextField()),
            ],
            options={
                'verbose_name': 'Text',
                'verbose_name_plural': 'Texts',
            },
            bases=('contents.field',),
        ),
        migrations.CreateModel(
            name='FieldGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.AddField(
            model_name='field',
            name='field_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.fieldgroup'),
        ),
        migrations.AddField(
            model_name='field',
            name='parent',
            field=polymorphic_tree.models.PolymorphicTreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='contents.field', verbose_name='parent'),
        ),
        migrations.AddField(
            model_name='field',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_contents.field_set+', to='contenttypes.contenttype'),
        ),
    ]