"""Load messages from a folder into dict based on list of codes."""
from json import loads

from jsoni18n.languages import get_available_languages


def get_messages(language, messagefiles, fallback="eng", fileformat="json"):
    """Get a dict with message-name: value for a language based on file. Default to english version if missing.

    Args:
        language (str): language to load
        messagefiles (str): path to messages.  Example: /path/{}
        fallback (str): fallback language if requested is missing messages. Default: 'eng'
        fileformat (str): filetype. Default: json

    Returns:
        dict: message-name: value for each detected message

    Raises:
        ValueError: 'language' parameter does not match a valid language with a file.
    """
    available_lang_codes = get_available_languages(messagefiles, fileformat=fileformat)
    with open(
        f'{messagefiles.rstrip("/")}/{fallback}.{fileformat}', "r"
    ) as messagefileeng:
        messages = loads(messagefileeng.read())
        if language in available_lang_codes:
            if language != fallback:
                with open(
                    f'{messagefiles.rstrip("/")}/{language}.{fileformat}', "r"
                ) as messagefilelangs:
                    filedata = loads(messagefilelangs.read())
                    for message in filedata.keys():
                        messages[message] = filedata[message]
        else:
            raise ValueError("Language is not available")
    return messages
