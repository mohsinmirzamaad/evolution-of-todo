import json
from datetime import datetime, timezone

from pydantic import TypeAdapter
from sqlmodel import Session, select

from chatkit.store import NotFoundError, Store
from chatkit.types import Attachment, Page, ThreadItem, ThreadMetadata

from app.database import engine
from app.models import ChatKitItem, ChatKitThread

_thread_item_adapter = TypeAdapter(ThreadItem)
_attachment_adapter = TypeAdapter(Attachment)


class RequestContext:
    def __init__(self, user_id: str):
        self.user_id = user_id


class PostgresStore(Store["RequestContext"]):
    def _get_session(self) -> Session:
        return Session(engine)

    async def load_thread(self, thread_id: str, context: "RequestContext") -> ThreadMetadata:
        with self._get_session() as session:
            row = session.get(ChatKitThread, thread_id)
            if not row or row.user_id != context.user_id:
                raise NotFoundError(f"Thread {thread_id} not found")
            return self._row_to_metadata(row)

    async def save_thread(self, thread: ThreadMetadata, context: "RequestContext") -> None:
        with self._get_session() as session:
            row = session.get(ChatKitThread, thread.id)
            if row:
                row.title = thread.title
                row.status_json = thread.status.model_dump_json()
                row.updated_at = datetime.now(timezone.utc)
            else:
                row = ChatKitThread(
                    id=thread.id,
                    user_id=context.user_id,
                    title=thread.title,
                    status_json=thread.status.model_dump_json(),
                    created_at=thread.created_at,
                    updated_at=datetime.now(timezone.utc),
                )
                session.add(row)
            session.commit()

    async def load_threads(
        self, limit: int, after: str | None, order: str, context: "RequestContext"
    ) -> Page[ThreadMetadata]:
        with self._get_session() as session:
            stmt = select(ChatKitThread).where(ChatKitThread.user_id == context.user_id)
            if order == "desc":
                stmt = stmt.order_by(ChatKitThread.created_at.desc())
            else:
                stmt = stmt.order_by(ChatKitThread.created_at.asc())

            if after:
                cursor_row = session.get(ChatKitThread, after)
                if cursor_row:
                    if order == "desc":
                        stmt = stmt.where(ChatKitThread.created_at < cursor_row.created_at)
                    else:
                        stmt = stmt.where(ChatKitThread.created_at > cursor_row.created_at)

            rows = session.exec(stmt.limit(limit + 1)).all()
            has_more = len(rows) > limit
            rows = rows[:limit]
            return Page(
                data=[self._row_to_metadata(r) for r in rows],
                has_more=has_more,
                after=rows[-1].id if has_more and rows else None,
            )

    async def load_thread_items(
        self, thread_id: str, after: str | None, limit: int, order: str, context: "RequestContext"
    ) -> Page[ThreadItem]:
        with self._get_session() as session:
            stmt = select(ChatKitItem).where(ChatKitItem.thread_id == thread_id)
            if order == "desc":
                stmt = stmt.order_by(ChatKitItem.created_at.desc())
            else:
                stmt = stmt.order_by(ChatKitItem.created_at.asc())

            if after:
                cursor_row = session.get(ChatKitItem, after)
                if cursor_row:
                    if order == "desc":
                        stmt = stmt.where(ChatKitItem.created_at < cursor_row.created_at)
                    else:
                        stmt = stmt.where(ChatKitItem.created_at > cursor_row.created_at)

            rows = session.exec(stmt.limit(limit + 1)).all()
            has_more = len(rows) > limit
            rows = rows[:limit]
            return Page(
                data=[_thread_item_adapter.validate_json(r.data_json) for r in rows],
                has_more=has_more,
                after=rows[-1].id if has_more and rows else None,
            )

    async def add_thread_item(
        self, thread_id: str, item: ThreadItem, context: "RequestContext"
    ) -> None:
        with self._get_session() as session:
            row = ChatKitItem(
                id=item.id,
                thread_id=thread_id,
                type=item.__class__.__name__,
                data_json=item.model_dump_json(by_alias=True, exclude_none=True),
                created_at=item.created_at,
            )
            session.add(row)
            session.commit()

    async def save_item(
        self, thread_id: str, item: ThreadItem, context: "RequestContext"
    ) -> None:
        with self._get_session() as session:
            row = session.get(ChatKitItem, item.id)
            if row:
                row.data_json = item.model_dump_json(by_alias=True, exclude_none=True)
                row.type = item.__class__.__name__
            else:
                row = ChatKitItem(
                    id=item.id,
                    thread_id=thread_id,
                    type=item.__class__.__name__,
                    data_json=item.model_dump_json(by_alias=True, exclude_none=True),
                    created_at=item.created_at,
                )
                session.add(row)
            session.commit()

    async def load_item(
        self, thread_id: str, item_id: str, context: "RequestContext"
    ) -> ThreadItem:
        with self._get_session() as session:
            row = session.get(ChatKitItem, item_id)
            if not row or row.thread_id != thread_id:
                raise NotFoundError(f"Item {item_id} not found")
            return _thread_item_adapter.validate_json(row.data_json)

    async def delete_thread(self, thread_id: str, context: "RequestContext") -> None:
        with self._get_session() as session:
            items = session.exec(
                select(ChatKitItem).where(ChatKitItem.thread_id == thread_id)
            ).all()
            for item in items:
                session.delete(item)
            thread = session.get(ChatKitThread, thread_id)
            if thread:
                session.delete(thread)
            session.commit()

    async def delete_thread_item(
        self, thread_id: str, item_id: str, context: "RequestContext"
    ) -> None:
        with self._get_session() as session:
            row = session.get(ChatKitItem, item_id)
            if row and row.thread_id == thread_id:
                session.delete(row)
                session.commit()

    async def save_attachment(self, attachment: Attachment, context: "RequestContext") -> None:
        pass

    async def load_attachment(self, attachment_id: str, context: "RequestContext") -> Attachment:
        raise NotFoundError(f"Attachment {attachment_id} not found")

    async def delete_attachment(self, attachment_id: str, context: "RequestContext") -> None:
        pass

    def _row_to_metadata(self, row: ChatKitThread) -> ThreadMetadata:
        status_data = json.loads(row.status_json)
        return ThreadMetadata(
            id=row.id,
            title=row.title,
            created_at=row.created_at,
            status=status_data,
        )
