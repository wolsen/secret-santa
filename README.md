This is a program used to generate Secret Santa pairings. Given a set of
participants (or Santas), this program will randomly generate pairings of
giver to recipient.

# Getting Started

To get started to generate your own fun secret santa exchange list, the
following steps can be followed:

1. Open a terminal and `git clone https://github.com/wolsen/secret-santa`
2. Edit the secret-santa.yaml file, specifying the email information for
   the game-master and the list of recipients.
3. Edit the secretsanta/templates/santa.tmpl to configure the template which
   is sent to each of the secret santas.
4. Run the secret-santa tool (e.g. `python -m secretsanta.__init__ secretsanta`)
5. Have fun!

# The Game Master

The game master is the person that is configured such that the email is sent
from this person and email address. The game master will not only be the
originator of the outgoing secret santa emails, the game master will receive
a copy of the master selection list, which can be referred to later if one
of the santas forgets their recipient.


