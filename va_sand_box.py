from main import context, new_context


def context_landscape():
    landscape = 'новая фраза: {n.phrase}\n' \
                'imperative:\t{c.imperative} <- {n.imperative}\n' \
                'source:\t\t{c.source} <- {n.source}\n' \
                'subject:\t{c.subject} <- {n.subject}\n' \
                'location:\t{c.location} <- {n.location}\n' \
                'adverb:\t\t{c.adverb} <- {n.adverb}\n' \
                'addressee:\t{c.addressee} <- {n.addressee}\n' \
                'action:\t\t{c.action} <- {n.action}\n' \
                'intent:\t\t{c.intent} <- {n.intent}\n' \
                'text:\t\t{c.text} <- {n.text}\n'.format(c=context, n=new_context)
    return landscape
