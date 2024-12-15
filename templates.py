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