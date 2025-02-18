from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(
        max_length=7,
        default="#007bff",
        help_text="Выберите цвет в формате HEX (например, #ff5733)"
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    repo_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class MainPageSettings(models.Model):
    title = models.CharField(max_length=255, default="Welcome!")
    subtitle = models.TextField(default="Its description.")
    about_me = models.TextField(blank=True, default="Im very good.")
    contact_telegram = models.CharField(default="https://t.me", blank=True, max_length=255)
    contact_linkedin = models.CharField(default="https://linkedin.com", blank=True, max_length=255)
    contact_github = models.CharField(default="https://github.com", blank=True, max_length=255)
    contact_email = models.EmailField(default="support@localhost", blank=True)

    def __str__(self):
        return "Main Page Settings"
