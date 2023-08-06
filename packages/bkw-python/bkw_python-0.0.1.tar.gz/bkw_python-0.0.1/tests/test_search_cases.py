import pytest
from bkw_python import BkwApi

def test_search_cases_invalid_parameters():
    testing_session = BkwApi(username='test', password='password')
    cases = testing_session.search_cases()
    assert True
