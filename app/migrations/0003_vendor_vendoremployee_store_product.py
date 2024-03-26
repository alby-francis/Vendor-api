# Generated by Django 4.2.11 on 2024-03-23 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_customeruser_login_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VendorEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('login_token', models.CharField(default='null', max_length=256)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('supervisor', 'Supervisor'), ('salesperson', 'Salesperson')], max_length=20)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('contact', models.CharField(max_length=200)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('manufacturer', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(max_length=20)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.store')),
            ],
        ),
    ]
