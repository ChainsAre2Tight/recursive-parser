from internals.parsing_utils.utils import transform


def construct_file_name_from_link(link: str, prefix: str = '', postfix: str = '') -> str:
    """Construct a file name if provided with a link to the scanned page, a prefix and a postfix"""
    link = transform(link).replace(".", "_")
    return f'{prefix}-{link}-{postfix}'


def validate_file_name(name: str) -> bool:
    for char in r'/\*&?.,$#@':
        if char in name:
            return False
    return True


if __name__ == "__main__":
    print(
        construct_file_name_from_link(
            'https://lox.example.com/aboba',
            'result',
            'l3'
        )
    )
