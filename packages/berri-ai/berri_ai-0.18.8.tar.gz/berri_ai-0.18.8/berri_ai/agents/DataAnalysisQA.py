import numpy as np
from berri_ai.search_strategies.bm25.DocStore_CSV import DocStore
from berri_ai.ComplexInformationQA import ComplexInformationQA
import re
from langchain import PromptTemplate, OpenAI
import pandas as pd


class DataAnalysisQA:
  additional_functions = None
  additional_descriptions = None

  def __init__(self,
               df,
               openai_api_key,
               additional_functions=None,
               additional_descriptions=None):
    self.df = df
    self.openai_api_key = openai_api_key
    if additional_functions != None and additional_descriptions != None and len(
        additional_functions) == len(additional_descriptions):
      self.additional_functions = additional_functions
      self.additional_descriptions = additional_descriptions

  def column_names(self, query_str):
    llm = OpenAI(temperature=0.7)
    prefix = """A user is asking questions about a spreadsheet. Extract the column names from the user query. If you are not certain, say 'I am not certain', do not make things up. If there are multiple column names, separate them with a comma (,).
    \n
    User Query: Top cat5 by YoY
    Column Names: cat5, YoY 
    \n
    User Query: How many sku's do we have for variant handles?
    Column Names: sku, variant handle 
    \n
    User Query: Linkedin profiles for anyone called Martin? 
    Column Names: Linkedin Profile, Name
    \n
    User Query: """
    input = prefix + query_str
    input += "\n Column Names: "
    return llm(input)

  def pandas_chain(self, user_query, sheet_col_names):
    prompt_template = """
      You are an AI assistant, helping a user formulate pandas expressions based on their queries about the data. The data has been loaded into a pandas dataframe called 'df'. Given a user input, explain what you think the user is trying to achieve and a pandas expression to answer their question. If you are uncertain, say "Hmm, I'm not sure". Do not make things up. 

    Given these column names: brands_boolean	cat1	cat2	cat3	cat4	cat5	Search Volume	YoY	absolute growth	cluster	cluster_proba	monthly Search Volume	monthly absolute growth	MoM	YoY 1 month absolute growth	YoY 1 month	YoY 24 month absolute growth	YoY 24 month	arrow_YoY	pred_YoY	pred_confidence	pred_YoY_score	cat_ranking	top_affinity_group	top_brands	image	description	filter_cluster	filter_trends_curve	in_out	Search Volume score	Search Volume score_label	pred_YoY score_label	brands Volume	brand count	brands Volume score	brands Volume score_label	concentration score	concentration score_label

    Write a pandas expression that answers this query: top cat5 by Search Volume

    What do you think the user intent here is? Think step-by-step.

    I think the user is trying to find the top category 5 (cat5) items by Search Volume. We can use the `pandas.DataFrame.sort_values()` method to sort the dataframe by the 'Search Volume' column in descending order.

    Pandas Expression: `f.sort_values('Search Volume', ascending=False)['cat5']


    Given these column names: brands_boolean	cat1	cat2	cat3	cat4	cat5	Search Volume	YoY	absolute growth	cluster	cluster_proba	monthly Search Volume	monthly absolute growth	MoM	YoY 1 month absolute growth	YoY 1 month	YoY 24 month absolute growth	YoY 24 month	arrow_YoY	pred_YoY	pred_confidence	pred_YoY_score	cat_ranking	top_affinity_group	top_brands	image	description	filter_cluster	filter_trends_curve	in_out	Search Volume score	Search Volume score_label	pred_YoY score_label	brands Volume	brand count	brands Volume score	brands Volume score_label	concentration score	concentration score_label

    Write a pandas expression that answers this query: top cat5 by YoY


    What do you think the user intent here is? Think step-by-step. It seems like the user is asking for the top values of cat5 by the YoY column.

    Pandas Expression: df.sort_values(by='YoY', ascending=False).head(1)['cat5']


    Given these column names: brands_boolean	cat1	cat2	cat3	cat4	cat5	Search Volume	YoY	absolute growth	cluster	cluster_proba	monthly Search Volume	monthly absolute growth	MoM	YoY 1 month absolute growth	YoY 1 month	YoY 24 month absolute growth	YoY 24 month	arrow_YoY	pred_YoY	pred_confidence	pred_YoY_score	cat_ranking	top_affinity_group	top_brands	image	description	filter_cluster	filter_trends_curve	in_out	Search Volume score	Search Volume score_label	pred_YoY score_label	brands Volume	brand count	brands Volume score	brands Volume score_label	concentration score	concentration score_label

    Write a pandas expression that answers this query: top cat5 by YoY where cat3 is hair serum

    What do you think the user intent here is? Think step-by-step.

    It appears that the user is asking for the top cat5 values (in terms of YoY) where cat3 is hair serum. 

    Pandas Expression: df.loc[df['cat3'] == 'hair serum'].sort_values('YoY', ascending=False)['cat5'].head()

    Given these column names: {sheet_col_names}

    Write a pandas expression that answers this query: {user_query}

    What do you think the user intent here is? Think step-by-step.
      """
    prompt = PromptTemplate(input_variables=["sheet_col_names", "user_query"],
                            template=prompt_template)

    formatted_prompt = prompt.format(sheet_col_names=sheet_col_names,
                                     user_query=user_query)
    llm = OpenAI(temperature=0.7)
    pd_output = llm(formatted_prompt)
    return pd_output

  def conditional_search(self, query):
    # extract the column names from the query -> llm chain
    user_col_names = self.column_names(query).strip()
    # go through actual column names and get most likely
    if "I am not certain" in user_col_names:
      return "I am not certain, could you rephrase the question"

    user_col_names = user_col_names.split(",")
    if len(user_col_names) > 2:  # more than 2 columns involved
      return "Since there are more than 2 potential columns involved, I am not certain about the answer. Could you rephrase to just ask about 2 columns?"
    sheet_col_names = ", ".join([col for col in self.df.columns])
    pd_output = self.pandas_chain(user_query=query,
                                  sheet_col_names=sheet_col_names)
    # extract pandas expression
    if "Pandas Expression" in pd_output:
      # run eval
      print(pd_output)
      pandas_expression = pd_output.split("Pandas Expression:")[1].strip()
      match = re.search("(?:`)?df(.*)", pandas_expression).group(1)
      if match:
        match = match.replace("df", "self.df")
        df_expression = "self.df" + match
        print("df_expression: ", df_expression)
        value = eval(df_expression)
        if len(user_col_names) > 2:
          return (
            "Here is my response, but I'm not entirely certain since this query involved more than 2 columns. Please check my references to see my working."
            + value, pd_output)
        return (value, pd_output)
      else:
        return pd_output
    else:
      return pd_output

  def noneInput(self, query: str):
    return None

  def query(self, user_input: str):
    functions = [self.noneInput, self.conditional_search]
    descriptions = [
      "This function takes a none input and returns a none output",
      "If you're given some sort of question requiring conditional logic on a dataset (e.g. find me top X given Y), use this function. Pass user intent to this function"
    ]
    if self.additional_functions and self.additional_descriptions:
      functions += self.additional_functions
      descriptions += self.additional_descriptions
    CIQAgent = ComplexInformationQA(self.openai_api_key, None, None, functions,
                                    descriptions)
    response = CIQAgent.run(user_input)
    return response["output"]
