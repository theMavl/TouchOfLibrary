# Generated by Django 2.0.1 on 2018-02-06 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0021_auto_20180206_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patrontype',
            name='max_days',
        ),
        migrations.AddField(
            model_name='doctype',
            name='max_days',
            field=models.IntegerField(help_text='Maximum days for loan in regular case', null=True),
        ),
        migrations.AddField(
            model_name='doctype',
            name='max_days_bestseller',
            field=models.IntegerField(help_text='Maximum days for loan if document is bestseller', null=True),
        ),
        migrations.AddField(
            model_name='doctype',
            name='max_days_privileges',
            field=models.IntegerField(help_text='Maximum days for loan for privileged patrons', null=True),
        ),
        migrations.AddField(
            model_name='patrontype',
            name='privileges',
            field=models.BooleanField(default=False),
        ),
    ]