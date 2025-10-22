General
- windows 10/11 support
- currently coded in python, may change?

ClientGUI
- tkinter gui to display simple chatroom
	- maybe switch to PyQt / PySide
- connect to server through ip and port
	- default ip is local host (127.0.0.1) for testing.
	- default port is 5000
- user can set nickname
- currently no account system
- sends utf-8 messages
- has command line args to run
- required packages
	- socket, threading, tkinter, tkinter scrolledtext, argparse

Server
- hosts a chatroom for users to join and talk
- anyone can join, currently no password or verification implemented
- automatically hosts on local ip unless specified otherwise
- gathers host info from user if command line args not specified
	- command line args not tested
- required packages
	- socket, threading, argparse, datetime, os
- handles messages
	- all messages sent will be marked with timestamp and nickname
	- stores messages in ./Storage/chat_history.txt
	- all messages are currently plaintext
	- sends message history to new clients, persistant on shutdown
	- echoes data to cliens for them to display


