"""
Module with a simple class for nicer printouts.
"""


class ColorPrinter:
    """Simple class just for printing nicer printouts with colors."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def print_fail(self, msg):
        """Print fail with red color."""
        print(f"{self.FAIL}{msg}{self.ENDC}")

    def print_error(self, msg):
        """Print warning with yellow color."""
        print(f"{self.WARNING}{msg}{self.ENDC}")
