import argparse

def arguments_init() -> argparse.Namespace:
    """
    
    """

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--lexdiv', action='store_true')
    parser.add_argument('id', action='store_true')

    return parser.parse_args()

def arguments_events(registered_args: argparse.Namespace) -> None:
    """
    
    """

    if not isinstance(registered_args, argparse.Namespace):
        raise TypeError('args parameter must be an argparse Namespace.')

    args_action = {

    }

    for arg, action in args_action:
        if registered_args[arg]:
            ...

    return None

if __name__ == '__main__':
    args = arguments_init()
    arguments_events(args)