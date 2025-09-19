from py_8pzzl.utils import capture_input, live_update, print_table


def a_star():
    pass


def run() -> None:
    params = capture_input()
    while True:
        live_update(lambda: print_table(params[0][1]))
