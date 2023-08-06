"""Get information on langauges from pycountry."""
from glob import glob
from warnings import warn

from pycountry import languages


def get_lang_dict():
    """Get a dict with code: name for each language that is in pycountry.

    Returns:
        dict: code: name for each alpha_3 code in pycountry
    """
    langdict = {}
    for lang in languages:
        langdict[lang.alpha_3] = lang.name
    return langdict


def get_available_languages(message_location, fileformat='json'):
    """Get a dict with code: name for each language that is in pycountry.

    Args:
        message_location (str): path to messages.  Example: /path/{}
        fileformat (str): filetype. Default: json.

    Returns:
        list: list of valid lanuages that have a file in messagelocation.

    Raises:
        ValueError: No languages could be found
    """
    available_languages = []
    pattern = f'{message_location.rstrip("/")}/*.{fileformat}'
    for name in glob(pattern, recursive=True):
        lang = name[:-(len(fileformat)+1)
                    ][len(message_location.rstrip('/'))+1:]
        print(lang)
        if lang in get_lang_dict():
            available_languages.append(lang)
        else:
            warn(
                f'{lang} was found at {name} but is not a valid language', Warning)
    if available_languages == []:
        raise ValueError(
            f'No languages were found matching: {pattern}. Did you specify the right location and format?')
    return available_languages
