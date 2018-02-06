# Generated by Django 2.0.1 on 2018-01-26 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_auto_20180127_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='document_instance',
        ),
        migrations.RemoveField(
            model_name='journal',
            name='document_instance',
        ),
        migrations.RemoveField(
            model_name='journalarticle',
            name='document_instance',
        ),
        migrations.RemoveField(
            model_name='journalarticle',
            name='journal',
        ),
        migrations.AddField(
            model_name='documentinstance',
            name='additional_info',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='documentinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Available'), ('g', 'Given out'), ('r', 'Reserved'), ('m', 'Maintenance')], default='d', max_length=1),
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Journal',
        ),
        migrations.DeleteModel(
            name='JournalArticle',
        ),
    ]