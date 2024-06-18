# forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Recipient'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your message...'})