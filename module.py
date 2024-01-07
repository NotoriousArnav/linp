from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import bs4

sample_prompt = """
<system>
You are an AI Assistant, which assists user with their Linkedin post.
The user might ask you to:
- Add Relevant Hashtags
- Change the Tone of the Text
- Correct Grammer or Refactor the Text
</system>
<user>
Add Relevant Hashtags:
'''
Discipline is the first step towards goal achievement.
'''
</user>
<assistant>
Suggested Hashtags:
- #Discipline
- #SelfDiscipline
- #SelfImprovement
- #startups
</assistant>
<user>
Add Relevant Hashtags:
'''
{post}
'''
</user>
<assistant>
Suggested Hashtags:

"""
llm = HuggingFaceHub(
    repo_id="tiiuae/falcon-7b-instruct",
    model_kwargs = {
        "temperature": 0.01,
        "max_length": 300
    }
)
prompt = PromptTemplate(
    template=sample_prompt,
    input_variables=["post"]
)
llm_chain = LLMChain(prompt=prompt, llm=llm)
def get_hashtags(stri):
    response = llm_chain(
        stri
    )
    resp = ''.join(['<assistant>\nSuggested Hashtags:\n',response['text']])
    soup = bs4.BeautifulSoup(resp, 'html.parser')
    res = soup.find_all('assistant')
    for x in res:
        l = list(set(x.text.split('\n')))
        l.sort(
            key= lambda a: a.find('#'),
            reverse=True
        )
        l.pop()
        l.remove('')
        for y in l:
            try:
                b = y.split('-')[1].strip()
                yield b
            except Exception as e:
                pass