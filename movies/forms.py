from django import forms
from .models import Comment, Review

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={ 
        'placeholder':'Add Comment',
        'rows' : '2',
        'style': ' text-align:left; padding:50px 40px; background-color:#2b2b31; border-radius: 4px; border: 1px; color: #fff; font-size: 16px; width: 100%;',
    }))
    
    class Meta:
        model = Comment
        fields = ('comment',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'title']
