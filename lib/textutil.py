import re


def clean_source_tweet(source):
    """
    Menghilangkan tag html pada source
    """
    src = ""
    if source is not None:
        src = re.sub(r"""<.*?>""", "", source)
    return src


def truncate(text, max_length=140, pad_with_dot=True):
    """
    Men-truncate text secara manusiawi.
    """
    if len(text) > max_length:
        if pad_with_dot:
            return text[:max_length-3] + "..."
        else:
            return text[:max_length]
    return text


def get_or_else(var_dict, key, default_value):
    try:
        return var_dict[key]
    except KeyError:
        return default_value
