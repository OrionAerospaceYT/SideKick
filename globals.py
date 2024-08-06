"""
An auxillary file which holds global constants.
"""

ACCENT_COLOUR = "#252530"
TEXT_COLOUR = "#00f0c3"

SUCCESS_MSG = "<h1 style=\"color:#00f0c3\">\
Success</h1><font color=\"#FFFFFF\">"

FAILURE_MSG = "<p style=\"font-weight: bold;color:#E21919; font-size:24px\">\
Error "

USER_MESSAGE = "<h1 style=\"color:#34c0eb\">\
User command</h1>"

ERROR_TERMS = ["Error opening sketch",
               "Error during build",
               "exit status",
               "error during reset"]

MARKER = "<!-- A break -->"

COLOUR_ORDER = ["#FF0C0C",
                "#31f78e",
                "#02acf5",
                "#fc7703",
                "#9d03fc",
                "#fce803",
                "#fc03b1"]

NUM_OF_DATA_PTS = 2500

GRAPH_BEGINNING = "l058~"
GRAPH_ENDING = "zC43_"

START_REC = "#r3cK"
END_REC = "!r3Ck"

DEFAULT_BOARDS = [["Select Board", "None"],
                  ["SK Stem", "arduino:mbed_rp2040:pico"]]

DEFAULT_SETTINGS = """
Drop down options:\n
Board: Select Board\n
Project: None\n
"""

SK_LITE_ON_QSS = """
QPushButton {
border: 3px solid #00f0c3;
}
"""

SK_LITE_OFF_QSS = """
QPushButton {
border: none;
}
"""
