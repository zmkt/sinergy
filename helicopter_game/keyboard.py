import sys

import config


def read_key():
    """Читает одну клавишу без Enter (в терминале) или символ из потока ввода."""
    if sys.stdin.isatty():
        import termios
        import tty

        номер = sys.stdin.fileno()
        старые_настройки = termios.tcgetattr(номер)
        try:
            tty.setraw(номер)
            символ = sys.stdin.read(1)
        finally:
            termios.tcsetattr(номер, termios.TCSADRAIN, старые_настройки)
    else:
        # запуск со скриптом ввода: пропускаем переводы строк
        символ = sys.stdin.read(1)
        while символ in ("\n", "\r"):
            символ = sys.stdin.read(1)

    if символ == "" or символ == "\x03":     # конец ввода или Ctrl+C
        return "q"

    символ = символ.lower()
    return config.KEY_ALIASES.get(символ, символ)
