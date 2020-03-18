#include <file.au3>
#include <Array.au3>

Opt("TrayIconHide",1)

;initialization
Global $IsActivation=0
FileDelete(@HomeDrive & "\IsActivation")
FileDelete(@HomeDrive & "\IsNotActivation")
;call main function
_Main()

;main function
Func _Main()
	;determine whether to activate, mark the "IsActivation" parameter, and press the OK button at the same time
	If WinExists("Windows Script Host","已授权") Or WinExists("Windows Script Host","已取得授權") Or WinExists("Windows Script Host","Licensed") Then
		$IsActivation=1
		_FileCreate(@HomeDrive & "\IsActivation")
	Else
		_FileCreate(@HomeDrive & "\IsNotActivation")
	EndIf
EndFunc
