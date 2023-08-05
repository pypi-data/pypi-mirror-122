"""
Handles processing of search results, including key remapping,
type conversion, and restructuring.
"""

def _list_converter(elem, key, is_view):
    if key == 'item' and is_view:
        return elem[key]
    if isinstance(elem[key], list):
        return elem[key]
    return [elem[key]]

def _num_converter(elem, key, _):
    return int(elem[key])

def _string_converter(elem, key, _):
    if isinstance(elem[key], list):
        return elem[key][0]
    return elem[key]

def _restructure_conju_info(arr):
    for elem in arr:
        if not 'conjugation_info' in elem:
            return

        for key in list(elem['conjugation_info'].keys()):
            elem[key] = elem['conjugation_info'][key]

        del elem['conjugation_info']


CONVERTERS = {
    'category_info': _list_converter,
    'conju_info': _list_converter,
    'der_info': _list_converter,
    'error_code': _num_converter,
    'example_info': _list_converter,
    'item': _list_converter,
    'multimedia_info': _list_converter,
    'num': _num_converter,
    'link_target_code': _num_converter,
    'original_language_info': _list_converter,
    'pattern_info': _list_converter,
    'pronunciation_info': _list_converter,
    'pos': _string_converter,
    'ref_info': _list_converter,
    'rel_info': _list_converter,
    'sense': _list_converter,
    'sense_info': _list_converter,
    'sense_order': _num_converter,
    'start': _num_converter,
    'subword_info': _list_converter,
    'subsense_info': _list_converter,
    'sup_no': _num_converter,
    'target_code': _num_converter,
    'translation': _list_converter,
    'total': _num_converter
}
HANDLERS = {
    'conju_info': _restructure_conju_info
}
REMAPS = {
    'channel': 'data',
    'conju_info': 'conjugation_info',
    'der_info': 'derivative_info',
    'item': 'results',
    'lastBuildDate': 'last_build_date',
    'num': 'num_results',
    'ref_info': 'reference_info',
    'rel_info': 'related_info',
    'sup_no': 'homograph_num',
    'sense': 'meaning',
    'sense_info': 'meaning_info',
    'sense_order': 'order',
    'subsense_info': 'submeaning_info',
    'pos': 'part_of_speech',
    'start': 'start_index',
    'word_grade': 'vocabulary_grade',
    'trans_lang': 'language',
    'trans_word': 'word',
    'trans_dfn': 'definition',
    'total': 'total_results'
}


def _handle_remap(elem, key, rename, is_view):
    if key not in REMAPS:
        return

    new_key = REMAPS[key] if not (is_view and key == 'item') else 'result'
    rename.append([elem, key, new_key])

def _handle_conversion(elem, key, is_view):
    if key not in CONVERTERS:
        return

    elem[key] = CONVERTERS[key](elem, key, is_view)

def clean_data(obj: dict, is_view: bool) -> None:
    """
    Cleans and restructures the search result object.

    Args:
        obj: The raw return object.
        is_view: True if the object is a result of a view API query.
    """

    stack = [[obj, None]]
    rename = []
    handle = []

    while len(stack) > 0:
        [elem, key] = stack.pop()

        if key is not None:
            if elem[key] is None:
                del elem[key]
                continue

            _handle_remap(elem, key, rename, is_view)
            _handle_conversion(elem, key, is_view)

            elem = elem[key]

            if key in HANDLERS:
                handle.append([HANDLERS[key], elem])

        if isinstance(elem, list):
            for value in elem:
                stack.append([value, None])
        elif isinstance(elem, dict):
            for elem_key in elem:
                stack.append([elem, elem_key])

    for [container, old_key, new_key] in rename:
        container[new_key] = container[old_key]
        del container[old_key]

    for [handler, elem] in handle:
        handler(elem)

    if not is_view and 'data' in obj and not 'results' in obj['data']:
        obj['data']['results'] = []
