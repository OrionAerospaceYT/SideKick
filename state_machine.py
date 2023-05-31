"""
A python state machine for the sidekick app.
"""

class StateMachine():
    """
    A python state machine for the sidekick app.
    """

    def __init__(self):
        self.record = False
        self.cli_upload = False
        self.cli_compile = False
        self.cli_usr = False
        