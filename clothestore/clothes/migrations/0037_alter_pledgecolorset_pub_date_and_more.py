# Generated by Django 4.1.5 on 2023-04-17 14:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0036_ipaddress_alter_pledgecolorset_pub_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledgecolorset',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 17, 14, 52, 1, 91434, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='PledgeColorSetVisualisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clothes.ipaddress')),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothes.pledgecolorset')),
            ],
        ),
    ]
