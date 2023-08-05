from simple_ddl_parser import DDLParser

ddl = """
create table test(
  `id` bigint not null,
  `updated_at` timestamp(3) not null default current_timestamp(3) on update current_timestamp(3),
  primary key (id)
);
    """
result = DDLParser(ddl).run(group_by_type=True, output_mode="bigquery")
import pprint

pprint.pprint(result)
