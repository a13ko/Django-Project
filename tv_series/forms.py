from django import forms
from tv_series.models import Comment,CommentEpisode

class CommentForm(forms.ModelForm):
    comment =  forms.CharField(widget=forms.Textarea(attrs={ 
        'placeholder':'Add Comment',
        'rows' : '2',
        'style':
                 ' text-align:left; padding:50px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; font-size: 16px; width: 100%;',
    }))
    class Meta:
        model = Comment
        fields = ('comment',)


class CommentEpisodeForm(forms.ModelForm):
    commentepisode =  forms.CharField(widget=forms.Textarea(attrs={ 
        'placeholder':'Add Comment',
        'rows' : '1',
        'style':
                 ' text-align:left; padding:50px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; font-size: 16px; width: 100%;',
    }))
    class Meta:
        model = CommentEpisode
        fields = ('commentepisode',)

