# Generated by Django 5.0 on 2024-07-06 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_job_employer'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblisting',
            name='company',
            field=models.CharField(default='Your Company Name', max_length=255),
        ),
    ]
