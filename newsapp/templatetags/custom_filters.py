from django import template
register = template.Library()

@register.filter
def censor(value):
    censored_words = {'редиска', 'дурак', 'идиот'}

    if not isinstance(value, str):
        raise ValueError("Фильтр censor может применяться только к строкам")

    result = []
    word_buffer = []
    def process_word(word_chars):
        if not word_chars:
            return ''
        word = ''.join(word_chars)
        if word.lower() in censored_words:
            return word[0] + '*' * (len(word) - 1)
        else:
            return word

    for char in value:
        if char.isalpha():
            word_buffer.append(char)
        else:
            result.append(process_word(word_buffer))
            word_buffer = []
            result.append(char)

    result.append(process_word(word_buffer))

    return ''.join(result)
