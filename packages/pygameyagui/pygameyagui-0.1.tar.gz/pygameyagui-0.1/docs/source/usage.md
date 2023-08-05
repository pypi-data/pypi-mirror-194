# Usage

## Installation

Currently, you can download the zip package on github:

>[Pygame-YaGUI on GitHub](https://github.com/alxndremaciel/pygameyagui/archive/refs/heads/main.zip)

## Importing

Rename the folder `pygameyagui-main` to `pygameyagui` and put this folder in the same directory of your project. In your project you need to add the following:

```{eval-rst}
.. code-block:: python
    :linenos:

    import sys
    import pygame
    import pygameyagui as yagui

    pygame.init()
```

You are all set to use the Pygame-YaGUI environment. You will need to create an interface ({py:class}`pygameyagui.Interface`) that is necessary for hosting (any amount of) toolboxes ({py:class}`pygameyagui.base.toolbox.Toolbox`). Each toolbox can have (any amount of) your widgets. Have fun!

## Creating an Interface

Create an {py:class}`pygameyagui.Interface` object with:
```{eval-rst}
.. code-block:: python
    :linenos:

    interface = yagui.Interface()
```

```{eval-rst} 
.. autoclass:: pygameyagui.Interface
```

## Creating a Toolbox

Create a {py:class}`pygameyagui.base.toolbox.Toolbox` object with:

```{eval-rst}
.. autoclass:: pygameyagui.base.toolbox.Toolbox
``` 

## Creating a Widget

A Widget object can be of two types: _output_ and _input_