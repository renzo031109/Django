from django.shortcuts import render

posts = [
    {
        'Author': 'Renan',
        'Title': 'Great Day',
        'Content': 'First post content',
        'Date_posted': 'July 4, 2023'
    },
    {
        'Author': 'Analyn',
        'Title': 'Sad Boy',
        'Content': 'First post content',
        'Date_posted': 'July 4, 2023'
    },
]

# Create your views here.
def home(request):
    return render(request,'blog/home.html')

def about(request):
    return render(request,'blog/about.html')