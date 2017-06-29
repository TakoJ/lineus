from django import forms
from .models import Member

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('성명','생년월일','휴대번호','주소','성별','종류선택','등급','피트니스기간','필라테스기간','추가사항','락카개월수','병력및주의사항','운동시간대','결제금액','결제방식')

class PT_RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('등록세션','PT결제금액','PT결제방식')