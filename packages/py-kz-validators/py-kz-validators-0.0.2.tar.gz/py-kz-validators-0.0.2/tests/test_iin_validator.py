import pytest

from kz.validators import IIN, IINValidationError


def test_validate_iin_success():
    assert IIN.is_valid('791028302728')


@pytest.mark.parametrize(
    'iin',
    [
        '12345678901D',  # contains non-numeric characters
        '123',  # too short
        '1234567890123',  # too long
        '010101600586',  # invalid control digit
    ],
)
def test_validate_iin_failure(iin):
    assert IIN.is_valid(iin) is False


@pytest.mark.parametrize(
    'iin, expected',
    [
        ('12345678901D', 'Value must contain only numeric values and exact 12 symbols'),
        ('010101600586', 'IIN is not valid'),
    ],
)
def test_validate_iin_raise_exception(iin, expected):
    with pytest.raises(IINValidationError) as exc_info:
        IIN.is_valid(iin, raise_exception=True)

    assert str(exc_info.value) == expected
