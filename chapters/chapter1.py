#!/usr/bin/env python
# -*- coding: utf-8 -*-


from header import *


cd("/*/Specific Requirements")

Chapter("Customer Requirements")
cd("./-")

Req("Clean at night",
    "The robot shall clean the appartment at night.",
    {'Priority': 1,
     'Effort': 20,
     'Optional': 1})

Req("Power",
    "The suction power must not exceed a given threshold.",
    {'Priority': 1})


Req("Silence", "The operation of the vacuum cleaner should be as silent as possible.",
    {'Priority': 2,
     'Trace': [node("./*/Power"), node("./*/Clean")]})
cd("./-")
Inf("The vacuum cleaner should not disturb the persons living in the apartment.")
cd("..")

Table("Characteristics of good requirements",
      [
          ['Characteristic', 'Explanation'],
          ['Complete', 'The requirement is fully stated in one place with no missing information.',
           'Consistent', 'The requirement does not contradict any other requirement and is fully consistent with '
                         'all authoritative external documentation.']
      ], "The characteristics of good requirements are variously stated by different writers, with each writer "
         "generally emphasizing the characteristics most appropriate to their general discussion or the specific "
         "technology domain being addressed. However, the following characteristics are generally acknowledged")
