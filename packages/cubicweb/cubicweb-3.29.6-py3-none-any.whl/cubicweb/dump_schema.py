from cubicweb.schema import (
    CubicWebSchema,
    CubicWebEntitySchema,
    CubicWebRelationDefinitionSchema,
)
import json


def dump_schema_to_json(schema: CubicWebSchema):
    """Dumps a CubicWebSchema as JSON"""
    return SchemaToJSONDumper(schema).dump()


class SchemaToJSONDumper:

    _entity_types = []
    _relation_definitions = []

    def __init__(self, schema: CubicWebSchema):
        self._schema = schema

    def _entity_to_json(self, entity):
        return {
            "type": entity.type,
            "description": entity.description,
            "final": entity.final,
        }

    def _relation_definition_to_json(self, rdef: CubicWebRelationDefinitionSchema):
        schema_json = {
            "type": rdef.rtype.type,
            "description": rdef.description,
            "final": rdef.final,
            "subject": rdef.subject.type,
            "object": rdef.object.type,
            "cardinality": rdef.cardinality,
        }
        if hasattr(rdef, "default"):
            schema_json["default"] = rdef.default
        return schema_json

    def dump(self):

        entities_json = [
            self._entity_to_json(entity) for entity in self._schema.entities()
        ]

        rdefs_json = [
            self._relation_definition_to_json(rdef)
            for rel in self._schema.relations()
            for rdef in rel.rdefs.values()
        ]

        return json.dumps(
            {
                "entities": entities_json,
                "relations_definitions": rdefs_json,
            },
            indent=2,
        )
