# Generated by Django 2.2.5 on 2020-03-11 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qluis', '0004_auto_20200311_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='qgroup',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='E.g. the commissioner', null=True, on_delete=django.db.models.deletion.PROTECT, to='qluis.Person'),
        ),
    ]
