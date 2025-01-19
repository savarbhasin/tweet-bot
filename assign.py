import json
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from utils import get_tweet_pid, create_tweet_document, create_updated_tweet, get_tweet_with_analytics
from chains import similar_tweet_chain


embeddings = OpenAIEmbeddings()

vector_store = Chroma(
    collection_name='tweets',
    embedding_function=embeddings,
    persist_directory='./tweet_db'
)

def format_output(data):
    return json.dumps(data, indent=2)

def add_to_vector_db(tweet_url):
    tweet_data = get_tweet_pid(tweet_url)
    results = vector_store.similarity_search_with_score(
        tweet_data['post_content'],
        k=1
    )
    if(results!=[]): 
        print('Results score:', results[0][-1])

    if results == []:
        tweet_doc = create_tweet_document(tweet_data)
        vector_store.add_documents([tweet_doc], ids=[tweet_data['id']])
        
        analytics_tweet = get_tweet_with_analytics(tweet_doc)

        return format_output({"status": "Tweet added to database", "analytics": analytics_tweet})

    for res, score in results:
        if res.id == tweet_data['id']:
            return format_output({"status": "Tweet already exists in the database"})
        ids = res.metadata['ids'].split(',')
        if tweet_data['id'] in ids:
            return format_output({"status": "Tweet already exists in the database"})
    
    for res, score in results:
        if score >= 0.25:
            tweet_doc = create_tweet_document(tweet_data)
            vector_store.add_documents([tweet_doc], ids=[tweet_data['id']])

            analytics_tweet = get_tweet_with_analytics(tweet_doc)

            return format_output({"status": "Tweet added to database", "analytics": analytics_tweet})
        else:
            post_content_prev = res.page_content
            post_content_new = tweet_data['post_content']

            unique_points = similar_tweet_chain.invoke({
                "previous": post_content_prev,
                "new": post_content_new
            })

            updated_doc = create_updated_tweet(res, tweet_data, unique_points)


            analytics_tweet = get_tweet_with_analytics(updated_doc)

            vector_store.update_document(
                document=updated_doc,
                document_id=res.id
            )
            
            return format_output({"status": "Tweet updated", "analytics": analytics_tweet})


print(add_to_vector_db('https://x.com/erbmjha/status/1878771719416185221'))
print(add_to_vector_db('https://x.com/ManishM918/status/1880242103269437719'))
print(add_to_vector_db('https://x.com/lalitgrateful/status/1879441164841128400'))
print(add_to_vector_db('https://x.com/TimesAlgebraIND/status/1879193550325453138'))
print(add_to_vector_db('https://x.com/NewIndianXpress/status/1880249968868618647'))

print(add_to_vector_db('https://x.com/aigram_software/status/1880481067326743034'))
print(add_to_vector_db('https://x.com/mikuxsol/status/1880463677725565355'))