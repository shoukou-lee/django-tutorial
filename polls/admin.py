from django.contrib import admin
from .models import Choice, Question

# Register your models here.

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['question_text']}),
        ('Date information',    {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    # 관리자 페이지에서 투표 이름만 보이던 것을 개선하기 위해, pub_date를 포함한 리스트로 관리한다.
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    
    # pub_date 필드에 의해 변경 목록을 필터링할 수 있게 해주는 Filter 사이드바 추가
    list_filter = ['pub_date']
    # 검색창 추가   
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)