# Generated by Django 4.2.9 on 2024-03-12 11:55

from django.conf import settings
from django.db import migrations
from django.db.models import Q
from geonode.base.enumerations import LINK_TYPES

from geonode.base.models import Link, LocalAsset, ResourceBase



def migrate_files(apps, schema_editor):
    if hasattr(ResourceBase, "files"):
        # looping on available resources with files to generate the LocalAssets
        for resource in ResourceBase.objects.exclude(Q(files__isnull=True) | Q(files__exact=[])).iterator():
            # creating the local asset object
            asset = LocalAsset(
                title="files",
                description="Original uploaded files path",
                owner=resource.owner,
                location=resource.files
            )
            asset.save()
            # creating the association between asset and Link
            # lets check if a original link exists

            link = resource.link_set.filter(link_type="original").first()
            if link:
                # if exists, we can assign the asset to the link
                link.asset = asset
                link.save()
            else:
                # otherwise we create the link with the assigned asset
                Link.objects.create(
                    resource=resource.get_self_resource(),
                    asset=asset,
                    link_type="original",
                    name="Original",
                    url=resource.get_real_instance().download_url
                )


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0091_asset_remove_resourcebase_files_and_more"),
    ]

    operations = [
        migrations.RunPython(migrate_files, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="resourcebase",
            name="files",
        ),
    ]
