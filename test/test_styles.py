from fstringify.format import QuoteTypes, get_quote_type, set_quote_type
from fstringify import lexer
import pytest

# @pytest.fixture()
# def string():
#     yield

@pytest.mark.parametrize(argnames=['code', 'quote_type'],
                         argvalues=[("'abra'", QuoteTypes.single),
                                    ('"bobro"', QuoteTypes.double),
                                    ("'''abra'''", QuoteTypes.triple_single),
                                    ('"""bobro"""', QuoteTypes.triple_double)])
def test_get_quote_type_token(code, quote_type):

    chunk = list(lexer.get_chunks(code))[0]
    token = chunk.tokens[0]

    assert token.get_quote_type() == quote_type


@pytest.mark.parametrize(argnames=['code', 'quote_type'],
                         argvalues=[("'abra'", QuoteTypes.single),
                                    ('"bobro"', QuoteTypes.double),
                                    ("'''abra'''", QuoteTypes.triple_single),
                                    ('"""bobro"""', QuoteTypes.triple_double)])
def test_get_quote_type(code, quote_type):
    assert get_quote_type(code) == quote_type

@pytest.mark.parametrize(argnames='code',
                         argvalues=["'abra'", '"bobro"', "'''abra'''", '"""bobro"""'])
def test_cycle(code):
    assert set_quote_type(code, get_quote_type(code)) == code

import random
@pytest.mark.parametrize(argnames='quote_type', argvalues=QuoteTypes.all)
def test_initial_doesnt_matter(quote_type):
    code = random.choice(["'abra'", '"bobro"', "'''abra'''", '"""bobro"""'])
    assert get_quote_type(set_quote_type(code, quote_type)) == quote_type


def test_single():
    code = '"alpha123"'
    expected = "'alpha123'"

    assert set_quote_type(code, QuoteTypes.single) == expected

def test_single_from_triple():
    code = '"""alpha123"""'
    expected = "'alpha123'"

    assert set_quote_type(code, QuoteTypes.single) == expected

