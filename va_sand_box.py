from va_assistant import context, new_context
from va_assistant import assistant


def context_landscape():
    intent = assistant.intent
    landscape = 'imperative:\t{c.imperative}\n' \
                'target:\t\t{c.target}\n' \
                'subject:\t{c.subject}\n' \
                'location:\t{c.location}\n' \
                'adverb:\t\t{c.adverb}\n' \
                'addressee:\t{c.addressee}\n' \
                'text:\t\t{c.text}\n' \
                'assistant.intent:\t{intent}'.format(c=context, intent=intent)
    return landscape
