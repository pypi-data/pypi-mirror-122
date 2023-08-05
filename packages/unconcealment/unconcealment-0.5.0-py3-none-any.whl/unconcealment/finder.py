from typing import Final

from unconcealment.secret_pattern import SecretPattern

MAX_TESTED_LENGTH: Final = 5000


def contains_secret_pattern(tested: str, secret_pattern: SecretPattern) -> bool:
    """ Check if a string contains a secret using regexp"""
    if len(tested) == 0:
        return False
    for i in range(0, len(tested), MAX_TESTED_LENGTH):
        value = tested[i:i + MAX_TESTED_LENGTH]
        for inclusion in secret_pattern.value.inclusions:
            result = inclusion.match(value)
            if result is None:
                return False
    for exclusion in secret_pattern.value.exclusions:
        if exclusion.search(tested):
            return contains_secret_pattern(exclusion.sub('', tested), secret_pattern)
    return True
