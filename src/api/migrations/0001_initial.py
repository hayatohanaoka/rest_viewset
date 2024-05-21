# Generated by Django 5.0.6 on 2024-05-21 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('detail', models.TextField(max_length=500)),
            ],
            options={
                'db_table': 'tbl_facilities',
            },
        ),
    ]
