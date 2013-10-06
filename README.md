goat-tower
==========

* [Initial Ideas](#whiteboard)
* [Installation](#install)
* [Design](#design)
    * [Actors](#actors)
    * [Attributes](#attributes)
    * [Commands](#commands)


<a name="whiteboard" />
## Initial Ideas
http://i.imgur.com/wQM9vkr.jpg

<a name="install" />
## Installation/Use
1. git clone git@github.com:nijotz/goat-tower
1. cd goat-tower
1. mkvirtualenv goat-tower
1. pip install -r requirements.txt
1. createdb goattower
1. cd goattower
1. python load.py objects/test_location.yaml yaml
1. python cli.py 3 look
1. python cli.py 3 north
1. etc...

<a name="design" />
## Design
The design of Goat Tower is relatively simple. Goat Tower is a heavily MOO influenced, relational and modifiable game.

<a name="actors" />
The game consists of a world, which is populated by Actors. Actors have several key properties and a list of attributes. The key properties are as follows:

* Parent ID
* Name
* is_player

Every Actor has a parent actor, because everything is inside of something else (probably). It is possible to build a graph wherein several nodes exist with no parents. The decision behind this choice was to allow for diversity in locomotion, mainly that you can move north, south, or into weird complex situations like 'move temporally into the past' or 'move south into Jimmy's mind'.

<a name="attributes" />
In addition to the key attributes of every actors are certain mutable attributes. These are designed to be things like 'zombiness', 'sickness', 'health', 'panic', 'resemblance to President Reagan' or really anything else that can be thought of. This is to keep the game dynamic and modifiable from inside.

For example, you could construct an Actor such that using 'look' in it's vicinity would set the player on fire, or a self-perpetuating memetic virus that overrides every say command with the rick roll text. 

<a name="commands" />
The command structure is hierarchical in a similar fashion to the Actor model. Actions on Actors can be accomplished with an augmented subset of simple CRUD commands. Deleting, modifying or creating new attributes, in addition to things that cannot be implemented using those like `say_text`.

The precedence for command execution is a fall through structure that goes Game -> Player Actor -> Children Actors -> Parent Actor -> Children of the Parent Actor. This allows you to have certain system commands that will not be overridden by uppity actors.

When executing commands, a lookup in the database is performed to see if the current item in the precedence chain has a corresponding command (Command.regex). If it does, another lookup is performed to get any Code objects that correspond to that command.

This structure lets you have many commands that can be executed at once, or a rich command that sets you on fire, moves you north and lowers your health attribute to 0 while displaying the text 'Fire destroys the room you are in'.

The syntax for getting commands to work is currently in flux.
