# Generated by Django 5.0 on 2024-07-09 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_remove_jobcategory_slug_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblisting',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobs.jobcategory'),
        ),
    ]