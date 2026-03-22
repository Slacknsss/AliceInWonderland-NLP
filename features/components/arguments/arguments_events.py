import argparse

import requests


def arguments_events(registered_args: argparse.Namespace, args_action: dict[str, dict[str, function|list]]) -> None:
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
                *[getattr(registered_args, sub_arg) for sub_arg in data['sub_args']] or None
            )
            if result and not isinstance(result, requests.Response):
                print(result)

    return None
