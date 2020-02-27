# Generated by Django 2.2.6 on 2020-02-27 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qluis', '0009_auto_20200115_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='bhv_certificate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='external_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qluis.ExternalCard'),
        ),
        migrations.AlterField(
            model_name='person',
            name='external_card_deposit_made',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_student',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='membership_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='membership_start',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='permission_exquus',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='sepa_direct_debit',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='tue_card_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
