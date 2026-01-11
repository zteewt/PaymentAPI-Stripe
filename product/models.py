from django.db import models

class Discount(models.Model):
    name = models.CharField(max_length=40)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    stripe_coupon_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=40)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    stripe_tax_rate_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Taxes"   


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    discount = models.ManyToManyField(Discount, blank=True)
    tax = models.ManyToManyField(Tax, blank=True)


    def __str__(self):
        return self.name
    
    def get_price_in_dollars(self):
        return f"${self.price / 100:.2f}"
    

class Order(models.Model):
    created_at = models.DateField(auto_now_add=True)
    discount = models.ManyToManyField(Discount, blank=True)
    tax = models.ManyToManyField(Tax, blank=True)

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_amount(self):
        return sum(orderitem.total_price() for orderitem in self.order_items.all()) / 100
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    snapshot_price = models.PositiveIntegerField(blank=True)

    def save(self, *args, **kwargs):
        if not self.snapshot_price:
            self.snapshot_price = self.item.price
        super().save(*args, **kwargs)

    def total_price(self):
        return self.quantity * self.snapshot_price
    
    def template_price_in_dollars(self):
        return self.quantity * self.snapshot_price / 100