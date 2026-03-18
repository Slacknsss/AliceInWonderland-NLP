import argparse
from features.lexical_diversity import lexical_diversity
from features.book_summarization import summarize_book
from features.book_card import make_book_card

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
    }
}

sub_args = [('book_id', int)]

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

    for arg in args_action.keys():
        group.add_argument(f'--{arg}', action='store_true')

    for sub_arg in sub_args:
        parser.add_argument(sub_arg[0], type=sub_arg[1])

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
            if result:
                print(result)

    return None

if __name__ == '__main__':
    args = arguments_init()
    arguments_events(args)