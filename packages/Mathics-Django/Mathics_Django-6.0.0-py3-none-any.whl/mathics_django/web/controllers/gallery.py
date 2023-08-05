"""
Handles "about" section: information about the Mathics Django installation:
configuration information, software information, OS, and machine information.

"""

from django.shortcuts import render

def gallery_page(request):
    """
    This view gives information about the version and software we have loaded.
    """
    return render(
        request,
        "gallery.html",
    )
