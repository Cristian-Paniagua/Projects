from flask import jsonify
from pandas.core.dtypes.common import classes

from dao.DaoSyllabus import DaoSyllabus, DaoClass
from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.summarize import load_summarize_chain
import time
from rapidfuzz import fuzz, process
import re

class ChatHandler:
    def mapTodict(self, tuple):
        result = {}
        result['cid'] = tuple[0]
        result['cname'] = tuple[1]
        result['ccode'] = tuple[2]
        result['cdesc'] = tuple[3]
        return result


    def extractCidFromCourseCode(self, question, classes):
        # Regular expression with groups for letters and digits
        match = re.search(r"\b(ciic|inso)\s*(\d{4})\b", question, re.IGNORECASE)
        if match:
            department = match.group(1).upper()  # First group: CIIC or INSO
            course_number = match.group(2)       # Second group: 4-digit number
              # Full course code with space
            for course in classes:
                if course_number == course['ccode'] and department == course['cname']:
                    return course['cid']
        return None  # If no match is found


    def extractCidFromQuery(self, question, classes):
        dao = DaoClass()  # Initialize DaoClass once

        # Fetch all course names from the classes list (could be from the DB as well)
        course_names = [course["cdesc"] for course in classes]

        # Perform fuzzy matching on course names
        matches = process.extract(question, course_names, limit=1, scorer=fuzz.partial_ratio)
        print(matches)
        if matches and matches[0][1] > 60:  # If match is above 75% confidence
            matched_name = matches[0][0]  # Best matching course name
            print(matched_name)
            # Fetch course ID by matched name
            for course in classes:
                if matched_name == course['cdesc']:
                    return course['cid']
        return None  # If no good match is found




    def QuestionAndAnswer(self, question_json):
        start_time = time.time()

        model = SentenceTransformer("all-mpnet-base-v2")
        # model = SentenceTransformer("all-MiniLM-L6-v2")

        question = question_json.get('question')

        if question is None:
            return {"error": "No question provided"}, 400


        #question = "What is the time distribution of this theme 'Machine learning software libraries and frameworks'"
        #question = "What methods are used for the evaluation strategies?"
        #question = "What weight is the project for this class?"
        #question= "What are the textbooks used in the CIIC 4030 course?"
        #question = "How are grades divided for the CIIC 4082 course?"
        #question = "What are the requisites of the course CIIC 5150? "
        #question = "What are the requisites of the course CIIC 4151 (Design Project)?"
        #question = "Tell me at least 3 topics that are taught in the introduction to database (CIIC4060) course? "
        #question = "How are grades divided in the Machine Learning Course?"
        #question = "How are grades divided in the INSO 5111 course?"
        #question = "For the course CIIC 4010, tell me at least 3 topics that are taught in the introduction?"
        # question = """Where these books appear in the syllabus of CIIC 5150 '* A. Geron, "Hands-On Machine Learning with Scikit-Learn and TensorFlow"
        # * E. Alpaydin, "Introduction to Machine Learning" (4th edition)
        # * C. Bishop, "Pattern Recognition and Machine Learning' """
        #question = "What is the theme with more hours in the Time Distribution?"

        dao = DaoSyllabus()
        classes=[]
        cls = DaoClass().getAllClasses()
        for t in cls:
            classes.append(self.mapTodict(t))

        cid = self.extractCidFromCourseCode(question, classes)
        if cid is None:
            cid = self.extractCidFromQuery(question, classes)

        print(cid)
        emb = model.encode(question)



        fragments = dao.getSyllabus(str(emb.tolist()), cid)
        context = []

        for f in fragments:
            print(f)
            context.append(f[3])
        # print(context[0])

        documents = "\\n".join(c for c in context)
        # print(documents)
        # print(documents)


        prompt = PromptTemplate(
            template="""You are an assistant for question-answering tasks and your personal name is Tarzan.
            Use the following documents to answer the question. These documents are
            syllabuses offered at the university. If the question is 'empty' or not asking nothing, just say who you are and in
            what you could help with. If you are asked with questions non related to the university, just answer them normally
            forgetting about the documents. When they ask a question, it will usually
            mention either a name and a code (like CIIC 4030) or the name of the course (like Data Structures).
            Use the general information section to identify the course and provide details such as the amount of credits, 
            contact hours, and prerequisites. In the evaluation strategies section, find grade distributions, 
            and textbooks can be found in the bibliography unless specified in a textbook area.
            
            If the documents have conflicting information, prioritize the most detailed or recent source. When asking 'how the grades are divided for
            a certain class' it means that wants a format of evaluation strategy like an exam and the weight for the final grade like 20%,  that is the most important
            thing, later you could add how many hours could take the evaluation but that is not necessary. There is a mark that is either '[ ]'
            or '[ x ]', when it's marked with an x it means that the strategy at the right has been chosen for the evaluation of the course. There are cases where
            it states 'other' and a series of other evaluations, You must list them as well. The 'others' area could be homework, laboratory, etc. Then comes the quantity and the percent.
            For the evaluation strategies section, don't multiply the quantity with the percentage of the weight, for example if the quantity is equal 2 and the percent 35%, it means that 
            those 2 exams are equal the 35%. That is a very important step. If the percent doesn't equal to a hundred, keep searching or say that
            you don't know where the rest is.
            
            Take in mind that CIIC 5150 (Machine Learning Course) has a different syllabus format, in the student evaluation strategies
            appears all the types of different evaluations like exams, quizzes, etc. Also, for this course (CIIC 5150), the textbooks are located
            after the 'text books' area or in the 'Bibliography' (hint: there are 7 books). For topics of the class you can use the thematic outline.
            If the conflict cannot be resolved, state that the information is unclear. If you don't know the answer, just say that you don't know.
            Use five sentences maximum and keep the answer concise. Ignore unrelated information.
            
            Documents: {documents}
            Question: {question}
            Answer:
            """,
            input_variables=["question", "documents", "classes"],
        )

        # print(prompt)
        # print(prompt.format(question=question, documents=documents))

        llm = ChatOllama(
            model = "llama3.1",
            temperature=0.3,
        )



        rag_chain = prompt | llm | StrOutputParser()

        answer = rag_chain.invoke({"question": question, "documents": documents})

        print(answer)
        print("done")

        time.sleep(2)  # Simulating a delay
        end_time = time.time()

        print(f"Operation took {end_time - start_time:.2f} seconds.")
        return jsonify(answer)