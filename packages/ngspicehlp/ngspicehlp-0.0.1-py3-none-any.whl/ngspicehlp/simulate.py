"""setup or run an ngspice simulation
"""
import subprocess
from pathlib import Path
from .analyses import Analyses
from .control import Control


class Simulate:
    """ngspice simulation"""

    def __init__(
        self,
        ngspice_exe: Path,
        netlist_filename: Path,
        cntl: Control,
        list_analyses: list[Analyses],
    ) -> None:

        self.ngspice_exe: Path = ngspice_exe
        self.netlist_filename: Path = netlist_filename
        self.cntl: Control = cntl
        self.list_analyses: list[Analyses] = list_analyses
        self.ngspice_command: str = f"{self.ngspice_exe} {self.netlist_filename}"

        for index in self.list_analyses:
            self.cntl.insert_lines(index.lines_for_cntl())

        self.cntl.content_to_file()

    def __str__(self) -> str:
        return self.ngspice_command

    def run(self) -> None:
        """execute the simulation"""
        subprocess.run(self.ngspice_command, check=True)
