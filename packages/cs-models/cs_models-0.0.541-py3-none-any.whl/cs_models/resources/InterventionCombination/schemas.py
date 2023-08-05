from marshmallow import (
    Schema,
    fields,
    validate,
)


class InterventionCombinationResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    main_intervention_id = fields.Integer(required=True)
    intervention_id = fields.Integer(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
