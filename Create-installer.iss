#define MyAppName "Niv_Louie"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "Me"
#define URL "http://example.com"
#define sourceDir "C:\Users\mrpau\OneDrive\Dokumenter\GitHub\Ccuneiform-in-NVDA"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=.
OutputBaseFilename={#MyAppName}-installer

[Files]
Source: "{#sourceDir}\dist\niv_louie.exe"; DestDir:{app}
Source: "{#sourceDir}\Justicon-Free-Simple-Line-Arrow-Solution-Business-Computer-Technology.512.ico"; DestDir:{app}

[Icons]
Name:{group}\{#MyAppName}; Filename:{app}\niv_louie.exe; IconFilename:{app}\Justicon-Free-Simple-Line-Arrow-Solution-Business-Computer-Technology.512.ico