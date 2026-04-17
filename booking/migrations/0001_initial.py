from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminpenal', '0004_tickettype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price_per_ticket', models.PositiveIntegerField()),
                ('total_price', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ground', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='adminpenal.post')),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='adminpenal.tickettype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
