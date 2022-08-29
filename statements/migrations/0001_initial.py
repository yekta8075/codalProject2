# Generated by Django 4.0.6 on 2022-08-10 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement_title', models.CharField(max_length=300, null=True)),
                ('statement_json', models.JSONField()),
            ],
        ),
    ]
