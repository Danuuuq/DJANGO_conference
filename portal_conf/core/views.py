from django.shortcuts import render


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию; 
    # выводить её в шаблон пользовательской страницы 404 мы не станем.
    return render(request, 'core/404.html', status=404) 