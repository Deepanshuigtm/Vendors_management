from django.db import models
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        total_completed_pos = completed_pos.count()

        if total_completed_pos == 0:
            return 0.0

        return (on_time_deliveries / total_completed_pos) * 100

    def calculate_quality_rating_avg(self):
        completed_pos_with_rating = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        total_completed_pos_with_rating = completed_pos_with_rating.count()

        if total_completed_pos_with_rating == 0:
            return 0.0

        total_quality_ratings = completed_pos_with_rating.aggregate(total_ratings=models.Sum('quality_rating'))['total_ratings']
        return total_quality_ratings / total_completed_pos_with_rating

    def calculate_average_response_time(self):
        completed_pos = self.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
        total_completed_pos = completed_pos.count()

        if total_completed_pos == 0:
            return None

        total_response_time = sum([(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos])
        return total_response_time / total_completed_pos

    def calculate_fulfillment_rate(self):
        total_pos = self.purchaseorder_set.count()
        if total_pos == 0:
            return 0.0

        successfully_fulfilled_pos = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=True).count()
        return (successfully_fulfilled_pos / total_pos) * 100

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"PO Number: {self.po_number}, Vendor: {self.vendor}, Status: {self.status}"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"