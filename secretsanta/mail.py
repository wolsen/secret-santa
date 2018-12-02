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

from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from datetime import datetime as dt
import os
import six
import smtplib

# Get the directory for this file.
SECRET_SANTA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'templates')
j2env = Environment(loader=FileSystemLoader(SECRET_SANTA_DIR),
                    trim_blocks=False)


class SantaMail(object):
    """
    The SantaMail object is used to send email. This class will load email
    templates that should be sent out (the master list email and the email
    for each Secret Santa.

    Templates will be loaded from the template directory and is configurable
    via the template_master and template_santa configuration variables.
    """
    REQUIRED_PARAMS = ['author', 'email', 'smtp', 'username', 'password']

    def __init__(self, author, email, smtp, username, password,
                 template_master="master.tmpl", template_santa="santa.tmpl"):
        self.author = author
        self.email = email
        self.smtp = smtp
        self.username = username
        self.password = password
        self.template_master = template_master
        self.template_santa = template_santa

    def send(self, pairings):
        """
        Sends the emails out to the secret santa participants.

        The secret santa host (the user configured to send the email from)
        will receive a copy of the master list.

        Each Secret Santa will receive an email with the contents of the
        template_santa template.
        """
        for pair in pairings:
            self._send_to_secret_santa(pair)

        self._send_master_list(pairings)

    def _do_send(self, toaddr, body, subject):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = toaddr

            server = smtplib.SMTP(self.smtp)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.email, [toaddr], msg.as_string())
            server.quit()
        except:
            print("Error sending email to %s!" % toaddr)

    def _send_to_secret_santa(self, pair):
        """
        Sends an email to the secret santa pairing.
        """
        (giver, receiver) = pair
        template = j2env.get_template(self.template_santa)
        body = template.render(giver=giver, receiver=receiver)
        year = dt.utcnow().year
        subject = ('Your %s Farmer Family Secret Santa Match' % year)
        self._do_send(giver.email, body, subject)

    def _send_master_list(self, pairings):
        """
        Sends an email to the game master.
        """
        pair_list = []
        for pair in pairings:
            (giver, recipient) = pair
            pair_list.append("%s -> %s" % (giver.name, recipient.name))

        template = j2env.get_template(self.template_master)
        body = template.render(pairs=pair_list)
        year = dt.utcnow().year
        subject = ('%s Farmer Family Secret Santa Master List' % year)
        self._do_send(self.email, body, subject)
