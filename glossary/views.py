from django.shortcuts import render
from .models import Term
def term_list(request):
    q, letter = request.GET.get("q", "").strip(), request.GET.get("letter", "")
    terms = Term.objects.filter(published=True)
    if q: terms = terms.filter(term__icontains=q)
    if letter: terms = terms.filter(letter=letter.upper())
    return render(request, "glossary/list.html", {"terms": terms, "q": q, "selected_letter": letter, "letters": Term.objects.filter(published=True).values_list("letter", flat=True).distinct()})
