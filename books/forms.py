from books.models import Book, Book_Review
from django import forms


class Book_ReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = Book_Review
        fields = ('stars_given', 'body')
    
    def __init__(self, *args, **kwargs):
        super(Book_ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name=='body':
                field.widget.attrs.update({'class': 'input', 'placeholder':'Add a comment',})
            else:
                field.widget.attrs.update({'class': 'input'})


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'description', 'cover_img', 'isbn')

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name=='description':
                field.widget.attrs.update({'class': 'textarea', 'placeholder': 'Book description'})
            else:
                field.widget.attrs.update({'class': 'input', 'placeholder': f'Book {name}'})
