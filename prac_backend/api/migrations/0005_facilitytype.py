# Generated by Django 5.0.6 on 2024-05-22 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_nama_equipment_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facility_types', to='api.facility')),
            ],
            options={
                'db_table': 'tbl_facility_types',
            },
        ),
    ]
