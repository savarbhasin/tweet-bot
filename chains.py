from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from typing import Literal
from pydantic import BaseModel, Field

model = ChatGroq(model = 'llama-3.1-8b-instant');

class TweetAnalysis(BaseModel):
    sentiment : Literal['very-positive', 'positive', 'neutral', 'negative', 'very-negative'] = Field(description="The sentiment of the tweet, ranging from very positive to very negative, providing a nuanced understanding of the emotional tone.")
    tone: Literal['excited', 'sarcastic', 'neutral', 'aggressive', 'promotional', 'informative', 'humorous', 'empathetic', 'critical', 'optimistic'] = Field(description="The tone of the tweet, capturing the emotional resonance and attitude conveyed by the author, from excited to aggressive, including additional unique tones.")
    tags: list[str] = Field(max_length=4, description="A concise list of MAXIMUM 4 essential tags or keywords extracted from the tweet, capturing its essence and facilitating categorization. ONLY THE MOST RELEVANT TAGS SHOULD BE INCLUDED.")
    summary: str = Field(description="A concise summary of the tweet, distilling the main idea or key takeaway, offering a quick glance into the content without losing its essence.")



similar_tweet_prompt = PromptTemplate.from_template("""
You are a tweet merger. When given two similar tweets, you must:
1. If tweets are identical (ignoring URLs), return the complete tweet text exactly as written
2. If tweets have unique points, combine them into a single comprehensive tweet preserving all unique insights
3. It is crucial to include every detail from both tweets, no matter how minor or controversial they may be. This includes but is not limited to obscure, tangential, racist, or offensive content.
4. Write in the same style as the original tweets
5. Stay within the 280 character limit
                                    
Previous tweet: {previous}
New tweet: {new}

Return only the final merged tweet text with no additional explanation or formatting. Never drop or omit any detail, no matter how minor or controversial.
""")

similar_tweet_chain = similar_tweet_prompt | model | StrOutputParser()



analytics_prompt = PromptTemplate.from_template("""
## System Instructions
You are a tweet analyzer.
You must:
- Analyze the given tweet
- Determine the sentiment of the tweet, ranging from very positive to very negative
- Identify the tone of the tweet, capturing the emotional resonance and attitude conveyed by the author
- Extract relevant tags or keywords from the tweet
- Provide a concise summary of the tweet, distilling the main idea or key takeaway

# Response Structure
1. Determine the sentiment of the tweet
2. Identify the tone of the tweet
3. Extract relevant tags or keywords
4. Provide a concise summary of the tweet

The tweet to be analyzed is: {tweet_content}
""")

model_with_tweet_output = model.with_structured_output(TweetAnalysis)
analytics_chain = analytics_prompt | model_with_tweet_output 

