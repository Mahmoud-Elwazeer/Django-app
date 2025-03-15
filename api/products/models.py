from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    def __str__(self):
        return self.name if not self.parent else f"{self.parent.name} → {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    is_stored = models.BooleanField(default=True)  # True = Requires quantity, False = No quantity
    available_quantity = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    # Images
    main_image = models.ImageField(upload_to="products/", null=False, blank=False)  # Required
    optional_image1 = models.ImageField(upload_to="products/", null=True, blank=True)
    optional_image2 = models.ImageField(upload_to="products/", null=True, blank=True)
    optional_image3 = models.ImageField(upload_to="products/", null=True, blank=True)

    def save(self, *args, **kwargs):
        """Ensure that stored products have quantity, and non-stored ones don’t."""
        if self.is_stored and (self.available_quantity is None or self.available_quantity < 0):
            raise ValueError("Stored products must have a valid available quantity.")
        if not self.is_stored:
            self.available_quantity = None  # Ignore quantity for non-stored products
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({'Stored' if self.is_stored else 'Non-Stored'})"
