from django.contrib import admin
from .models import Level, Topic, VocabularyTopic, VocabularyCard, Dictation, GrammarTopic, GrammarClip,GrammarExercise
from .models import StudentProfile
from .models import ReadingPassage, ReadingQuestion
from .models import Article


# Register your models here.
admin.site.register(Level)
admin.site.register(Topic)
@admin.register(VocabularyTopic)
class VocabularyTopic(admin.ModelAdmin):
    search_fields=['title']
    list_filter = ('level',)
    search_fields = ('title',)



@admin.register(VocabularyCard)

class VocabularyCard(admin.ModelAdmin):

    search_fields=['word', 'order']


admin.site.register(Dictation)



@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display=("user", "full_name", "level")
    search_fields=("user__username", "full_name")
    list_filter=("level",)
    list_display_links=("user", "full_name")
    ordering=("user__username",)
    fieldsets=(
        ("اطلاعات حساب کاربری",{
            "fields":("user", )

        }),

        ("اطلاعات زبان‌آموز", {
            "fields": ("full_name", "level")
        }),

    )
class GrammarClipInline(admin.TabularInline):
    model = GrammarClip
    extra = 1
    fields = (
        "title",
        "video_file",
        "video_url",
        "order",
        "is_published",
    )
    ordering = ("order", "id")














@admin.register(GrammarTopic)
class GrammarTopicAdmin(admin.ModelAdmin):


    list_display = (
    "title",
    "level",
    "order",
    "created_at",
)
    search_fields = ("title", "content")
    ordering = ("order", "id")
    list_editable = ("order",)
    inlines = [GrammarClipInline]
    fieldsets = (
    ("اطلاعات درس", {
        "fields": ("title", "level", "order")
    }),
    ("متن آموزشی", {
        "fields": ("content", "text")
    }),
)

   

@admin.register(GrammarClip)
class GrammarClipAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "order",
        "is_published",
        "created_at",
    )
    list_filter = ("is_published", "topic")
    search_fields = ("title", "topic__title")
    ordering = ("topic__order", "order", "id")
    list_editable = ("order", "is_published")


@admin.register(GrammarExercise)
class GrammarExerciseAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "topic",
        "level",
        "correct_option",
        "order",
    )

    list_filter = (
        "level",
        "topic",
    )

    search_fields = (
        "question",
        "topic__title",
    )

    ordering = (
        "topic__order",
        "order",
        "id",
    )

    list_editable = (
        "order",
    )

    fieldsets = (
        ("اطلاعات تمرین", {
            "fields": (
                "topic",
                "level",
                "order",
            )
        }),
        ("سؤال و گزینه‌ها", {
            "fields": (
                "question",
                "option_a",
                "option_b",
                "option_c",
                "option_d",
                "correct_option",
            )
        }),
        ("توضیح پاسخ", {
            "fields": (
                "explanation",
            )
        }),
    )
@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    list_display=("title", "level", "topic", "is_published")
    list_filter=("level", "is_published")
    search_fields=("title", "topic", "text")
    fields=(
        "title",
        "text",
        "level",
        "topic",
        "is_published",

    )



@admin.register(ReadingQuestion)
class ReadingQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "passage", "correct_answer")
    list_filter = ("passage", "correct_answer")
    search_fields = ("question_text",)
    fields = (
        "passage",
        "question_text",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_answer",
    )





@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "created_at",
        "is_published",
    )

    list_filter = (
        "is_published",
        "category",
        "created_at",
    )

    search_fields = (
        "title",
        "excerpt",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = ("is_published",)


   

admin.site.site_header = "E Français Administration"
admin.site.site_title = "E Français Admin"
admin.site.index_title = "Welcome to the Admin Panel"

