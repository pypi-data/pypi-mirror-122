import datetime
import json
import uuid


class JSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time/timedelta,
    and UUID

    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            render = obj.isoformat()
            if render.endswith("+00:00"):
                render = render[:-6] + "Z"
            return render
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return str(obj.total_seconds())
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)
