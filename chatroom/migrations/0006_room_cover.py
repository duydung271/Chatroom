# Generated by Django 3.2.8 on 2021-11-05 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0005_room_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='cover',
            field=models.ImageField(default='background.jpg', upload_to=''),
        ),
    ]
