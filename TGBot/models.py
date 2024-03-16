from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone


# Create your models here.
class TGUserManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class TGUser(models.Model):
    objects = TGUserManager()
    tg_id = models.IntegerField(primary_key=True, verbose_name="Ідентифікатор")
    tg_username = models.CharField(max_length=100, verbose_name="Нікнейм в Telegram", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="ПІБ")
    instagram_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Нікнейм в Instagram")
    mail_address = models.CharField(max_length=100, blank=True, null=True, verbose_name="Пошта")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    registered = models.DateTimeField(default=timezone.now, auto_created=True)

    def __str__(self):
        return f"{self.name}|{self.phone}"

    class Meta:
        verbose_name = "абітурієнт"
        verbose_name_plural = "абітурієнти"


class Slider(models.Model):
    priority = models.IntegerField(verbose_name="Пріорітет відображення")
    image = models.ImageField(upload_to='images/', verbose_name="Рисунок")

    class Meta:
        verbose_name = "слайд"
        verbose_name_plural = "слайди"


class Specialty(models.Model):
    priority = models.IntegerField(verbose_name="Пріорітет відображення")
    image = models.ImageField(upload_to='specialty/', verbose_name="Рисунок")
    title = models.CharField(max_length=200, verbose_name="Підпис спеціальності")

    class Meta:
        verbose_name = "спеціальність"
        verbose_name_plural = "спеціальності"


TEMPLATE_BLOCKS_CHOICES = (
    ("START", "СТАРТ"),
    ("CONTACTS", "КОНТАКТИ"),
    ("SPECIALTY", "СПЕЦІАЛЬНОСТІ"),
)


class TemplateBlock(models.Model):
    # for start template and etc
    image = models.ImageField(upload_to='tmp_blocks/', verbose_name="Рисунок", blank=True, null=True)
    description = models.TextField(max_length=800, verbose_name="Підпис", null=True, blank=True)
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_BLOCKS_CHOICES,
        verbose_name="Тип шаблону"
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "шаблон"
        verbose_name_plural = "шаблони"


class Admins(models.Model):
    user = models.ForeignKey(TGUser, on_delete=models.CASCADE, default=0, verbose_name="Адміністратор")

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "адміністратор"
        verbose_name_plural = "адміністратори"
