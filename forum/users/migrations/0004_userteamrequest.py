# Generated by Django 3.0.4 on 2020-04-03 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200402_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTeamRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('email_was_send', models.BooleanField(default=False)),
                ('reject_cause', models.CharField(default='-----', max_length=255)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
