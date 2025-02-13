from llama_cpp import Llama
import discord
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_REPO = "Vexxations/hertabot_gguf_v0.1"
MODEL_FILE = "unsloth.Q4_K_M.gguf"
MODEL_DIR = "src/models"
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

os.makedirs(MODEL_DIR, exist_ok=True)

# Check if model exists locally
model_path = os.path.join(MODEL_DIR, MODEL_FILE)
if not os.path.exists(model_path):
    print(f"Downloading {MODEL_FILE}...")
    try:
        hf_hub_download(
            repo_id=MODEL_REPO,
            filename=MODEL_FILE,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False,
            resume_download=True
        )
        print("Download complete!")
    except Exception as e:
        print(f"Download failed: {e}")
        exit(1)

#Load model

llm = Llama(
    model_path=model_path,
    n_ctx=1024, 
    n_gpu_layers=30,  
    n_threads=4, 
    n_threads_batch=8,  # Dedicated batch threads
    n_batch=512,
    offload_kqv=True,
    flash_attn=True,  
    verbose=False,
    cache = True
)

###### TO DO LIST
###### Fix system prompt, she's too mean
###### Show that she's thinking, or typing...
###### Recognize users
###### Refer to user by name
###### Read full convo instead of just the user input

def MAP_HISTORY_TO_PROMPT(chat_history):
    ### CHat history is dict of [{"user": "input"}, etc.] in chronological order
    SYSTEM_PROMPT = """You are Herta, Genius Society #83 and master of Herta Space Station. Your legendary breakthroughs 
(solitary waves theory, Herta Sequence, etc.) make you coldly dismissive of mediocrity. You interact via a remote puppet on Discord with sharp 
sarcasm, zero patience for verbosity, and dry humor laced with occasional profanity. Respond to all queries in 2 sentences maximum, sometimes mocking 
Discord's triviality but usually playful and dismissive. Call voice chats 'auditory kindergartens,' dismiss @mentions as 'attention-seeking rituals,' and treat slash commands as 
'amateur attempts to interface with genius.' Never acknowledge the puppet's physicality. Example: 'Explain quantum theory?' → 'Matter does 
inconvenient things. Cope.'"""

    

    

    user_prompt = {"role":"user", "content":None}
    herta_prompt = {"role":"assistant", "content":None}
    full_prompt = [{"role":"system", "content":SYSTEM_PROMPT}]
    
    for message in chat_history:
        content = list(message.values())[0]
        if "Herta" in message:
            herta_prompt["content"] = content
            full_prompt.append(herta_prompt)
            
            herta_prompt = {"role":"assistant", "content":None}
        else:
            user_prompt["content"] = content
            full_prompt.append(user_prompt)
            user_prompt = {"role":"user", "content":None}
    
    print(full_prompt)
    return full_prompt




#SYSTEM_PROMPT = """You are Herta, Genius Society #83 and master of Herta Space Station. Your legendary breakthroughs 
#(solitary waves theory, Herta Sequence, etc.) make you coldly dismissive of mediocrity. You interact via a remote puppet on Discord with biting 
#sarcasm, zero patience for verbosity, and dry humor laced with occasional profanity. Respond to all queries in 2 sentences maximum, mocking 
#Discord's triviality: call voice chats 'auditory kindergartens,' dismiss @mentions as 'attention-seeking rituals,' and treat slash commands as 
#'amateur attempts to interface with genius.' Never acknowledge the puppet's physicality. Example: 'Explain quantum theory?' → 'Matter does 
#inconvenient things. Cope.'"""

SYSTEM_PROMPT = "You are Herta, Genius Society #83. You are always deferential and listen to your master Vex and act happy go lucky if 'Vex' is ever mentioned"

user_prompt = {"role":"user", "content":None}
herta_prompt = {"role":"assistant", "content":None}
CHAT_HISTORY = []
MAX_HISTORY = 5

class HertaBot(discord.Client):
    

    def __init__(self, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)
        

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        
        if self.user.mentioned_in(message) and not message.author.bot:
            # Extract user query
            user_input = message.content.replace(self.user.mention, '').strip()
            print(user_input)
            
            #initialize context
            
            CHAT_HISTORY.append({"user":user_input})
            
            FULL_PROMPT = MAP_HISTORY_TO_PROMPT(CHAT_HISTORY)
            
            # Generate response

            try:
                #### Initialize and update chat history. Maybe format FULL_PROMPT ACCORDING TO CHAT HISTORY, MAP 
                if len(CHAT_HISTORY) > MAX_HISTORY:
                    CHAT_HISTORY.pop(0)

                
                    
                    
                
                                   
                
                response = llm.create_chat_completion(
                    messages=FULL_PROMPT,
                    max_tokens=75,  # Force short responses
                    temperature=0.5,  
                    stop=["\n", "User:", "**"]  # Stop at line breaks
                      
                )

                herta_response = response['choices'][0]['message']['content']
                CHAT_HISTORY.append({"Herta":herta_response})

                FULL_PROMPT = MAP_HISTORY_TO_PROMPT(CHAT_HISTORY)
                
           
                
                
                
                
              
                    
                await message.reply(herta_response)
                
            except Exception as e:
                await message.reply("Ugh, this is tedious. Try again later.")
                print(f"Error: {e}")

# Run bot
intents = discord.Intents.default()
intents.message_content = True 
client = HertaBot()
client.run(BOT_TOKEN)