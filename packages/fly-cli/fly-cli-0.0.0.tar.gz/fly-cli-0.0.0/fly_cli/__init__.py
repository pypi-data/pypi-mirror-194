import argparse
import functools
import inspect
import os
import stat
import sys
import textwrap
import types

from inspect import Parameter, Signature


class FlyCLI():
    def __call__(self, obj):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='_command', metavar='command', required=True)
        for (name, method) in inspect.getmembers(obj, inspect.ismethod):
            if name[0] == '_':
                continue
            subparser = subparsers.add_parser(name)
            for parameter in inspect.signature(method).parameters.values():
                kwargs = {}
                if parameter.default is not Signature.empty:
                    kwargs['default'] = parameter.default
                if parameter.annotation and parameter.annotation is not Signature.empty:
                    kwargs['type'] = parameter.annotation
                if parameter.kind in [Parameter.POSITIONAL_ONLY] or parameter.default is Signature.empty:
                    subparser.add_argument(parameter.name, **kwargs)
                else:
                    subparser.add_argument(f'--{parameter.name}', **kwargs)
        args = vars(parser.parse_args(sys.argv[1:]))
        command = args.pop('_command')
        return getattr(obj, command)(**args)

    def stub(self, signature: str, filename: str):
        (module, cls) = signature.split(':')

        if module != 'fly':
            imports = f'from {module} import {cls}'

        contents = textwrap.dedent(f"""\
        #!/usr/bin/env python
        from fly_cli import FlyCLI
        {imports}


        def main():
            fly = FlyCLI()
            fly({cls}())

        if __name__ == '__main__':
            main()""")

        with open(filename, 'w') as f:
            f.write(contents)

        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR | stat.S_IXGRP)


def main():
    fly = FlyCLI()
    fly(fly)


if __name__ == '__main__':
    main()
