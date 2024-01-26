from pathlib import Path


def path(schema_name):
    return str(Path(__file__).parent.parent.joinpath(f'schemas/{schema_name}'))
