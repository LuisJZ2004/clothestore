# Generated by Django 4.1 on 2022-08-08 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0005_pledge_brand_alter_brand_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='description',
            field=models.TextField(max_length=60, null=True),
        ),
    ]
