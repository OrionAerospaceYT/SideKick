import os

user_name = os.getlogin()

with open("arduino-cli.yaml", "r") as arduino:
    new_arduino = arduino.read().replace("REPLACE_USER", f"{user_name}")

with open("arduino-cli.yaml", "w") as arduino:
    arduino.write(new_arduino)
