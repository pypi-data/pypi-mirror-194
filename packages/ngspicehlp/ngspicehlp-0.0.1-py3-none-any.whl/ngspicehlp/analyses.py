"""Vector set of signals for which to gather data, plot, ... """

ANALYSIS_UNITS: dict[str, tuple[str, str]] = {
    "tran": ("time", "sec"),
    "ac": ("freq", "Hz"),
}

from pathlib import Path
from .vectors import Vectors


class Analyses:
    """Vector set of signals for which to gather data, plot, ..."""

    def __init__(
        self,
        name: str,
        cmd: list[str | int | float],
        vector: Vectors,
        results_loc: Path,
    ) -> None:

        self.name: str = name
        self.cmd_type = str(cmd[0])  # "tran", "ac", ...

        self.cmd_strings: list[str] = [str(item) for item in cmd]
        self.cmd_line: str = " ".join(self.cmd_strings)

        results_filename: Path = results_loc / f"{self.name}.txt"

        if self.cmd_type == "ac":
            self.vec_output = f"wrdata {results_filename} {vector}"
        if self.cmd_type == "dc":
            self.vec_output = f"wrdata {results_filename} {vector}"
        if self.cmd_type == "op":
            self.vec_output = f"print line {vector} > {results_filename}"
        if self.cmd_type == "tran":
            self.vec_output = f"wrdata {results_filename} {vector}"

    def get_units(self) -> tuple[str, str]:
        """checks the type of analysis ("tran", "ac", ...) and returns proper units

        Returns:
            tuple[str, str]: unit type and units
        """
        return ANALYSIS_UNITS[self.cmd_type]

    def lines_for_cntl(self) -> list[str]:
        """returns a list of the command lines for the control file

        Returns:
            list[str]: command lines
        """
        return [self.cmd_line, self.vec_output]
