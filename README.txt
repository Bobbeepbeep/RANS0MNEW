RANSOM SAFE VISUAL SIMULATOR

This is a harmless visual simulator, not ransomware.
It does NOT scan real drives, encrypt files, modify the registry,
create startup entries, contact the network, or delete files.
The file paths shown are fictional display strings only.

BUILD A STANDALONE EXE WITHOUT INSTALLING PYTHON ON YOUR LAPTOP

1. Create a GitHub repository and upload the contents of this folder
   (including the hidden .github folder).
2. Open the repository's Actions tab.
3. Select "Build RANSOM standalone EXE".
4. Click "Run workflow" and wait for the Windows build to finish.
5. Open the completed workflow run and download the artifact named
   "RANSOMTRIAGE-Windows-EXE".
6. Extract the downloaded artifact. Run RANSOMTRIAGE.exe.

GitHub's temporary Windows runner installs Python only to package the app.
The resulting one-file EXE bundles the Python runtime and Pillow, so the
computer running the EXE does not need Python installed.

ESC exits the simulator at any time.
