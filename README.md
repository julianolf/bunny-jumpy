# Bunny Jumpy
A platform game written in Python.

## Installing

### Requires

- [Python 3](https://www.python.org)
- [Pygame 1.9](https://www.pygame.org)

#### Downloading the source code
You can download the zip file by clicking at the button [Clone or Download] and selection the *Download ZIP* option and than extracting the content anywhere you want.

Another option is cloning the project, you can do that by opening a terminal and typing the following command:

```
$ git clone https://github.com/julianolf/bunny-jumpy.git
```

#### Python 3
There are many different ways to get Python 3 installed, I recommend following the instructions on [python's guide](https://docs.python-guide.org) website.

#### Pygame
It's highly recommended to use [Pipenv](https://pipenv.readthedocs.io) in order to install Pygame library under a virtual environment. Take a look at Pipenv's website for instructions on how to get it installed.

After installed Pipenv open a terminal and run the following commands:

```
$ cd path/to/bunny-jumpy # point to the source code directory
$ pipenv install
```

## Running

Open a terminal and run the following commands:

```
$ cd path/to/bunny-jumpy # point to the source code directory
$ pipenv run python main.py
```

TIP:

If you have [Make](https://www.gnu.org/software/make/#content) installed you can just run `$ make` instead of `$ pipenv run ...` command.
