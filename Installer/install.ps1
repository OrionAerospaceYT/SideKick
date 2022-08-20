## NOTE: Checks to be done throughout runtime

# Define static environment variables
$username = [system.environment]::username
$c_users = "C:\Users\"
$users_path = Join-Path $c_users $username

# Define file paths for installs
$sidekick_dir = "C:\Program Files\SideKick"

$arduino_cli_name = "\AppData\Local\Arduino15"
$arduino_cli_dir = Join-Path $users_path $arduino_cli_name

$teensy_package_name = "\AppData\Local\Arduino15\package_teensy_index.json"
$teensy_package = Join-Path $users_path $teensy_package_name

$execution_dir = (Get-Item .).FullName

$config_file = "\arduino-cli.yaml"
$config_dir =  Join-Path $execution_dir $config_file
$cli_congif_dir = Join-Path $arduino_cli_dir $config_file
# Boolean variables for checks
$arduino_cli_installed = 0
$sidekick_dir_installed = 0
$teensy_package_installed = 0

# Check if dependencies are installed
if (Test-Path -Path $arduino_cli_dir) {
    #$arduino_cli_installed = 1
    echo "arduino cli found"
}
if (Test-Path -Path $sidekick_dir) {
    $sidekick_dir_installed = 1
    echo "sidekick directory found"
}
if (Test-Path -Path $teensy_package) {
    $teensy_package_installed = 1
    echo "teensy package found"
}

# Download dependencies if not already
if ($arduino_cli_installed -eq 0) {
    # Downloads the arduino cli
    Invoke-WebRequest https://downloads.arduino.cc/arduino-cli/nightly/arduino-cli_nightly-latest_Windows_64bit.zip -O arduino-cli.zip
    # Unzips the arduino-cli download
    Expand-Archive -LiteralPath arduino-cli.zip -DestinationPath arduino-cli
    # Deletes the arduino-cli.zip
    Remove-Item ./arduino-cli.zip
    # Runs arduino-cli commands
    ./arduino-cli/arduino-cli.exe core update-index
    ./arduino-cli/arduino-cli.exe config init
    ./arduino-cli/arduino-cli.exe core install arduino:avr
    ./arduino-cli/arduino-cli.exe core install arduino:samd
}
if ($sidekick_dir -eq 0) {
    ## TO DO:
}
if ($teensy_package_installed -eq 0 ) {
    # Downloads the teensy package - can probably be deleted
    Invoke-WebRequest https://www.pjrc.com/teensy/td_156/package_teensy_index.json -O package_teensy_index.json
    # Edit the provided yaml config changing temp user to username
    (Get-Content -path $config_dir -Raw) -replace 'REPLACE_USER', $username
    # Move the provided yaml to the arduino15 dir
    Move-Item -LiteralPath $config_dir -Destination $cli_congif_dir -Force
    ./arduino-cli/arduino-cli.exe core install teensy:avr
}

# Defines variables for downloads

# File managment and create SideKick directory

# Download installation

# Move arduino-cli into sidekick

# Finished outputs
#./arduino-cli/arduino-cli.exe board listall