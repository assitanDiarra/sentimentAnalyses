# Generated by Django 2.0.3 on 2018-04-09 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentiments_analysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='sentiment_type',
            field=models.CharField(max_length=47, null=True),
        ),
    ]
