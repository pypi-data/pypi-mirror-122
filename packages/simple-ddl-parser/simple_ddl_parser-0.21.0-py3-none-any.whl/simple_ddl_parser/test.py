from simple_ddl_parser import DDLParser

ddl = """
   
CREATE TABLE [dbo].[SLIPAPLICACAO] (
    -- Referencia do SLIPEVENTO
    [cdSLIPMvto] [bigint] NOT NULL,
    [seqLcto] [int] NOT NULL,
    -- Quando È efetivamente aplicado
    [dtAplicacaoEfetiva] [date]  NOT NULL,
    CONSTRAINT [pk_slipsApl] PRIMARY KEY CLUSTERED ( [cdSLIPMvto], [seqLcto] ),
        -- a FK de aplicacao nao pode ser usada pois o MSSQL SERVER nao admite FKs a
        -- a referencias que nao sejam UNIQUE .,
    CONSTRAINT [fk_slipsAplVSMvt] FOREIGN KEY  ( [cdSLIPMvto], [seqLcto] ) REFERENCES  SLIPMOVIMENTO(cdSLIPMvto, [seqLcto] )

) ON [PRIMARY]
GO
    """
result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
