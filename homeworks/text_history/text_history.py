from abc import ABC, abstractmethod
from math import inf
from typing import List


class Action(ABC):
    def __init__(self, pos: int, from_version: int, to_version: int) -> None:
        self._pos = pos
        self._from_version: int = from_version
        self._to_version = to_version

    @property
    def pos(self) -> List[int]:
        return self._pos

    @pos.setter
    def pos(self, pos: int | None) -> None:
        self._pos = pos

    @property
    def from_version(self) -> int:
        return self._from_version

    @from_version.setter
    def from_version(self, version: int) -> None:
        self._from_version = version

    @property
    def to_version(self) -> int:
        return self._to_version

    @to_version.setter
    def to_version(self, version: int) -> None:
        self._to_version = version

    @abstractmethod
    def apply(self, old_text: str) -> str:
        pass


class InsertAction(Action):
    def __init__(self, pos: int, text: str, from_version: int, to_version: int) -> None:
        super(InsertAction, self).__init__(pos, from_version, to_version)
        self.new_text = text

    @property
    def new_text(self) -> str:
        return self._new_text

    @new_text.setter
    def new_text(self, value: str) -> None:
        self._new_text = value

    def apply(self, old_text: str) -> str:
        if self.from_version >= self.to_version or self.from_version < 0:
            raise ValueError("Wrong version values")
        if self.pos is None:
            return f"{old_text}{self.new_text}"
        else:
            if self.pos > len(old_text) or self.pos < 0:
                raise ValueError
            else:
                return f"{old_text[0: self.pos]}{self.new_text}{old_text[self.pos:]}"


class ReplaceAction(Action):
    def __init__(self, pos: int, text: str, from_version: int, to_version: int) -> None:
        super(ReplaceAction, self).__init__(pos, from_version, to_version)
        self.new_text = text

    @property
    def new_text(self):
        return self._new_text

    @new_text.setter
    def new_text(self, value):
        self._new_text = value

    def apply(self, old_text: str) -> str:
        if self.from_version >= self.to_version or self.from_version < 0:
            raise ValueError("Wrong version values")
        if self.pos is None:
            return f"{old_text}{self.new_text}"
        else:
            if self.pos > len(old_text) or self.pos < 0:
                raise ValueError
            else:
                return f"{old_text[0: self.pos]}{self.new_text}{old_text[self.pos  + len(self.new_text):]}"


class DeleteAction(Action):
    def __init__(
        self,
        pos: int,
        length: int,
        from_version: int,
        to_version: int,
    ) -> None:
        super(DeleteAction, self).__init__(pos, from_version, to_version)
        self.length = length

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    def apply(self, old_text: str) -> str:
        if self.from_version >= self.to_version or self.from_version < 0:
            raise ValueError("Wrong version values")
        if (
            self.pos > len(old_text)
            or self.pos < 0
            or self.length > len(old_text[self.pos :])
        ):
            raise ValueError
        else:
            return f"{old_text[0:self.pos]}{old_text[self.pos + self.length:]}"


class TextHistory:
    def __init__(self):
        self.text = ""
        self.version = 0
        self.actions = list()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value) -> None:
        self._text = value

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, value) -> None:
        self._version = value

    @property
    def actions(self) -> list:
        return self._actions

    @actions.setter
    def actions(self, value) -> None:
        self._actions = value

    def insert(self, text: str, pos: int = None) -> int:
        insert_action = InsertAction(
            pos=pos,
            text=text,
            from_version=self.version,
            to_version=self.version + 1,
        )
        self.text = insert_action.apply(self.text)
        self.version = insert_action.to_version
        self.actions.append(insert_action)
        return insert_action.to_version

    def replace(self, text: str, pos: int = None) -> int:
        replace_action = ReplaceAction(
            pos=pos,
            text=text,
            from_version=self.version,
            to_version=self.version + 1,
        )
        self.text = replace_action.apply(self.text)
        self.version = replace_action.to_version
        self.actions.append(replace_action)
        return replace_action.to_version

    def delete(self, pos: int, length: int) -> int:
        delete_action = DeleteAction(
            pos=pos,
            length=length,
            from_version=self.version,
            to_version=self.version + 1,
        )
        self.text = delete_action.apply(self.text)
        self.version = delete_action.to_version
        self.actions.append(delete_action)
        return delete_action.to_version

    def action(self, action: Action) -> int:
        self.text = action.apply(self.text)
        self.version = action.to_version
        self.actions.append(action)
        return action.to_version

    def get_actions(self, from_version: int = 0, to_version: int = inf) -> list[Action]:
        if from_version > to_version:
            raise ValueError("Incorrect Versions")
        elif from_version < to_version:
            return [
                i
                for i in self.actions
                if ((i.to_version >= from_version) and (i.to_version <= to_version))
            ]
        elif to_version == 0:
            return list()

        elif from_version == to_version:
            return [i for i in self.actions if i.to_version == from_version]
