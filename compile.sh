# requires pyinstaller
#linux
pyinstaller ./Securedrop.py --distpath ./releases/linux --name secure_drop --onefile 
cp ./releases/linux/secure_drop ./