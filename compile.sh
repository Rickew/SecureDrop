# requires pyinstaller
#linux
mkdir linuxdistro
cp ./Securedrop.py ./secure_drop.py
pyinstaller ./secure_drop.py --distpath ./releases/linux --onefile
cp ./releases/linux/secure_drop ./
rm secure_drop.py