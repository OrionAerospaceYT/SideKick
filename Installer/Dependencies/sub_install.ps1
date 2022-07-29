Write-Output "1"

#COMMENT OUT FOR RELEASE HAVE THE EXE ASK FOR PRIVS
#if(!([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    #Start-Process -FilePath PowerShell.exe -Verb Runas -ArgumentList "-File `"$($MyInvocation.MyCommand.Path)`"  `"$($MyInvocation.MyCommand.UnboundArguments)`""
    #Exit
#}

$usr_var = [system.environment]::username

$program_dir = "C:\Program Files\SideKick"

$exec_dir = (Get-Item .).FullName

if (Test-Path $program_dir) {
    Write-Host "Folder Exists"
}
else
{
    New-Item $program_dir -ItemType Directory
}

Set-Location $program_dir

Invoke-WebRequest https://downloads.arduino.cc/arduino-cli/nightly/arduino-cli_nightly-latest_Windows_64bit.zip -O arduino-cli.zip
Expand-Archive -LiteralPath arduino-cli.zip -DestinationPath arduino-cli
$PATH = [Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::Machine)
$arduino_cli = "C:\Program Files\SideKick\arduino-cli"

if( $PATH -notlike "*"+$arduino_cli+"*" ){
    [Environment]::SetEnvironmentVariable("PATH", "$PATH;$arduino_cli", [System.EnvironmentVariableTarget]::Machine)
}

arduino-cli core update-index
arduino-cli core install arduino:avr
arduino-cli core install arduino:samd
Invoke-WebRequest https://www.pjrc.com/teensy/td_156/package_teensy_index.json -O package_teensy_index.json

arduino-cli config init



$base = "C:\Users\"
$base2 = Join-Path $base $usr_var
$append = "\AppData\Local\Arduino15"
$target = Join-Path $base2 $append
$yaml = "\arduino-cli.yaml"
$config = Join-Path $exec_dir $yaml 
Write-Output $target
(Get-Content -path $config -Raw) -replace 'REPLACE_USER', $usr_var
Move-Item -LiteralPath package_teensy_index.json -Destination $target -Force
Copy-Item -LiteralPath $config -Destination $target -Force

arduino-cli core install teensy:avr

#Set-Location $exec_dir

#$exe_base = "\src"
#$exe_target = Join-Path $exec_dir $exe_base
#$documents = Join-Path $base $usr_var
#$docs_exten = "\Documents\"
#$documents_final = Join-Path $documents $docs_exten
#Write-Output $exe_target
#Write-Output $documents_final
#Get-ChildItem -Path $exe_target -Recurse | Move-Item -Path $exe_target -Destination $documents_final
#$current = Join-Path $documents_final $exe_base
#$new_name = "\SideKick"
#$final = Join-Path $documents_final $new_name
#Rename-Item -Path $current -NewName $final

#$new_exe = "\Sidekick.exe"
#$comb_exe = Join-Path $final $new_exe

#$SourceExe = $comb_exe
#$desktop = "\Desktop"
#$desktop_final = Join-Path $base $usr_var
#$DestinationPath = Join-Path $desktop_final $desktop

#$WshShell = New-Object -comObject WScript.Shell
#$Shortcut = $WshShell.CreateShortcut($DestinationPath)
#$Shortcut.TargetPath = $SourceExe
#$Shortcut.Save()