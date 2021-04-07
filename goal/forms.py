# from django.forms import ModelForm
from .models import ClockIn, SetUp
from django import forms
from django_bootstrap5.widgets import RadioSelectButtonGroup


# class ClockInForm(ModelForm):
#     class Meta:
#         model = ClockIn
#         fields = "__all__"

class ClockInForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        # 动态的选项
        self._user = user
        super(ClockInForm, self).__init__(*args, **kwargs)
        self.fields['setup_id'] = forms.ChoiceField(
            label="选择打卡",
            widget=forms.RadioSelect,
            choices=(("1", "2"), ("2", "4"),),
            initial=1,
        )
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'
    setup_id = forms.ChoiceField(label="选择打卡类型")
    iamge_0 = forms.ImageField(label="图片")

    def save(self):
        user_id = self._user.id
        setup_id = self.cleaned_data['setup_id']
        image_0 = self.cleaned_data['iamge_0']
        # # image_1 = request.FILES['image_1']
        clock_in = ClockIn(
            user_id=user_id,
            setup_id=setup_id,
            image_0=image_0,
        )
        clock_in.save()
