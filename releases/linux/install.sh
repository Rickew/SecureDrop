cp ./secure_drop /usr/bin/
chmod +x /usr/bin/secure_drop
cp -r ./scdusers /home/$SUDO_USER/.scdusers
chown $SUDO_USER:$(id -gn) /home/$SUDO_USER/.scdusers