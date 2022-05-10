!define APP_NAME "UpotpuniMe"
Name "${APP_NAME}"

# define the name of the installer
Outfile "upotpuni_me_installer.exe"
 
# define the directory to install to, the desktop in this case as specified  
# by the predefined $DESKTOP variable
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "Install_Dir"

!include "MUI2.nsh"
!define MUI_PAGE_CUSTOMFUNCTION_SHOW DirectoryShow
!insertmacro MUI_LANGUAGE "Croatian"

Function DirectoryShow
    GetDlgItem $R0 $HWNDPARENT 1037
    ShowWindow $R0 ${SW_HIDE}
    GetDlgItem $R0 $HWNDPARENT 1038
    ShowWindow $R0 ${SW_HIDE}
FunctionEnd

Page directory
Page instfiles
UninstPage instfiles
 
# default section
Section
    # define the output path for this file
    SetOutPath "$INSTDIR"

	; Check to see if already installed
	  ReadRegStr $R0 HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString"

      StrCpy $R2 $R0 1
      ${If} $R2 == '"'
          StrCpy $R0 $R0 "" 1
      ${EndIf}
      StrCpy $R2 $R0 "" -1
      ${If} $R2 == '"'
        StrCpy $R0 $R0 -1
      ${EndIf}

	  IfFileExists $R0 +1 NotInstalled
      MessageBox MB_YESNO "${APP_NAME} is already installed. Uninstall the existing version?" /SD IDYES IDNO Quit
		Pop $R1
	  StrCmp $R1 2 Quit UninstallExisting
	Quit:
	  Quit
    UninstallExisting:
        StrCpy $1 "upotpunime.exe"

        DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
        DeleteRegKey HKLM SOFTWARE\${APP_NAME}
        DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Run"
        Delete "$SMPROGRAMS\${APP_NAME}.lnk"
        Delete "$SMPROGRAMS\Uninstall ${APP_NAME}.lnk"
        Delete "$DESKTOP\${APP_NAME}.lnk"
        RMDir /r "$INSTDIR"
	NotInstalled:
     
    # define what to install and place it in the output path
    File /r dist\run

    #AccessControl::GrantOnFile "$INSTDIR\run" "(BU)" "FullAccess"

    SetOutPath "$INSTDIR\run"
    CreateShortcut "$SMPROGRAMS\${APP_NAME}.lnk" "$INSTDIR\run\upotpunime.exe" "" "$INSTDIR\run\logo4.ico"
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\run\upotpunime.exe" "" "$INSTDIR\run\logo4.ico"

    WriteUninstaller "$INSTDIR\uninstall.exe"
    CreateShortCut "$SMPROGRAMS\Uninstall ${APP_NAME}.lnk" "$INSTDIR\uninstall.exe"
    
    WriteRegStr HKLM SOFTWARE\${APP_NAME} "Install_Dir" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1

    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Run" "${APP_NAME}" '"$INSTDIR\run\upotpunime.exe"'
SectionEnd

function un.onInit
	MessageBox MB_OKCANCEL "Permanantly remove ${APP_NAME}?" IDOK next
		Abort
	next:
functionEnd

!include "LogicLib.nsh"
Section Uninstall

    StrCpy $1 "upotpunime.exe"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKLM SOFTWARE\${APP_NAME}
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Run"
    Delete "$SMPROGRAMS\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\Uninstall ${APP_NAME}.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir /r "$INSTDIR"
    SetAutoClose false
SectionEnd

