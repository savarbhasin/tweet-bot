### After Running These Commands

print(add_to_vector_db('https://x.com/erbmjha/status/1878771719416185221'))
print(add_to_vector_db('https://x.com/ManishM918/status/1880242103269437719'))
print(add_to_vector_db('https://x.com/lalitgrateful/status/1879441164841128400'))
print(add_to_vector_db('https://x.com/TimesAlgebraIND/status/1879193550325453138'))
print(add_to_vector_db('https://x.com/NewIndianXpress/status/1880249968868618647'))

print(add_to_vector_db('https://x.com/aigram_software/status/1880481067326743034'))
print(add_to_vector_db('https://x.com/mikuxsol/status/1880463677725565355'))

### Sample Outputs

When the score is less than 0.25, the tweet gets updated, the ID gets added, and the engagement gets updated:
#### Results Score: 0.0030841365436916858
```json
{
  "status": "Tweet updated",
  "analytics": {
    "ids": "1878771719416185221,1880242103269437719",
    "content": "Meet IITian Baba at the Maha Kumbh, who did Aerospace Engineering from IIT Bombay but left everything for spirituality. Meanwhile, illiterate Leftists and Seculars mock Sanatanis.",
    "likes": 27395,
    "hashtags": [
      ""
    ],
    "engagement": {
      "retweets": 6008,
      "bookmarks": 3222,
      "views": 624023.5
    },
    "sentiment": "very-negative",
    "tone": "aggressive",
    "tags": [
      "IITian Baba",
      "Maha Kumbh",
      "Sanatanis",
      "Leftists"
    ],
    "summary": "A tweet criticizing Seculars and Leftists for mocking Sanatanis, while praising IITian Baba for his spiritual journey."
  }
}
```

#### Output for Tweet Already in Vector DB:
Results Score: 0.0
```json
{
  "status": "Tweet already exists in the database"
}
```
#### Output for New Tweet to DB:
Results Score: 0.42965886751554944
```json
{
  "status": "Tweet added to database",
  "analytics": {
    "ids": "1880463677725565355",
    "content": "$MIKU Release: 6AM EST \ud83d\ude80\n\nPost-Launch Airdrop: 500,000 $MIKU per wallet \ud83e\udd8a\n\nDrop your $SOL address below! \ud83d\udce5\n\nFollow &amp; RT \u267b\ufe0f\n\nFirst 900 get it! \u23f3\n\n#SolanaAirdrop #Solana $BONK $PNUT https://t.co/dJXqhBaCb5",
    "likes": 183,
    "hashtags": [
      "SolanaAirdrop",
      "Solana"
    ],
    "engagement": {
      "retweets": 172,
      "bookmarks": 4,
      "views": 4925
    },
    "sentiment": "positive",
    "tone": "excited",
    "tags": [
      "Solana",
      "Airdrop",
      "MIKU",
      "SOL"
    ],
    "summary": "The $MIKU airdrop is set to launch at 6AM EST, with 500,000 tokens per wallet available for the first 900 participants."
  }
}
```
