Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c rating-crawler.bat"
oShell.Run strArgs, 0, false