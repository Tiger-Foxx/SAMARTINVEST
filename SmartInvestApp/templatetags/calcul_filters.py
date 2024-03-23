from django import template

register = template.Library()

@register.filter(name='soustraire_pourcentage')
def soustraire_pourcentage(value, percentage):
    try:
        # Convertit la valeur et le pourcentage en float et effectue le calcul
        value = float(value)
        percentage = float(percentage)
        return value - (value * percentage / 100)
    except (ValueError, TypeError):
        return value  # Retourne la valeur originale en cas d'erreur

@register.filter(name='calculer_pourcentage')
def calculer_pourcentage(montant, pourcentage):
    return montant * pourcentage / 100