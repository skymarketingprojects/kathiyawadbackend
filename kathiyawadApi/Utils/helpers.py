
import urllib.parse
# NOTE: In a real Django project, settings.py is used for constants
BUSINESS_WHATSAPP_NUMBER = "919876543210" # Placeholder phone number

def createWhatsappLink(productName):
    """Creates a wa.me link with a pre-filled message."""
    message = f"Hello, I'm interested in the product: *{productName}*. Can you provide more details?"
    encodedMessage = urllib.parse.quote(message)
    return f"https://wa.me/{BUSINESS_WHATSAPP_NUMBER}?text={encodedMessage}"

def paginateData(queryset, request):
    """
    Helper function for pseudo-pagination.
    (In a real DRF app, use DRF's Paginator classes)
    """
    PAGE_SIZE = 10
    
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
        
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    
    count = queryset.count()
    totalPages = (count + PAGE_SIZE - 1) // PAGE_SIZE
    
    # Fetch the specific slice of data
    paginatedData = queryset[start:end]

    return {
        "count": count,
        "totalPages": totalPages,
        "currentPage": page,
        "data": paginatedData
    }