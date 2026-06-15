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

Example chunks:
1. {
    "source": "any_ideas_on_tackling_off_campus_housing",
    "source_type": "reddit",
    "chunk_index": 1,
    "text": "We had luck w Irvine Company, no guarantor, just four average incomes (highest in our household is $37k/year). We had savings galore and good credit at the time of move in, though, if that is applicable to you.\n\nI wish it was. I have decent credit but no one seems to be hiring this summer, waiting to hear back from a couple places. That being said none of my roommates work so I think im cooked.\n\nhttps://discord.gg/ucihousing some people are looking for roommates"
  }

  2. {
    "source": "uci_housing_megathread_2022_2023",
    "source_type": "reddit",
    "chunk_index": 4,
    "text": "Yes, the ACC apartments are considered as on-campus housing and you will receive aid.\n\nWhat dorm/ACC apartment is the best/what should I pick?\n\nI’ll post a few relevant past comments near the bottom of the thread detailing past comments of experiences from living in their respective ACC apartments, and others are encouraged to comment their own relevant past experiences. I would refrain from looking too much into online Google/Yelp reviews for the ACC apartments."
  }

  3. {
    "source": "uci_housing_megathread_2022_2023",
    "source_type": "reddit",
    "chunk_index": 12,
    "text": "- Puerta: The closest to campus, I believe this is the smallest apartment community. Albertsons is right across the street so its very accessible for groceries, small issue is you have to cross the street every time you want to get to campus quick to get to the fast shuttle.\n\n- VDC: The farthest away from campus, it’s a secluded area that you normally wouldn’t go to. That being said, the room quality is similar to VDCN and at its price its still a solid bet."
  }

  4. {
    "source": "uci_non_dorms_pros_cons_video",
    "source_type": "transcript",
    "chunk_index": 1,
    "text": "let's check it out\n\nChapter 3: Plaza Verde (PV)\nalright so we're here at plaza verde or pv it's the most recent housing complex and it's also definitely the most nicest looking one it's also immediately priced compared to the other housing sites and it has its own laundry facilities even though it's shared there's indoor and outdoor study spaces as well and for those of you who are interested in working out there's a rec center but i mean the ark is just right down the street and i'll just go there just because it's just a lot better um plaza verde has its own parking structure so for those of you who want to bring their car down here you've got plenty of space to park\n\nChapter 4: Vista Del Campo Norte (VDC Norte, or just Norte)\nnorte doubles are actually pretty big and some of them have"
  }

  5. {
    "source": "why_choose_acc_over_residence_halls",
    "source_type": "reddit",
    "chunk_index": 1,
    "text": "price of acc is cheaper than dorms and as a second year that didn’t have guaranteed housing in the dorms, acc was the next option. you also have more privacy if you opt for non-shared bedrooms. kitchen space is also good when you don’t have to share it with the whole floor. though some of the acc communities are far away from campus, its not a dealbreaker :)"
  }

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

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |What do students say are advantages of living in the UCI ACC apartments?|Students say that ACC is convenient because it is close to campus, provides furniture, and designed for UCI students.|decent quality, students enjoy their amenities, quite nice, nice pools, may be a more available option for upperclassmen since very few upperclassmen get placement in the dorms, main advantage not explicitly stated.|relevent|accurate|
| 2 |What tradeoffs do students mention when comparing ACC housing with off-campus apartment housing such as UTC?|ACC is usually described as convenient and student-focused while UTC and other off-campus housing is usually a bit cheaper with a group but harder to coordinate.|ACC apartments are "cheap", but may have issues such as "ants, mildew, ripped furniture". In contrast, off-campus housing is "more expensive".|partially relevant|inaccurate|
| 3 |What should students consider besides rent when choosing UCI continuing housing options?|Students should consider distance to campus, parking, roommates, lease terms, maintenance quality, noise, safety, and transportation, and community.|distance from the main campus, Anteater Express provided|relevant|accurate|
| 4 |What are some ways students can find off-campus housing besides ACC?|The Anteater Housing Network and Irvine Company are good place to look.|Not enough information|off-target|N/A|
| 5 |What are advantages of the Puerto Del Sol ACC community?|Puerto Del Sol is generally the cheapest ACC housing option and is also the closest to campus.|not specifically mentioned, another ACC community, Camino del Sol, has advantages such as being cheaper and more convenient than living off campus, having AC, large spaces, nice bathrooms, and decent amenities. It is not clear if these advantages apply to Puerto Del Sol as well.|off-target|partially accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---
## Retrieval — Relevant Chunks Returned for Queries (Examples of questions and corresponding top 5 chunks)
Question 1: What do students say about the wifi at ACC apartments?
Chunks: These chunks are all accurate because they all are directly related to wifi and ACC community. None of them contain a lot of unrelated info and each of them help the Groqe AI answer the question properly.
Chunk 1 — r/Are the ACC apartments really that bad? (distance: 0.3529)
Are the Acc apartments really that bad? I am an transfer student and have a lease for the 3 bed - 2 Bath B at VDCN, and have been hearing horror stories about the communities online. Mostly about wifi, and while wifi is a concern to me, I can't imagine it can't be fixed with an ethernet cable or router.

Chunk 2 — r/I've heard bad things about ACC — is off campus better? (distance: 0.3765)
I would stick to ACC… I live off campus and it’s very expensive compared to ACC. You might have shit Wi-Fi at ACC from what I’ve witnessed thruout this Reddit pg but at least you have a place that’s already furnished and with the utilities already embedded or at little cost. I already had to spend money to furnish my place, the application fee, security deposit, trash fee, do laundry, and water, electricity, Wi-Fi, and gas are all separate utilities that need to be payed.

Chunk 3 — r/Are the ACC apartments really that bad? (distance: 0.3967)
Most stories are true but can be handled. Some apartments are quite dirty that you have to clean them yourself which can be a hassle when moving in. Wifi is terrible across all ACCs but some do suffer more than others. As a matter of fact it’s common for outages to occur in certain buildings within a community while it works in others. Wifi connection has always been fixed for me using an Ethernet cable and I find it to work 95% of the time for me but that’s just me tho.

Chunk 4 — r/Are the ACC apartments really that bad? (distance: 0.4042)
I lived in vdcn my jr and senior year. 2 bed 2 bath and it was great. My own room, own bathroom, me and my roomate did our own thing and never had any issues. The wifi does suck sometimes but for the most part works fine. My dorm did/does have some roach issues but i mean oh well lol

Chunk 5 — r/Are the ACC apartments really that bad? (distance: 0.4189)
ACC wifi is pretty much the same (if im right), meaning when vdcn wifi is down, the vdc and camino wifi are down as well, as well as most of the other ACC apartment complexes. I lived in vdcn with the same floor plan as you. You could bring an ethernet cable for your computer, and somehow it usually works when the wifi is broken. I would say the wifi may break once or twice a month, maybe three or four times. Im not really sure as im often working out or at the dining hall or on campus.

Question 2: Is ACC housing worth it compared to living off campus?
Chunks: These chunks are relevant because they directly have some sort of comparison between ACC and off-campus housing options (and slightly favor ACC). One chunk notes that ACC is decent while another notes that it's nice compared to other universities, allowing Groqe AI to provide an accurate answer.
Chunk 1 — r/I've heard bad things about ACC — is off campus better? (distance: 0.1665)
I’ve heard bad things about ACC so far… Is off campus a better bet? Ants, mildew, ripped furniture, just a couple of things I’ve heard from people who just moved in. Is a more expensive apartment worth it ?
ACC is better. I’m not living in luxury but it’s a roof over my head, and it’s cheap. So I’m not gonna complain. I only have to pay for electricity, and I get a stipend for laundry (puerta). No complaints so far.
I’m not living in luxury

Chunk 2 — r/Why choose ACC apartments over residence halls? (distance: 0.2087)
price of acc is cheaper than dorms and as a second year that didn’t have guaranteed housing in the dorms, acc was the next option. you also have more privacy if you opt for non-shared bedrooms. kitchen space is also good when you don’t have to share it with the whole floor. though some of the acc communities are far away from campus, its not a dealbreaker :)

Chunk 3 — r/UCI Housing Megathread (2022–2023) (distance: 0.2132)
Please refrain from starting new housing related threads and instead refer to this thread/the comment section below. If you have previously dormed on campus or lived in an ACC apartment, you are encouraged to give your opinion of the place and state what you liked/disliked about living there to help other students. (Students who have lived in off-campus housing such as UTC are also welcome!)

Chunk 4 — r/UCI Housing Megathread (2023–2024) (distance: 0.2132)
Please refrain from starting new housing related threads and instead refer to this thread/the comment section below. If you have previously dormed on campus or lived in an ACC apartment, you are encouraged to give your opinion of the place and state what you liked/disliked about living there to help other students. (Students who have lived in off-campus housing such as UTC are also welcome!)

Chunk 5 — r/I've heard bad things about ACC — is off campus better? (distance: 0.2305)
You pay for it, but they are nice.
Tbh, yeah I definitely agree! I meant like I’m not living in anything grand. But compared to most university apartments this is very nice! Compared to my own house they are pretty nice 🤷🏽‍♂️. Idk what standard of living people are used to, but ACC really isn’t bad whatsoever.
If you can get plaza verde then I would say it’s better than off campus given its price

Question 3: What are the cheapest ACC housing options?
Chunks:
Chunk 1 — r/Why choose ACC apartments over residence halls? (distance: 0.3812)

price of acc is cheaper than dorms and as a second year that didn’t have guaranteed housing in the dorms, acc was the next option. you also have more privacy if you opt for non-shared bedrooms. kitchen space is also good when you don’t have to share it with the whole floor. though some of the acc communities are far away from campus, its not a dealbreaker :)

Chunk 2 — r/I've heard bad things about ACC — is off campus better? (distance: 0.4010)

From my own experience and my friends', ACC is a much better in terms of price and overall worth. Off-campus works, but unless you're planning on spending $1500-$2000 minimum for a private bedroom, you'll be sharing a room with someone. For ACC apartments, Plaza Verde comes in at 1st and Camino del Sol at 2nd, the rest are all up in the air in my opinion.

Chunk 3 — r/I've heard bad things about ACC — is off campus better? (distance: 0.4227)

I’ve heard bad things about ACC so far… Is off campus a better bet? Ants, mildew, ripped furniture, just a couple of things I’ve heard from people who just moved in. Is a more expensive apartment worth it ?

ACC is better. I’m not living in luxury but it’s a roof over my head, and it’s cheap. So I’m not gonna complain. I only have to pay for electricity, and I get a stipend for laundry (puerta). No complaints so far.

I’m not living in luxury

Chunk 4 — r/What apartment communities don't suck? (distance: 0.4229)

Parkwest is definitely one of the cheaper options, and only down Harvard for a short drive. If you can get someone to live in the living room, prices per room is significantly cheaper.

Puerta is pretty nice, if you don't mind a really small double. You also get free parking at the ARC. Really quiet and most likely the cheapest too.

Chunk 5 — r/UCI Housing Megathread (2023–2024) (distance: 0.4547)

Please refrain from starting new housing related threads and instead refer to this thread/the comment section below. If you have previously dormed on campus or lived in an ACC apartment, you are encouraged to give your opinion of the place and state what you liked/disliked about living there to help other students. (Students who have lived in off-campus housing such as UTC are also welcome!)

---
## Failure Case Analysis

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


## Video Walkthrough!
https://drive.google.com/file/d/1Z1xJoxXGKf3IFS89nm_t_xh886leW7CC/view?usp=sharing
Covers:
- walkthrough of system: input and output fields and sample interaction
- 2 happy cases and 1 failure case + deep dive into why failure occured
- proof of response attribution
- proof of grounding
