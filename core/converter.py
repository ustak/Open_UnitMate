
def convert_units(value, input_unit, output_unit):
    if input_unit == "mm":
        mm_value = value
    elif input_unit == "um":
        mm_value = value / 1000.0
    elif input_unit == "inch":
        mm_value = value * 25.4
    elif input_unit == "mil":
        mm_value = value * 0.0254
    else:
        raise ValueError(f"Invalid input unit: {input_unit}")

    if output_unit == "mm":
        return mm_value
    elif output_unit == "um":
        return mm_value * 1000.0
    elif output_unit == "inch":
        return mm_value / 25.4
    elif output_unit == "mil":
        return mm_value / 0.0254
    else:
        raise ValueError(f"Invalid output unit: {output_unit}")
