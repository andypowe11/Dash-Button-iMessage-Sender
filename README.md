# Dash Button iMessage Sender

When I was a kid, my parents bought a primitive
intercom for our house - two grey boxes, one downstairs in the kitchen, one upstairs,
joined by wires. By pressing a button on the one downstairs a buzzer sounded upstairs and you could actually speak.
This was the mid-1970s and we thought it was awesome.

For about a week.

Then we realised that no-one really wanted to speak. But we still used the buzzer. When tea was ready, mum
or dad would sound the buzzer and we'd run downstairs, drooling like Pavlov's dogs!

Of course, now that we all have smart-phones such things seem quaint - we can communicate more flexibly with iMessage,
Twitter, Facebook Messenger and the rest. But I find myself regularly sending a txt with just the letter 't' to my son at
around 7pm
- he's 2 floors up in the loft conversion so it's the easiest way to tell him that tea is ready.

This project takes a standard Amazon Dash button and turns it into a tool for sending a message to
one of your contacts via iMessage on your iMac or Macbook. I use it to send a reminder to my son to either 1) come and have tea,
2) get out of bed in the morning or 3) pop downstairs (depending on the time of day that the button is pressed). It's
effectively like the buzzer on those grey boxes.

You can use it to send whatever messages you like.

There are plenty of example sites for hacking Dash buttons but most seem to be written for either Windows
or the Raspberry Pi and didn't work quite as expected under MacOS. The instructions below should get you up and
running on your favorite Apple computer.

## Set up the Amazon Dash button

Follow the instructions for configuring your Dash button but don't complete the final step, associating it with
a product. Quit before doing this. In doing so, you'll be giving the button enough information to connect to your
wifi network but leaving it unable to actually buy anything. It'll just flash red a few times when pressed.

If you are using an iPhone, you'll probably also want to disable notifications from the Amazon app -
otherwise it will keep reminding you to finish the setup process.

## Install Scapy

Scapy is a powerful interactive packet manipulation program - http://www.secdev.org/projects/scapy/. We're going to use
its Python library to monitor the network. I needed help with the install of Scapy (props to @guedou on Twitter for his advice)
because the standard way of doing it didn't work for me on my iMac.
For a working install, I cloned the scapy-bpf repository from GitHub -
https://github.com/guedou/scapy-bpf - and installed from there. I think the command was:

    sudo setup.py install

## Find the Dash button's MAC address

Run the finddash.py script:

    sudo finddash.py

Ignore the warning about 'No route found for IPv6 destination'. Press the Dash button once - it'll flash red a few times. The
MAC address should pop up (possibly with some other messages).
Repeat a couple of times to check you are seeing the button
and not something else.

## Configure and test dash2imessage.py

Edit the variables at the top of the dash2imessage.py file. Configure the email address of the person you want to
send an iMessage to and the newly discovered MAC address. Optionally change the filename of the file we'll be using to
track when the button was last pressed.

You're good to go. Run the command:

    sudo dash2imessage.py

Press the Dash button again. You should get an iMessage at your configured email address a few moments later.

## Run it as a daemon

Assuming everything worked, you now need to configure the script to run as a daemon. Put
the dash2imessage.py and dash2imessage.sh scripts somewhere permanent and make sure they are executable.
Edit the net.andypowe11.dash2imessage.plist file, changing the locations as necessary.
Note that launchd - http://launchd.info/ - calls the Shell script not the Python script. This allows it to set the environment
correctly before running Python.

Then do the following:

    sudo cp net.andypowe11.dash2imessage.plist /Library/LaunchDaemons/
    sudo launchctl load /Library/LaunchDaemons/net.andypowe11.dash2imessage.plist

It's possible that you'll need to reboot at this point but I don't think so. See how you get on.

That's it! Pressing the Dash button should now send an appropriate iMessage to your contact.
