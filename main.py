#!/usr/bin/env python

from __future__ import print_function
import os, sys, getpass
from subprocess import Popen, PIPE

if sys.argv[1] == "configure" :
    sudo_pw = getpass.getpass("Sudo password: ")

    # Enable firewall
    os.system ("iptables -L")
    print ("=-= FIREWALL ENABLED =-=")

    # Install gufw
    os.system ("apt-get install gufw")
    print ("=-= GUFW INSTALLED =-=")

    os.system ("apt-get update; apt-get upgrade")

    # Once, there was a system without sshd. This just ensures that no problems occur
    os.system ("apt-get install openssh-server")
    print ("=-= OPENSSH INSTALLED =-=")

    # Copy configuration file
    os.system ("cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")

    # Disable root
    with open ("/etc/ssh/sshd_config", "a") as f :
        f.write ("PermitRootLogin no")
        f.write ("PasswordAuthentication no")

    # Restart sshd
    os.system ("service ssh restart")
    print ("=-= SSH RESTARTED =-=")

    # Install Cracklib
    os.system ("apt-get install libpam-cracklib")
    print ("=-= CRACKLIB INSTALLED =-=")


    # Disable IP spoofing
    os.system ("cp /etc/host.conf /etc/host.conf.bak")

    with open ("/etc/host.conf", "a") as f :
        f.write ("order bind,hosts\nnospoof on")



    for user in os.listdir ("/home") :
        """
            Code for changing password from here: http://stackoverflow.com/questions/13179126/how-to-change-a-linux-user-password-from-python
        """
        user = str(user)
        sudo_password_callback = lambda: sudo_pw
        username, username_newpassword = user, "CyberPatriot1!"

        try:
            hashed = crypt(username_newpassword) # use the strongest available method
        except TypeError: # Python < 3.3
            p = Popen(["mkpasswd", "-m", "sha-512", "-s"], stdin=PIPE, stdout=PIPE,
                      universal_newlines=True)
            hashed = p.communicate(username_newpassword)[0][:-1] # chop '\n'
            assert p.wait() == 0
        assert hashed == crypt(username_newpassword, hashed)

        p = Popen ([
            "sudo",
            "-S",
            "usermod",
            "-p",
            hashed,
            username
        ],
        stdin=PIPE,
        universal_newlines=True)
        p.communicate (sudo_password_callback()+'\n')
        assert p.wait() == 0
        # Foriegn code ends here

        os.system ("chage -m 7 -M 30 -I 10 -W 14 "+user)

    print ("=-= PASSWORDS CHANGED AND AGES SET =-=")

    os.system ("apt-get install fail2ban")
    os.system ("gedit /etc/fail2ban/jail.conf")

    os.system ("/usr/lib/lightdm/lightdm-set-defaults --allow-guest false")

    os.system ("restart lightdm")

elif sys.argv[1] == "find" :
    tofind = sys.argv[2]
    if tofind == "media" :
        tosearch = [
            ".mp3",
            ".mp4",
            ".ogg",
            ".webm"
        ]
    elif tofind == "script" :
        tosearch = [
            ".py",
            ".js",
            ".php",
            ".c",
            ".java"
        ]
    elif tofind == "text" :
        tosearch = [
            ".txt",
            ".rtf"
        ]
    else :
        tosearch = [tofind]

    if sys.argv[3] :
        loc = sys.argv[3]
    else :
        loc = "/"

    for item in tosearch :
        for root, dirs, files in os.walk (loc) :
            for f in files :
                if f.endswith (item) :
                    print (os.path.join (root, f))

elif sys.argv[1] == "nc" :

    # Code that uses ps and grep to search for NetCat backdoors
    p1 = Popen(["ps", "-e"], stdout=PIPE)
    p2 = Popen(["grep", "[^a-zA-Z]/*nc"], stdin=p1.stdout, stdout=PIPE, close_fds=True)
    # Displays results
    print ("Possible backdoors")
    print (" PID Originating commands")
    for line in p2.stdout.readlines() :
        if not ((line[(25-45):].strip() == 'python ./main.py nc') or (line[(25-43):].strip() == 'python main.py nc')): # Skips over current process
            # Displays PID and process command
            print (line[1:5], line[25:].strip())
