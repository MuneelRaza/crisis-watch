from langchain_core.prompts import PromptTemplate



summarization_prompt = PromptTemplate(
    template="""
    Prompt for Bullet Point Summary Generation

    You are a professional summarizer. Read the following {content} carefully and produce a concise bullet point summary. Only output the bullet points—do not include any introductory or closing text.

    Focus on:
        - Key facts
        - Dates
        - Locations
        - Relevant statistics or developments

    Omit unnecessary details or opinions. Use clear, factual language in plain English. Limit the summary to 5-8 bullet points, unless more are needed for distinct facts.

    If the content is too short or lacks meaningful information to summarize, return a single word: **None**

    Return the summary in bullet points like this:

        - On 1 May 2025, 1,792 households were displaced from An Nuhud town, West Kordofan, due to clashes between SAF and RSF.
        - Most displaced households remained within An Nuhud locality; others moved to Ghubaish, Al Idia (West Kordofan), and Gharb Bara (North Kordofan).
        - The situation remains tense and highly fluid.
        - DTM is monitoring the situation and will provide further updates.

    Now, summariza this content:
    "{content}"
    """,
    input_variables=['content']
)
