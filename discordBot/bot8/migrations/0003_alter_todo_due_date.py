# Generated by Django 4.1.7 on 2023-03-09 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot8', '0002_alter_todo_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='due_date',
            field=models.DateTimeField(null=True),
        ),
    ]
