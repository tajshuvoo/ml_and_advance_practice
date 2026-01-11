from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda

load_dotenv()

# -----------------------
# Model
# -----------------------
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation",
    temperature=0
)

model = ChatHuggingFace(llm=llm)
parser = StrOutputParser()

# -----------------------
# Prompts
# -----------------------
prompt_classifier = PromptTemplate(
    template=(
        "Classify the sentiment of the feedback.\n"
        "Respond with ONLY ONE WORD: positive or negative.\n\n"
        "Feedback: {feedback}"
    ),
    input_variables=["feedback"],
)

prompt_positive = PromptTemplate(
    template="Write an appropriate response to this positive feedback:\n{feedback}",
    input_variables=["feedback"],
)

prompt_negative = PromptTemplate(
    template="Write an appropriate response to this negative feedback:\n{feedback}",
    input_variables=["feedback"],
)

# -----------------------
# Chains
# -----------------------
classifier_chain = prompt_classifier | model | parser

normalize_sentiment = RunnableLambda(
    lambda x: "positive" if "positive" in x.lower() else "negative"
)

branch_chain = RunnableBranch(
    (
        lambda x: x == "positive",
        prompt_positive | model | parser,
    ),
    (
        lambda x: x == "negative",
        prompt_negative | model | parser,
    ),
    RunnableLambda(lambda _: "Could not determine sentiment"),
)

chain = classifier_chain | normalize_sentiment | branch_chain

# -----------------------
# Run
# -----------------------
result = chain.invoke({"feedback": "This is a terrible phone to have. very bad in use"})
print(result)

chain.get_graph().print_ascii()
