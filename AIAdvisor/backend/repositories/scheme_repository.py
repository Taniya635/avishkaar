
from mock_data.schemes import MOCK_SCHEMES


def get_all_schemes():
    return MOCK_SCHEMES


def get_scheme_by_id(scheme_id: str):
    for scheme in MOCK_SCHEMES:
        if scheme["scheme_id"] == scheme_id:
            return scheme

    return None
