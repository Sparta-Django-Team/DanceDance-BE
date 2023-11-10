# Generated by Django 4.2.7 on 2023-11-10 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0013_alter_uservideo_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='originalvideo',
            name='platform_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenges.platformtype'),
        ),
        migrations.AddField(
            model_name='uservideo',
            name='platform_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenges.platformtype'),
        ),
    ]
