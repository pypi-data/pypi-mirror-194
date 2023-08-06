from .use_cases import Formatter
from .core import Codes


def output(function):

    def wrapper(*args, **kwargs):
        return_value = function(*args, **kwargs)

        print(return_value)
        if kwargs.get('flush'):
            print(Codes.line_up, end=Codes.line_clear)

    return wrapper


class Logger:
    name: str | None = None

    def __init__(self, name: str) -> None:
        self.set_name(name)

    @classmethod
    def set_name(cls, name: str):
        cls.name = name

    @classmethod
    @output
    def info(cls, *message, sep: str = '', flush: bool = False) -> str:
        prefix: str = Formatter.green(Formatter.bold('[INFO]'))
        instance_name: str = ''
        if cls.name:
            instance_name = Formatter.green(f'[{cls.name}]')
        output_message: str = Formatter.green(sep.join(map(str, message)))
        return f'{prefix}{instance_name} {output_message}'

    @classmethod
    @output
    def debug(cls, *message, sep: str = '', flush: bool = False) -> str:
        prefix: str = Formatter.blue(Formatter.bold('[DEBUG]'))
        instance_name: str = ''
        if cls.name:
            instance_name = Formatter.blue(f'[{cls.name}]')
        output_message: str = Formatter.blue(sep.join(map(str, message)))
        return f'{prefix}{instance_name} {output_message}'

    @classmethod
    @output
    def warning(cls, *message, sep: str = '', flush: bool = False) -> str:
        prefix: str = Formatter.yellow(Formatter.bold('[WARNING]'))
        instance_name: str = ''
        if cls.name:
            instance_name = Formatter.yellow(f'[{cls.name}]')
        output_message: str = Formatter.yellow(sep.join(map(str, message)))
        return f'{prefix}{instance_name} {output_message}'

    @classmethod
    @output
    def error(cls, *message, sep: str = '', flush: bool = False) -> str:
        prefix: str = Formatter.red(Formatter.bold('[ERROR]'))
        instance_name: str = ''
        if cls.name:
            instance_name = Formatter.red(f'[{cls.name}]')
        output_message: str = Formatter.red(sep.join(map(str, message)))
        return f'{prefix}{instance_name} {output_message}'
