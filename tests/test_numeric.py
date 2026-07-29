from fractions import Fraction

import pytest

from scp._numeric import is_float


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, True),
        (0.0, True),
        (False, False),
        (Fraction(1, 2), False),
        ("0.0", False),
    ],
)
def test_is_float(value: object, expected: bool) -> None:
    assert is_float(value) is expected
