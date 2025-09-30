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


class TaskStatus(models.Model):
    class Meta:
        db_table = "comapanies_task_status"

    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=155)


class Task(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
