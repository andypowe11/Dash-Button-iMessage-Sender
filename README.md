# Dash Button iMessage Sender

This project takes a standard Amazon Dash button and turns it into something will send an iMessage to
one of your contacts via your iMac or Macbook. I use it to send a reminder to my son to either 1) come and have tea,
2) get out of bed or 3) pop downstairs (depending on the time of day that the button is pressed. You can
use it to do what you like.

There are plenty of example sites for hacking Dash buttons but most seem to be written for either Windows
or the Raspberry Pi and didn't work quite as expected under MacOS. The instructions below should get you up and
running with your favorite Apple computer.

## Set up your Amazon Dash button

Follow the instructions for configuring your Dash button but don't complete the final step, associating it with
a product. Quit before doing this step. Doing so, gives the button enough information for connecting the your
wifi network but leaves it unable to actually buy anything. It'll just flash red a few times when pressed.

You'll probably want to disable notifications from the Amazon app on your iPhone,
otherwise it will keep telling you to finish the setup process.

## Install scapy

I needed help with this because the standard way of instally scapy didn't work. Clone the scapy-bpf repository from GitHub -
https://github.com/guedou/scapy-bpf and install from there. I think the command was:

    setup.py install

## Find the button's  MAC address

Run the finddash.py script:

    sudo finddash.py

Ignore the warning about'No route found for IPv6 destination'. Press the Dash button once - it'll flash red a few times. Its
MAC address should pop up (possibly with some other messages. Repeat a couple of times to check you are seeing the button
and not something else.

## Configure dash2imessage.py

Edit the 3 variables at the top of the dash2imessage.py file. Put the email address of the person you want to
send an iMessage to, the newly discovered MAC address. Optionally change the filename of the file we'll be using to
track when the button was last pressed.

You're good to go. Run the command:

    sudo dash2imessage.py

Press the Dash button again. You should get an iMessage at your configured email address a few moments later.

## Run as a daemon

Assuming everything worked you now need to configure the script to run as a daemon. Put
the dash2imessage.py and dash2imessage.sh scripts somewhere permanent and make sure they are executable.
Edit the net.andypowe11.dash2imessage.plist file, changing the locations as necessary.
Then do the following:

    cp net.andypowe11.dash2imessage.plist /Library/LaunchDaemons/
    launchctl load /Library/LaunchDaemons/net.andypowe11.dash2imessage.plist

It's possible that you'll need to reboot at this point I'm not sure.

That's it, pressing the Dash button should now send an iMessage to your contact.
