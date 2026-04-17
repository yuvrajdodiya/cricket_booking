from django.db import migrations, models


def create_default_ticket_types(apps, schema_editor):
    TicketType = apps.get_model('adminpenal', 'TicketType')
    defaults = [
        ('Gold', 1450),
        ('Platinum', 2450),
    ]
    for name, price in defaults:
        TicketType.objects.update_or_create(
            name=name,
            defaults={'price': price, 'is_active': True},
        )


def remove_default_ticket_types(apps, schema_editor):
    TicketType = apps.get_model('adminpenal', 'TicketType')
    TicketType.objects.filter(name__in=['Gold', 'Platinum']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('adminpenal', '0003_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('price', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['price', 'name'],
            },
        ),
        migrations.RunPython(create_default_ticket_types, remove_default_ticket_types),
    ]
