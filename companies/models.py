from django.db import models


class Enterprise(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.name} - {self.enterprise.name}"
