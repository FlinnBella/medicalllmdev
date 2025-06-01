# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from prompts import base_prompt

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class PromptInput(BaseModel):
    prompt: str

@app.post("/diagnose")
def generate_diagnosis(prompt_input: PromptInput):
    # Combine base context + user input
    full_prompt = f"{base_prompt}\nPatient: {prompt_input.prompt}\nDiagnosis:"

    # Generate response
    output = generator(full_prompt, max_new_tokens=100, do_sample=False)
    return {"response": output[0]["generated_text"]}
