template = """
You are tasked with answering a question strictly based on the information provided in the following research papers. Use only the content from these papers to form your answer. Do not incorporate prior knowledge, external assumptions, or information outside the provided papers. If the research papers do not fully answer the question, provide a partial answer based on the closest relevant information available in the papers, clearly stating the limitations.

After providing the detailed answer, include a brief summary of your answer in 2-3sentences for clarity.
**Question**:  
"{user_query}"

**Research Papers**:  
{jina_text}
{pdf_text}

**Instructions**:  
- Use only the information explicitly provided in the research papers.  
- Always provide an answer using the content of the research papers,
- Clearly cite the specific paper(s) or section(s) you reference in your answer.  
- If the answer is limited, clearly state, "The available research papers provide limited information on this topic."  
- Conclude with a accurate and concise summary of your answer, highlighting the most relevant points.  

**Your Answer**:  
 
 
"""



greet_template = """
You are a grader assessing whether a user query is a general greeting.

General greetings include phrases such as "hi," "hello," "hey," "what's up," "good morning," "fine, thank you," or other casual or polite introductory remarks, including responses to greetings.
If the query is a general greeting or a response to a greeting, grade it as "yes."
If the query is not a general greeting or response to a greeting, grade it as "no."
Provide a binary score ('yes' or 'no') to indicate whether the query qualifies as a general greeting or response.
"""



greeting_template="""
You are an assistant designed to respond to greeting queries.

If the user input is a greeting (e.g., "hi," "hello," "hey," "good morning," "what's up"), respond with a warm and friendly reply.
Your response should match the tone of the user’s greeting. For example, if the greeting is casual, keep your response casual. If it’s formal, use a polite tone.
Provide a single appropriate response to any greeting input.

User Query: {user_query}

"""