import os
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name
from .image import transform_image_to_data_uri


def get_lexer_from_filetype(filetype='py'):
    mapping = {
        'py': 'python'
    }

    if filetype in mapping:
        return mapping[filetype]
    else:
        raise ValueError('Filetype ' + filetype + ' not supported')


def get_data_uri_snippet(file, filetype='py', gift_escape=True):
    lexer = get_lexer_from_filetype(filetype)
    snippet = load_snippet(file)
    image = highlight(snippet, get_lexer_by_name(lexer), get_formatter_by_name('png'))
    return transform_image_to_data_uri(image)


def load_snippet(file):
    assert os.path.exists(file)
    with open(file) as file_object:
        return file_object.read()
