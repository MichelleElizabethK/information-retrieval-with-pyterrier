import argparse
from process_docs import ParsedDocument
from pyterrier_framework import PythonTerrier
# Expected usage:
# ./run -q topics.xml -d documents.lst -r run -o sample.res ...

# Where:
#   -q topics.xml -- a file including topics in the TREC format 
#   -d documents.lst -- a file including document filenames 
#   -r run -- a string identifying the experiment (will be inserted in the
#      result file as "run_id")
#   -o sample.res -- an output file 


def main():
    parser = argparse.ArgumentParser(description="Command Line Arguments for Vector Space Model",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-q", help="a file including topics in the TREC format")
    parser.add_argument("-d", help="a file including document filenames")
    parser.add_argument(
        "-r", help="a string identifying the experiment (will be inserted in the result file as \"run_id\"")
    parser.add_argument("-o", help="an output file")

    args = parser.parse_args()
    config = vars(args)
    parsed_doc_df = ParsedDocument()
    parsed_doc_df.process_documents(config['q'], config['d'], config['r'])
    ir_framework = PythonTerrier(parsed_doc_df.parsed_docs, parsed_doc_df.lang, parsed_doc_df.run)
    ir_framework.index_docs()
    parsed_doc_df.create_queries()
    result = ir_framework.query_docs(parsed_doc_df.query_df)
    parsed_doc_df.get_output(result, config['o'], config['r'])


if __name__ == '__main__':
    main()
