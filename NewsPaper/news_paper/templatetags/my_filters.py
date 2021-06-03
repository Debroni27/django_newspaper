from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    marked_words = ['плохие слова', 'мат', 'бранная лексика']
    for word in marked_words:
        if value == word:
            raise ValueError(f'Нельзя использовать {word} в тексте!')
    return str(value)