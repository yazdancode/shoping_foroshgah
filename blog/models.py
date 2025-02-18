import jdatetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from jalali_date import datetime2jalali
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


def persian_now():
    now = jdatetime.datetime.now()
    return now.togregorian()


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "پیش‌نویس"),
        ("published", "منتشر شده"),
    )

    title = models.CharField("عنوان", max_length=250)
    slug = models.SlugField(
        "اسلاگ", max_length=250, unique=True
    )  # Ensure global uniqueness
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="نویسنده",
    )
    body = models.TextField("متن")
    publish = models.DateTimeField("تاریخ انتشار", default=persian_now, db_index=True)
    created = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated = models.DateTimeField("آخرین بروزرسانی", auto_now=True)
    status = models.CharField(
        "وضعیت", max_length=15, choices=STATUS_CHOICES, default="draft", db_index=True
    )

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ("-publish",)
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "post_details",
            kwargs={"slug": self.slug, "pk": self.id},
        )

    def jalali_publish(self):
        return datetime2jalali(self.publish).strftime("%Y/%m/%d - %H:%M")

    def jalali_created(self):
        return datetime2jalali(self.created).strftime("%Y/%m/%d - %H:%M")

    def __repr__(self):
        return f"<Post(title={self.title}, status={self.status})>"


class Account(models.Model):
    GENDER_CHOICES = [
        ("male", "مرد"),
        ("female", "زن"),
        ("other", "سایر"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account", verbose_name="کاربران"
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name="جنسیت",
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=255, verbose_name="آدرس", null=True, blank=True
    )
    first_name = models.CharField(max_length=50, verbose_name="نام", default="")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی", default="")
    email = models.EmailField(
        max_length=254, verbose_name="ایمیل", unique=True, blank=True, null=True
    )
    password = models.CharField(max_length=128, verbose_name="رمز عبور")
    phone = models.CharField(
        max_length=11, verbose_name="تلفن", unique=True, null=True, blank=True
    )
    picture = models.ImageField(
        upload_to="profile_pictures/", verbose_name="عکس پروفایل", null=True, blank=True
    )
    age = models.PositiveBigIntegerField(
        default=0, verbose_name="سن کاربران", blank=True, null=True
    )
    created = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "حساب کاربری"
        verbose_name_plural = "حساب‌های کاربری"

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست"
    )
    name = models.CharField(max_length=100, verbose_name="نام")
    body = models.TextField(verbose_name="بدنه")
    publish = models.DateTimeField(
        "تاریخ فعال سازی", default=persian_now, db_index=True
    )
    created = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="آخرین به روز رسانی", auto_now=True)
    active = models.BooleanField(default=False, verbose_name="فعال")

    def __str__(self):
        return "نظر {} در مورد {}".format(self.name, self.post)

    class Meta:
        ordering = ("created",)
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
