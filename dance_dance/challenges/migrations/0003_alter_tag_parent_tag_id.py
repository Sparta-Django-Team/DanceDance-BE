# Generated by Django 4.2.7 on 2023-11-15 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_alter_originalvideo_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='parent_tag_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='challenges.tag'),
        ),
    ]
