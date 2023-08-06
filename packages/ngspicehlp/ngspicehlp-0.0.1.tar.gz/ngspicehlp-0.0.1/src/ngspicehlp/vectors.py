"""Vector set of signals for which to gather data, plot, ... """

from typing import TypeVar

# used to get rid of type errors from static error checking (mypy, etc.)
T = TypeVar("T", bound="Vectors")


class Vectors:
    """Vectors are a list of signals to specified for simulation, display, ..."""

    def __init__(self, vector: list[str | int]):
        self.vector: list[str] = [str(signal) for signal in vector]
        self._words_to_items()
        self._remove_dups()

    def __str__(self) -> str:
        return " ".join(self.vector)

    def _words_to_items(self) -> None:
        """Convert words separated by spaces into separate list items"""
        my_list = []
        for item in self.vector:
            if " " in item:
                # Split the string into multiple items
                split_items = item.split(" ")
                # Add the new items to the new list
                my_list.extend(split_items)
            else:
                my_list.append(item)
        self.vector = my_list

    def _remove_dups(self) -> None:
        """remove duplicate signals"""
        my_list = self.vector
        no_dups: list[str] = []
        for item in my_list:
            if item not in no_dups:
                no_dups.append(item)
        self.vector = no_dups

    def list_out(self) -> list[str]:
        """Outputs vector as a list"""
        return self.vector

    def sort(self) -> None:
        """Sort the signals"""
        self.vector = sorted(self.vector)

    def _union_one(self: T, vec2: T) -> None:
        """Combine the vector object with a second one"""
        self.vector = self.list_out() + vec2.list_out()
        self._remove_dups()

    def union(self: T, *vecs: T) -> None:
        """Combine the vector ob
        ject with others passed in"""
        for vec in vecs:
            self._union_one(vec)

    def subtract(self: T, vec2: T) -> None:
        """Remove from this vector the signals in the second one"""
        list1 = self.list_out()
        list2 = vec2.list_out()
        self.vector = [item for item in list1 if item not in list2]
        self._remove_dups()


def main() -> None:
    """main"""


if __name__ == "__main__":
    main()
