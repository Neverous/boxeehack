#!/bin/sh
BASEDIR=`dirname $0`;
INSTALLDIR="/data/hack";
SOURCE="https://github.com/neverous/boxeehack/archive/modular.tar.gz";
SOURCE_NAME="boxeehack-modular";

# turn the logo red to indicate we're working
dtool 6 1 0 100;
dtool 6 2 0 0;

# stop Boxee from running and screwing things up
killall U99boxee; killall BoxeeLauncher; killall run_boxee.sh; killall Boxee; killall BoxeeHal;

# stop booxehack if exists
if [ -x "${INSTALLDIR}/boxeehack" ];
then
    ${INSTALLDIR}/boxeehack stop;
fi;

# make backup if already installed
if [ -d "${INSTALLDIR}" ];
then
    rm -Rf ${INSTALLDIR}-old;
    mv ${INSTALLDIR} ${INSTALLDIR}-old;
fi;

# install version from the USB drive
if [ -f "${BASEDIR}/boxeehack.tar.gz" ];
then
    # cleanup previous data
    rm -Rf /download/boxeehack;
    mkdir -p /download/boxeehack;

    # copy compressed version to temporary directory
    cp -aR ${BASEDIR}/boxeehack.tar.gz /download/boxeehack;
    cd /download/boxeehack;
    /bin/busybox tar xf boxeehack.tar.gz;

    # install files
    cp -aR /download/boxeehack/hack ${INSTALLDIR};

    # cleanup
    cd /;
    rm -Rf /download/boxeehack;

# download the latest version from $SOURCE
else
    # cleanup previous data
    rm -Rf /download/boxeehack;
    mkdir -p /download/boxeehack;

    # download latest version to temporary directory
    cd /download/boxeehack;
    /opt/local/bin/curl -L ${SOURCE} -o ${SOURCE_NAME}.tar.gz;
    /bin/busybox tar xf ${SOURCE_NAME}.tar.gz;

    # install files
    cp -aR /download/boxeehack/${SOURCE_NAME}/hack ${INSTALLDIR};

    # cleanup
    cd /;
    rm -Rf /download/boxeehack;
fi;

# enable boxeehack (make everything runnable and add script to hostname to run it every boot)
chmod +x ${INSTALLDIR}/boxeehack;
${INSTALLDIR}/boxeehack install;

# turn the logo back to green
sleep 3;
dtool 6 1 0 0;
dtool 6 2 0 50;
sleep 2;

# reboot to run boxeehack
reboot;
