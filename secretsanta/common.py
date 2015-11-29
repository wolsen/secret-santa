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

import six
import yaml


class Config(dict):
    """
    The configuration for the Secret Santa program. This will be read in
    from secret-santa.yaml
    """

    @property
    def participants(self):
        """
        Returns the list of participants
        """
        if 'participants' not in self:
            return None

        return [Participant(p) for p in self['participants']]

    @property
    def email(self):
        """
        Returns the email configuration
        """
        return self['email']

    @staticmethod
    def load(config_file='secret-santa.yaml'):
        """
        Loads the configuration from the specified config file.

        The configuration is in yaml format and should contain the necessary
        information regarding the list of participants, the restrictions
        which are in place, and which rules are in place for the current
        secret santa logic.
        """
        content = None
        with open(config_file, 'r+') as f:
            content = yaml.safe_load(f)

        return Config(content)


class Participant(dict):
    """
    A participant who is playing the secret santa game. The participant has
    various bits of information included:

    - name
    - email
    - spouse

    In which the name is the name of the Participant, the email is the email
    address for the participant, and the blacklist is a list of names the
    participant cannot be paired with (e.g. their spouse, etc).
    """

    @property
    def name(self):
        """
        Returns the name of the participant.
        """
        if 'name' in self:
            return self['name']
        return ''

    @property
    def email(self):
        """
        Returns the email address of the participant.
        """
        if 'email' in self:
            return self['email']
        return None

    @property
    def spouse(self):
        """
        Returns the spouse or significant other for this participant.
        """
        if 'spouse' not in self:
            return None

        return self['spouse'] or None

    def __hash__(self):
        return 31 * len(self['name'])
