import sys
from . import InvertIndexIdf

indexer = InvertIndexIdf.indexer(default_path=sys.argv[1], json_name=sys.argv[2])
indexer.Main()
