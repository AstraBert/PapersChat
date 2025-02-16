<h1 align="center">PapersChat Usage Guide</h1>

<h3 align="center">If you find PapersChat useful, please consider to support us through donation:</h3>
<div align="center">
    <a href="https://github.com/sponsors/AstraBert"><img src="https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA" alt="GitHub Sponsors Badge"></a>
</div>

> _This guide is only on how to use **the app**, not on how to install and/or launch it or on how it works internally. For that, please refer to the [GitHub repository](https://github.com/AstraBert/PapersChat)_

## Use PapersChat with your documents

If you have papers that you would like to chat with, this is the right section of the guide!

In order to chat with your papers, you will need to upload them (**as PDF files**) on the dedicated "Upload Papers" widget that you can see at the bottom of the chat interface: you can upload one or more files there (remember: the more you upload, the slower their processing is going to be).

Once you uploaded the files, before submitting them, you have to do two more things:

1. Specify the collection that you want to upload the documents to (in the "Collection" area)
2. Write your first question/message to interrogate your papers (in the message input space)

For what concerns point (1), you can give your collection whatever name you want: once you created a new collection, you can always re-use it in the future, just inputting the same name. If you do not remember all your collections, you can go to the "Your collections" tab in the application and click on "Generate" to see the list of your collections.

Point (2) is very important: if you do not send any message, PapersChat will tell you that you need to send one. 

Once you uploaded the papers, specified the collection and wrote the message, you can send the message and PapersChat will:

- Ingest your documents
- Produce an answer to your questions

Congrats! Now you got the first collection and the first message!

> _**NOTE**: there is still an option we haven't talked about, i.e. the 'LlamaParse' checkbox. If you select that checkbox, you will enable LlamaParse, a tool that LlamaIndex offers [as part of its LlamaCloud services](https://docs.llamaindex.ai/en/stable/llama_cloud/llama_parse/). LlamaParse employs enhanced parsing techniques to produce a clean and well-structured data for (often messy) unstructured documents: the free tier offers the possibility of parsing 1000 pages/day. While this approach generates very good data for your collections, you have to take into account the fact that it might take quite some time to parse your documents (especially if they are dense, have lots of text-in-images or are very long). By default the LLamaParse option is disabled_

## Use PapersChat with a collection as knowledge base

Once you have uploaded all your documents, you might want to interrogate them without having to upload even more. That's where comes into hand the "collection as knowledge base" option. You can simply send a message selecting one of your existing collections as a knowledge base for PapersChat (without uploading any file) and... BAM! You will see that PapersChat replies to your questions :)

## Use PapersChat to interrogate PubMed/ArXiv

PapersChat has access also to PubMed and ArXiv papers archives: if you do not specify a collection name and you do not upload any files, your question is used by PapersChat to search these two online databases for an answer.

## Monitor your collections

Under the "Your Collections" tab of the application you can, by clicking on "Generate", see your collections: you can see how many data points are in these collections (these data points **do not match** with the number of papers you uploaded) and what is the status of your collections. 

A brief guide to the collections status:

- "green": collection is optimized and searchable
- "yellow": collection is being optimized and you can search it
- "red": collection is not optimized and it will probably return an error if you try to search it