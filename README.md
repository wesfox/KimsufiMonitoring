# Kimsufi Monitoring

A very basic Kimsufi crawler which check if a type of server is available.

Check for the line below :

    searching_for = {
        "name":"KS-2",
        "ref":"1801sk13"
    }

to monitor another type of server. 'ref' is 'data-ref' attribute of the tr.zone-dedicated-availability block.

It seems to be : KS-n => 1801sk(n+11)

- KS-1 : 1801sk12
- KS-2 : 1801sk13
- KS-3 : 1801sk14
...
- KS-12 : 1801sk23

For Canada it's 1804 instead of 1801.

## Install

> ./install.sh

You also need to get a unique gmail password for the app. (you may need to add a 2 step auth in order to get this option available)
go -> https://myaccount.google.com/apppasswords?utm_source=google-account&utm_medium=web

> echo "myGmailPwd" > gg_mdp_access.txt

## Run

> ./launch.sh