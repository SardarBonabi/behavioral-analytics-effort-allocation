"""Representative workflow sample. Research under review; full code/data proprietary.

Private source adapters, cohort rules, credentials, and manifests are withheld.
These interfaces describe boundaries; they are not a runnable acquisition kit.
"""
from dataclasses import dataclass
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class Job:
    project: str
    snapshot: str  # Immutable input/query/parser version; change it for a fresh run.
    stage: str
    partition: str  # Opaque manifest key, never a credential or raw user identifier.

    def __post_init__(self):
        if any(not isinstance(value, str) or not value.strip() for value in
               (self.project, self.snapshot, self.stage, self.partition)):
            raise Permanent('invalid_job_identity')

    @property
    def key(self) -> tuple[str, str, str, str]:
        return self.project, self.snapshot, self.stage, self.partition


@dataclass(frozen=True)
class Checkpoint:
    cursor: str | None = None  # None means start unless complete is True.
    complete: bool = False
    revision: int = 0


    def __post_init__(self):
        if type(self.complete) is not bool or type(self.revision) is not int or self.revision < 0:
            raise Permanent('invalid_checkpoint_state')
        _validate_cursor(self.cursor)
        if self.complete and self.cursor is not None:
            raise Permanent('completed_checkpoint_has_cursor')


@dataclass(frozen=True)
class Page:
    rows: tuple[Mapping[str, Any], ...]
    next_cursor: str | None
    complete: bool  # Explicit terminal-page evidence, not inferred from row count.


    def __post_init__(self):
        _validate_cursor(self.next_cursor)
        if type(self.complete) is not bool or self.complete != (self.next_cursor is None):
            raise Permanent('inconsistent_page_state')


def _validate_cursor(cursor):
    if cursor is not None and (not isinstance(cursor, str) or not cursor.strip()):
        raise Permanent('invalid_cursor')


@dataclass(frozen=True)
class Record:
    key: str  # Stable, de-identified natural key within a stage and snapshot.
    values: Mapping[str, Any]


class Source(Protocol):
    def fetch(self, job: Job, cursor: str | None) -> Page:
        """Fetch/parse one bounded page, with timeouts and schema/completeness checks.

        Private implementation resolves manifest keys and endpoint requests;
        checks all pagination, missing-page and redirect conditions; and converts
        source-specific fields into the allowlisted records used by this sample.
        """
        ...


class Store(Protocol):
    def load(self, job: Job) -> Checkpoint: ...

    def commit_page(self, job: Job, previous: Checkpoint, page: Page,
                    records: tuple[Record, ...]) -> Checkpoint:
        """Atomically upsert records and advance the expected checkpoint revision."""
        ...


class CollectionError(Exception):
    """Safe error code only. Do not attach headers, payloads, URLs, or secrets."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class Retryable(CollectionError):
    def __init__(self, retry_after: float = 0):
        super().__init__('temporary_source_failure')
        self.retry_after = retry_after


class Permanent(CollectionError):
    pass


class ConcurrentUpdate(CollectionError):
    def __init__(self):
        super().__init__('checkpoint_conflict')
