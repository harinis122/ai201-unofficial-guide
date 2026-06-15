# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain
     This system is a housing survival guide for continuing students at UC Irvine.
     This is valuable because there UCI has many continuing student housing options such as ACC, Arroyo Vista, residence halls, and even UTC off-campus. Students can make a more informed decision on where to live from other students' expereinces (especially with noise level, mold, etc) more than just reading official documentation about each option. There are generally things that students say about off campus housing that's important and not mentioned in official sources.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |r/UCI HOUSING MEGATHREAD (2022-2023)|Reddit megathread|https://www.reddit.com/r/UCI/comments/vfp0la/uci_housing_megathread_20222023|
| 2 |r/UCI HOUSING MEGATHREAD (2023-2024)|Reddit megathread| https://www.reddit.com/r/UCI/comments/16cucqr/uci_housing_megathread_20232024/|
| 3 |r/Are the Acc apartments really that bad?|Reddit thread|https://www.reddit.com/r/UCI/comments/14wks9z/are_the_acc_apartments_really_that_bad/|
| 4 |r/ACC vs off-campus housing advice|Reddit thread|https://www.reddit.com/r/UCI/comments/okh61o/acc_vs_offcampus_housing_advice/|
| 5 |r/I’ve heard bad things about ACC so far… Is off campus a better bet?|Reddit thread|https://www.reddit.com/r/UCI/comments/xq3q8e/ive_heard_bad_things_about_acc_so_far_is_off/|
| 6 |r/Any ideas on Tackling off campus housing?|Reddit thread|https://www.reddit.com/r/UCI/comments/1lygzfl/any_ideas_on_tackling_off_campus_housing/|
| 7 |r/What apartment communities don't suck?|Reddit thread|https://www.reddit.com/r/UCI/comments/1byxvg/what_apartment_communities_dont_suck/|
| 8 |r/Why choose ACC apartments over residence halls?|Reddit thread|https://www.reddit.com/r/UCI/comments/rtaopg/why_choose_acc_apartments_over_residence_halls/|
| 9 |UCI Housing Tour (Non-Dorms) | Pros and Cons Breakdown|YouTube|/Users/harinis/codepath/ai201/ai201-unofficial-guide/documents/uci_housing.txt|
| 10 |UC Irvine Student Housing Continuing Student Process Application Webinar 2026-2027|YouTube|/Users/harinis/codepath/ai201/ai201-unofficial-guide/documents/uci_official_housing.txt|

---

## Chunking Strategy

**Chunk size:**
Before chunking, all documents will be cleaned (reddit post actions will be removed and youtube video timestamps will be removed). Reddit sources should be chunked by blank lines, but if a paragraph is longer than 500 characters, it will be split at 500 characters. There will be a 150-character overlap. The webinar transcript/ official housing information should use 500-character chunks with 150-character overlap. The Youtube tour will have 800 character chunking with 150 characters of overlap.

**Overlap:**
I will use 150 characters of overlap for all sources.

**Why these choices fit your documents:**
In reddit threads, people write in small paragraphs of about 500 characters each, and each person has different points of view so I want to separate text from different people. In YouTube videos and official guides, information is more in depth and is not from multiple points of view, so 800 characters is needed to keep all the information without unnecessarily splitting it. 100 characters of overlap is to account for cutting a chunk mid sentence.

**Final chunk count:**
257 chunks total across all 10 documents.

---

## Embedding Model

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers because it has no cost and runs locally without an API key, and it is good enough for a small project. After embedding, the vectors will be stored in ChromaDB.


**Production tradeoff reflection:**
If I were deploying this for real users, I would compare different embedding models primarily based on retrieval accuracy and latency. I would want the model to work at a reasonable speed and I would also want to ensure that it is as accurate as possible, because after all, students will be using it to decide where to spend money on housing. Multilingual support isn't as important as latency and accuracy because students are mostly familiar with English and all official sources are in English as well.

---

## Grounded Generation

**System prompt grounding instruction:**
My system enforces grounding through a very detailed and explicit instruction to only use the context from given documents in its answer. The full prompt is below:
"Rules you must follow:
- Do not use any knowledge from outside the provided chunks. If you know something about UCI housing that is not in the chunks, do not say it.
- You may draw conclusions that are directly supported by the text (e.g. if a chunk says "ACC is cheap and close to campus", you may say those are advantages). Do not go beyond what the text supports.
- Do not fabricate details, statistics, prices, or opinions that do not appear in the chunks.
- If the chunks are about a completely different topic than the question and contain nothing relevant, respond with exactly: "I don't have enough information on that."
- If only part of the question can be answered, answer that part and note what you couldn't find.
- Cite the source of each piece of information in parentheses, e.g. (source: heard_bad_things_about_acc).
- Be concise and direct."

**How source attribution is surfaced in the response:**
After the Groq AI produces each component of an answer, it includes parenthetical citation of the source's text file. For example, "Camino del Sol is considered one of the best on-campus apartment communities, possibly tied with Plaza Verde (source: uci_housing_megathread_2023_2024, uci_housing_megathread_2022_2023)". The actual reddit thread/YouTube video source name is listed under "sources used".

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |What do students say is the main advantage of living in the UCI ACC apartments?|Students say that ACC is convenient because it is close to campus, provides furniture, and designed for UCI students.|decent quality, students enjoy their amenities, quite nice, nice pools, may be a more available option for upperclassmen since very few upperclassmen get placement in the dorms, main advantage not explicitly stated.|relevent|accurate|
| 2 |What tradeoffs do students mention when comparing ACC housing with off-campus apartment housing such as UTC?|ACC is usually described as convenient and student-focused while UTC and other off-campus housing is usually a bit cheaper with a group but harder to coordinate.|ACC apartments are "cheap", but may have issues such as "ants, mildew, ripped furniture". In contrast, off-campus housing is "more expensive".|partially relevant|inaccurate|
| 3 |What should students consider besides rent when choosing UCI continuing housing options?|Students should consider distance to campus, parking, roommates, lease terms, maintenance quality, noise, safety, and transportation, and community.|distance from the main campus, Anteater Express provided|relevant|accurate|
| 4 |What are some ways students can find off-campus housing besides ACC?|The Anteater Housing Network and Irvine Company are good place to look.|Not enough information|off-target|N/A|
| 5 |What are advantages of the Puerto Del Sol ACC community?|Puerto Del Sol is generally the cheapest ACC housing option and is also the closest to campus.|not specifically mentioned, another ACC community, Camino del Sol, has advantages such as being cheaper and more convenient than living off campus, having AC, large spaces, nice bathrooms, and decent amenities. It is not clear if these advantages apply to Puerto Del Sol as well.|off-target|partially accurate|

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
What are advantages of the Puerta Del Sol ACC community?
**What the system returned:**
Only 2 weakly relevant chunks were returned:
"ACC vs off-campus housing advice I just got an offer from ACC for Puerto del Sol. I’m stumped on signing the lease agreement for Puerto del Sol or housing with a couple of friends of mine who own a condo right next to campus. The price range is similar for both offers. I will have to start paying beginning of August for both. I can’t afford housing out-of-pocket so I’m relying on financial aid." and "camino del all is very nice so far besides the couches the furniture is pretty solid, there’s ac, large spaces, nice bathrooms, decent amenities, etc the wifi sucks but it’s cheaper and more convenient than living off campus". The chunk that explicitly describes Puerta Del Sol wasn't retrieved.

**Root cause (tied to a specific pipeline stage):**
The YouTube tour transcript was chunked with an 800-char sliding window that ignored the Chapter N: section headers present in the cleaned text. Puerta Del Sol's content got merged into a chunk also covering grad housing and UTC, diluting its embedding vector so it ranked outside the top 5 for a Puerta Del Sol-specific query. Since "Puerto del Sol" generally did not appear much elsewhere within the 10 sources, there was no fallback source that would still provide accurate information for this question.

**What you would change to fix it:**
I would split the YouTube ACC tour transcript by chapter headers using re.split(r'\n(?=Chapter \d+:)', text) before applying the character limit, so each ACC community gets its own focused chunk. Additionally, when searching for "Puerto del Sol" elsewhere, I reaalized that it gets misspelled quite a bit in the transcript so a spell correction algorithm for ACC apartment names would be a good change to implement as well. 
---

## Spec Reflection

**One way the spec helped you during implementation:**
The clarity of the spec gave me something solid to rely on throughout the process of building this system, and was valuable especially when using Claude to build out the system. Having established the system design and overall goals beforehand enabled me to know exactly how to direct Claude and prevented me from AI-generating random code which I was not familiar with.

**One way your implementation diverged from the spec, and why:**
After my first round of chunking, I realized that the chunks were a bit off. The reddit thread chunks and the official webinar transcript seemed to combine a lot of unrelated information. I decided to change the chunking of the reddit threads to separate a each blank line but be a maximum of 500 characters. I made the webinar transcript also chunk into 500 characters each to break apart the information.
---

## AI Usage

**Instance 1**

- *What I gave the AI:*
I gave Claude the cleaned documents and asked it to look at planning.md and chunk the text accordingly.

- *What it produced:*
Claude did do as I asked because it chunked exactly as I originally wanted (600 characters each for reddit threads and 800 characters each for the webinar and ACC tour transcript).

- *What I changed or overrode:*
I ended up changing this because I realized the chunking approach I used did not work on reddit threads and the webinar transcript because it combined so many unrelated ideas. I decided to separate reddit thread chunks at empty lines and cap them at 500 characters and keep the webinar chunks at 500 characters each. I found this was much better at keeping similar information together.

**Instance 2**

- *What I gave the AI:*
I told Claude to implement the Groq AI generation logic under a separate script called generate.py, given the retrieving logic under retrieve.py and the overall architecture and context under planning.md.
- *What it produced:*
Claude produced a working generate.py module. However, the codebase did seem a bit messy because there were so many logic-heavy modules at this point and it was very unclear where all this logic starts and ends.

- *What I changed or overrode:*
I added a main.py module and redirected Claude to refactor code to this module. I made main.py facilitate the entire logic of this system to make the code much more readable. I ensured that the logic starts and ends in main.py and that it refers to logic from other modules as needed.
