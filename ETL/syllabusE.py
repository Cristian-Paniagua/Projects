from PyPDF2 import PdfReader
import fitz
import os
from os import listdir
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from dao.DaoSyllabus import DaoSyllabus
from sentence_transformers import SentenceTransformer
import re
model = SentenceTransformer("all-mpnet-base-v2")
#model = SentenceTransformer("all-MiniLM-L6-v2")


files = listdir("../syllabuses")
#print(files)

SyllDao = DaoSyllabus()

for f in files:
    basename = os.path.splitext(f)[0]
    parts = basename.split("-")
    cname = parts[0]
    ccode = parts[1]
    #
    try:
        # Open the PDF file using fitz
        file_path = f"../syllabuses/{f}"
        with fitz.open(file_path) as doc:
            # Extract text from each page and filter out empty strings
            pdf_text = [page.get_text().strip() for page in doc if page.get_text().strip()]
            normalized_text = [text.lower() for text in pdf_text]
            normalized_text = [re.sub(r'☒', '[X]', text).replace('☐', '[ ]') for text in pdf_text]
            if (cname != 'CIIC') and (ccode != '5150'):
                # Apply re.sub to each text in normalized_text
                normalized_text = [re.sub(r"12\.\s*a.*", "", text, flags=re.DOTALL) for text in normalized_text]

        #print(pdf_text[0] if pdf_text else "No extractable text")

    except Exception as e:
        print(f"Error processing {f}: {e}")
    # fname = "../syllabuses/" + f
    # reader = PdfReader(fname)
    # pdf_text = [p.extract_text().strip() for p in reader.pages]
    #
    # pdf_text = [text for text in pdf_text if text]
    # normalized_text = [text.lower() for text in pdf_text]
    # normalized_text = [re.sub(r'☒', '[X]', text).replace('☐', '[ ]') for text in pdf_text]
    #
    # #normalized_text = ' '.join([text.lower() for text in pdf_text])
    # if (cname != 'CIIC') and (ccode != '5150'):
    #     normalized_text = [re.sub(r"12\.\s*a.*", "", text, flags=re.DOTALL) for text in normalized_text]


    #print(fname)
    #print(pdf_text[0])
    if (cname == 'CIIC') and (ccode == '5150'):
        character_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""],
                                                            chunk_size=250, chunk_overlap=25)
        character_split_texts = character_splitter.split_text('\n\n'.join(normalized_text))
        print(f"\nTotal chunks: {len(character_split_texts)}")
        token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=25, tokens_per_chunk=256)

    else:
        character_splitter = RecursiveCharacterTextSplitter( separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=800 , chunk_overlap=80)

        character_split_texts = character_splitter.split_text('\n\n'.join(normalized_text))
        # print(character_split_texts[25])
        print(f"\nTotal chunks: {len(character_split_texts)}")
    #
    # [print(t) for t in character_split_texts]
    # print()

        token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=80, tokens_per_chunk=256)

    token_split_texts = []
    for text in character_split_texts:
        token_split_texts+= token_splitter.split_text(text)
        # print("token")
        # print(token_split_texts[10])
        # [print(t) for t in token_split_texts]
    print(f"\nTotal Splitted chunks: {len(token_split_texts)}")

    for t in token_split_texts:
        emb = model.encode(t)

        syllabus = [cname, ccode, emb.tolist(), t]
        SyllDao.insertSyllabus(syllabus)