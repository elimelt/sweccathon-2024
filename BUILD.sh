# Enter new venv
python3 -m venv venv                                           
source venv/bin/activate

# Install deps
python3 -m pip install -r requirements.txt

# Shut up pyinstaller
touch toc.py

# Compile to binary
pyinstaller --onefile toc.py

# Deactivate venv
deactivate

# Move executable to root
mv ./dist/toc .

# Remove generated files
rm -rf ./build/ ./dist/ ./toc.spec

mkdir build
mv ./toc ./build/
