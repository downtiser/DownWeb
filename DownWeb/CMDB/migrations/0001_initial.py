# Generated by Django 2.1 on 2018-09-07 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('region', models.CharField(max_length=32)),
                ('host_name', models.CharField(max_length=64)),
                ('host_ip', models.GenericIPAddressField()),
                ('host_port', models.IntegerField()),
                ('statue', models.CharField(default='running', max_length=64)),
                ('os', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('ctime', models.DateTimeField(auto_now_add=True, null=True)),
                ('uptime', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='hostinfo',
            name='user_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='CMDB.UserInfo'),
        ),
    ]