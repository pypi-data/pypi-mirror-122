from simple_ddl_parser import DDLParser

ddl = """
  


    """
result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
