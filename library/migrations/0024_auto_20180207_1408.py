# Generated by Django 2.0.1 on 2018-02-07 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0023_document_bestseller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentinstance',
            name='is_reference',
        ),
        migrations.AddField(
            model_name='document',
            name='is_reference',
            field=models.BooleanField(default=False, help_text='Reference materials can not be borrowed.'),
        ),
    ]