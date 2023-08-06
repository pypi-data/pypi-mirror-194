import subprocess
import typer
from typing import List
from langchain import LLMChain, OpenAI, PromptTemplate
import platform

class GPTshell:
  def __init__(self):
    self.system = platform.system()
  def text_to_command(self, prompt: str, num_outputs: int = 1):
    template_text_to_command = PromptTemplate(input_variables=["num_outputs","human_input"], template="""Convert the input to {num_outputs}"""+ self.system + """possible  command: {human_input}""")
    llm = LLMChain(llm=OpenAI(temperature=0), prompt=template_text_to_command, verbose=False)
    return llm.predict(human_input=prompt, num_outputs=num_outputs).strip()
  
  def command_to_text(self, prompt: str):
    template_command_to_text = PromptTemplate(input_variables=["human_input"], template="""Describe the """ + self.system + """ command in English Language: {human_input}""")
    llm = LLMChain(llm=OpenAI(temperature=0), prompt=template_command_to_text, verbose=False)
    return llm.predict(human_input=prompt).strip()

app = typer.Typer()
LLMCommands = GPTshell()

  
@app.command(help="text to command: Execute a shell command by providing its description.")
def ttc(ttc: List[str]):
  text_to_command = " ".join(ttc)
  output = LLMCommands.text_to_command(text_to_command)
  print(f"\033[1;32;40m{output}\033[0m Do you want to run this command? (y/n)")
  if input().lower() == 'y':
    result = subprocess.run(["powershell", "-Command", output], capture_output=True, text=True)
    print(result.stdout)

@app.command(help="command to text: Get the description of a shell command.")
def ctt(ctt: List[str]):
  command = " ".join(ctt)
  output = LLMCommands.command_to_text(command)
  print(output)

if __name__ == "__main__":
  app()
