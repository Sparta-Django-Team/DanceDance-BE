# Generated by Django 4.2.7 on 2023-11-08 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_remove_originalvideo_challenge_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='originalvideo',
            name='hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='parent_tag_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenges.tag'),
        ),
    ]