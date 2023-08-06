from idegui import IDEWindow


def is_delete(word: str):
    return word.strip().startswith(('break', 'return', 'continue', 'pass', 'raise'))


window = IDEWindow(__name__)
window.config.set('delete_indent', is_delete)
window.init()
window.show()
