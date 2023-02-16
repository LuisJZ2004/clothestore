# Generated by Django 4.1.5 on 2023-02-16 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0029_alter_pledge_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='pub_date',
            field=models.DateField(default=datetime.date(2023, 2, 16)),
        ),
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
