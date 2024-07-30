#define MyAppName "Niv_Louie"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "Me"
#define URL "http://example.com"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=.
OutputBaseFilename={#MyAppName}-installer

[Files]
Source: "C:\Users\mrpau\OneDrive\Dokumenter\GitHub\Ccuneiform-in-NVDA\dist\niv-louie.exe"; DestDir:{app}
Source: "C:\Users\mrpau\OneDrive\Dokumenter\GitHub\Ccuneiform-in-NVDA\Justicon-Free-Simple-Line-Arrow-Solution-Business-Computer-Technology.512.ico"; DestDir:{app}

[Icons]
Name:{group}\{#MyAppName}; Filename:{app}\niv-louie.exe; IconFilename:{app}\Justicon-Free-Simple-Line-Arrow-Solution-Business-Computer-Technology.512.ico