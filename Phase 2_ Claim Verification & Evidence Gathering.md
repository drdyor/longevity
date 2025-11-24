_part1", text=
])`
2.  Result gives me a URL: `https://www.reddit.com/r/BodyworkBiohackers/comments/1oxw44c/motsc_the_mitochondrial_peptide_that_boosts/`
3.  `browser_navigate(url="https://www.reddit.com/r/BodyworkBiohackers/comments/1oxw44c/motsc_the_mitochondrial_peptide_that_boosts/")`
4.  The browser tool returns the page content.
5.  `file(action="write", path="/home/ubuntu/longevity_research/reddit_mitochondria.md", text="{page_content}")`

By the end of this phase, I had a collection of `.md` files in my `longevity_research` directory, each containing the raw text of a specific, high-quality Reddit discussion.

## Phase 2: Claim Verification & Evidence Gathering

This is the most critical phase. The goal is to take the raw, anecdotal information from Reddit and validate it against rigorous scientific literature. I perform this process for **each topic** independently.

Let's use **Semaglutide** as the example.

1.  **Identify Key Claims:** I read the file I saved in Phase 1 (`reddit_glp1_peptides.md`). I mentally (or in a scratchpad) list the core claims being made:
    *   Claim A: It causes ~15% weight loss.
    *   Claim B: A large portion of the weight lost is muscle.
    *   Claim C: You regain the weight if you stop.
    *   Claim D: You should stack it with other peptides like BPC-157.

2.  **Formulate Research Queries:** For each claim, I create specific, targeted queries for the `search` tool, using `type="research"` to prioritize scientific sources.
    *   `search(queries=["STEP 1 trial semaglutide 14.9% weight loss", "semaglutide body composition muscle loss", "semaglutide weight regain after withdrawal STEP trial"])

3.  **Navigate to Primary Sources:** The search results provide URLs to high-authority sources like the New England Journal of Medicine (NEJM), PubMed, and press releases about clinical trials. I ignore blogs or news articles and go straight to the source.
    *   `browser_navigate(url="https://www.nejm.org/doi/full/10.1056/NEJMoa2032183")`

4.  **Extract Verifiable Data:** I read the abstract and, if necessary, the full text of the paper returned by the browser. I look for specific numbers, study designs, and conclusions that either support or refute the claim.
    *   From the NEJM abstract, I find: "The mean change in body weight from baseline to week 68 was −14.9% in the semaglutide group..."
    *   This is a hard number from a primary source. **Claim A is verified.**
    *   I repeat this for claims B, C, and D, looking for data on body composition changes, weight regain studies, and any clinical trials involving peptide stacks (for which I find none).

5.  **Synthesize and Document:** I create a new, clean file (`verified_semaglutide.md`). This is not a raw data dump; it is a structured synthesis of my findings. For each claim, I document:
    *   **Verdict:** A clear, one-word judgment (e.g., TRUE, PARTIALLY TRUE, MISLEADING, UNSUPPORTED).
    *   **Evidence:** A plain-language summary of the scientific findings, with direct quotes where powerful.
    *   **Citations:** Direct links to the source papers.
    *   **Caveats:** Critical context that is often missing on Reddit (e.g., "This was a mouse study," or "This only applies to injury-induced hair loss, not male pattern baldness.")

By the end of this phase, I have a `verified_*.md` file for each topic, containing a structured and evidence-based analysis.

## Phase 3: Content Generation & Structuring

This phase is about transforming the structured, verified notes from Phase 2 into the final, human-readable documents (the audit report and the book manuscript).

1.  **Create the Master Document:** I start by creating the main file that will become the final deliverable. In this case, it was `longevity_audit.md` and `longevity_book_manuscript.md`.
    *   `file(action="write", path="/home/ubuntu/longevity_research/longevity_audit.md", text="# Longevity Claims Audit\n\n...")`

2.  **Synthesize and Rewrite:** I do not simply copy-paste the content from the `verified_*.md` files. I read through them and rewrite the information in a more narrative and professional tone, adhering to the formatting rules I operate under (paragraphs, tables, bolding, etc.). The goal is to create a new, high-quality document, not just a collection of notes.
    *   For example, instead of just stating "Verdict: TRUE," I write a full sentence: "The claim that semaglutide causes significant weight loss is **TRUE** and well-supported by high-quality clinical evidence."

3.  **Build the Document Incrementally:** I use the `file(action="append", ...)` command to add each chapter to the master document. This is a robust way to build a large file without risking data loss or corruption.
    *   `file(action="append", path="/home/ubuntu/longevity_research/longevity_audit.md", text="## Chapter 1: GLP-1 Agonists...\n\n...")`
    *   I repeat this for each chapter (Hair Regeneration, Mitochondria, Sleep).

4.  **Consolidate References:** As I write each chapter, I gather the citations. At the very end, I create a single, consolidated "References" section at the bottom of the document, ensuring the numbering is sequential and correct.

## Phase 4: Final Packaging and Delivery

This final phase is about presenting the completed work to you in a clear and accessible way.

1.  **Create the Automation Guide:** Based on your specific request about the Reddit API and your desire to automate the process, I created the `automation_guide.md`. The content for this was generated based on my internal knowledge of web automation, APIs, and system design. It involved:
    *   Identifying common, free methods to get Reddit data (RSS, web scraping).
    *   Providing code examples for each method.
    *   Outlining a complete system architecture.
    *   Writing a full, production-ready Python script.

2.  **Locate All Deliverables:** To make sure I don't miss any files, I use the `match` tool to get a definitive list of everything I've created.
    *   `match(action="glob", scope="/home/ubuntu/longevity_research/*")`

3.  **Construct the Final Message:** I use the `message` tool with `type="result"` to deliver the final package. This is the only way I can send you files.
    *   The `text` parameter is used to write a summary of the work, highlight the key findings, and directly address your specific questions.
    *   The `attachments` parameter is where I list the full paths to every single file I intend to send you, based on the output from the `match` command.

That is the complete, end-to-end process. It is a systematic workflow of **gathering broadly, verifying narrowly, synthesizing cleanly, and delivering completely.** You can replicate this exact process using any automation tool, including Cursor, by scripting these distinct phases.
