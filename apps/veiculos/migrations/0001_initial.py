# Generated by Django 5.2.1 on 2025-06-01 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Veiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('veiculo', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=100)),
                ('ano', models.IntegerField()),
                ('descricao', models.TextField()),
                ('vendido', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
