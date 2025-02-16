from utils import ingest_documents, qdrant_client, List, QdrantVectorStore, VectorStoreIndex, embedder
import gradio as gr
from toolsFunctions import pubmed_tool, arxiv_tool
from llama_index.core.tools import QueryEngineTool, FunctionTool
from llama_index.core import Settings
from llama_index.llms.mistralai import MistralAI
from llama_index.core.llms import ChatMessage
from llama_index.core.agent import ReActAgent
from dotenv import load_dotenv
from phoenix.otel import register
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
import time
import os

load_dotenv()

## Observing and tracing
PHOENIX_API_KEY = os.getenv("phoenix_api_key")
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"
tracer_provider = register(
    project_name="llamaindex", 
) 
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

## Globals
Settings.llm = MistralAI(model="mistral-small-latest", temperature=0, api_key=os.getenv("mistral_api_key"))
Settings.embed_model = embedder
arxivtool = FunctionTool.from_defaults(arxiv_tool, name="arxiv_tool", description="A tool to search ArXiv (pre-print papers database) for specific papers")
pubmedtool = FunctionTool.from_defaults(pubmed_tool, name="pubmed_tool", description="A tool to search PubMed (printed medical papers database) for specific papers")
query_engine = None
message_history = [
    ChatMessage(role="system", content="You are a useful assistant that has to help the user with questions that they ask about several papers they uploaded. You should base your answers on the context you can retrieve from the PDFs and, if you cannot retrieve any, search ArXiv for a potential answer. If you cannot find any viable answer, please reply that you do not know the answer to the user's question")
]

## Functions
def reply(message, history, files: List[str] | None, collection: str | None, llamaparse: bool = False):
    global message_history
    if message == "" or message is None:
        response = "You should provide a message"
        r = ""
        for char in response:
            r+=char
            time.sleep(0.001)
            yield r
    elif files is None and collection == "":
        res = "### WARNING! You did not specify any collection, so I only interrogated ArXiv and/or PubMed to answer your question\n\n"
        agent = ReActAgent.from_tools(tools=[pubmedtool, arxivtool], verbose=True)
        response = agent.chat(message = message, chat_history = message_history)
        response = str(response)
        message_history.append(ChatMessage(role="user", content=message))
        message_history.append(ChatMessage(role="assistant", content=response))
        response = res + response
        r = ""
        for char in response:
            r+=char
            time.sleep(0.001)
            yield r
    elif files is None and collection != "" and collection not in [c.name for c in qdrant_client.get_collections().collections]:
            response = "Make sure that the name of the existing collection to use as a knowledge base is correct, because the one you provided does not exist! You can check your existing collections and their features in the dedicated tab of the app :)"
            r = ""
            for char in response:
                r+=char
                time.sleep(0.001)
                yield r
    elif files is not None:
        if collection == "":
            response = "You should provide a collection name (new or existing) if you want to ingest files!"
            r = ""
            for char in response:
                r+=char
                time.sleep(0.001)
                yield r
        else:
            collection_name = collection
            index = ingest_documents(files, collection_name, llamaparse)
            query_engine = index.as_query_engine()
            rag_tool = QueryEngineTool.from_defaults(query_engine, name="papers_rag", description="A RAG engine with information from selected scientific papers")
            agent = ReActAgent.from_tools(tools=[rag_tool, pubmedtool, arxivtool], verbose=True)
            response = agent.chat(message = message, chat_history = message_history)
            response = str(response)
            message_history.append(ChatMessage(role="user", content=message))
            message_history.append(ChatMessage(role="assistant", content=response))
            r = ""
            for char in response:
                r+=char
                time.sleep(0.001)
                yield r
    else:
        vector_store = QdrantVectorStore(client = qdrant_client, collection_name=collection, enable_hybrid=True)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        query_engine = index.as_query_engine()
        rag_tool = QueryEngineTool.from_defaults(query_engine, name="papers_rag", description="A RAG engine with information from selected scientific papers")
        agent = ReActAgent.from_tools(tools=[rag_tool, pubmedtool, arxivtool], verbose=True)
        response = agent.chat(message = message, chat_history = message_history)
        response = str(response)
        message_history.append(ChatMessage(role="user", content=message))
        message_history.append(ChatMessage(role="assistant", content=response))
        r = ""
        for char in response:
            r+=char
            time.sleep(0.001)
            yield r

def to_markdown_color(grade: str):
    colors = {"red": "ff0000", "yellow": "ffcc00", "green": "33cc33"}
    mdcode = f"![#{colors[grade]}](https://placehold.co/15x15/{colors[grade]}/{colors[grade]}.png)"
    return mdcode

def get_qdrant_collections_dets():
    collections = [c.name for c in qdrant_client.get_collections().collections]
    details = []
    counter = 0
    for collection in collections:
        counter += 1
        dets = qdrant_client.get_collection(collection)
        p = f"### {counter}. {collection}\n\n**Number of Points**: {dets.points_count}\n\n**Status**: {to_markdown_color(dets.status)} {dets.status}\n\n"
        details.append(p)
    final_text = "<h2 align='center'>Available Collections</h2>\n\n"
    final_text += "\n\n".join(details)
    return final_text

## Frontend
accordion = gr.Accordion(label="⚠️Set up these parameters before you start chatting!⚠️")

iface1 = gr.ChatInterface(fn=reply, additional_inputs=[gr.File(label="Upload Papers (only PDF allowed!)", file_count="multiple", file_types=[".pdf","pdf",".PDF","PDF"], value=None), gr.Textbox(label="Collection", info="Upload your papers to a collection (new or existing)", value=""), gr.Checkbox(label="Use LlamaParse", info="Needs the LlamaCloud API key", value=False)], additional_inputs_accordion=accordion)
u = open("usage.md")
content = u.read()
u.close()
iface2 = gr.Blocks()
with iface2:
    with gr.Row():
        gr.Markdown(content)
iface3 = gr.Interface(fn=get_qdrant_collections_dets, inputs=None, outputs=gr.Markdown(label="Collections"), submit_btn="See your collections")
iface = gr.TabbedInterface([iface1, iface2, iface3], ["Chat💬", "Usage Guide⚙️", "Your Collections🔎"], title="PapersChat📝")
iface.launch(server_name="0.0.0.0", server_port=7860)