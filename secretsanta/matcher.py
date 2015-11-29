#!/bin/env python
#
# The MIT License (MIT)
# 
# Copyright (c) 2015 Billy Olsen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy
import random


def create_pairings(participants):
    """
    Determines the pairings and returns the set of tuples (giver, receiver)
    for this secret santa game.

    Start with all participants are both givers and receivers. In order to
    provide some randomness, start by shuffling the list of participants.
    """
    givers = copy.copy(participants)
    recipients = copy.copy(participants)
    pairings = set()

    for g in givers:
        r = choose_recipient(g, recipients)
        recipients.remove(r)
        pairings.add((g, r))

    return pairings


def choose_recipient(giver, recipients):
    """
    Selects a recipient at random from the recipients list and pairs him/her
    with the selected giver.

    If the first recipient chosen at random is not able to pair with the
    giver (due to rules in place), then the next person is tried. If all
    possible recipients fail, this method will raise an exception indicating
    that the current giver cannot be paired with the current recipients.
    """
    ordering = copy.copy(recipients)
    random.shuffle(ordering)

    try:
        ordering.remove(giver)
    except ValueError:
        # No guarantee that the giver is in the set of recipients
        pass

    for r in ordering:
        print("Giver %s (%s) to recipient %s (%s)" %
              (giver.name, giver.spouse, r.name, r.spouse))
        
	if not_married(giver, r):
            return r

    raise ValueError("Giver %s cannot be matched with any of the "
                     "recipients: %s" %
                     (giver.name, str([r.name for r in recipients])))


def not_married(g, r):
    """
    This is a rule which ensures that the giver is not married to the
    recipient.

    :param g: the giver
    :param r: the recipient
    :return: True if the giver is not married to the recpient, False
             if the giver and recipient are married
    """
    # Yes, this can be shortened but I find this logic easier to read
    if g.spouse == None or r.spouse == None:
        return True

    if g.spouse.lower() == r.name.lower():
        return False

    if g.name.lower() == r.spouse.lower():
        return False

    return True
