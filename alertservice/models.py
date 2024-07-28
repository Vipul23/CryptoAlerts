from django.db import models

# Create your models here.

class Alert(models.Model):
    name = models.CharField(max_length=100) # User Assigned Alert Name
    symbol = models.CharField(max_length=10) # Coin Symbol
    set_price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of setting alert
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price to trigger alert
    status = models.CharField(max_length=100,default="Created") # Created, Triggered, Alerted, Cancelled
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', related_name='alerts', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + " : " + str(self.symbol)
    
    class Meta:
        ordering = ['updated_at']

