"""Define some fixtures to use in the project."""

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import query

@pytest.fixture(scope='session')
def pqo():
    """
    get pqo (Persistent Query Object)
    """
    return query.PersistentQueryObject()

@pytest.fixture(scope='session')
def get_something():
    """A session scope fixture."""
    return "Bubu was here"
