# Chat with YouTube (STT - TTS and RAG-based Architeture) Model
![alt text](<DALL·E 2024-10-30 14.54.58 - Create an image of the YouTube logo, centered and large, with vibrant red and white colors on a clean background, giving it a high-resolution and bold.webp>)


## Main Goal

I am building a RAG-based chatbot that process any youtube video and answer questions directly through an interactive user interface.
The chatbot takes a YouTube link as input then process it with OpenAI's Whisper model and build an faiss index which stores the textual data used to retrieve relevant context and responses.

### Description about the model.
The users can record their questions in audio format and the questions are captured in real-time, processed, the underlying GPT model will embed and process the quection, extract relevant answers which can then be provided back in either textual or speech format.

## Extension

The model can be extended to process any speech captured in audio or video format. 
The transcribed speech or recorded speech can also be translated into speech using the TTS (Text-To-Speech) technollogy integrated in this model. I have specifically used Google Text-to-Speech API which has a high accuracy.

## Further implementation
### __Real-Time Voice AI chatbot__

- Implement a function that will take in voice recorded from the user, transcribe into text, do the required text, respond as a text or audio. 
- Try to find OpenAI/Gemini API that can facilitate this instead of starting from scratch.
