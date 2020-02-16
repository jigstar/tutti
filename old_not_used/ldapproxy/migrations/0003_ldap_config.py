# Generated by Django 2.2.5 on 2019-09-20 22:42

from django.db import migrations


def ldap_config(apps, schema_editor):
    ObjectClassMapping = apps.get_model('ldapproxy', 'ObjectClassMapping')
    AttributeMapping = apps.get_model('ldapproxy', 'AttributeMapping')
    LdapEntry = apps.get_model('ldapproxy', 'LdapEntry')
    LdapEntryObjectClasses = apps.get_model('ldapproxy', 'LdapEntryObjectClasses')
    Member = apps.get_model('qluis', 'Member')

    # Member table
    member_table = Member._meta.db_table
    member_oc = ObjectClassMapping.objects.create(name='inetOrgPerson',
                                                  key_table=member_table,
                                                  key_column='id')
    # Member name
    member_name_select = 'CONCAT({tbl}.first_name,\' \',{tbl}.last_name)'.format(tbl=member_table)
    member_name_attr = AttributeMapping.objects.create(object_class_mapping=member_oc,
                                                       name='cn',
                                                       select_expression=member_name_select,
                                                       from_tables=member_table)
    member_last_name_select = '{}.last_name'.format(member_table)
    member_last_name_attr = AttributeMapping.objects.create(object_class_mapping=member_oc,
                                                            name='sn',
                                                            select_expression=member_last_name_select,
                                                            from_tables=member_table)
    pass


def ldap_config_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('ldapproxy', '0002_auto_20190920_2215'),
        ('qluis', '0002_group_member')
    ]

    operations = [
        migrations.RunPython(ldap_config)
    ]