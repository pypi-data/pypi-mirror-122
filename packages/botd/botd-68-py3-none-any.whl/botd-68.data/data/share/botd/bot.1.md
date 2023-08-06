% BOT(1) BOTD version 67
% Bart Thate 
% Oct 2021

# NAME

**bot** - client version of the BOTD channel daemon, uses ~/.bot

# SYNOPSIS

 bot \<cmd\> \[key=value\] \[key==value\] 
    
# DESCRIPTION

**BOTD** is to achieve OS level integration of bot technology, a solid,
non hackable bot, that runs under systemd as a 24/7 background service.

# IRC

IRC configuration is done with the use of the cfg command.

> $ bot cfg server=\<server\> channel=\<channel\> nick=\<nick\> 

default channel/server is #botd on localhost.

# SASL

some irc channels require SASL authorisation (freenode,libera,etc.) and
a nickserv user and password needs to be formed into a password. You can use
the pwd command for this.

> $ bot pwd \<nickservnick\> \<nickservpass\>

after creating you sasl password add it to you configuration.

> $ bot cfg password=\<outputfrompwd\>

# USERS

if you want to restrict access to the bot (default is disabled), enable
users in the configuration and add userhosts of users to the database.

> $ bot cfg users=True

> $ bot met \<userhost\>

# RSS

if you want rss feeds in your channel install feedparser.

> $ sudo apt install python3-feedparser

add a url to the bot and the feed fetcher will poll it every 5 minutes.

> $ bot rss <url>

# COPYRIGHT

**bot** is placed in the Public Domain, no Copyright, no LICENSE.

# SEE ALSO

| https://pypi.org/project/botd
