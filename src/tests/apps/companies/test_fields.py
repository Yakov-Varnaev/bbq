from companies.api.fields import LowercaseCharField


def test_to_internal_value(lowercase_char_field: LowercaseCharField) -> None:
    assert lowercase_char_field.to_internal_value("Hello World") == "hello world"


def test_to_representation(lowercase_char_field: LowercaseCharField) -> None:
    assert lowercase_char_field.to_representation("Hello World") == "hello world"


def test_ignore_whitespaces(lowercase_char_field: LowercaseCharField) -> None:
    input_value = "   Hello World   "

    assert lowercase_char_field.to_internal_value(input_value) == "hello world"
    assert lowercase_char_field.to_representation(input_value) == "hello world"
