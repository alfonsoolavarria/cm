# Generated by Django 2.2.10 on 2020-04-29 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maracay', '0006_tools_hilo_en_proceso'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagosImagenes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('picture', models.ImageField(upload_to='imagespagos')),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_pago', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
