# Cipher-Suite
A CLI for performing encryption on local files

<p>Welcome to Cipher Suite, a way one stop for encrypting your local files. Why do that you ask? I say just for fun. It provides an extremely user-friendly CLI that anyone can understand (A basic knowledge of ciphers may be required, like for RSA) </p>

<p>Encryption Algorithms supported: <br>
  <ul>
    <li>Caesar cipher</li>
    <li>Vernam cipher</li>
    <li>Hill cipher</li>
    <li>Keyless/Column Transposition cipher</li>
    <li>RSA</li>
  </ul>
</p>

<p>File types supported : <br>
  <ul>
    <li>Any file </li>
    <li>Any folder containing files </li>
    <li>Any password protected or unprotected zip file</li>
    <li>Or literally anything else (a wildcard '*' can also be entered) </li>
  </ul>
</p>

<p>You can save the output in the format :
  <ul>
    <li>All files in a folder</li>
    <li>All files in a zipped file (which can be password protected) </li>
    <li>All processed files in zipped file and a separate keys file for easy access</li>
  </ul>
</p>

<h3>Features</h3>
<ul>
  <li>After every encryption/decryption, a "keys" file is generated in the same output folder. The file contains details regarding the process including the keys</li>
  <li>This keys file can be locked inside a locker folder with a password. Pretty cool. Only for Windows currently though :(</li>
  <li>The keys file is by default made read-only to avoid any accidental changes.</li>
  <li>The batch file created for locking/unlocking keys file is obfuscated automatically to prevent anyone from reading the password.</li>
  <li>A settings file is also there which has several parameters you can tweak with. It's in a simple JSON format so is highly readable. Even if you delete the settings file, it will be generated again with the default settings. Enjoy.</li>
</ul>

<p>I made this just for fun. Had a lot of time to kill after placements and was bored to death watching YouTube. So the code is not highly optimized and may look like a spaghetti code. I highly appreciate if you can expand on this idea. I personally found this pretty cool.</p>
