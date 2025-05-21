from django.db import models


class Product(models.Model):
    product = models.CharField(max_length=200)
    prais = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product} (Quantity: {self.quantity}'


class Estimation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    laik = models.IntegerField(default=0)
    dlaik = models.IntegerField(default=0)


class Comit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comit = models.CharField(max_length=1000)


class Answer_comit(models.Model):
    comit = models.ForeignKey(Comit, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)


class Plyer(models.Model):
    ip = models.GenericIPAddressField()


class Clik(models.Model):
    plaer = models.ForeignKey(Plyer, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


class Level(models.Model):
    plaer = models.ForeignKey(Plyer, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
