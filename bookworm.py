import argparse
import requests
from features.lexical_diversity import lexical_diversity
from features.book_summarization import summarize_book
from features.book_card import make_book_card
from features.download_all_books import download_all_books
from features.components.fetch_cover import fetch_cover

args_action = {
    'lexdiv': {
        'action': lambda book_id: lexical_diversity(book_id),
        'sub_args': ['book_id']
    },
    'summarize': {
        'action': lambda book_id: summarize_book(book_id),
        'sub_args': ['book_id']
    },
    'card': {
        'action': lambda book_id: make_book_card(book_id),
        'sub_args': ['book_id']
    },
    'cover': {
        'action': lambda book_id: fetch_cover(book_id, True),
        'sub_args': ['book_id']
    },
    'download': {
        'action': lambda author, category: (
            download_all_books(author, None)
            if author is not None
            else download_all_books(None, category)
        ),
        'sub_args': ['author', 'category'],
        'optional_args': [
            ('--author', str),
            ('--category', str)
        ]
    }
}

def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """
    Validate combinations of arguments.

    ## Parameters
        **parser**: Arguments parser
        **args**: Arguments Namespace

    ## Returns
        None
    """

    selected_commands = [cmd for cmd in args_action if getattr(args, cmd)]

    if len(selected_commands) != 1:
        parser.error('You must specify exactly one command.')

    command = selected_commands[0]
    command_sub_args = args_action[command]['sub_args']

    if 'book_id' in command_sub_args:
        if args.book_id is None:
            parser.error(f'--{command} requires book_id.')

        bad_flags = []
        for flag in args._get_kwargs():
            if flag[1] and flag[0] not in command_sub_args and flag[0] not in args_action.keys():
                bad_flags.append(flag[0])

        allowed_commands = [cmd for cmd, data in args_action.items() if set(bad_flags).issubset(data['sub_args'])]

        if bad_flags:
            parser.error(f'{' / '.join(bad_flags)} can only be used with --{' --'.join(allowed_commands)}')
    else:
        found = 0
        for i, expected_arg in enumerate(command_sub_args):
            if getattr(args, expected_arg) is None and i == len(command_sub_args)-1 and found == 0:
                parser.error(f'--{command} requires at least {' or '.join(command_sub_args)}.')
            elif getattr(args, expected_arg) is not None:
                found += 1

def arguments_init() -> argparse.Namespace:
    """
    Get the Namespace of registered arguments.

    ## Parameters
        None

    ## Returns
        Argparse Namespace of registered args
    """

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    registered_sub_args = []

    for arg, data in args_action.items():
        group.add_argument(f'--{arg}', action='store_true')

        for opt_arg, arg_type in data.get('optional_args', []):
            parser.add_argument(opt_arg, type=arg_type)

        for sub_arg in data.get('sub_args', []):
            if sub_arg not in registered_sub_args and ('--'+sub_arg) not in [arg[0] for arg in data.get('optional_args', [])]:
                parser.add_argument(sub_arg, type=int, nargs='?')
                registered_sub_args.append(sub_arg)

    args = parser.parse_args()
    validate_args(parser, args)

    return parser.parse_args()

def arguments_events(registered_args: argparse.Namespace) -> None:
    """
    Add arguments event.

    ## Parameters
        **registered_args**: argparse Namespace of registered arguments
    
    ## Returns
        None
    """

    if not isinstance(registered_args, argparse.Namespace):
        raise TypeError('args parameter must be an argparse Namespace.')
    
    for arg, data in args_action.items():
        if getattr(registered_args, arg):
            result = data['action'](
                *[getattr(registered_args, sub_arg) for sub_arg in data['sub_args']]
                or None
            )
            if result and not isinstance(result, requests.Response):
                print(result)

    return None

if __name__ == '__main__':
    args = arguments_init()
    arguments_events(args)