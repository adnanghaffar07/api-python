from marshmallow import Schema, fields


class TaskSerializer(Schema):
    """
        Offender client model.
    """
    user_id = fields.Str(required=True)
    content = fields.Str(required=True)
    is_done = fields.Bool(required=True)
    created_time = fields.Int(required=True)
    task_id = fields.Str(required=True)
    ttl = fields.Int(required=True)
