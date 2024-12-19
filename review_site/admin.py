from django.contrib import admin
from .models import Company, Category, Review, Feedback


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "cat", "description")
    search_fields = ("name",)
    list_filter = ("cat",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("mark", "company", "user", "comment")
    search_fields = ("comment",)
    list_filter = ("mark",)


class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ("name", "email", "message")


admin.site.site_header = "ScoreXpert Admin Panel"
admin.site.site_title = "Admin Panel ScoreXpert"
admin.site.index_title = "Welcome!"
admin.site.register(Category)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Review, ReviewAdmin)
