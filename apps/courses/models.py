from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Plan(models.Model):
    TIER_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Naira (NGN)")
    description = models.TextField()
    features = models.JSONField(default=list, help_text='List of feature strings')
    is_active = models.BooleanField(default=True)
    seats_available = models.PositiveIntegerField(default=50, help_text="0 = unlimited")
    is_featured = models.BooleanField(default=False)
    badge_text = models.CharField(max_length=50, blank=True, help_text="e.g., 'Most Popular'")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.name} (₦{self.price:,.0f})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:plan_detail', kwargs={'slug': self.slug})

    @property
    def price_formatted(self):
        return f"₦{self.price:,.0f}"

    @property
    def enrolled_count(self):
        return self.enrollments.filter(is_active=True).count()

    @property
    def seats_left(self):
        if self.seats_available == 0:
            return None
        return max(0, self.seats_available - self.enrolled_count)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default='shield', help_text="Bootstrap icon name")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    plans = models.ManyToManyField(Plan, related_name='courses', help_text="Which plans include this course")
    instructor = models.CharField(max_length=100, default='Eccentric Academy Team')
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_hours = models.PositiveIntegerField(default=0, help_text="Estimated hours to complete")
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, help_text="External thumbnail URL (fallback)")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    what_you_learn = models.JSONField(default=list, help_text='List of learning outcomes')
    prerequisites = models.JSONField(default=list, help_text='List of prerequisites')
    tools_covered = models.JSONField(default=list, help_text='List of tools/technologies covered')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['difficulty', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})

    @property
    def difficulty_color(self):
        colors = {
            'beginner': 'success',
            'intermediate': 'warning',
            'advanced': 'danger',
        }
        return colors.get(self.difficulty, 'primary')


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_free_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text/Article'),
        ('lab', 'Hands-on Lab'),
        ('quiz', 'Quiz'),
    ]

    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='text')
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    is_free_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.course.title} > {self.module.title} > {self.title}"
