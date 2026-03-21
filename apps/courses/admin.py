from django.contrib import admin
from .models import Plan, Course, Category, CourseModule, Lesson


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'price_formatted', 'enrolled_count', 'seats_available', 'is_active', 'is_featured']
    list_filter = ['tier', 'is_active', 'is_featured']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = []

    def enrolled_count(self, obj):
        return obj.enrolled_count
    enrolled_count.short_description = 'Enrolled'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 0
    fields = ['title', 'order', 'is_free_preview']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'duration_hours', 'is_published', 'is_featured', 'updated_at']
    list_filter = ['difficulty', 'is_published', 'is_featured', 'category', 'plans']
    search_fields = ['title', 'description', 'instructor']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['plans']
    inlines = [CourseModuleInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'plans', 'instructor', 'difficulty', 'duration_hours')
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'thumbnail', 'thumbnail_url')
        }),
        ('Learning Details', {
            'fields': ('what_you_learn', 'prerequisites', 'tools_covered'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured')
        }),
    )


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['title', 'content_type', 'duration_minutes', 'order', 'is_free_preview']


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'order', 'is_free_preview']
    list_filter = ['course']
    inlines = [LessonInline]
