from dataclasses import dataclass, field
from typing import Any

from .base import AulaDataClass
from .easyiq_calendar_event import EasyIQCalendarEvent


@dataclass
class EasyIQHomework(AulaDataClass):
    id: str
    title: str
    description: str = ""
    due_date: str = ""
    subject: str = ""
    is_completed: bool = False
    _raw: dict | None = field(default=None, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EasyIQHomework:
        return cls(
            _raw=data,
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            due_date=data.get("dueDate", ""),
            subject=data.get("subject", ""),
            is_completed=data.get("isCompleted", False),
        )

    @classmethod
    def from_calendar_event(cls, event: EasyIQCalendarEvent) -> EasyIQHomework:
        """Build homework from an EasyIQ calendar row of item type 4.

        The portal's calendar rows carry no assignment id or completion flag,
        so ``id`` falls back to the start timestamp and ``is_completed`` stays
        ``False``. The subject doubles as the title, matching how the EasyIQ
        widget itself labels homework.

        The homework controller's rows carry the subject as ``CoursesDisplay``
        (e.g. "Dansk"), not the ``Courses``/``courses`` key
        :attr:`EasyIQCalendarEvent.courses` reads, so ``subject`` is empty if
        read from there; it falls back to ``courses`` for rows that do use
        that key.
        """
        row = {str(k).lower(): v for k, v in (event._raw or {}).items()}
        return cls(
            _raw=event._raw,
            id=str(row.get("id") or "") or event.start,
            title=event.title,
            description=event.description,
            due_date=event.start,
            subject=row.get("coursesdisplay") or event.courses,
            is_completed=False,
        )
