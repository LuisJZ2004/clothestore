# Generated by Django 4.1 on 2022-08-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0009_alter_pledge_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
