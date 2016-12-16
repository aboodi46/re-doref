#!/usr/bin/env python
# -*- coding: utf-8 -*-

from doref.ref import *

#------------------------------------------------------------
# example_method.py
# not really a method, but an example of how to use the framework
#
#------------------------------------------------------------
# World (Discourse Perspective)
# Semantic model of domain -> derive from Concept

# BEGIN EXAMPLE


class Actors(Concept):
    pass
# END EXAMPLE
#------------------------------------------------------------
# derive your specific structures for recurring subcapters from Chapter
# BEGIN EXAMPLE


class UseCaseDescription(Chapter):
        def __init__(self, name, content=None, pNode=None):
            if content is None:
                content = {'goal': "Goal of the use case",
                           'actor': "Actor who initiates the use case",
                           'description': "Detailed description of the flow of events"}
            Chapter.__init__(self, 'Use Case: ' + name, "", {}, pNode)
            Inf(content['goal'], {}, Chapter("Goal", "", {}, self))
            Inf(content['actor'], {}, Chapter("Actors", "", {}, self))
            Inf(content['description'], {}, Chapter("Description", "", {}, self))
# END EXAMPLE
