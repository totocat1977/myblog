from django import forms
from db.models import Comment
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['mbc_auther', 'mbc_auther_id', 'mbc_content', 'mbc_post_id', 'mbc_reply_id']
        labels = {
            'mbc_content': _('Content'),
                }
        widgets = {
            'mbc_content': Textarea(attrs={'rows': 5, 'class': 'uk-textarea uk-width-1-1', 'placeholder': _('Input your comment')}),
        }
