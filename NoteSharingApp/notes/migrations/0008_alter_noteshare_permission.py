# Generated by Django 5.2.1 on 2025-07-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_alter_note_workspace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noteshare',
            name='permission',
            field=models.CharField(choices=[('view', 'View'), ('edit', 'Edit')], default='view', max_length=10),
        ),
    ]
