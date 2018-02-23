# Generated by Django 2.0.1 on 2018-02-23 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0030_auto_20180223_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiveOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='library.Document')),
                ('document_instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='library.DocumentInstance')),
                ('patron', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='library.PatronInfo')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='recordslog',
            name='document',
        ),
        migrations.RemoveField(
            model_name='recordslog',
            name='document_instance',
        ),
        migrations.RemoveField(
            model_name='recordslog',
            name='user',
        ),
        migrations.DeleteModel(
            name='RecordsLog',
        ),
    ]
