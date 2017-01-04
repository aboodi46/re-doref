# Requirements Engineering DOREF assignment

This repository is the outcome of an assignment of *Requirements Engineering*'s
master course. The assignment is about defining a project mission and also write
its requirements usign the
[DOREF](https://www.pimes.fh-dortmund.de/gitlab/re-research-group/doref)
framework.

##TODO:

- [ ] Create PlantUML Diagrams

## Installing dependencies

First ```latex``` package have to be installed by running;

```
# apt-get install texlive-latex-base \
  texlive-latex-recommended	\
  texlive-latex-extra	\
  texlive-fonts-recommended	\
  texlive-lang-german

```
**Note:** if you have earlier installed graphviz or sphinx for python2.7, it is recommended to uninstall them before proceeding.

Now install ```graphviz``` by running;

```
# apt-get install graphviz
```

And finally install ```pip3``` by running;

```
# apt-get install python3-pip
```

## Virtual Environment

It is highly recommended to create a ```python``` ***virtual environment*** and
install DOREF framework in it. If ```pyvenv``` is not install, install it by
running;

```
# apt-get install python3-venv
```

Create the ***virtual environment*** running;

```
$ cd <project-root>
$ pyvenv venv
```

Activate the ***virtual environment*** running;

```
$ source <project-root>/venv/bin/Activate
```

### Installing DOREF

For building the code you need to install **DOREF** framework first. Since
the original repository didn't have support for installing the framework as
a ```pip``` package a ```fork``` was created with ```pip``` support. Install
DOREF running;

```
(venv)$ pip3 install  git+https://www.pimes.fh-dortmund.de/gitlab/pedro.cuadrachamorro/doref.git@master
```

## Build documentation

Build the documentation running;

```
(venv)$ cd <project-root>
(venv$ python main.py
```
