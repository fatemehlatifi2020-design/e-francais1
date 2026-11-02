from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='topics/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class GrammarTopic(models.Model):
    title= models.CharField(max_length=200, blank=True, verbose_name="عنوان درس")
    content=models.TextField(verbose_name='محتوای گرامر')
    order=models.PositiveBigIntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    text=models.TextField(max_length=2000, blank=True)
    level = models.ForeignKey(
            'Level',
            on_delete=models.CASCADE,
            null=True,
            blank=True,
            # verbose_name="سطح"
        )

   


    def __str__(self):
        return self.title


    
    class Meta:
        ordering = ['order', 'id']
        # verbose_name = "مبحث گرامر"
        # verbose_name_plural = "مباحث گرامر"


class GrammarClip(models.Model):
    topic= models.ForeignKey(
        GrammarTopic,
        on_delete= models.CASCADE,
        related_name="clips"
    )
    title= models.CharField(
        max_length=200,
        blank= True
    )

    video_file= models.FileField(
        upload_to='grammar_clips/',
        blank=True,
        null=True
     )
    video_url = models.URLField(
        blank=True,
        # verbose_name="لینک ویدئو"
    )

    order = models.PositiveIntegerField(
        default=0,
        # verbose_name="ترتیب نمایش"
    )

    is_published = models.BooleanField(
        default=False,
        # verbose_name="منتشر شده"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        # verbose_name="تاریخ ایجاد"
    )

    class Meta:
        ordering = ["order", "id"]
        # verbose_name = "کلیپ گرامر"
        # verbose_name_plural = "کلیپ‌های گرامر"

    def __str__(self):
        return self.title



class VocabularyTopic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level = models.ForeignKey(
        'Level',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='vocabulary_topics/',
        blank=True,
        null=True
    )






    def __str__(self):
        return self.title


class VocabularyCard(models.Model):
    topic = models.ForeignKey(
        VocabularyTopic,
        on_delete=models.CASCADE,
        related_name='cards'
    )
    word = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=100, blank=True)
    image = models.ImageField(
        upload_to='vocabulary_cards/',
        blank=True,
        null=True
    )
    audio = models.FileField(
        upload_to='vocabulary_audio/',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.word


private_audio_storage = FileSystemStorage(
    location=settings.PRIVATE_MEDIA_ROOT
)



class Dictation(models.Model):
    title = models.CharField(max_length=200)

    level = models.ForeignKey(
        'Level',
        on_delete=models.CASCADE
    )

    audio = models.FileField(
    storage=private_audio_storage,
    upload_to='dictation_audio/'
)

    text = models.TextField()

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class StudentProfile(models.Model):
        LEVEL_CHOICES=[
            ("A1", "A1- مبتدی"),
            ("A2", "A2-مقدماتی"),
            ("B1", "B1-متوسط"),
            ("B2", "B2-متوسط پیشرفته"),
            ("C1", "C1-پیشرفته"),

        ]
        user= models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="Student_Profile"
        )

        full_name= models.CharField(
            max_length=100,
            blank=True,
            # verbose_name="نام و نام خانوادگی"
        )

        level=models.CharField(
            max_length=2,
            choices=LEVEL_CHOICES,
            default="A1",
            # verbose_name="سطح زبان فرانسه",
        )

        def __str__(self):
            return self.user.username




class GrammarExercise(models.Model):

    LEVEL_CHOICES = [
        ("A1", "A1 - Débutant"),
        ("A2", "A2 - Élémentaire"),
        ("B1", "B1 - Intermédiaire"),
        ("B2", "B2 - Intermédiaire avancé"),
        ("C1", "C1 - Avancé"),
        ("C2", "C2 - Maîtrise"),
    ]

    OPTION_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]

    topic = models.ForeignKey(
        GrammarTopic,
        on_delete=models.CASCADE,
        related_name="exercises",
        # verbose_name="درس گرامر"
    )

    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        default="A1",
        # verbose_name="سطح"
    )

    question = models.CharField(
        max_length=500,
        # verbose_name="متن سؤال"
    )

    option_a = models.CharField(
        max_length=250,
        # verbose_name="گزینه A"
    )

    option_b = models.CharField(
        max_length=250,
        # verbose_name="گزینه B"
    )

    option_c = models.CharField(
        max_length=250,
        # verbose_name="گزینه C"
    )

    option_d = models.CharField(
        max_length=250,
        # verbose_name="گزینه D"
    )

    correct_option = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES,
        # verbose_name="پاسخ صحیح"
    )

    explanation = models.TextField(
        blank=True,
        # verbose_name="توضیح پاسخ"
    )

    order = models.PositiveIntegerField(
        default=0,
        # verbose_name="ترتیب نمایش"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        # verbose_name="تاریخ ایجاد"
    )

    class Meta:
        ordering = ["order", "id"]
        # verbose_name = "تمرین گرامر"
        # verbose_name_plural = "تمرین‌های گرامر"

    def __str__(self):
        return f"{self.topic.title} - {self.question}"



class ReadingPassage(models.Model):
    title=models.CharField(max_length=200, blank=True)
    text=models.TextField()
    level=models.ForeignKey(
        "level",
        on_delete=models.PROTECT,
        related_name="reading_passage",
    )
    topic=models.ForeignKey(
        "topic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reading_passages",

    )
    is_published=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ReadingQuestion(models.Model):
    passage = models.ForeignKey(
        ReadingPassage,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_text = models.CharField(max_length=500)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("a", "A"),
            ("b", "B"),
            ("c", "C"),
            ("d", "D"),
        ],
    )

    def __str__(self):
        return self.question_text




class Article(models.Model):

    title = models.CharField(
        max_length=200,
        # verbose_name="عنوان مقاله"
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        allow_unicode=True,
        # verbose_name="آدرس مقاله"
    )

    excerpt = models.TextField(
        max_length=500,
        blank=True,
        # verbose_name="خلاصه مقاله"
    )

    content = models.TextField(
        # verbose_name="متن مقاله"
    )

    image = models.ImageField(
        upload_to="articles/",
        blank=True,
        null=True,
        # verbose_name="تصویر شاخص"
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        # verbose_name="دسته‌بندی"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        # verbose_name="تاریخ ایجاد"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        # verbose_name="آخرین ویرایش"
    )

    is_published = models.BooleanField(
        default=False,
        # verbose_name="انتشار مقاله"
    )

    class Meta:
        ordering = ["-created_at"]
        # verbose_name = "مقاله"
        # verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title






