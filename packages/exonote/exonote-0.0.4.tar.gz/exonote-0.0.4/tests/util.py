def get_data(structure, element):
    for e, data in structure:
        if e == element:
            return data
    return None
