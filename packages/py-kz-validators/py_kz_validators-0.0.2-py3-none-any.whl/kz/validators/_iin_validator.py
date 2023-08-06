import re


class IINValidationError(Exception):
    pass


class IIN:
    @classmethod
    def is_valid(cls, iin: str, raise_exception: bool = False) -> bool:
        if not re.match(r'[0-9]{12}', iin):
            if raise_exception:
                raise IINValidationError('Value must contain only numeric values and exact 12 symbols')
            else:
                return False

        splitted_iin_symbols_as_int = [int(value) for value in iin]
        weights = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
        control_digit = cls._calculate_control_digit(splitted_iin_symbols_as_int, weights)
        if control_digit == 10:
            weights = {3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2}
            control_digit = cls._calculate_control_digit(splitted_iin_symbols_as_int, weights)

        iin_is_valid = control_digit == splitted_iin_symbols_as_int[-1]
        if raise_exception and not iin_is_valid:
            raise IINValidationError(
                'IIN is not valid',
            )

        return iin_is_valid

    @staticmethod
    def _calculate_control_digit(splitted_iin: list[int], weights: set[int]) -> int:
        # in the zip method, the iterator stops when the shortest iterable is exhausted.
        # so last number of iin will be ignored

        return sum([weight * digit for weight, digit in zip(weights, splitted_iin)]) % 11
