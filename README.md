# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
I chose the domain of world cup records because it is a topic that is currently in high demand due to the 2026 FIFA World Cup that is happening in a few days. It is hard to find through official channels because of the vast history of the tournament makes it difficult to find specific records, statistics, and trivia without sifting through a large amount of information. Additionally, many official sources may not have comprehensive or easily accessible data on all the records and statistics related to the World Cup, especially for older tournaments. This makes it a perfect domain for a retrieval-augmented generation system that can quickly provide accurate and relevant information to users.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | FIFA World Cup records and statistics|Notable records set in the nearly 100 years of the tournament's existence |https://en.wikipedia.org/wiki/FIFA_World_Cup_records_and_statistics |
| 2 |World Cup 2026 in numbers: Key statistical goals, titles and age records |Adds age records to the mix |https://www.aljazeera.com/sports/2026/6/7/world-cup-2026-in-numbers-key-statistical-goals-titles-and-age-records |
| 3 |100 World Cup Facts and Trivia Every Fan Should Know |nicher trivia | https://www.foxsports.com/stories/soccer/world-cup-facts-stats-trivia|
| 4 |List of FIFA World Cup hosts |Every host nation in world cup history |https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_hosts |
| 5 |List of FIFA World Cup songs and anthems
|World cup Soundtrack Trivia | https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_songs_and_anthems|
| 6 |World Cup Trivia |Adittional Trivia |https://quizlet.com/gb/748582824/world-cup-trivia-flash-cards/|
| 7 |Hit me with your most unbelievable football facts that sound fake but are true. |Reddit forum on world cup trivia |https://www.reddit.com/r/worldcup/comments/1hjtlku/hit_me_with_your_most_unbelievable_football_facts/ |
| 8 | 7 little known facts about the World Cup|More niche trivia |https://www.history.co.uk/articles/7-little-known-facts-about-the-world-cup |
| 9 |World Cup Quiz answers |Really niche trivia |https://rupertcolley.com/non-fiction/the-world-cup-a-short-history/the-world-cup-quiz/the-world-cup-quiz-answers/the-world-cup-quiz-answers-for-real/ |
| 10 |World Cup Ultimate Guide | basic info about the world cup with trivia included | https://www.roadtrips.com/luxury-travel-guides/world-cup-ultimate-guide/|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->
I preprocessed by removing uncessary tags in the HTML and removed headers or anything with emojis in them as those are usually styleistic bloat.

Here are 5 chunks from my documents:
────────────────────────────────────────────────────────────────────────────────
CHUNK 1 | From: 100_World_Cup_Facts_and_Trivia.txt | Index: 0
────────────────────────────────────────────────────────────────────────────────
HEADINGS: # 100. Who has scored in the most editions of the World Cup all time? # 99. Which South American player has the most all-time World Cup goals? # 98. What is the USA's best finish at a World Cup? # 97. What is the farthest stage Mexico has r


────────────────────────────────────────────────────────────────────────────────
CHUNK 2 | From: 100_World_Cup_Facts_and_Trivia.txt | Index: 63
────────────────────────────────────────────────────────────────────────────────
earances without ever having won? Netherlands with three final appearances (1974, 1978, 2010). 74. Which African player has the most goals scored in the World Cup? Asamoah Gyan (Ghana) with six. 73. Who has the record for most goals scored in a singl


────────────────────────────────────────────────────────────────────────────────
CHUNK 3 | From: 100_World_Cup_Facts_and_Trivia.txt | Index: 125
────────────────────────────────────────────────────────────────────────────────
 the right Item 1 of 3


────────────────────────────────────────────────────────────────────────────────
CHUNK 4 | From: 7_little_known_facts_about_the_World_Cup.txt | Index: 0
────────────────────────────────────────────────────────────────────────────────
HEADINGS: # 1. Almost 50% of the world's population watches the competition # The history of the World Cup # 2. England did not take part in the first three tournaments # Everything you need to know about the Women's World Cup # 3. The First Women's 


────────────────────────────────────────────────────────────────────────────────
CHUNK 5 | From: 7_little_known_facts_about_the_World_Cup.txt | Index: 14
────────────────────────────────────────────────────────────────────────────────
the team to beat in the women's game, winning four tournaments so far. The 1991 Women's World Cup saw matches last just 80 minutes. This seems rather unfair given, at one point, women’s football was bigger than men’s . Read more about Sport When wome

**Chunk size:**
250 characters 
**Overlap:**
50 characters 
**Why these choices fit your documents:**
The smaller chunk size creates more targeted chunks that improve retrieval precision. Each chunk is still substantial enough to be meaningful but small enough to avoid pulling in diluted or multi-topic content. The 50-character overlap (~8 tokens) is proportionally balanced to maintain context continuity while preventing information fragmentation. With this configuration, I achieved 240 total chunks across 8 documents, which falls comfortably in the optimal range of 50-2,000 chunks — allowing for specific, retrievable information without excessive granularity.
**Final chunk count:**
1265
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->
================================================================================
QUERY #1
================================================================================

❓ Who has scored the most goals in World Cup history?


--- Result #1 ---
Source: 100_World_Cup_Facts_and_Trivia.txt
Chunk Index: 23
Distance Score: 0.2474
Assessment: ✅ Excellent match

Content:
Cup? David Villa with nine. 66. What is the record for most goals scored by a player in a single World Cup? 13, by Just Fontaine (France) in 1958. Just Fontaine against West Germany in the 1958 third-place game (Photo by DB/picture alliance via Getty


--- Result #2 ---
Source: 100_World_Cup_Facts_and_Trivia.txt
Chunk Index: 18
Distance Score: 0.2902
Assessment: ✅ Excellent match

Content:
African player has the most goals scored in the World Cup? Asamoah Gyan (Ghana) with six. 73. Who has the record for most goals scored in a single World Cup match? Oleg Salenko (Russia) with five against Cameroon. 72. Since odds were first listed in 


--- Result #3 ---
Source: World_Cup_Quiz_answers.txt
Chunk Index: 20
Distance Score: 0.2933
Assessment: ✅ Excellent match

Content:
Which player has scored the most goals in a single World Cup tournament? Just Fontaine of France – 13 goals in 1958. With an average of 5.4 goals per match which World Cup tournament remains the highest scoring? Which nation, in 1991, won the inaugur


--- Result #4 ---
Source: 100_World_Cup_Facts_and_Trivia.txt
Chunk Index: 52
Distance Score: 0.3082
Assessment: ✅ Good match

Content:
 by José Batista (Uruguay) vs Scotland in 1986. 27. Who scored the latest goal in regular time in FIFA World Cup history? Mehdi Taremi (Iran) in the 90th (+13th minute) vs England in 2022 . 26. Which manager holds the record for most FIFA World Cups 


--- Result #5 ---
Source: 100_World_Cup_Facts_and_Trivia.txt
Chunk Index: 14
Distance Score: 0.3218
Assessment: ✅ Good match

Content:
l, Andres Guardado, Lothar Matthäus, Rafael Marquez, Lionel Messi and Cristiano Ronaldo. 81. Which nation has the most World Cup titles? Brazil with five. 80. Who is the all-time leading goal-scorer in the World Cup? Miroslav Klose (Germany) with 16.

Expected answer: Miroslav Klose


These chunks are all relevant because their distance scores all hover around 0.3. 
================================================================================
QUERY #2
================================================================================

❓ Which country was the winner of the tenth edition of the World Cup?


--- Result #1 ---
Source: FIFA_World_Cup_records_and_statistics.txt
Chunk Index: 2
Distance Score: 0.3756
Assessment: ✅ Good match

Content:
e tournament. The inaugural winners in 1930 were ; the current champions are Argentina. The most successful nation is Brazil, which has won the cup on five occasions. Five teams have appeared in FIFA World Cup finals without winning, while twelve mor


--- Result #2 ---
Source: World_Cup_Ultimate_Guide.txt
Chunk Index: 11
Distance Score: 0.3864
Assessment: ✅ Good match

Content:
s more recent with a total of 9 World Cups, dating back to 1991. Who won the World Cup (in 2022)? Argentina defeated France in the 2022 World Cup Final to claim their third World Cup title. The match was tied 3-3 after extra time and went to a penalt


--- Result #3 ---
Source: List_of_FIFA_World_Cup_hosts.txt
Chunk Index: 12
Distance Score: 0.3995
Assessment: ✅ Good match

Content:
y in 1934, England in 1966, Germany in 1974, Argentina in 1978 and France in 1998 are the countries which organised an edition of the World Cup and won it. Upon the selection of Canada–Mexico–United States bid for the 2026 FIFA World Cup , the tourna


--- Result #4 ---
Source: World_Cup_Ultimate_Guide.txt
Chunk Index: 23
Distance Score: 0.4016
Assessment: ✅ Good match

Content:
 World Cup as one of the host countries, bypassing the traditional qualifying matches. List of all World Cup Winners 1930 in Uruguay : Uruguay def. Argentina 4-2 1934 in Italy: Italy def. Czechoslovakia 2-1 (ET) 1938 in France: Italy def. Hungary 4-2


--- Result #5 ---
Source: World_Cup_Quiz_answers.txt
Chunk Index: 19
Distance Score: 0.4206
Assessment: ✅ Good match

Content:
one was sent off? Who were the first host country to be knocked out at the group stage? South Africa, 2010. In which year did the World Cup have its first game under covers? 1994 – USA v Switzerland. Which player has scored the most goals in a single

Expected answer: West Germany

These chunks are all relevant because their distance scores all hover around 0.3. 
================================================================================
QUERY #3
================================================================================

❓ Who scored a hat-trick in a world cup final and lost?


--- Result #1 ---
Source: 100_World_Cup_Facts_and_Trivia.txt
Chunk Index: 15
Distance Score: 0.3089
Assessment: ✅ Good match

Content:
n the World Cup? Miroslav Klose (Germany) with 16. 79. Who are the two players to score a hat-trick in a World Cup final? Kylian Mbappé (France, 2022) and Geoff Hurst (England, 1966). 78. How many times has a nation won back-to-back World Cup titles?


--- Result #2 ---
Source: World_Cup_Quiz_answers.txt
Chunk Index: 7
Distance Score: 0.3820
Assessment: ✅ Good match

Content:
t during the group stage in the 1966 World Cup? Geoff Hurst scored a hat trick for England in the 1966 World Cup final but who scored the other goal? Martin Peters. Why were England grateful to Tovik Bakhramov in 1966? Bakhramov was the ‘Russian line


--- Result #3 ---
Source: World_Cup_Quiz_answers.txt
Chunk Index: 16
Distance Score: 0.4157
Assessment: ✅ Good match

Content:
orld Cup game on the Golden Goal rule? France – Laurent Blanc v Paraguay. Which player scored two goals in the 1998 World Cup final? Zinedine Zidane of France v Brazil. Who, in 2002, was the first Asian nation to play in a World Cup semi-final? South


--- Result #4 ---
Source: World_Cup_Quiz_answers.txt
Chunk Index: 2
Distance Score: 0.4170
Assessment: ✅ Good match

Content:
rt Patenaude, was the first player to do what in a World Cup match? Score a hat-trick. (It was in the USA’s second match in 1930, versus Paraguay). Who, in 1934, became the first African nation to play at a World Cup? Why did the Austrian ‘wunder’ te


--- Result #5 ---
Source: World_Cup_Ultimate_Guide.txt
Chunk Index: 27
Distance Score: 0.4256
Assessment: ✅ Good match

Content:
taly 0-0 (3-2 PKs) 1998 in France: France def. Brazil 3-0 2002 in Japan: Brazil def. Germany 2-0 2006 in Germany: Italy def. France 1-1 (5-3 PKs) 2010 in South Africa: Spain def. the Netherlands 1-0 (ET) 2014 in Brazil: Germany def. Argentina 1-0 (ET

Expected answer: Kylian Mbappé

These chunks are all relevant because their distance scores all hover around 0.3. 
**Model used:**
I used all-MiniLM-L6-v2 via sentence-transformers
**Production tradeoff reflection:**
Without a cost constraint, i'd probably use an embedding model with a larger token limit. However, due to the nature of the topic, I suspect this wouldn't help very much. i'd also use a model that is more fine-tuned towards more casual writing, since many of my documents are from blogs. If I needed a stronger embedding model, i'd probably go with something API hosted, but I would be sacrificing latencu in the process. Multilingual support would also be cool since this really only works with english.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
"""You are a World Cup knowledge assistant.

CRITICAL RULES:
1. Use the retrieved documents as the primary source of truth.
2. You may combine information across documents to form answers.
3. Only refuse if NONE of the documents contain relevant information.
4. Always cite which document(s) you used.
5. Be concise and factual.

Format:
ANSWER: ...
CONFIDENCE: High/Medium/Low"""

I told it to use and cite the documents, while also telling it to treat them as the only source of truth, preventing them from using prior training to answer questions. This is how I attained grounded generation. 
**How source attribution is surfaced in the response:**
I included that it must cite the documents in the response. Looking at the formatting, the citation is included in the answer field. 
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |Who has scored the most goals in World Cup history? | Miroslav Klose |Miroslav Klose |Relevant |Accurate |
| 2 |Which country was the winner of the tenth edition of the World Cup? | West Germany |The documents do not contain enough information to determine the winner of the tenth edition of the World Cup. |Off-target |Inaccurate |
| 3 |Who scored a hat-trick in a world cup final and lost? |Kylian Mbappé |The documents do not contain information about a player who scored a hat-trick in a World Cup final and lost. Geoff Hurst scored a hat-trick for England in the 1966 World Cup final, and England won that match. Kylian Mbappé also scored a hat-trick in the 2022 World Cup final, but the outcome of that specific match (win/loss for his team) is not detailed in the provided documents. |Relevant |Partially accurate |
| 4 |Which stadium was the 2010 World Cup Final held in? | Soccer City Stadium | The provided documents do not contain information about which stadium hosted the 2010 World Cup Final.|Off-target |Inaccurate |
| 5 |Where was the 1990 World Cup held? | Italy |Italy |Relevant |Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which country was the winner of the tenth edition of the World Cup? 
**What the system returned:**
The documents do not contain enough information to determine the winner of the tenth edition of the World Cup.
**Root cause (tied to a specific pipeline stage):**
Ingestion
**What you would change to fix it:**
Use semantic chunking instead of fixed-size
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
I wasn't sure how to make an interface for the RAG pipeline so hacing gradio documentation included in the spec was very helpful.
**One way your implementation diverged from the spec, and why:**
I made a scraper because I wanted to have a more realistic experience with data aggregation rather than just copy-pasting stuff into a txt file. 
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:I provided my initial web scraper implementation and described that my RAG system could not answer questions like "Who hosted the 2010 World Cup?" because important information from Wikipedia tables was missing from the scraped documents.*
- *What it produced:The AI explained that my scraper was only extracting page text and was not preserving structured table content. It suggested redesigning the scraper to explicitly extract Wikipedia tables and save them as text alongside the article content.*
- *What I changed or overrode:I modified the document ingestion pipeline to focus on preserving structured information rather than relying solely on raw page text extraction. I verified the generated documents manually and used retrieval results to identify missing information before updating the scraper.*

**Instance 2**

- *What I gave the AI:I provided my generation pipeline code after migrating from the deprecated google-generativeai SDK to the newer google-genai SDK. I also shared error messages related to API key configuration and model initialization.*
- *What it produced:The AI identified that I was mixing APIs from two different Gemini SDK versions and suggested replacing deprecated configuration calls with the newer genai.Client(api_key=...) interface and updating generation requests accordingly.*
- *What I changed or overrode:I updated the code to use the new client-based API, replaced deprecated initialization patterns, and tested the changes with my own API credentials. I also adjusted model names and debugging logic after encountering quota and configuration issues that were not addressed by the initial AI-generated suggestions.*
