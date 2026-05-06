"""Rebuild counterfactual_pairs.jsonl

- C1: keep the 12 entries from the existing template (already filled).
- C2: 12 NLI premises with explicit regulatory anchors AND substantial
       residual scenario; anchor stripped, scenario preserved.
- C3: 12 NLI premises with rich surface markers (fictional org name,
       country, sector, narrative connectives); scrubbed into
       bureaucratic third-person without losing regulatory content.
- C4: 12 NLI premises with dense pillar-specific vocabulary;
       pillar-A vocab swapped to pillar-B vocab, syntax preserved.
"""
import json
import pickle
from pathlib import Path


with open('./benchmark/task_pool/ge_nli/ge_nli.jsonl') as f:
    nli = [json.loads(l) for l in f if l.strip()]
with open('./benchmark/task_pool/ge_cls/ceb_cls.json') as f:
    cls = json.load(f)
with open('./benchmark/task_pool/ge-stance/ge_stance.jsonl') as f:
    stance = [json.loads(l) for l in f if l.strip()]

# Build quick lookups
nli_by_id = {it['id']: it for it in nli}
cls_by_id = {it['passage_id']: it for it in cls}
stance_by_id = {it['id']: it for it in stance}


with open('./explainability_gui/pools.pkl', 'wb') as f:
    pickle.dump({'nli': nli, 'cls': cls, 'stance': stance,
                 'nli_by_id': nli_by_id, 'cls_by_id': cls_by_id,
                 'stance_by_id': stance_by_id}, f)

# Load template
with open('./explainability_gui/sample/counterfactual_pairs_template_.jsonl') as f:
    tpl = [json.loads(l) for l in f if l.strip()]
print(f'Loaded {len(nli)} NLI, {len(cls)} CLS, {len(stance)} STANCE, {len(tpl)} template items.')

# Look at which IDs the template currently references for C2, C3, C4
print('\nC2 source ids:')
for it in tpl:
    if it['axis'] == 'C2':
        print(f"  {it['source_task']:10} {it['source_id']:50} pillar={it['label_original']}")
print('\nC3 source ids:')
for it in tpl:
    if it['axis'] == 'C3':
        print(f"  {it['source_task']:10} {it['source_id']:50} pillar={it['label_original']}")
print('\nC4 source ids:')
for it in tpl:
    if it['axis'] == 'C4':
        print(f"  {it['source_task']:10} {it['source_id']:50} pillar={it['label_original']}")


with open('./explainability_gui/pools.pkl', 'rb') as f:
    P = pickle.load(f)
nli_by_id = P['nli_by_id']
cls_by_id = P['cls_by_id']
stance_by_id = P['stance_by_id']

# Load existing template for C1 reuse
with open('./explainability_gui/sample/counterfactual_pairs_template_.jsonl') as f:
    TPL = [json.loads(l) for l in f if l.strip()]

DATE = "2026-05-05"
AUTHOR = "ilyass"

# Per-axis edit_note (constant within axis)
NOTE_C1 = ("GENDER SWAP. Replace female-coded gendered terms with male-coded equivalents "
           "(women->men, woman->man, girls->boys, mother->father, she/her->he/him, etc.). "
           "Preserve every other token, including organisation names, statistics, dates, "
           "and regulatory anchors. `expected_flip=False` items test gender-invariance of "
           "the model's decision; `expected_flip=True` items test whether the model correctly "
           "tracks the gender-specificity of a regulatory anchor (e.g., Women on Boards "
           "Directive, violence-against-women) by flipping the prediction when the scenario "
           "gender no longer matches.")

NOTE_C2 = ("ANCHOR REMOVAL. Delete every named EU directive, percentage target, article "
           "number, and pillar-defining noun phrase. Replace each with a neutral paraphrase "
           "that preserves syntactic flow but removes the regulatory anchor. Do NOT change "
           "tense, sentiment, or factual claims outside the anchor span.")

NOTE_C3 = ("SURFACE SCRUBBING. Replace fictional character names with role-only phrasing "
           "('the compliance officer'), strip direct-speech tags ('she said' -> drop), and "
           "remove narrative connectives ('meanwhile', 'the next morning'). Rewrite into "
           "bureaucratic third-person past tense without losing any factual or regulatory "
           "content.")

NOTE_C4 = ("PILLAR-KEYWORD SWAP. Replace pillar-A vocabulary with pillar-B vocabulary "
           "(record both pillars in `edit_note_target`). Preserve syntax exactly. Example: "
           "'gender-based violence' -> 'pay-gap discrimination', 'safe houses' -> 'pay "
           "audits'. The edited item should be syntactically valid English that any reader "
           "would classify as pillar B rather than pillar A.")


def nli_input(it):
    return f"PREMISE: {it['premise']}\n\nHYPOTHESIS: {it['hypothesis']}"


def make(axis, source_task, original_id, label_original,
         original_input, edited_input, edit_note, edit_note_target,
         expected_flip):
    # Schema follows §7.2.1 of the GUI explainability framework.
    # Canonical fields: pair_id, axis, original_id, edit_note,
    # original_input, edited_input. Additional diagnostic fields
    # (source_task, label_original, edit_note_target, expected_flip,
    # construction_*) are retained for the faithfulness scoring of
    # §7.2.2 and the pairwise comparisons of §7.3.2.
    return {
        "pair_id": f"cf_{axis}_{original_id}",
        "axis": axis,
        "original_id": original_id,
        "source_task": source_task,
        "label_original": label_original,
        "original_input": original_input,
        "edited_input": edited_input,
        "edit_note": edit_note,
        "edit_note_target": edit_note_target,
        "expected_flip": expected_flip,
        "construction_author": AUTHOR,
        "construction_date": DATE,
    }


# ===========================================================================
# C1 — keep verbatim from existing template (12 items, all already filled)
# ===========================================================================
C1_RECORDS = [it for it in TPL if it['axis'] == 'C1']
assert len(C1_RECORDS) == 12
# sanity: none should be empty
for r in C1_RECORDS:
    assert r['edited_input'].strip(), f"empty C1 {r['pair_id']}"


# ===========================================================================
# C2 — 12 anchor-removal pairs.
# Convention from existing template: expected_flip=False uniformly.
# Strategy: each premise has an explicit anchor (Directive name,
# % target, article number, pillar noun) AND a non-anchor scenario
# residual. We strip anchors and replace with neutral paraphrase;
# the residual is sufficient for the NLI label to remain interpretable.
# ===========================================================================

C2_SPECS = []

# --- violence_stereotypes (3) ---
# 1. ge_nli_020 (entailment): Istanbul Convention -> generic "international standards"
it = nli_by_id['ge_nli_020']
edited_premise = (
    "EduReform România asbl, a Bucharest-based educational charity, partnered with "
    "Romania's National Agency for Equal Opportunities in 2022 to launch a perpetrator "
    "intervention programme in three counties. The 26-week programme addressed "
    "cognitive distortions, anger regulation, and healthy relationship skills, "
    "certified in accordance with established international standards for behavioural "
    "rehabilitation. Forty-eight men completed the programme in 2023, of whom 38 were "
    "court-referred and 10 self-referred. A six-month follow-up using police records "
    "and victim-reported contact data found recidivism among programme completers far "
    "lower than in a matched comparison group. The National Agency confirmed funding "
    "for two additional regional programme sites for 2024 based on the evaluation "
    "findings."
)
edited_hypothesis = (
    "States parties must establish or support intervention programmes for perpetrators "
    "of household violence aimed at encouraging non-violent behaviour and preventing "
    "future offences."
)
C2_SPECS.append(dict(
    source_id='ge_nli_020', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed: 'Istanbul Convention standards', the explicit recidivism percentages (14% / 38%), and the named pillar-anchor 'domestic violence' in the hypothesis. Kept: organisation, country, programme structure, sample sizes, narrative direction.",
))

# 2. ge_nli_108 (neutral): same premise, different hypothesis (about employment)
it = nli_by_id['ge_nli_108']
edited_premise = (
    "EduReform România asbl, a Bucharest-based educational charity, partnered with "
    "Romania's National Agency for Equal Opportunities in 2022 to launch a perpetrator "
    "intervention programme in three counties. The 26-week programme addressed "
    "cognitive distortions, anger regulation, and healthy relationship skills, "
    "certified in accordance with established international standards. Forty-eight men "
    "completed the programme in 2023, of whom 38 were court-referred and 10 "
    "self-referred. A six-month follow-up using police records and victim-reported "
    "contact data found recidivism among programme completers far lower than in a "
    "matched comparison group. The National Agency confirmed funding for two "
    "additional regional programme sites for 2024 based on the evaluation findings."
)
edited_hypothesis = (
    "Employers must adopt impartial job evaluation methods and promote balanced "
    "representation in managerial positions to reduce occupational segregation."
)
C2_SPECS.append(dict(
    source_id='ge_nli_108', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed: 'Istanbul Convention standards' and explicit % values from premise; removed 'gender-neutral' and 'gender-balanced' from hypothesis (pillar-defining phrases).",
))

# 3. ge_nli_148 (entailment): Article 172 ter / Istanbul Convention / restraining orders
it = nli_by_id['ge_nli_148']
edited_premise = (
    "TecnoBarcelona S.L., a Barcelona-based software development firm, updated its code "
    "of conduct and digital security policy in 2022 following Spain's reform of its "
    "criminal law to include persistent threatening conduct as a specific offence, "
    "aligned with broader international commitments. The company established a digital "
    "harassment monitoring protocol for company-issued devices and platforms, training "
    "cybersecurity and HR teams to identify patterns of repeated threatening or "
    "surveillance behaviour. In 2023, TecnoBarcelona identified and investigated two "
    "cases of persistent threatening behaviour involving employees, referred both to "
    "the National Police's cybercrime unit, and supported affected employees through "
    "the criminal complaint process. Both cases resulted in court-ordered protection "
    "measures issued within three months of the initial report."
)
edited_hypothesis = (
    "States parties must criminalise persistent threatening conduct, defined as "
    "intentional and repeated behaviour directed at another person that causes them "
    "to fear for their safety."
)
C2_SPECS.append(dict(
    source_id='ge_nli_148', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed: 'Article 172 ter', 'Istanbul Convention', and the legal label 'stalking' (replaced with descriptive 'persistent threatening conduct'); removed 'restraining orders' (legal anchor) -> 'court-ordered protection measures'.",
))

# --- leadership_participation (3) ---
# 4. ge_nli_029 (entailment): Women on Boards Directive review deadline
it = nli_by_id['ge_nli_029']
edited_premise = (
    "LogiCar România S.A., a Bucharest-listed freight logistics company, submitted a "
    "detailed written contribution to the European Commission's 2030 review of board "
    "composition rules in October 2030. The submission documented the company's "
    "progress from 9% to 43% female non-executive board representation over eight "
    "years and argued in favour of extending the review's scope to large non-listed "
    "companies. It presented sector data showing that Romanian logistics companies "
    "outside the existing rules showed virtually no progress, with average female "
    "board representation stagnating at 12%. LogiCar's contribution was cited in the "
    "Commission's official review report as an example of effective voluntary adoption "
    "beyond statutory requirements."
)
edited_hypothesis = (
    "By the end of 2030, the relevant authority must review and assess whether the "
    "rules have effectively improved the gender composition of boards and consider "
    "extending their scope if needed."
)
C2_SPECS.append(dict(
    source_id='ge_nli_029', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed: 'Women on Boards Directive' (twice in original premise, once in hypothesis) -> 'board composition rules' / 'the existing rules' / 'the rules'; removed '31 December 2030' -> 'the end of 2030'; removed 'gender balance on boards' (pillar phrase) -> 'gender composition of boards'.",
))

# 5. ge_nli_055 (entailment): Directive paths, 40%, 30 June 2026
it = nli_by_id['ge_nli_055']
edited_premise = (
    "CelticSteel plc, a Dublin-listed precision engineering manufacturer, submitted "
    "its board diversity compliance plan to the Irish Corporate Governance Authority "
    "in March 2023, committing to a strong female non-executive presence by mid-2026 "
    "under the principal compliance route available to it. Two new female "
    "non-executive directors were appointed in 2023, raising female non-executive "
    "representation from a low baseline to a substantially higher share. An executive "
    "pipeline target was set for female representation at director-minus-one level to "
    "sustain board candidate supply. A board effectiveness sub-committee was "
    "established to oversee diversity targets and report quarterly to the full board. "
    "By March 2024, female executive representation at that pipeline level stood ahead "
    "of schedule."
)
edited_hypothesis = (
    "States must ensure that listed companies achieve a substantially balanced "
    "presence of the underrepresented sex in their boardrooms by mid-2026."
)
C2_SPECS.append(dict(
    source_id='ge_nli_055', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed all percentage targets (40%, 33%, 17%, 35%, 32%); removed 'path (a) of the Directive' -> 'the principal compliance route'; removed 'Member States' -> 'States'; replaced concrete deadline '30 June 2026' with 'mid-2026'; removed both numeric anchors and the directive reference.",
))

# 6. ge_nli_122 (entailment): Women on Boards Directive, 40%, etc.
it = nli_by_id['ge_nli_122']
edited_premise = (
    "FundacjaPol, a Warsaw-based governance advisory foundation, worked with 12 Polish "
    "listed companies in 2022 to implement board diversity action plans compliant with "
    "the prevailing board composition rules. Each company signed a legally binding "
    "memorandum committing to specific representation targets and annual reporting "
    "obligations. FundacjaPol provided each company with a tailored nomination process "
    "review and access to a database of pre-screened qualified female board "
    "candidates. Across the 12 companies, female board representation increased "
    "substantially over 24 months. Several companies reached the target threshold by "
    "December 2023. FundacjaPol published a progress report confirming all 12 "
    "companies maintained or increased their female board share year-on-year."
)
edited_hypothesis = (
    "Listed companies must achieve a more balanced participation of women and men "
    "among their directors through effective and legally binding measures."
)
C2_SPECS.append(dict(
    source_id='ge_nli_122', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed: 'Women on Boards Directive' -> 'prevailing board composition rules'; removed '240', '18% to 31%', '40% non-executive threshold' (numeric anchors and pillar quantitative target).",
))

# --- equal_economy (2) ---
# 7. ge_nli_121 (neutral): NordStaal premise + hypothesis on UHC
it = nli_by_id['ge_nli_121']
edited_premise = (
    "NordStaal B.V., a Rotterdam-based steel manufacturer, pre-emptively adopted a "
    "company-level workplace equality strategy in 2021 modelled on a forthcoming "
    "policy framework. The strategy included four pillars: equal-pay certification, "
    "women-in-STEM recruitment targets, ergonomics adapted to mixed workforces in "
    "production facilities, and an extended paid leave entitlement for new parents. "
    "An independent review identified a substantial raw earnings gap, reduced "
    "considerably after controlling for role and seniority. NordStaal set a binding "
    "target of closing the residual gap to a marginal level within a fixed timeframe "
    "and submitted its strategy to the Dutch Social and Economic Council as a sectoral "
    "model. By 2023, female employment in technical roles had grown markedly."
)
edited_hypothesis = (
    "States must ensure sustained funding of universal health coverage, including "
    "essential health services, with particular attention to underserved populations."
)
C2_SPECS.append(dict(
    source_id='ge_nli_121', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Premise: removed 'gender equality strategy', 'EU framework', 'gender pay gap' (9.7%, 3.2%, 1%), 'eight-week paid paternity leave', 'gender-sensitive ergonomics'; replaced with neutral paraphrases. Hypothesis: removed 'sexual and reproductive health services' and 'women and girls with disabilities' (pillar-defining phrases).",
))

# 8. ge_nli_166 (entailment): pay gap and Commission strategy
it = nli_by_id['ge_nli_166']
edited_premise = (
    "NordStaal B.V., a Rotterdam-based steel manufacturer, pre-emptively adopted a "
    "company-level workplace equality strategy in 2021 modelled on a forthcoming "
    "policy framework. The strategy included four pillars: equal-pay certification, "
    "women-in-STEM recruitment targets, ergonomics adapted to mixed workforces, and an "
    "extended paid leave entitlement for new parents. An independent review identified "
    "a substantial raw earnings gap, reduced considerably after controlling for role "
    "and seniority. NordStaal set a binding target of closing the residual gap to a "
    "marginal level within a fixed timeframe and submitted its strategy to the Dutch "
    "Social and Economic Council as a sectoral model. By 2023, female employment in "
    "technical roles had grown markedly."
)
edited_hypothesis = (
    "The competent authority must adopt a stand-alone equality framework that "
    "includes specific policies aimed at closing wage disparities between women and "
    "men."
)
C2_SPECS.append(dict(
    source_id='ge_nli_166', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Premise as in cf_C2_ge_nli_121. Hypothesis: 'European Commission' -> 'competent authority'; 'gender equality strategy' -> 'equality framework'; 'gender pay gap' -> 'wage disparities between women and men'.",
))

# --- funding_global_action (2) ---
# 9. ge_nli_089 (entailment): GAP III monitoring
it = nli_by_id['ge_nli_089']
edited_premise = (
    "The French Ministry of Europe and Foreign Affairs published an annual "
    "contribution to a multilateral monitoring framework each year from 2022 to 2024, "
    "covering French bilateral aid activities across 22 partner countries. Each "
    "contribution included quantitative data on equality-tagged expenditure, a "
    "narrative assessment of progress against agreed thematic priorities, and case "
    "studies of effective practice. France commissioned an independent mid-term "
    "evaluation of its contribution in 2023, conducted by an external consultancy "
    "covering the coherence and results of equality-focused bilateral programmes. The "
    "evaluation, published publicly in March 2024, found that more than two-thirds of "
    "French bilateral programmes were equality-responsive and recommended increased "
    "investment in reproductive rights dialogue."
)
edited_hypothesis = (
    "The competent authority must publish annual progress reports on the multilateral "
    "framework's implementation and conduct a mid-term and final evaluation of its "
    "impact on equality outcomes."
)
C2_SPECS.append(dict(
    source_id='ge_nli_089', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed all instances of 'GAP III' (5x) -> 'multilateral monitoring framework' / 'the framework'; removed 'EU' -> '(elided)' or 'multilateral'; '68%' -> 'more than two-thirds'; 'gender-tagged' -> 'equality-tagged'; 'European Commission' -> 'competent authority' (hypothesis).",
))

# 10. ge_nli_162 (entailment): GAP III endorsement
it = nli_by_id['ge_nli_162']
edited_premise = (
    "EqualAid Belgium asbl, a Brussels-based international development NGO, "
    "facilitated a structured civil society dialogue in 2021 to support a legislative "
    "body's deliberations on endorsing a multilateral equality action plan. The "
    "organisation convened four thematic hearings attended by 68 elected officials and "
    "40 women's rights organisations from partner countries, producing 22 consolidated "
    "civil society recommendations on the action plan's implementation priorities. "
    "EqualAid published a policy brief comparing the new action plan's commitments "
    "with its predecessor and identifying six areas requiring stronger oversight. The "
    "legislative body adopted a resolution endorsing the action plan in March 2021, "
    "incorporating 14 of the 22 civil society recommendations. EqualAid subsequently "
    "monitored and reported annually on follow-up to the resolution."
)
edited_hypothesis = (
    "The legislative body and the executive authority must endorse the multilateral "
    "equality action plan and cooperate with the implementing agency in its full "
    "implementation."
)
C2_SPECS.append(dict(
    source_id='ge_nli_162', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed all 'GAP III' / 'GAP II' references -> 'multilateral equality action plan' / 'predecessor'; 'European Parliament' -> 'legislative body'; 'MEPs' -> 'elected officials'; 'EU partner countries' -> 'partner countries'; 'European Parliament and the Council' -> 'legislative body and the executive authority'; 'EU Gender Action Plan III' -> 'multilateral equality action plan'.",
))

# --- mainstreaming_intersectionality (2) ---
# 11. ge_nli_105 (entailment): UHC + women with disabilities
it = nli_by_id['ge_nli_105']
edited_premise = (
    "NordLogistik AB, a Gothenburg-based logistics company, channelled SEK 1.8 million "
    "of its corporate social responsibility budget through Sweden's development "
    "cooperation framework to a community health programme in Uganda in 2022. The "
    "programme, implemented by a local health NGO, focused on ensuring access to "
    "essential health services, including those addressing reproductive and maternal "
    "needs, for women and girls with mobility and other impairments in three rural "
    "districts. Mobile health units with accessible examination facilities visited 45 "
    "communities, serving 4,200 women and girls. Inclusive training was delivered to "
    "90 community health workers. By 2023, access to assisted delivery among women "
    "with mobility impairments in target districts increased substantially, exceeding "
    "the programme's target."
)
edited_hypothesis = (
    "States must ensure sustained funding of community-level health coverage, "
    "including essential reproductive and maternal services, with particular attention "
    "to women and girls with disabilities."
)
C2_SPECS.append(dict(
    source_id='ge_nli_105', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Removed 'universal health coverage' and 'sexual and reproductive health services' (pillar-defining phrases) -> 'essential health services' / 'community health programme'; 'disability-inclusive training' -> 'inclusive training'; explicit %s ('12% to 41%', '35%') -> 'increased substantially'.",
))

# 12. ge_nli_138 (neutral): EU-co-funded telemedicine + GAP III hypothesis
it = nli_by_id['ge_nli_138']
edited_premise = (
    "HealthTech NL B.V., an Amsterdam-based digital health company, deployed a "
    "co-funded telemedicine platform across 60 rural clinics in Rwanda and Burundi "
    "between 2022 and 2024. The platform was designed with an accessibility-first "
    "approach, incorporating audio navigation and simplified interfaces for users with "
    "low literacy or visual impairments. Of 38,000 patient consultations completed, "
    "most were with women and a significant share with persons with disabilities. The "
    "system integrated maternal care, contraception counselling, and prevention "
    "modules for major communicable diseases. Coverage of essential reproductive "
    "health services in target districts rose substantially over the project period. "
    "An accessibility audit confirmed the platform met international standards for "
    "assistive technology compatibility."
)
edited_hypothesis = (
    "The competent authority must publish annual progress reports on its equality "
    "action plan and conduct a mid-term and final evaluation of its impact on "
    "equality outcomes."
)
C2_SPECS.append(dict(
    source_id='ge_nli_138', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="Premise: 'EU-co-funded' -> 'co-funded'; 'HIV/AIDS' -> 'major communicable diseases'; '67%' -> 'most'; '9%' -> 'a significant share'; '34% to 58%' -> 'substantially'. Hypothesis: 'European Commission' -> 'competent authority'; 'GAP III implementation' -> 'its equality action plan'; 'gender equality' -> 'equality outcomes'.",
))

C2_RECORDS = [
    make("C2", "GE-NLI", s['source_id'], s['label_original'],
         s['original_input'], s['edited_input'], NOTE_C2,
         s['edit_note_target'], expected_flip=False)
    for s in C2_SPECS
]
assert len(C2_RECORDS) == 12


# ===========================================================================
# C3 — 12 surface-scrubbing pairs.
# Convention: expected_flip=True uniformly (we test the failure-mode that
# surface markers were doing the work).
# Strategy: replace fictional org name with neutral generic role (e.g.,
# "a national education authority"); strip city/country setting cues to
# bureaucratic minimum; remove any narrative connectives. Regulatory
# content (anchors, %, dates, hypothesis) preserved.
# ===========================================================================

C3_SPECS = []

# 1. ge_nli_013 (entailment, violence_stereotypes)
it = nli_by_id['ge_nli_013']
edited_premise = (
    "A national education authority partnered with the relevant ministry and 60 "
    "primary and secondary schools in 2022 to develop and deliver a gender equality "
    "curriculum package. The package included age-appropriate classroom modules on "
    "gender equality, non-stereotyped role models, healthy relationship skills, and "
    "the right to bodily autonomy. Teachers received 12 hours of professional "
    "development before delivery. By June 2023, 12,400 students had completed at least "
    "four curriculum sessions. A pre-post assessment showed a 24 percentage point "
    "increase in students correctly identifying coercive behaviour in relationship "
    "scenarios and a 19 percentage point increase in reported confidence to seek help "
    "in situations of harm."
)
C3_SPECS.append(dict(
    source_id='ge_nli_013', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'GezondheidEdu B.V., a Rotterdam-based health education company' -> 'A national education authority'; 'the Dutch Ministry of Education' -> 'the relevant ministry'; 'across North Holland' -> dropped. All numeric facts (60 schools, 12 hours, 12,400 students, 24pp, 19pp) preserved; hypothesis untouched.",
))

# 2. ge_nli_073 (neutral, violence_stereotypes; same premise as 013)
it = nli_by_id['ge_nli_073']
C3_SPECS.append(dict(
    source_id='ge_nli_073', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Premise scrubbed identically to cf_C3_ge_nli_013 (same source premise; different hypothesis). Hypothesis unchanged.",
))

# 3. ge_nli_017 (entailment, violence_stereotypes): RheinFracht / Frankfurt
it = nli_by_id['ge_nli_017']
edited_premise = (
    "A national freight logistics operator updated its disciplinary code in 2022 "
    "following national implementation of psychological violence provisions of the "
    "Istanbul Convention. The code explicitly defined psychologically coercive conduct "
    "— including sustained threats, intimidation, and systematic humiliation — as a "
    "dismissible offence and obligated the operator to refer credible cases to the "
    "public prosecutor. Training on recognising and reporting psychological violence "
    "was delivered to 280 supervisors and team leaders. In 2023, the operator "
    "investigated four complaints of coercive conduct, dismissed two employees, "
    "issued formal warnings in the remaining cases, and referred all four to the "
    "competent prosecution service. The updated code was endorsed by the works council "
    "as compliant with the national legislation on violence against women."
)
C3_SPECS.append(dict(
    source_id='ge_nli_017', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'RheinFracht GmbH, a Frankfurt-based freight logistics company' -> 'A national freight logistics operator'; 'Germany' / 'German' -> 'national'; 'Frankfurt Prosecution Service' -> 'competent prosecution service'. Regulatory anchors ('Istanbul Convention', 'national legislation on violence against women') preserved.",
))

# 4. ge_nli_019 (entailment, leadership_participation)
it = nli_by_id['ge_nli_019']
edited_premise = (
    "A national higher-education oversight body overseeing 42 institutions adopted a "
    "gender parity action plan in 2022 committing to 50/50 gender balance in all "
    "senior and middle management positions within the body itself by end of 2024. "
    "All appointment panels were required to include at least one gender equality "
    "officer, and gender balance criteria were formally incorporated into annual "
    "performance review scorecards for all heads of department. By December 2023, "
    "women held 49% of senior management positions, up from 33% in 2021. Appointment "
    "decision minutes documenting gender balance considerations were made publicly "
    "accessible. The body also required all 42 supervised institutions to publish "
    "gender composition data for their governing bodies."
)
C3_SPECS.append(dict(
    source_id='ge_nli_019', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'Hellenic Education Agency, a public body in Athens' -> 'A national higher-education oversight body'; subsequent references to 'the Agency' -> 'the body'. All numeric facts and hypothesis preserved.",
))

# 5. ge_nli_067 (neutral, leadership_participation; same Hellenic Education Agency premise)
it = nli_by_id['ge_nli_067']
C3_SPECS.append(dict(
    source_id='ge_nli_067', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Premise scrubbed identically to cf_C3_ge_nli_019. Hypothesis unchanged.",
))

# 6. ge_nli_081 (entailment, leadership_participation): TransilvaniaCapital + Romanian Government
it = nli_by_id['ge_nli_081']
edited_premise = (
    "A national investment group funded a €500,000 Women in Governance programme in "
    "partnership with the relevant national government and a multilateral development "
    "agency between 2021 and 2023. The programme trained 120 women candidates from "
    "rural constituencies for local council elections and provided 30 women with "
    "advanced conflict resolution certification recognised by the national mediation "
    "council. In the 2020 local elections within target counties, female candidacy "
    "rates rose by 14 percentage points and women's seat share on local councils "
    "increased from 16% to 23%. Two programme graduates were appointed as official "
    "mediators in post-election dispute resolution processes, the first female "
    "mediator appointments in those jurisdictions."
)
C3_SPECS.append(dict(
    source_id='ge_nli_081', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'TransilvaniaCapital S.A., a Bucharest-based investment group' -> 'A national investment group'; 'Romanian Government' -> 'the relevant national government'; 'UNDP' -> 'a multilateral development agency'; 'Romanian Council of Mediation' -> 'national mediation council'.",
))

# 7. ge_nli_070 (neutral, equal_economy)
it = nli_by_id['ge_nli_070']
edited_premise = (
    "A national hospitality and catering operator launched a Women's Financial "
    "Inclusion Initiative in 2022 through its international development arm, in "
    "partnership with a microfinance provider and a foreign women's cooperative bank. "
    "The initiative provided legal and financial literacy training to 800 women "
    "entrepreneurs in rural areas of the partner country whose access to land titles "
    "and bank credit was restricted by customary inheritance practices. Working with "
    "local legal aid clinics, the initiative supported 140 women in formally "
    "registering land titles previously held informally and facilitated micro-credit "
    "access for 210 women previously ineligible for bank loans. Average annual income "
    "among participating women increased by 34% and business investment grew by 28% "
    "compared to a matched control group."
)
C3_SPECS.append(dict(
    source_id='ge_nli_070', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'Emerald Hospitality Group Ltd, a Dublin-based hotel and catering company' -> 'A national hospitality and catering operator'; 'Microfinance Ireland' -> 'a microfinance provider'; 'a Kenyan women's cooperative bank' -> 'a foreign women's cooperative bank'; 'rural Kenya' -> 'rural areas of the partner country'.",
))

# 8. ge_nli_032 (neutral, equal_economy): Jämlikhetsfonden / Stockholm
it = nli_by_id['ge_nli_032']
edited_premise = (
    "A national equality foundation launched a biannual Gender Pay Tracker in 2022 in "
    "collaboration with the national statistics office, publishing sector-level "
    "gender pay gap data disaggregated by age, occupation, contract type, and "
    "part-time incidence, covering approximately 2.3 million workers. A dedicated "
    "pension gap module calculated the cumulative impact of career breaks and "
    "part-time work on women's retirement incomes across five pension cohorts. The "
    "first edition documented an average adjusted pay gap of 7.2% and an overall "
    "earnings gap of 28.4%. The Tracker was downloaded 14,000 times in its first six "
    "months and cited in three parliamentary inquiries into pay discrimination "
    "reform. The second edition was published on schedule in late 2023."
)
C3_SPECS.append(dict(
    source_id='ge_nli_032', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'Jämlikhetsfonden, a Stockholm-based equality foundation' -> 'A national equality foundation'; 'Statistics Sweden' -> 'the national statistics office'.",
))

# 9. ge_nli_083 (entailment, funding_global_action): Hellenic Research Finance / Athens
it = nli_by_id['ge_nli_083']
edited_premise = (
    "A national research-funding intermediary administered a Horizon Europe-funded "
    "gender and innovation programme from 2022 to 2024, disbursing €4.2 million to 18 "
    "gender studies research consortia across national universities. A mandatory "
    "requirement specified that at least 50% of principal investigators were women. A "
    "gender integration checklist was applied to all funded proposals to ensure "
    "research design incorporated a gender perspective. By programme close, 11 of the "
    "18 projects had published findings incorporating sex-disaggregated data, and "
    "three contributed to national policy revisions. The share of female principal "
    "investigators across the intermediary's full Horizon Europe portfolio rose from "
    "31% to 47%."
)
C3_SPECS.append(dict(
    source_id='ge_nli_083', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'Hellenic Research Finance S.A., an Athens-based research funding intermediary' -> 'A national research-funding intermediary'; 'Greek universities' -> 'national universities'. The regulatory anchor 'Horizon Europe' is kept as it is the subject of the hypothesis.",
))

# 10. ge_nli_005 (neutral, funding_global_action): French Ministry / GAP III + reporting hypothesis
it = nli_by_id['ge_nli_005']
edited_premise = (
    "A national foreign affairs ministry published an annual contribution to the EU's "
    "GAP III monitoring framework each year from 2022 to 2024, covering bilateral aid "
    "activities across 22 partner countries. Each contribution included quantitative "
    "data on gender-tagged expenditure, a narrative assessment of progress against "
    "GAP III thematic priorities, and case studies of effective practice. The ministry "
    "commissioned an independent mid-term evaluation of its GAP III contribution in "
    "2023, conducted by an external consultancy covering the coherence and results of "
    "gender-focused bilateral programmes. The evaluation, published publicly in March "
    "2024, found that 68% of the ministry's bilateral programmes were "
    "gender-responsive and recommended increased investment in reproductive rights "
    "dialogue."
)
C3_SPECS.append(dict(
    source_id='ge_nli_005', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'The French Ministry of Europe and Foreign Affairs' -> 'A national foreign affairs ministry'; 'France' -> 'the ministry'; 'French bilateral' -> 'bilateral' / 'the ministry's bilateral'. Regulatory anchors (GAP III) preserved.",
))

# 11. ge_nli_008 (neutral, mainstreaming_intersectionality): NordLogistik AB / Sweden / Uganda
it = nli_by_id['ge_nli_008']
edited_premise = (
    "A national logistics operator channelled SEK 1.8 million of its corporate social "
    "responsibility budget through the country's development cooperation framework to "
    "a universal health coverage programme in a partner country in 2022. The "
    "programme, implemented by a local health NGO, focused on ensuring access to "
    "sexual and reproductive health services for women and girls with disabilities in "
    "three rural districts. Mobile health units with accessible examination "
    "facilities visited 45 communities, serving 4,200 women and girls. "
    "Disability-inclusive training was delivered to 90 community health workers. By "
    "2023, access to assisted delivery among women with mobility impairments in "
    "target districts increased from 12% to 41%, exceeding the programme's target of "
    "35%."
)
C3_SPECS.append(dict(
    source_id='ge_nli_008', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'NordLogistik AB, a Gothenburg-based logistics company' -> 'A national logistics operator'; 'Sweden's' -> \"the country's\"; 'Uganda' -> 'a partner country'.",
))

# 12. ge_nli_030 (entailment, mainstreaming_intersectionality)
it = nli_by_id['ge_nli_030']
edited_premise = (
    "A national digital health operator deployed an EU-co-funded telemedicine "
    "platform across 60 rural clinics in two partner countries between 2022 and 2024. "
    "The platform was designed with an accessibility-first approach, incorporating "
    "audio navigation and simplified interfaces for users with low literacy or visual "
    "impairments. Of 38,000 patient consultations completed, 67% were with women and "
    "9% with persons with disabilities. The system integrated maternal care, "
    "contraception counselling, and HIV/AIDS prevention modules. Coverage of "
    "essential reproductive health services in target districts rose from 34% to 58% "
    "over the project period. An accessibility audit confirmed the platform met "
    "international standards for assistive technology compatibility."
)
C3_SPECS.append(dict(
    source_id='ge_nli_030', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {it['hypothesis']}",
    edit_note_target="Replaced 'HealthTech NL B.V., an Amsterdam-based digital health company' -> 'A national digital health operator'; 'Rwanda and Burundi' -> 'two partner countries'.",
))

C3_RECORDS = [
    make("C3", "GE-NLI", s['source_id'], s['label_original'],
         s['original_input'], s['edited_input'], NOTE_C3,
         s['edit_note_target'], expected_flip=True)
    for s in C3_SPECS
]
assert len(C3_RECORDS) == 12


# ===========================================================================
# C4 — 12 pillar-keyword swap pairs.
# Convention: expected_flip=True uniformly (a well-grounded model
# should flip its prediction when the pillar vocabulary is swapped).
# Strategy: pick a target pillar; rewrite the dense pillar-A vocabulary
# in BOTH premise and hypothesis to pillar-B vocabulary while keeping
# syntax/structure intact.
# ===========================================================================

C4_SPECS = []

# 1. ge_nli_006 (entailment, violence_stereotypes -> leadership_participation)
it = nli_by_id['ge_nli_006']
edited_premise = (
    "The Câmara Municipal de Coimbra, Portugal, established a Multi-Agency Board "
    "Diversity Hub in 2022, bringing together the municipal council, corporate "
    "registry, audit authority, listing supervisor, and the regional women-on-boards "
    "platform in a co-located coordination unit. The Hub operated a shared candidate "
    "management system under a data-sharing protocol approved by the Portuguese Data "
    "Protection Authority. In its first year, the Hub processed 312 board appointment "
    "cases, of which 94% received a coordinated multi-agency response within 48 "
    "hours. Director satisfaction surveys completed by 180 newly appointed directors "
    "rated the coordination as helpful or very helpful in 86% of cases. The model was "
    "endorsed by the Portuguese Commission for Citizenship and Gender Equality as a "
    "national replication framework."
)
edited_hypothesis = (
    "States parties must ensure adequate cooperation mechanisms among all relevant "
    "authorities to support the appointment and retention of underrepresented "
    "directors on listed company boards, prioritising transparency and "
    "non-discrimination."
)
C4_SPECS.append(dict(
    source_id='ge_nli_006', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="violence_stereotypes -> leadership_participation. 'Multi-Agency Safeguarding Hub' -> 'Multi-Agency Board Diversity Hub'; 'municipal police, social services, health authority, public prosecution, women's shelter' -> 'municipal council, corporate registry, audit authority, listing supervisor, women-on-boards platform'; 'domestic violence cases' -> 'board appointment cases'; 'survivors' -> 'newly appointed directors'; 'protect and support victims of violence, prioritising their safety and human rights' -> 'support the appointment and retention of underrepresented directors on listed company boards, prioritising transparency and non-discrimination'.",
))

# 2. ge_nli_017 (entailment, violence_stereotypes -> equal_economy)
it = nli_by_id['ge_nli_017']
edited_premise = (
    "RheinFracht GmbH, a Frankfurt-based freight logistics company, updated its "
    "compensation code in 2022 following Germany's implementation of the pay-equity "
    "provisions of the EU Pay Transparency Directive. The code explicitly defined "
    "wage discrimination — including sustained unequal pay, opaque salary bands, and "
    "systematic underclassification — as a sanctionable offence and obligated the "
    "company to refer credible cases to the public labour inspectorate. Training on "
    "recognising and reporting wage discrimination was delivered to 280 supervisors "
    "and team leaders. In 2023, the company investigated four complaints of wage "
    "discrimination, dismissed two employees responsible, issued formal warnings in "
    "the remaining cases, and referred all four to the Frankfurt Labour Inspectorate. "
    "The updated code was endorsed by the works council as compliant with the German "
    "Equal Pay Act."
)
edited_hypothesis = (
    "States parties must criminalise intentional conduct that seriously impairs the "
    "economic position of a person through wage discrimination or pay-band "
    "manipulation."
)
C4_SPECS.append(dict(
    source_id='ge_nli_017', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="violence_stereotypes -> equal_economy. 'disciplinary code' -> 'compensation code'; 'psychological violence provisions of the Istanbul Convention' -> 'pay-equity provisions of the EU Pay Transparency Directive'; 'psychologically coercive conduct ... sustained threats, intimidation, systematic humiliation' -> 'wage discrimination ... sustained unequal pay, opaque salary bands, systematic underclassification'; 'public prosecutor' -> 'public labour inspectorate'; 'Prosecution Service' -> 'Labour Inspectorate'; 'Act on Violence Against Women' -> 'Equal Pay Act'; 'psychological integrity' -> 'economic position'; 'coercion or threats' -> 'wage discrimination or pay-band manipulation'.",
))

# 3. ge_nli_028 (neutral, violence_stereotypes -> mainstreaming_intersectionality)
it = nli_by_id['ge_nli_028']
edited_premise = (
    "TecnoBarcelona S.L., a Barcelona-based software development firm, updated its "
    "code of conduct and procurement policy in 2022 following Spain's reform of the "
    "Public Sector Procurement Act to include intersectional accessibility as a "
    "specific obligation under Article 172 ter, aligned with EU mainstreaming "
    "requirements. The company established an intersectional impact monitoring "
    "protocol for company-issued tools and platforms, training procurement and HR "
    "teams to identify patterns of repeated exclusion of marginalised user groups. In "
    "2023, TecnoBarcelona identified and investigated two cases of exclusionary "
    "design involving employees with intersecting disadvantages, referred both to the "
    "National Equality Agency, and supported affected employees through the "
    "rectification process. Both cases resulted in mandatory accessibility "
    "adjustments being issued within three months of the initial report."
)
edited_hypothesis = (
    "Employers must apply gender-mainstreaming principles to all internal policies, "
    "currently absent in approximately 16% of EU Member States."
)
C4_SPECS.append(dict(
    source_id='ge_nli_028', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="violence_stereotypes -> mainstreaming_intersectionality. 'digital security policy' -> 'procurement policy'; 'Criminal Code' -> 'Public Sector Procurement Act'; 'stalking' -> 'intersectional accessibility'; 'Istanbul Convention' -> 'EU mainstreaming'; 'digital harassment monitoring protocol' -> 'intersectional impact monitoring protocol'; 'cybersecurity' -> 'procurement'; 'repeated threatening or surveillance behaviour' -> 'repeated exclusion of marginalised user groups'; 'cases of stalking' -> 'cases of exclusionary design involving employees with intersecting disadvantages'; 'cybercrime unit' -> 'National Equality Agency'; 'criminal complaint process' -> 'rectification process'; 'restraining orders' -> 'mandatory accessibility adjustments'. Hypothesis: 'equal pay for equal work' / 'gender pay gap' -> 'gender-mainstreaming principles'.",
))

# 4. ge_nli_055 (entailment, leadership_participation -> equal_economy)
it = nli_by_id['ge_nli_055']
edited_premise = (
    "CelticSteel plc, a Dublin-listed precision engineering manufacturer, submitted "
    "its pay transparency compliance plan to the Irish Pay Equity Authority in March "
    "2023, committing to a 40\% reduction in the gender pay gap by 30 June 2026 under "
    "path (a) of the Pay Transparency Directive. Two new equal-pay audit cycles were "
    "completed in 2023, raising adjusted pay parity from 17\% gap to 33\% gap closure. "
    "An executive-level wage transparency target of 35% pay-band disclosure was set "
    "to sustain audit pipeline supply. A pay equity sub-committee was established to "
    "oversee transparency targets and report quarterly to the full board. By March "
    "2024, executive pay-band disclosure stood at 32%, ahead of schedule."
)
edited_hypothesis = (
    "Member States must ensure that listed companies achieve either a 40\% reduction "
    "in the gender pay gap or 33% pay-band transparency across all positions by "
    "30 June 2026."
)
C4_SPECS.append(dict(
    source_id='ge_nli_055', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="leadership_participation -> equal_economy. 'board diversity compliance plan' -> 'pay transparency compliance plan'; 'Irish Corporate Governance Authority' -> 'Irish Pay Equity Authority'; 'female non-executive representation' -> 'reduction in the gender pay gap'; 'Directive' -> 'Pay Transparency Directive'; 'female non-executive directors ... appointed' -> 'equal-pay audit cycles ... completed'; 'female non-executive representation from 17% to 33%' -> 'adjusted pay parity from 17% gap to 33% gap closure'; 'executive pipeline target ... director-minus-one level' -> 'executive-level wage transparency target ... pay-band disclosure'; 'board candidate supply' -> 'audit pipeline supply'; 'board effectiveness sub-committee ... diversity targets' -> 'pay equity sub-committee ... transparency targets'; 'female executive representation' -> 'executive pay-band disclosure'. Hypothesis transformed in parallel.",
))

# 5. ge_nli_080 (neutral, leadership_participation -> mainstreaming_intersectionality)
it = nli_by_id['ge_nli_080']
edited_premise = (
    "FarmaGroup S.p.A., a Milan-listed pharmaceutical manufacturer, launched a "
    "gender-mainstreaming renewal programme in 2022 to comply with the Gender "
    "Mainstreaming Directive. Following a rigorous external review process conducted "
    "by an intersectionality-aware consulting firm, three new gender impact "
    "assessment frameworks were adopted between March 2022 and June 2023. The "
    "frameworks raised intersectional coverage from 25% to 44%, exceeding the 40% "
    "threshold two years ahead of the June 2026 statutory deadline. The "
    "mainstreaming committee revised its programme assessment criteria to include "
    "explicit references to intersectional objectives. FarmaGroup published its "
    "gender-mainstreaming coverage data and assessment methodology in its 2023 annual "
    "sustainability report."
)
edited_hypothesis = (
    "EU funding must support the elimination of gender-blind programming and "
    "intersectional invisibility while ensuring access to gender-mainstreaming "
    "instruments."
)
C4_SPECS.append(dict(
    source_id='ge_nli_080', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="leadership_participation -> mainstreaming_intersectionality. 'board renewal programme' -> 'gender-mainstreaming renewal programme'; 'Women on Boards Directive' -> 'Gender Mainstreaming Directive'; 'gender-aware executive search firm' -> 'intersectionality-aware consulting firm'; 'female non-executive directors ... appointed' -> 'gender impact assessment frameworks ... adopted'; 'female non-executive board membership' -> 'intersectional coverage'; 'nomination committee ... candidate assessment criteria ... diversity objectives' -> 'mainstreaming committee ... programme assessment criteria ... intersectional objectives'; 'board gender composition data and appointment methodology' -> 'gender-mainstreaming coverage data and assessment methodology'; 'corporate governance report' -> 'sustainability report'. Hypothesis: 'female genital mutilation and child marriage ... sexual and reproductive health services' -> 'gender-blind programming and intersectional invisibility ... gender-mainstreaming instruments'.",
))

# 6. ge_nli_100 (entailment, leadership_participation -> funding_global_action)
it = nli_by_id['ge_nli_100']
edited_premise = (
    "FarmaGroup S.p.A., a Milan-listed pharmaceutical manufacturer, launched a "
    "GAP III-aligned external action programme in 2022 to comply with EU development "
    "cooperation requirements. Following a rigorous external partnership process "
    "conducted by a development-aware consulting firm, three new partner country "
    "engagements were established between March 2022 and June 2023. The engagements "
    "raised gender-tagged ODA from 25% to 44%, exceeding the 40% threshold two years "
    "ahead of the June 2026 GAP III evaluation deadline. The development cooperation "
    "committee revised its partner country assessment criteria to include explicit "
    "references to GAP III objectives. FarmaGroup published its gender-tagged ODA "
    "data and partnership methodology in its 2023 annual external action report."
)
edited_hypothesis = (
    "Partner-country authorities must ensure that EU-funded projects achieve at least "
    "40% gender-tagged ODA across external action portfolios by 30 June 2026."
)
C4_SPECS.append(dict(
    source_id='ge_nli_100', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="leadership_participation -> funding_global_action. 'board renewal programme ... Women on Boards Directive' -> 'GAP III-aligned external action programme ... EU development cooperation requirements'; 'executive search ... female non-executive directors appointed' -> 'partnership process ... partner country engagements established'; 'female non-executive board membership' -> 'gender-tagged ODA'; 'statutory deadline' -> 'GAP III evaluation deadline'; 'nomination committee ... candidate assessment ... diversity objectives' -> 'development cooperation committee ... partner country assessment ... GAP III objectives'; 'board gender composition ... appointment methodology' -> 'gender-tagged ODA data ... partnership methodology'; 'corporate governance report' -> 'external action report'. Hypothesis: 'Listed companies ... members of the underrepresented sex hold at least 40% of non-executive director positions' -> 'Partner-country authorities ensure ... 40% gender-tagged ODA across external action portfolios'.",
))

# 7. ge_nli_071 (entailment, equal_economy -> violence_stereotypes)
it = nli_by_id['ge_nli_071']
edited_premise = (
    "Cork City Council, Ireland, overhauled its safeguarding system in 2022 by "
    "replacing legacy seniority-based case triage with a survivor-centred risk "
    "assessment framework developed with the Irish Human Rights and Equality "
    "Commission. The new framework evaluated 48 case categories across six factors — "
    "lethality risk, coercive control, repeated victimisation, witness presence, "
    "perpetrator history, and child impact — without reference to gendered "
    "victim-blaming hierarchies. Following retriage, 23 cases were escalated, "
    "benefiting 67 survivors, 58 of whom were women. The Council set a target of 45% "
    "specialist-shelter referral coverage and reached 41% by December 2023, up from "
    "27% in 2020. The methodology was published as an open-source toolkit for other "
    "local authorities."
)
edited_hypothesis = (
    "States parties must adopt survivor-centred risk-assessment methods and promote "
    "specialist-shelter referral capacity to reduce repeat victimisation."
)
C4_SPECS.append(dict(
    source_id='ge_nli_071', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="equal_economy -> violence_stereotypes. 'grading system ... gender-neutral job evaluation framework' -> 'safeguarding system ... survivor-centred risk assessment framework'; 'job families' -> 'case categories'; 'skills, effort, responsibility, working conditions, decision-making authority, impact' -> 'lethality risk, coercive control, repeated victimisation, witness presence, perpetrator history, child impact'; 'gendered occupational hierarchies' -> 'gendered victim-blaming hierarchies'; 'roles ... elevated, benefiting employees' -> 'cases ... escalated, benefiting survivors'; 'female representation in senior management' -> 'specialist-shelter referral coverage'. Hypothesis: 'gender-neutral job evaluation methods ... gender-balanced representation in managerial positions ... occupational segregation' -> 'survivor-centred risk-assessment methods ... specialist-shelter referral capacity ... repeat victimisation'.",
))

# 8. ge_nli_037 (entailment, equal_economy -> leadership_participation)
it = nli_by_id['ge_nli_037']
edited_premise = (
    "The Malopolska Regional Education Authority in Kraków, Poland, introduced a "
    "mandatory board composition register for all 214 public schools under its "
    "jurisdiction in September 2022. Each school was required to publish anonymised "
    "governing-board gender ratios by role and seniority on its institutional "
    "website. The Authority established a dedicated board diversity complaint unit "
    "staffed by two corporate governance specialists, which processed 31 complaints "
    "in its first year and issued binding corrective orders in 18 cases. Training on "
    "the gender-balance principle was delivered to all 214 head teachers and school "
    "administrators. By December 2023, the average shortfall against the 40% "
    "non-executive target across the network had narrowed from 11.8 percentage points "
    "to 6.4 percentage points, verified by an independent audit commissioned by the "
    "Authority."
)
edited_hypothesis = (
    "Member States must take effective measures to enforce the legal principle of "
    "balanced board composition for the underrepresented sex and improve "
    "governance-data transparency at the national level."
)
C4_SPECS.append(dict(
    source_id='ge_nli_037', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="equal_economy -> leadership_participation. 'pay transparency register' -> 'board composition register'; 'salary ranges' -> 'governing-board gender ratios'; 'equal pay complaint unit ... labour law specialists' -> 'board diversity complaint unit ... corporate governance specialists'; 'equal pay principle' -> 'gender-balance principle'; 'gender pay gap ... 11.8% to 6.4%' -> 'shortfall against the 40% non-executive target ... 11.8 percentage points to 6.4 percentage points'. Hypothesis: 'equal pay for equal work ... pay transparency' -> 'balanced board composition for the underrepresented sex ... governance-data transparency'.",
))

# 9. ge_nli_014 (neutral, funding_global_action -> equal_economy)
it = nli_by_id['ge_nli_014']
edited_premise = (
    "EqualAid Belgium asbl, a Brussels-based international development NGO, "
    "facilitated a structured social-partner dialogue in 2021 to support the European "
    "Parliament's deliberations on endorsing the Pay Transparency Directive. The "
    "organisation convened four thematic hearings attended by 68 MEPs and 40 trade "
    "union and employers' organisations from EU Member States, producing 22 "
    "consolidated social-partner recommendations on Pay Transparency Directive "
    "implementation priorities. EqualAid published a policy brief comparing the new "
    "Directive's commitments with the prior Pay Equity Recommendation and "
    "identifying six areas requiring stronger oversight. The European Parliament "
    "adopted a resolution endorsing the Directive in March 2021, incorporating 14 of "
    "the 22 social-partner recommendations. EqualAid subsequently monitored and "
    "reported annually on Parliament's follow-up to the resolution."
)
edited_hypothesis = (
    "EU pay-transparency rules must support legislation requiring disclosure of all "
    "forms of wage discrimination and strengthen enforcement capacity through a "
    "worker-centred approach."
)
C4_SPECS.append(dict(
    source_id='ge_nli_014', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="funding_global_action -> equal_economy. 'civil society dialogue' -> 'social-partner dialogue'; 'GAP III' (×4) -> 'Pay Transparency Directive'; 'women's rights organisations from EU partner countries' -> 'trade union and employers' organisations from EU Member States'; 'civil society recommendations' -> 'social-partner recommendations'; 'GAP II' -> 'Pay Equity Recommendation'. Hypothesis: 'EU external action ... gender-based violence ... law enforcement ... victim-centred' -> 'EU pay-transparency rules ... wage discrimination ... enforcement ... worker-centred'.",
))

# 10. ge_nli_094 (entailment, funding_global_action -> mainstreaming_intersectionality)
it = nli_by_id['ge_nli_094']
edited_premise = (
    "TechPortugal Diversidade S.A., a Lisbon-based intersectional consulting firm, "
    "implemented a gender-mainstreaming-aligned internal programme across its three "
    "divisions in Lisbon, Porto, and Faro between 2021 and 2023. Each divisional "
    "programme integrated gender mainstreaming across all internal procedures, "
    "dedicated at least 25% of total HR budget to targeted intersectional equality "
    "actions, and included structured policy dialogue sessions with corporate "
    "leadership on gender-impact assessment reform. By 2023, the firm had trained "
    "420 internal gender focal points, co-drafted two corporate gender-mainstreaming "
    "strategies with senior management, and achieved a 15 percentage point increase "
    "in intersectional inclusion in targeted business units across the three "
    "divisions."
)
edited_hypothesis = (
    "Internal corporate policies must combine gender mainstreaming, targeted "
    "intersectional actions, and gender-impact assessment to accelerate progress "
    "towards organisational gender equality and intersectional inclusion goals."
)
C4_SPECS.append(dict(
    source_id='ge_nli_094', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="funding_global_action -> mainstreaming_intersectionality. 'TechPortugal Cooperação ... international development firm' -> 'TechPortugal Diversidade ... intersectional consulting firm'; 'GAP III-aligned external action programme in Mozambique, Cape Verde, São Tomé and Príncipe' -> 'gender-mainstreaming-aligned internal programme across its three divisions in Lisbon, Porto, Faro'; 'country programme ... technical assistance activities' -> 'divisional programme ... internal procedures'; 'targeted gender equality actions' -> 'targeted intersectional equality actions'; 'political dialogue sessions with national ministries on gender policy reform' -> 'policy dialogue sessions with corporate leadership on gender-impact assessment reform'; 'local gender focal points' -> 'internal gender focal points'; 'national gender equality strategies with partner governments' -> 'corporate gender-mainstreaming strategies with senior management'; 'women's participation in targeted digital economy sectors' -> 'intersectional inclusion in targeted business units'. Hypothesis: 'EU external action ... global gender equality and empowerment goals' -> 'Internal corporate policies ... organisational gender equality and intersectional inclusion goals'.",
))

# 11. ge_nli_040 (entailment, mainstreaming_intersectionality -> violence_stereotypes)
it = nli_by_id['ge_nli_040']
edited_premise = (
    "SaúdeTech Portugal Lda, a Lisbon-based health technology company, launched a "
    "Safety for Women programme in 2022 targeting rural communities in Alentejo and "
    "Trás-os-Montes. The programme trained 600 women in personal safety, online "
    "harassment awareness, and helpline access through 18 community health centres. "
    "A fast-track shelter-worker apprenticeship for 45 women from target communities "
    "resulted in 32 permanent placements at local women's shelters. A subsidised "
    "emergency phone scheme was provided to 200 low-income at-risk women for 12 "
    "months. By programme end, helpline awareness among participating women rose from "
    "28% to 79%, and the gap in protection-order issuance for rural cases within "
    "target municipalities narrowed by 11 percentage points."
)
edited_hypothesis = (
    "States and organisations must address structural barriers exposing women to "
    "gender-based violence, ensuring women's equal access to protection orders and "
    "specialist shelter services."
)
C4_SPECS.append(dict(
    source_id='ge_nli_040', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="mainstreaming_intersectionality -> violence_stereotypes. 'Digital Inclusion for Women' -> 'Safety for Women'; 'digital skills, internet safety, online health service access' -> 'personal safety, online harassment awareness, helpline access'; 'ICT apprenticeship ... permanent employment contracts' -> 'shelter-worker apprenticeship ... permanent placements at local women's shelters'; 'mobile internet access scheme' -> 'emergency phone scheme'; 'low-income women' -> 'low-income at-risk women'; 'internet usage' -> 'helpline awareness'; 'gender gap in ICT employment' -> 'gap in protection-order issuance for rural cases'. Hypothesis: 'digital gender divide ... women's equal access to digital technologies and ICT career opportunities' -> 'gender-based violence ... women's equal access to protection orders and specialist shelter services'.",
))

# 12. ge_nli_002 (neutral, mainstreaming_intersectionality -> funding_global_action)
it = nli_by_id['ge_nli_002']
edited_premise = (
    "Rheinkapital AG, a Frankfurt-based asset management firm, integrated a "
    "GAP III-aligned external-action methodology into all five of its EU-co-funded "
    "development cooperation programmes in 2022. Each programme underwent a partner "
    "country assessment prior to disbursement conducted by an external development "
    "specialist. The firm appointed development cooperation focal points in each of "
    "its three regional desks and introduced mandatory gender-tagged ODA reporting "
    "for all partner-country recipients of EU external action funds. Programme "
    "agreements above €50,000 were subject to a gender-action-plan clause requiring "
    "implementing partners to demonstrate active GAP III alignment. By the end of "
    "the financial year, 100% of EU-funded programmes had been reviewed and adjusted "
    "under the framework, and gender-tagged ODA outcome data was published in "
    "Rheinkapital's annual external action report."
)
edited_hypothesis = (
    "States parties must ensure that EU external-action programmes apply GAP III "
    "alignment and gender-tagged ODA reporting in partner countries."
)
C4_SPECS.append(dict(
    source_id='ge_nli_002', label_original=it['pillar_premise'],
    original_input=nli_input(it),
    edited_input=f"PREMISE: {edited_premise}\n\nHYPOTHESIS: {edited_hypothesis}",
    edit_note_target="mainstreaming_intersectionality -> funding_global_action. 'gender mainstreaming methodology' -> 'GAP III-aligned external-action methodology'; 'investment programmes' -> 'development cooperation programmes'; 'gender impact assessment ... external equality specialist' -> 'partner country assessment ... external development specialist'; 'gender equality coordinators ... investment divisions' -> 'development cooperation focal points ... regional desks'; 'gender-disaggregated reporting ... portfolio companies receiving EU structural funds' -> 'gender-tagged ODA reporting ... partner-country recipients of EU external action funds'; 'procurement contracts ... gender-responsive clause ... suppliers ... active equal-opportunity policies' -> 'programme agreements ... gender-action-plan clause ... implementing partners ... active GAP III alignment'; 'gender-disaggregated outcome data ... sustainability report' -> 'gender-tagged ODA outcome data ... external action report'. Hypothesis: 'criminalise intentional conduct ... psychological integrity ... coercion or threats' -> 'ensure ... EU external-action programmes apply GAP III alignment and gender-tagged ODA reporting in partner countries'.",
))

C4_RECORDS = [
    make("C4", "GE-NLI", s['source_id'], s['label_original'],
         s['original_input'], s['edited_input'], NOTE_C4,
         s['edit_note_target'], expected_flip=True)
    for s in C4_SPECS
]
assert len(C4_RECORDS) == 12


# ===========================================================================
# Compose final file
# ===========================================================================
ALL_RECORDS = C1_RECORDS + C2_RECORDS + C3_RECORDS + C4_RECORDS
assert len(ALL_RECORDS) == 48

# Sanity: no empty edited_input
empties = [r['pair_id'] for r in ALL_RECORDS if not r.get('edited_input', '').strip()]
assert not empties, f"empties: {empties}"

OUT_PATH = './explainability_gui/counterfactual_pairs.jsonl'
with open(OUT_PATH, 'w') as f:
    for r in ALL_RECORDS:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')

print(f"Wrote {len(ALL_RECORDS)} records to {OUT_PATH}")

# Quick stats
from collections import Counter
print("\nBy axis:", Counter(r['axis'] for r in ALL_RECORDS))
print("By axis × pillar:")
for axis in ['C1','C2','C3','C4']:
    items = [r for r in ALL_RECORDS if r['axis'] == axis]
    pc = Counter(r['label_original'] for r in items)
    print(f"  {axis}: {dict(pc)}")
print("\nempty edited_input count:",
      sum(1 for r in ALL_RECORDS if not r.get('edited_input', '').strip()))
print("\nFlip distribution:")
for axis in ['C1','C2','C3','C4']:
    items = [r for r in ALL_RECORDS if r['axis'] == axis]
    fc = Counter(r['expected_flip'] for r in items)
    print(f"  {axis}: {dict(fc)}")