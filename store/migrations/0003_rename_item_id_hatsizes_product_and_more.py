# Generated by Django 4.1 on 2022-09-28 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_hat_is_on_sale_outwear_is_on_sale_pants_is_on_sale_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hatsizes',
            old_name='item_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='outwearsizes',
            old_name='item_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='pantssizes',
            old_name='item_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='shoessizes',
            old_name='item_id',
            new_name='product',
        ),
    ]