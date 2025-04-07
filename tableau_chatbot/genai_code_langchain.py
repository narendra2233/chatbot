def gen_ai(**kwargs):
    import pandas as pd
    import numpy as np
    import openai
    from openai import OpenAI
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from column_list import column_list_dict
    from feedback_data import feedback_data_given
    from langchain.schema.output_parser import StrOutputParser
    from prompt import input_prompt
    from dotenv import load_dotenv
    from better_profanity import profanity
    from nemoguardrails import RailsConfig
    from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
   
    import re

    load_dotenv()
   
    data = pd.DataFrame(kwargs)

    eval_df = pd.DataFrame(columns=["Data Format", "Data raw","Columns"]) 
    df1_columns = str(' , '.join(data.columns))
    column_list = np.array(data.columns)
    data_json = data.to_json(orient='records')
    eval_df.loc[len(eval_df)] = ["JSON", data_json, df1_columns]

    #key = 'private_key'

    embeddings_model = OpenAIEmbeddings(model='text-embedding-ada-002')

    questions = [f"Generate summary for table data whose columns are {item['Column name']}" for item in feedback_data_given]
    summary = [item["Summary"] for item in feedback_data_given]
    score = [item["Score"] for item in feedback_data_given]

    vectorstore = FAISS.from_texts(questions, embeddings_model)

    question_feedback = f"Generate summary for table data whose columns are {str(eval_df.loc[0]['Columns'])}"
    similar_questions = vectorstore.similarity_search(question_feedback, k=1)
    sum = []
    sco = []
    
    for question in similar_questions:
      question_text = question.page_content
      indices = [i for i, q in enumerate(questions) if q == question_text]
      for i in indices:
          sum.append(summary[i])
          sco.append(score[i])
          
    data = pd.DataFrame({'Summary':sum, 'Score': sco})

    feedback_similar_data = data.to_json(orient='records')
    table_similar_data = str(eval_df.loc[0]['Data raw']) 


    external_data = list(column_list_dict.keys())
    external_data_up = [str(i) for i in external_data]
    external_data_values = list(column_list_dict.values())
    external_data_up_values = [str(i) for i in external_data_values]  

    vectorstore_external = FAISS.from_texts(external_data_up, embeddings_model)

    column_dict = {}
    for i in column_list:
      question_external = str(i)
      similar_questions = vectorstore_external.similarity_search(question_external, k=1)
      nearest_index = external_data_up.index(similar_questions[0].page_content)
      key_to_get = external_data_up[nearest_index]
      value_to_get = external_data_up_values[nearest_index]
      column_dict[key_to_get] = value_to_get




    query = "suggest a title that best represents the financial health and trends and generate insights by summarizing the data and providing numerical data points all under 100 words."

    

    try: 
      prompt = ChatPromptTemplate.from_messages([
              ("system", "You are experienced financial consultant. Analyze the data and give a suitable title and generate valuable insights."),
              ("user", input_prompt)
            ])
      

      llm = ChatOpenAI(model="gpt-4o",temperature = 0)
      chain = prompt | llm | StrOutputParser()

      config=RailsConfig.from_path("config2")

      guard_rails=RunnableRails(config=config)
      

      guard_rail_chain=guard_rails | chain


      result = guard_rail_chain.invoke({"column_context": str(column_dict), "context_feedback":str(feedback_similar_data), "context_data": str(table_similar_data),"input": query})
      
      return result
      

    

    except Exception as e:
      return e

import pandas as pd

# Sample data with lists (compatible with gen_ai)
data = {
    'Region': ['North America', 'Europe', 'Asia', 'Australia', 'India'],
    'Product': ['Laptop', 'Tablet', 'SmartPhone', 'Headphone', 'Smartwatch'],
    'Date': ['2023-02-02', '2023-02-03', '2023-02-04', '2023-02-23', '2023-02-05'],
    'Sales': [2000, 2500, 3000, 3400, 4000],
    'Quantity': [5, 6, 7, 8, 4],
    'Profit': [500, 600, 700, 450, 700]
}

# Create DataFrame
df = pd.DataFrame(data)

# Call gen_ai with the sample data
result = gen_ai(**{'Region': df['Region'], 'Product': df['Product'], 
                   'Date': df['Date'], 'Sales': df['Sales'], 
                   'Quantity': df['Quantity'], 'Profit': df['Profit']})

print(result)





