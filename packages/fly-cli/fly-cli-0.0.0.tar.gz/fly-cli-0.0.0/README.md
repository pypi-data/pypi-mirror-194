# fly

Invoke object methods from the command-line. WIP.

## install

Add this package to your dependencies in requirements.txt or use pip install:

```
pip install fly-cli
```

## usage

Let's say you have a class Client in module app (app.py) that you want to create a CLI for:

```
class Greeter:
    def greet(name, message='hi there'):
        print(f'{greet}, {name}')
```

Run this command to generate a stub:

```
fly stub app:Greeter greeter
```

This will create a binary called `greeter` with the following contents:

```
#!/usr/bin/env python
from fly_cli import FlyCLI
from app import Greeter


def main():
    fly = FlyCLI()
    fly(Greeter())

if __name__ == '__main__':
    main()
```

The FlyCLI class inspects the object and generates a sub-command for each method, analysing the method parameters to add arguments to the parser.

Now you can run the script to call an instance of the class:

```
> ./greeter greet --message="hola" bob
hola bob
```

Edit the script to add constructor arguments or configuration if required.

To add more subcommands, add more methods on the class.

If you add type annotations, it will coerce the values into the specified type when parsing arguments.
