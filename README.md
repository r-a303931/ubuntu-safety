ubuntu-safety
==============

Just a small python script I wrote that makes Linux a bit more secure.

Instructions for use:
---------------------

Until I can simplify part of the netcat search function, the program needs to remain named main.py

It takes certain arguments, currently 3 different ones.

### configure

Running `sudo ./main.py configure` will launch the main portion that starts SSH, enables GUFW and the firewall, etc.

### find

Running `sudo ./main.py find type [location]`, where type is either `media`, `script`, `text`, or something you put in yourself will search location for files ending in what you put in or ending in a predefined list of endings that goes with each option

### nc

Running `./main.py nc` will search for different netcat backdoors and give you the PID and command of these processes, since computer error may ruin everything.

MD5
---

This is a security script, right? It's supposed to be secure itself, so here is the MD5 hash

 > 4bd846f0aa886faa772cb18e31c7aea7
