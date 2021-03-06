# Generated by Django 2.2.3 on 2020-09-23 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='Product_pics')),
                ('name', models.CharField(max_length=100)),
                ('preview_text', models.TextField(max_length=200)),
                ('details', models.TextField(max_length=500)),
                ('price', models.FloatField()),
                ('old_price', models.FloatField(default=0.0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('catagory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catagory', to='app_shop.Category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
