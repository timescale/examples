-- TimescaleDB metadata
-- set_chunk_interval()

select chunk_table, ranges, table_size, index_size, toast_size, total_size
from chunk_relation_size_pretty('mta');