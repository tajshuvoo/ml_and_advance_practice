from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Literal, Optional

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",#llama doesn't support it , openAI supports it
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

#schema

class Review(TypedDict):
    key_themes : Annotated[list[str], "Write down all the key themes discussed in the review in a list"]
    summary : Annotated[str, "A brief summary of the review"]
    sentiment : Annotated[Literal["pos", "neg"], "Return sentiment of the review either negative, positive or neutral"]
    pros: Annotated[str, "Write down all the pros of the review"]
    cons: Annotated[str, "Write down all the cons of the review"]
    name : Annotated[Optional[str], "write the name of the reviewer"]
    
structured_model = model.with_structured_output(Review)

result = structured_model.invoke(""" The hardware is great , but the software feels bloated. 
                                 There are too many pre-installed apps that I can't remove. 
                                 Also , the UI looks outdated compared to other brands. 
                                 Hoping for a software update to fix this.""")

print(result.content)