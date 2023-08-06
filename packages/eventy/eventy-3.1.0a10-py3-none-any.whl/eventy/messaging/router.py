from eventy.record import Record, Response


class RecordRouter:
    def route(self, record: Record) -> str:
        raise NotImplementedError


class SimpleRouter:
    def __init__(
        self,
        topic: str,
    ):
        self._topic = topic

    def route(self, record: Record) -> str:
        return self._topic


class ServiceTopicRecordRouter(RecordRouter):
    def route(self, record: Record) -> str:
        if isinstance(record, Response):
            service = record.destination.split(':')[-1]
        else:
            service = record.namespace.split(':')[-1]
        suffix = {
            'EVENT': 'events',
            'REQUEST': 'requests',
            'RESPONSE': 'responses',
        }.get(record.type, 'unknown')
        return f'{service}-{suffix}'
