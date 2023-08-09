import functools


def input_error(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter both name and phone"

    return inner