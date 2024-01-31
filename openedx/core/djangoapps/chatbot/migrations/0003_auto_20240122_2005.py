# Generated by Django 3.2.20 on 2024-01-22 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_chatbotquery_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbotquery',
            name='error',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='chatbotquery',
            name='status',
            field=models.CharField(choices=[('idle', 'Idle'), ('pending', 'Pending'), ('failed', 'Failed'), ('succeeded', 'Succeeded'), ('canceled', 'Canceled')], default='idle', max_length=9),
        ),
    ]
