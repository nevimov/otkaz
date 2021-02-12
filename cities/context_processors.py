from .models import City


def cities(request):
    all_cities = City.objects.all().select_related('site')
    current_city, other_cities = None, []
    for city in all_cities:
        if city.site != request.site:
            other_cities.append(city)
        else:
            current_city = city

    return {
        'cities': {
            'all': all_cities,
            'current': current_city,
            'others': other_cities,
        }
    }