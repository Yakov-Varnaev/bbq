from companies.api.fields import LowercaseCharField


def test_to_internal_value(lowercase_char_field: LowercaseCharField):
    assert lowercase_char_field.to_internal_value("Hello World") == "hello world"


def test_to_representation(lowercase_char_field: LowercaseCharField):
    result = lowercase_char_field.to_representation("Hello World")
    assert result == "hello world"


def test_ignore_whitespaces(lowercase_char_field: LowercaseCharField):
    input_value = "   Hello World   "
    internal_value = lowercase_char_field.to_internal_value(input_value)
    representation = lowercase_char_field.to_representation(input_value)

    assert internal_value == "hello world"
    assert representation == "hello world"
