# minecraft_server

Just some files that help set up a minecraft server on an [Oracle free tier VPS](https://github.com/Fitzsimmons/oracle-always-free-vps).

## Installation

ssh into your VPS, then:

```
# as root...
sudo su -

	# install required system packages
	apt update
	apt install curl nano vnstat tmux openjdk-19-jre-headless rclone git build-essential caddy python3-pip python3-dev python3-numpy python3-pil

	# temporarily disable the webserver
	systemctl disable --now caddy

	git clone https://github.com/Fitzsimmons/minecraft_server.git
	cp -rv minecraft_server/root/* /

	# set up the firewall
	iptables-restore < /etc/iptables/rules.v4

	# install the minecraft server manager
	git clone https://github.com/Edenhofer/minecraft-server.git
	cd minecraft-server
	make
	make install
	systemd-sysusers

	# find latest download url from here https://www.minecraft.net/en-us/download/server
	cd /srv/minecraft && curl -o minecraft_server.jar [https://whatever-download-url]

	# if you want to restore a backup, e.g.:
		rclone copy -P minecraft_backup:archive/minecraft_backups/2022_09_11_12.00.08.tar.gz .
		chown minecraft 2022_09_11_12.00.08.tar.gz
		minecraftd restore 2022_09_11_12.00.08.tar.gz

	# if you want to change any server settings do it now
	nano -w /srv/minecraft/server.properties

	# change the ownership of the minecraft files to the minecraft service user
	chown -R minecraft:minecraft /srv/minecraft

	# change the ownership of the overviewer files to the ubuntu user
	chown ubuntu:ubuntu /home/ubuntu/run_overviewer.sh /home/ubuntu/overviewer_config.py
	chmod a+x /home/ubuntu/run_overviewer.sh

	# change the ownership of the public overviewer website files to the ubuntu user and the caddy group
	mkdir -p /srv/http/overviewer
	chown ubuntu:caddy /srv/http/overviewer

	# edit Caddyfile to have the correct domain name
	nano -w /etc/caddy/Caddyfile

	systemctl enable --now minecraftd.service
	systemctl enable --now minecraftd-backup.timer
	systemctl enable --now minecraft-overviewer.timer
	systemctl enable --now caddy.service

	# use the minecraft server console to add operators and whitelisted players. To exit, first press Ctrl+b (nothing will appear to happen). Then press d. You should see a message that says [detached (from session minecraft)].
	minecraftd console
		[you can use minecraft console commands here, e.g.]
		whitelist JSFitzsimmons
		op JSFitzsimmons

	# Once you'd made yourself an operator, you can also just log in and issue the commands from in-game.

	# if you have a remote file storage service that's compatible with rclone (https://rclone.org/#providers), set it up
	# make sure to call the remote `minecraft_backup`. The backup files will be stored in `archive/minecraft_backups`.
		rclone config

		# modify the remote backup service if you don't like these defaults
		nano -w /usr/lib/systemd/system/minecraft-remote-backup.service

		systemctl enable --now minecraft-remote-backup.timer

	# exit back to being the "ubuntu" user
	exit

# edit the overviewer config file, e.g. to change the world name:
nano -w overviewer_config.py

# clone minecraft overviewer and build it
cd
git clone https://github.com/overviewer/Minecraft-Overviewer.git
cd Minecraft-Overviewer.git
python3 setup.py build

# Follow the steps from https://docs.overviewer.org/en/latest/running/#installing-the-textures to install the textures
```
