# Requires pyinstaller

# Windows
pyinstaller ./Securedrop.py --distpath ./releases/windows --onefile
cp ./releases/windows/Securedrop.exe ./