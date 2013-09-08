for m in /media/*; do
	if [ -f ${m}/xbmc.bin ]; then
		cd ${m}
		/etc/rc3.d/U94boxeehal stop
		/etc/rc3.d/U99boxee stop
		killall BoxeeHal
		killall BoxeeLauncher
		killall Boxee
		killall run_boxee.sh
		mount -o bind /data/hack/xbmc.sh /opt/boxee/BoxeeLauncher
		break
	fi
done

