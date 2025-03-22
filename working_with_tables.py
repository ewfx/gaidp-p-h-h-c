from unstructured.partition.pdf import partition_pdf

#Partition PDF tables, text
file_path = "D:\\My Projects\\hackathon-wf\\documents\\finra.pdf"
chunks = partition_pdf(
    filename=file_path,
    infer_table_structure=True,            # extract tables
    strategy="hi_res",                     # mandatory to infer tables

    chunking_strategy="by_title",          # or 'basic'
    max_characters=10000,                  # defaults to 500
    combine_text_under_n_chars=2000,       # defaults to 0
    new_after_n_chars=6000,
)
set([str(type(el)) for el in chunks])