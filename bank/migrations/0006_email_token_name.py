# Generated by Django 3.0.7 on 2021-09-16 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_email_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='email_token',
            name='name',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
    ]