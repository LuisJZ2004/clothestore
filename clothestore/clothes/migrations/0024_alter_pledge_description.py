# Generated by Django 4.1.5 on 2023-01-31 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0023_alter_size_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='description',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
