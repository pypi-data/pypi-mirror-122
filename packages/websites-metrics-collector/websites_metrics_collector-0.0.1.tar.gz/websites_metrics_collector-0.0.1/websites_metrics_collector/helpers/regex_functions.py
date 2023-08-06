def check_patterns_in_webpage(webpage_text: str, patterns: list) -> bool:
    """
    This function is responsible to check if if the given patterns exist in the webpage_text
    :param webpage_text:
    :param patterns:
    :return:
    """
    import re
    if type(patterns) is not list:
        return False
    for patter in patterns:
        if not re.search(patter, webpage_text):
            return False
    return True
