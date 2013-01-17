#!/bin/sh

INSTALLDIR="/data/hack";

# turn the logo red to indicate we're working
dtool 6 1 0 100;
dtool 6 2 0 0;

# stop Boxee from running and screwing things up
killall U99boxee; killall BoxeeLauncher; killall run_boxee.sh; killall Boxee; killall BoxeeHal;

# stop and disable booxehack
if [ -x "${INSTALLDIR}/boxeehack" ];
then
    ${INSTALLDIR}/boxeehack stop;
    ${INSTALLDIR}/boxeehack uninstall;
fi;

# remove all files
rm -Rf ${INSTALLDIR};

# turn the logo back to green
sleep 3;
dtool 6 1 0 0;
dtool 6 2 0 50:
sleep 2;

# reboot
reboot;
