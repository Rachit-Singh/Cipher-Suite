@if (@CodeSection == @Batch) @then


@echo off
setlocal DisableDelayedExpansion

REM Obfuscate.bat: Obfuscate Batch files
REM Antonio Perez Ayala

if "%~1" equ "" echo Usage: Obfuscate filename.bat & goto :EOF
if not exist "%~1" echo File not found: "%~1" & goto :EOF

set "at=@"
set "pass=%random%"
(
   echo %at%if (@Pass == @X%pass%^) @begin
   echo    @echo off
   echo    CScript //nologo //E:JScript.Encode "%%~F0" ^> %pass%.bat
   echo    call %pass%
   echo    del %pass%.bat
   echo    exit /B
   echo %at%end 
   echo //**Start Encode**
   echo var a = new Array(^);

   set "i=0"
   for /F "usebackq delims=" %%a in ("%~1") do (
      set /A i+=1
      set "line=%%a"
      setlocal EnableDelayedExpansion
      echo a[!i!] = '!line:'=\x27!';
      endlocal
   )

   setlocal EnableDelayedExpansion
   echo for ( var i=1; i^<=!i!; ++i ^) WScript.Stdout.WriteLine(a[i]^);
) > "%~N1.tmp"

CScript //nologo //E:JScript "%~F0" "%~N1.tmp"
del "%~N1.tmp"
goto :EOF


@end


// Encode a JScript source file
// Antonio Perez Ayala

var fileToEncode = WScript.Arguments(0);

// Read the source file

var oFSO = WScript.CreateObject("Scripting.FileSystemObject");
var oFile = oFSO.GetFile(fileToEncode);
var oStream = oFile.OpenAsTextStream(1);
var sSourceFile = oStream.ReadAll();
oStream.Close();

// Encode the file

var oEncoder = WScript.CreateObject("Scripting.Encoder");
var sDest = oEncoder.EncodeScriptFile(".js",sSourceFile,0,"")

// Write the encoded version

var sFileOut = fileToEncode.slice(0,-3)+"obf.bat";
var oEncFile = oFSO.CreateTextFile(sFileOut);
oEncFile.Write(sDest);
oEncFile.Close();