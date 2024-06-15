from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Str(dump_only=True) # dump_only – Fields to skip during deserialization (read-only fields) 
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    storeid = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)