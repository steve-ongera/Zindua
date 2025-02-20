# yourapp/management/commands/generate_order_ids.py
import random
import string
from django.core.management.base import BaseCommand
from myapp.models import Order

class Command(BaseCommand):
    help = 'Generate unique order IDs for all orders'

    def handle(self, *args, **options):
        orders = Order.objects.filter(order_id__isnull=True)
        count = orders.count()
        self.stdout.write(f'Generating IDs for {count} orders...')
        
        for order in orders:
            characters = string.ascii_uppercase + string.digits
            new_id = ''.join(random.choice(characters) for _ in range(6))
            order.order_id = new_id
            order.save()
        
        self.stdout.write(self.style.SUCCESS('Done!'))