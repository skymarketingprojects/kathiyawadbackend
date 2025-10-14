from django.shortcuts import render

def home(request):
    return render(request, 'base.html', {'page_name': 'Kathiyawad Home'})

"""
admin user - kathiyawad
password - kathiyawadBackend@123
"""