---
layout: post
title: "Past the 1870 Wall: Building a Genealogy Scraper for a Black American Family Tree"
date: 2026-05-13 12:00:00 +0000
categories: genealogy scraping llm-agents
excerpt: "Most online ancestry tools fall apart the moment you push a Black American family tree before 1870. I spent the last month building a scraper that doesn't — a reverse-engineered Ancestry Heritage Quest API, a Dawes Rolls scraper for Oklahoma freedmen, a claims pipeline that ingests a family group chat, and a write-back loop that pushes findings to a self-hosted Gramps-Web instance with full citations. Here is what the system looks like and how it found a great-great-great-grandmother named Jane Rushing Oliver whose mother died in Texas the day they read the free papers."
---

If you have ever tried to use Ancestry, FamilySearch, or 23andMe to trace a Black American family back more than four generations, you already know how this story ends: a clean tree up to the 1880 census, a couple of guesses on 1870, and then a wall. The wall has a name. Genealogists call it **the 1870 wall**, because the 1870 Census is the first one in which formerly enslaved people are listed by name. Everything before 1870, my ancestors were property — counted in slave schedules under a slaveholder's name, with nothing but an age, a sex, and a color.

The off-the-shelf tools are not built for the wall. They are optimized for white-presenting trees with continuous surnames, where the leaves climb cleanly into European parish records. The instant your tree hits a person whose last name was assigned in 1865, the recommendation engine stops being useful. You have to do the work by hand — and the records you need to do it with are scattered across a dozen archives that each have their own quirks, their own auth, and their own bad search UI.

So I built a system that does the work for me. The repo is [`census-scraper`](https://github.com/jbwashington), and over the past month it has taken my "Washington Family Tree" on a self-hosted [Gramps-Web](https://gramps-web.org/) instance from a couple dozen known ancestors to **108 people across nine generations**, with **23 frontier dead-ends** I'm still chasing. This post walks through what it does, why each piece exists, and the moment it found my great-great-great-grandmother, Jane Rushing Oliver.

## The shape of the problem

A normal genealogy workflow is: type a name into a search box, click a record, attach it to a person in your tree. The reasons that does not work for the 1870 wall:

1. **Names are unstable.** A man born "Jobe" on a plantation in 1857 might appear as Joby Washington in the 1870 census, Jobe Washington in 1880, and J.W. Washington on his death certificate. AHQ's search engine treats `Jobe` and `Joby` as different people — it does not soundex given names. I lost two weeks before I figured that out; the 1870 record had been one letter away the whole time.
2. **The pre-1870 records are not in the same database.** Slave schedules, Freedmen's Bureau records, Freedmen's Bank records, and the Library of Congress slave narratives all live in different collections with different schemas — and AHQ's collection filter is silently broken (more on that below).
3. **Family knowledge is the bridge.** My uncle Mark spent thirty years collecting names off backs of photographs, recordings of his grandmother, and handwritten notes. None of that is searchable on Ancestry. But it is the *only* thing that links the 1880 census of "Etta M Washington" in Pine Bluff to a six-year-old girl listed only as "F, 6, B" on an 1860 slave schedule in Bradley County, Arkansas.
4. **You have to be willing to call your shots.** Genealogy software prefers facts. Real research is a graph of *claims* — assertions with provenance and confidence — that you push toward "fact" status as corroboration lands.

The scraper is shaped by all four of those.

## Architecture in one diagram

```
Family documents ──→ parse_crossref() ──→ claims table (D1)
(chat, obituaries,                              │
 WPA narratives,                                 ▼
 handwritten notes)                      extract_search_hints()
                                                │
Gramps-Web ──→ get_frontier_ancestors() ──→ SearchQuery ──→ AHQ API ──→ normalize() ──→ Gramps-Web
                                                                  │
                                                          ingest_record() ──→ source_records (D1)
```

Three components do most of the work.

**Gramps-Web** is the source of truth. It runs in a Docker container on my homelab Mac Mini at `jamess-mac-mini.tail5b1923.ts.net:5050`, has a proper genealogy data model (people, events, places, sources, citations, notes), and is reachable over Tailscale from anywhere. The scraper reads from it, writes to it, and never duplicates state. The CLI commands it exposes are deliberately read-only-by-default:

```bash
uv run census-scraper research frontier         # who are the 23 dead-ends?
uv run census-scraper research claims --id I0016  # claims about a person
uv run census-scraper research search --id I0016  # search AHQ with claim hints
```

**The scrapers** talk to record providers. The big one is Ancestry Heritage Quest. The second is the Oklahoma Historical Society's Dawes Rolls index. The third is FamilySearch, which has the best Freedmen's Bureau collection but the worst auth flow. All three are reverse-engineered, which is most of what makes this project interesting.

**The claims pipeline** ingests unstructured family knowledge — group chat messages, obituaries, WPA narratives, my uncle's research notes — into a structured `claims` table with `fact_type`, `value`, `confidence`, and `source_description`. The research loop uses those claims as search hints; without them, you cannot prune an 1870 Arkansas Washington search down from thousands of hits to the right one.

## Reverse-engineering Ancestry Heritage Quest

Ancestry Heritage Quest is the institutional cousin of Ancestry.com — same record collections, slightly different UI, available through most public libraries with a library card. My cousin gave me her login. The public-facing site is a React app that calls an internal JSON API. The API is undocumented, but it is the same API the search page itself uses, so a few minutes in the network panel told me everything I needed.

Two endpoints carry the system:

1. **`GET /api/search-results`** — JSON search. Accepts a `collectionId` (`db`), name fragments, year ranges, `state`. Returns paginated hit summaries with internal record IDs.
2. **`/discoveryui-content/search/collections/{collection}/records/{id}?pf=true`** — the printer-friendly HTML for a full record. AHQ has a real JSON detail endpoint, but it's gated behind JWT that expires every ~30 minutes. The printer-friendly page renders the same data as a deterministic `<th>label</th><td>value</td>` table and works with the longer-lived `ATT` and `HAC` session cookies.

Auth is cookies, not bearer tokens. The login JWT expires fast but the search endpoint accepts the `ATT`/`HAC` cookies independently. I cache cookies in Cloudflare KV with a refresh-from-HAR script and never touch the JWT.

The collection IDs are the other half of the puzzle. They're stable, undocumented, and the only way to find them is to do a search and read the URL. The ones that matter for Black American genealogy:

| Collection | ID |
|---|---|
| 1850 Census | 8054 |
| 1860 Census | 7667 |
| 1870 Census | 7163 |
| 1880 Census | 6742 |
| 1900–1950 | 7602, 7884, 6061, 6224, 2442, 62308 |
| 1850 Slave Schedules | 7668 |
| 1860 Slave Schedules | 7669 |
| Freedmen's Bureau | 4406 |
| Freedmen's Bank | 4407 |

And the gotchas that cost me real time, in case you build on this:

- **The `db` parameter is silently ignored.** A search with `db=7163` (1870 Census) returns the same cross-collection results as a search with no filter. I filter post-hoc in the scraper now: pull the broader result set, then `if rec.collection_id != AHQ_1870: continue`. It is a ten-line workaround but until you know the filter is broken it looks like there's just no 1870 record for your person.
- **The `state` parameter is also silently ignored.** I confirmed this by running the same surname query with `state=mississippi`, `state=arkansas`, and `state=usa` and watching the result counts come back identical.
- **Given names are not soundexed.** `Jobe Washington` returns zero hits; `Joby Washington` returns the right record. I now expand every given name through a small list of spelling variants before searching.

The full reverse-engineering session — picking through the network panel, building the cookie loop, getting the first real record back — is published as an interactive Claude Code replay:

<div style="position: relative; width: 100%; padding-bottom: 75%; margin: 1.5rem 0;">
  <iframe src="/replays/2026-04-10-geneology-reverse-engineer.html" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 1px solid #333; border-radius: 8px;" allowfullscreen></iframe>
</div>

[Open the replay in full screen]({% post_url 2026-04-10-geneology-reverse-engineer %}){:target="_blank"} — it's the underlying session for everything that follows.

## The Dawes Rolls scraper

The Dawes Rolls (1898–1914) are the enrollment lists for the Five Civilized Tribes of Oklahoma — Cherokee, Choctaw, Chickasaw, Creek, Seminole — and, critically, the **Freedmen** rolls of Black people who lived on tribal land and were enrolled as tribal members or descendants of the enslaved. Several family lines that vanish in Arkansas in 1880 reappear on the Dawes Rolls in Indian Territory in 1900, which is why this scraper had to exist.

The Dawes Rolls are *not* on Ancestry Heritage Quest. They are on the Oklahoma Historical Society's free public search at `okhistory.org/research/dawesresults`. The interface is a 2007-era ColdFusion form, which means no auth, no rate limiting, no JavaScript, and a totally predictable query string. The scraper paginates by `start=` increments of 25 and has a `search_freedmen()` helper that filters to enrollment category = Freedmen across all five tribes.

Reverse-engineering AHQ took an afternoon. Reverse-engineering OHS took fifteen minutes. Old sites are kind to you.

## The claims pipeline

Pure scraping is not enough. If I search AHQ for "Washington, Arkansas, born 1850–1860" I get thousands of hits. The claims pipeline is what brings that to one.

A `Claim` is a structured assertion about a person:

```python
{
  "gramps_id": "I0016",
  "person_name": "Jane Rushing Oliver",
  "fact_type": "birth",
  "value": {"year": 1853, "place": "Leake County, Mississippi"},
  "source_description": "WPA Slave Narrative, Mrs. Bernice Bowden interviewer, Pine Bluff AR, ~1937. Jane reported age 81.",
  "confidence": 0.85,
  "status": "corroborated"
}
```

The fact types I care about are `birth`, `death`, `parent`, `marriage`, `residence`, `census_record`, `name`, `occupation`, and `note`. The values are typed JSON — different shape per fact type. The confidence scoring is deliberately coarse:

- **0.9** — published obituary or death certificate
- **0.8** — clear census image, WPA narrative direct quote
- **0.5** — family member's handwritten notes, group chat reports
- **0.3** — guesses I want to test but not yet believe

The status moves `pending → corroborated → pushed → rejected` as evidence accumulates. Once a claim is `corroborated` by an independent source it gets pushed to Gramps-Web as a real event with citations attached.

The input format is whatever I have. The cross-reference document is a long markdown file built from group chat threads, my uncle Mark's typewritten lineage notes, and handwritten genealogy charts I scanned and OCR'd. A regex-based parser splits it on headings, extracts `**Field**: value` pairs, parses census tables and handwritten notes, and emits claims. It has produced **55 claims across 31 people**, and that number is what made the rest of the project tractable.

When I run `census-scraper research search --id I0016`, the system pulls every claim for person `I0016`, extracts birth year, birthplace, and state hints, and feeds them into the AHQ search as filters. Thousands of hits becomes a handful. A handful I can read.

## Storage: the move from Postgres to D1

The project started on PostgreSQL + Redis in a Docker Compose stack on my Mac Mini. Two weeks in I migrated everything to Cloudflare D1 (SQLite over REST), Cloudflare KV (session cookies), and Cloudflare R2 (~235 MB of slave schedule scans, JSON findings, and HTML records). The reason was not scale — it was *portability*. I want to be able to run this from my laptop on the train without VPN-ing back to the Mini, and I want my cousins to be able to query the tree without me having to provision them homelab credentials. D1 + R2 gave me a stateless backend on a free tier; the Worker that fronts the D1 read APIs is a small TypeScript file.

The schema is eight tables: `persons`, `person_names`, `person_events`, `places`, `relationships`, `claims`, `source_records`, `data_sources`. Everything has a TEXT UUID primary key, audit timestamps, and JSON-as-TEXT for the polymorphic columns. SQLite is a great database for genealogy; the queries are mostly small graph walks and the working set fits in memory ten times over.

## Write-back is the part that has to be slow

The Gramps-Web REST API can create people, events, places, sources, citations, and notes. The scraper *could* write back automatically. It does not. Every push happens through a one-shot Python script in `scripts/` — `push_jobe_washington_1870_parents.py`, `update_jane_wpa_narrative.py`, `add_1880_oliver_family.py`, and so on — each one idempotent, each one logging every entity it created (with handles and gramps_ids) to a JSON sidecar like `1880_oliver_family_log.json`. Twenty-three of those scripts have run so far. If a push goes wrong I can read the log and back out exactly what was added; I never want to find out that a script duplicated a great-grandmother and then keep going.

One Gramps-Web integration gotcha worth writing down, because I lost a session to it: **POST and PUT responses come back as transaction envelopes, not entities.** Each item in the response is shaped like

```json
{
  "_class": "Family",
  "handle": "102c88f4fe2437cf5f7c291249c9",
  "type": "add",
  "old": null,
  "new": { "...full entity with gramps_id..." }
}
```

You have to dispatch on `_class` and unwrap `new` to read the `gramps_id`. None of the four scripts I wrote before figuring this out were getting the right gramps_id back on the first post; they were all running a brittle handle-and-pray retry. After the fix, every entity in the 1870 Jobe Washington push came back with the right ID on first POST.

## The Jane Rushing Oliver moment

This part is why I'm writing the post.

About three weeks in, the tree had a hard stop at the line **Etta M Washington (I0000) → Jane Rushing Oliver (I0016)**. I knew Etta — she was my great-great-grandmother, born ~1880 in Tennessee (or possibly Arkansas), married Mack L Washington, became a librarian and government worker in Little Rock. Her mother Jane was a name in family notes, a stub in the tree, and nothing else. The handwritten chart said Jane was "born a slave, Mississippi, came up through Arkansas." That was all.

The breakthrough came from the **Library of Congress Federal Writers' Project slave narratives** — the 1930s WPA interviews with formerly enslaved people. Around 2,300 of them are digitized. The Arkansas set includes an interview conducted in Pine Bluff by a Mrs. Bernice Bowden with a woman named Jane Oliver, age 81. Jane gave Bowden the entire story:

> "I was in the big house. ...When Miss Liza married they give sister to her and I stayed with Miss Netta. Her name was Drunetta Rawls. ...We come to Arkansas when I was small. ...I remember when they run us to Texas. ...Mama died in Texas and they buried her the day they read the free papers. ...My uncle Simon Rawls — he took me after the war."

Every sentence in that paragraph is a research hint. I parsed them into claims and let the scraper chase each one:

- **"They give sister to Miss Liza"** → there was a sister. Search AHQ 1880 census for Rawls households in Mississippi with a young Black woman. Hit: **Henrietta Rawls, b.~1845 MS, single hired hand, 1880 Carthage, Leake County, MS.** Jane's sister, separated from the rest of the family when Eliza M. Rawls married and took her along.
- **"Miss Netta — Drunetta Rawls"** → an enslaver. Drunetta is a Rawls family member; finding her in the Henry S. Rawls household sequence pinned down which Rawls plantation Jane was on.
- **"We come to Arkansas when I was small"** → migration. Henry S. Rawls's 1850 slave schedule was filed in Leake County, Mississippi (31 enslaved). His 1860 slave schedule was filed for his estate in Palestine Township, Bradley County, Arkansas (23 enslaved). He died sometime between 1853 and 1860; the operation moved during that gap.
- **"They run us to Texas"** → Civil War refugeeing. Slaveholders moved enslaved people to Texas during the war to keep them from Union lines.
- **"Mama died... the day they read the free papers"** → **Juneteenth, June 19, 1865.** Jane's mother died in Texas on the same day Black Texans were finally told they were free. There is no census, no death record, no marker — just a sentence in a sixty-page transcript.
- **"Uncle Simon Rawls took me after the war"** → custody. Simon is another search target. Not found yet.

The single hardest claim to corroborate was that Jane herself appeared on the 1860 slave schedule. The schedule is just numbers — age, sex, color, no name. But the 1860 Henry S. Rawls schedule, transcribed by ARGenWeb from Palestine Township, lists 23 people across three dwellings. Dwelling 1 has six entries:

| # | Age | Sex | Identity |
|---|-----|-----|----------|
| 1 | 66 | F | **Hannah** (b. ~1794, Virginia) — Jane's grandmother |
| 2 | 34 | F | **Jane's mother** (b. ~1826, Mississippi). Died Juneteenth 1865, Texas. |
| 3 | 17 | F | Older sister |
| 4 | 12 | M | Brother |
| 5 | 6 | F | **Jane** (b. ~1853, Mississippi) |
| —  |    |   | Henrietta (b. ~1845) — already given to Miss Liza, stayed in MS |

The proof that this is the right dwelling came from the grandmother. The 1870 Census of Vaugine Township, Jefferson County, Arkansas — Pine Bluff, where Jane eventually settled — lists a **Hannah Rolls, age 75, born Virginia, Black**. Same first name, same birthplace, same approximate birth year, same county Jane's family ended up in. The 1870 census is the **first** census in which Hannah is named at all. Before that she was "F, 66, B" under a slaveholder. I would not have found her — would not even have known to look for her — without Jane's narrative naming her.

What I want to be clear about: **none of this came from the LLM hallucinating a connection.** The LLM read the WPA narrative, extracted the structured claims, and stored them with citations back to the LoC. I corroborated each one manually against the slave schedules, the 1870 census, and the FamilySearch records. The system's job is to extract and store; my job is to corroborate. Genealogy is the wrong field to be cavalier in, and there is still work to do — the H.B. Rawls / Etta paternity claim, the two Henriettas, the Texas refugeeing route — that I am not yet willing to call corroborated.

## The other line: Jobe → Joby → Nick

The Washington side of the tree had a separate breakthrough I want to flag because it shows what happens when the scraper's quirks bite. The wall there was **James William Washington Sr. → Jobe Washington (I0296)**, born ~1857. Jobe's parents were unknown. I had searched the 1870 census for `Jobe Washington` half a dozen times. Zero hits.

It was the AHQ-no-soundex bug. `Joby Washington` returned record id 533736 immediately: a thirteen-year-old boy named Joby Washington in Ashley Township, Pulaski County, Arkansas, Dwelling 175. Same township as Jobe in the 1880 census. Same person.

The 1870 dwelling named the rest of the household. Father **Nick Washington**, age 47, born **North Carolina**, Black. Sister **Belle**, age 22, born Tennessee. Brother **Geo**, age 8, born Arkansas. Nick was a frontier ancestor I'd never seen before — a man born in 1823 in North Carolina, who had been enslaved, who had ended up in Arkansas with three children spread across three states by 1870. **Migration trajectory NC → TN → AR**, with the TN-to-AR move falling somewhere between 1857 and 1862. Almost certainly Civil War refugeeing, the same pattern that took Jane's family to Texas. Different family, different state, same shape.

I would still be searching for "Jobe."

## What I would tell you if you were going to build your own

A handful of things I wish I had known on day one:

- **Pick the family-knowledge encoding before you pick the database.** The claims schema is the most important decision in the project, because everything downstream is shaped by it. Fact types, confidence, and provenance are not optional.
- **Reverse-engineer the cookies, not the JWT.** Long-lived session cookies are how most genealogy sites *actually* authenticate the search API; the JWT is for the React app.
- **Assume the filters are broken until you've proven they work.** Run the same query three times with three different filter values and watch the result counts. AHQ silently ignores both `db` and `state`. OHS Dawes silently ignores nothing — which is why the OHS scraper took fifteen minutes.
- **The slave narratives are gold.** Roughly 2,300 first-person accounts of slavery, all in the public domain, all OCR'd, almost none of them indexed *for genealogy*. They are full of names: enslavers, siblings sold off, uncles who took children in after the war, plantations, migration paths, dates given in landmarks ("the day they read the free papers") instead of calendars. Every name in a narrative is a search hint.
- **Don't fight the records.** Pre-1870 records are a graph of partial evidence. The system has to be designed for that, not against it.
- **Self-host Gramps-Web.** It is the only piece of free-software genealogy that has a real REST API, a real data model, and a license that lets you write back to it programmatically. Ancestry will not let you do this.

## What's next

The 23 frontier ancestors are not all going to fall. Nick Washington, born 1823 NC, is going to need the North Carolina slave schedules and the Freedmen's Bureau labor contracts. The pre-Hannah Rawls line — Hannah was born ~1794 in Virginia and enslaved in Mississippi by 1860 — is going to need Virginia probate records and the kind of inventory that listed enslaved people by first name only. Some lines may end where the records end; "Born: Africa" on a slave schedule is the kind of entry you can chase into Sierra Leone Recaptive Registers, but those are partly digitized and partly still in paper archives.

The next chunk of work is the Freedmen's Bureau records (collection 4406) and the Leake County Mississippi probate indexes (DGS 5816569, DGS 5816570). Estate inventories listed enslaved people by name, and Henry S. Rawls's estate was probated in Leake County between 1853 and 1860. If Hannah, Jane's mother, or any of the eighteen people from the 1850 slave schedule who don't appear in the 1860 schedule were inventoried by name, they are in those volumes.

When the tree is in a stable place I'll cut a public read-only view of the Gramps-Web instance and link it here. In the meantime, the scraper repo is at [`github.com/jbwashington/census-scraper`](https://github.com/jbwashington) and the family tree is at 108 people and counting. Not bad for a wall.
