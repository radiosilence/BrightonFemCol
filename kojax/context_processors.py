def kojax(request):
    parent = 'nokojax.html'
    if request.kojax:
        parent = 'kojax.xml'
    return {
        'kojax': {
            'parent': parent
        }
    }