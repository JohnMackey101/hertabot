# HertaBot v0.1

    Developed by: Vexxations
    License: apache-2.0
    Finetuned from model : unsloth/llama-3-8b-Instruct-bnb-4bit
    4bit and 8bit quantized GGUF files for Hertabot v0.1, a conversational chatbot finetuned from llama-3-8b-instruct for deploying on Discord. This is an incredibly early-stage model that will be replaced as soon as improvements are made - and there are PLENTY

# Current features:

    - Has the personality and text mannerisms of Herta given an appropriate system prompt
    - Exclusively text-based, has /some/ ability to interpret contexts
    - TO BE TESTED

# Planned additions:

    - Discord action integration: allow for usage of images, emojis, gifs and other features on discord

    - Memory: remember users by name, traits inferred from messages

    - User recognition: distinguish users in context and address them accordingly

    - Enhanced persona believability: ensure Herta has no knowledge of "real life" subjects or distances herself from it (technically Earth is insignificant to her, and she's from the future)

    - Improved system prompt: Prompt atm is using Deepseekslop and I'd rather look over it and finetune it myself

    - Etc.

# Setup

    - DISCLAIMER: Model parameters are optimized for my flimsy GTX3060 with 7gigs of VRAM that I locally run the model on, feel free to tweak them at your discretion.
    
    1. Init local env in directory
    2. pip install -r requirements.txt
    3. py src/hertabot.py
    