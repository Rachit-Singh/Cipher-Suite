# Cipher-Suite
A CLI for performing encryption on local files

<p>Welcome to Cipher Suite, a way one stop for encrypting your local files. Why do that you ask? I say just for fun.</p>

<p>It provides an extremely user-friendly CLI that anyone can understand (A basic knowledge of ciphers may be required, like for RSA) </p>

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
  </ul>
</p>

<b>USEFUL NOTES</b>
<p>After every encryption/decryption, a "keys" file is generated in the same output folder. The file contains details regarding the process including the keys</p>
<p>A settings file is also there which has several parameters you can tweak with. It's in a simple JSON format so is highly readable. Even if you delete the settings file, it will be generated again with the default settings. Enjoy.</p>

<p>I made this just for fun. Had a lot of time to kill after placements and was bored to death watching YouTube. So the code is not highly optimized and may look like a spaghetti code. I higly appreciate if you can expand on this idea. I found this pretty cool.</p>
