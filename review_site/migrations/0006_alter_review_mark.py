# Generated by Django 5.1.3 on 2024-12-05 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review_site', '0005_alter_review_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='mark',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='5', max_length=10),
        ),
    ]