;————————————————————————————————————————
; File: setup.iss
;————————————————————————————————————————

[Setup]
; — Thông tin ứng dụng —
AppName=LTTEAM Free Video
AppVersion=1.0.2
AppPublisher=LTTEAM

; — Thư mục cài đặt —
; Mặc định vào %LOCALAPPDATA%\LTTEAM Free Video (trên ổ C:), user có quyền đọc/ghi
DefaultDirName={localappdata}\LTTEAM Free Video

; — Quyền —
; Không đòi UAC/Admin
PrivilegesRequired=none

; Hiển thị trang chọn folder, tắt chọn program group
DisableProgramGroupPage=no

; — Icon & Output —
SetupIconFile=icon.ico
OutputBaseFilename=LTTEAM_Free_Video_Setup


[Files]
; Chỉ copy đúng các thư mục & file project, không chạm đến thư mục Output
Source: "app\*";               DestDir: "{app}\app";             Flags: recursesubdirs createallsubdirs ignoreversion
Source: "LyTranTextToVideo\*"; DestDir: "{app}\LyTranTextToVideo";Flags: recursesubdirs createallsubdirs ignoreversion
Source: "resource\*";          DestDir: "{app}\resource";        Flags: recursesubdirs createallsubdirs ignoreversion
Source: "sites\*";             DestDir: "{app}\sites";           Flags: recursesubdirs createallsubdirs ignoreversion
Source: "webui\*";             DestDir: "{app}\webui";           Flags: recursesubdirs createallsubdirs ignoreversion
Source: "config.toml";         DestDir: "{app}";                  Flags: ignoreversion
Source: "icon.ico";            DestDir: "{app}";                  Flags: ignoreversion
Source: "LTTEAM.exe";          DestDir: "{app}";                  Flags: ignoreversion
Source: "main.py";             DestDir: "{app}";                  Flags: ignoreversion

[Icons]
; Shortcut trên Desktop
Name: "{commondesktop}\LTTEAM Free Video"; Filename: "{app}\LTTEAM.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"

; Shortcut trong Start Menu → Programs
Name: "{group}\LTTEAM Free Video";           Filename: "{app}\LTTEAM.exe"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"

[Run]
; Cho phép user chọn có chạy ngay sau cài không
Filename: "{app}\LTTEAM.exe"; Description: "Launch LTTEAM Free Video"; Flags: nowait postinstall skipifsilent
