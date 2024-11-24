# requires pyinstaller

#linux
pyinstaller ./Securedrop.py --distpath ./releases/linux --onefile
cp ./releases/linux/Securedrop ./