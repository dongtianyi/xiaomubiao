# from django.forms import ModelForm
from .models import ClockIn, SetUp
from django import forms
# from django_bootstrap5.widgets import RadioSelectButtonGroup
from django.forms import ModelForm


class ClockInForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        # 动态的选项
        self._user = user
        super(ClockInForm, self).__init__(*args, **kwargs)
        self.fields['setup_id'] = forms.ChoiceField(
            label="选择打卡",
            widget=forms.RadioSelect,
            # choices=(("1", "2"), ("2", "4"),),
            choices=[(su.id, su.name)
                     for su in SetUp.objects.filter(user_id=user.id)],
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
        clock_in = ClockIn(
            user_id=user_id,
            setup_id=setup_id,
            image_0=image_0,
        )
        clock_in.save()


class SetUpForm(ModelForm):
    class Meta:
        model = SetUp
        fields = ['name', 'times']

    def save(self, user_id):
        # name = self.cleaned_data["name"]
        # times = self.cleaned_data["times"]
        data = {
            "name": self.cleaned_data["name"],
            "times": self.cleaned_data["times"],
            "user_id": user_id
        }
        setup = SetUp.objects.create(**data)
        setup.save()
