

def clean_space(data: str):
    return data.replace('\n', '').replace(' ', '').replace('\r', '').replace('\xa0', '')
