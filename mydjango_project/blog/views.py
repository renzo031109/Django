from django.shortcuts import render

posts = [
    {
        'Author': 'Renan Rivera',
        'Title': 'Great Day',
        'Content': 'First post content',
        'Date_posted': 'July 4, 2023'
    },
    {
        'Author': 'Analyn Maglalang',
        'Title': 'Sad Boy',
        'Content': 'Second post content',
        'Date_posted': 'July 1, 2023'
    },
]

# Create your views here.
def home(request):
    context={
        'posts':posts
    }
    return render(request,'blog/home.html', context)

def about(request):
    return render(request,'blog/about.html',{'Title':'About'})