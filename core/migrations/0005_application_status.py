# Generated by Django 5.1.4 on 2024-12-17 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
