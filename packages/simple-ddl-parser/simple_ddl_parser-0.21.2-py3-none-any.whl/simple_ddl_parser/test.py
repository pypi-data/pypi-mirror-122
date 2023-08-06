from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE "schema--notification"."notification" (
    content_type "schema--notification"."ContentType",
    period "schema--notification"."Period"
);
"""
result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
