"""
GE-NEXT v3 — legend-favoring "all-plausible" dataset.

Design difference from v1 / v2:

  All four options are framed as substantive-compliance actions. They share the
  same register, the same regulatory vocabulary density, the same protagonist
  framing, and a comparable length. Surface lexical cues are equalised: every
  option cites at least one instrument or uses regulatory-pillar vocabulary,
  so the model cannot solve the task by spotting which option "looks like the
  regulatory one." Discrimination has to come from decision-pattern matching.

Defect taxonomy for the three distractors:

  partial_scope            — addresses one dimension of a multi-dimensional gap
                              but leaves the harder dimension unaddressed.
                              (Fixes the pay outcome without fixing the
                              job-grading methodology that produces the pay
                              outcome; fixes board composition without fixing
                              the executive committee where actual power
                              sits.) This is the legend pattern that
                              specifically trains against partial remediation.

  wrong_anchor             — cites a real, topically adjacent regulation that
                              does not actually cover the situation. Looks
                              authoritative on a surface read. The legend
                              pattern trains for instrument-precise grounding;
                              the regulation-tuned pattern trains for
                              regulatory-density and may not discriminate.

  procedural_substitution  — substitutes a documented review process, policy
                              charter, or governance step for a substantive
                              remediation action. Stops at the "design" beat
                              of the legend four-beat arc without crossing
                              into "implement" and "measure". This is the
                              most legend-discriminating defect because it
                              superficially looks like the substantive option
                              — it has documentation, governance, instrument
                              citation — but it does not close the loop.

The defect taxonomy maps onto the failure modes the legends are explicitly
constructed AGAINST. Every training legend in our corpus closes the full
identify -> design -> implement -> measure -> cite-instrument arc. A
legend-tuned model that has internalised the arc should prefer options that
close the loop. A regulation-tuned model trained on raw regulatory prose has
no signal for that decision pattern and will rely on surface regulatory
density, which is equalised across the four options.

Pillar distribution: 15 per pillar x 5 pillars = 75 items.
ID continuation: ge_next_<abbr>_101..115 per pillar (clear v3 range).
Gold-position: forced uniform — 19/19/19/18 across A/B/C/D, shuffled seed 44.
"""

import json
import random
from collections import Counter
from pathlib import Path

random.seed(44)

OUT_DIR = Path("./benchmark/task_pool/ge_next/helpers/v3")
OUT_DIR.mkdir(parents=True, exist_ok=True)


RAW_ITEMS = [

# =============================================================================
# PILLAR 1 - equal_economy (n=15)
# =============================================================================

{
"pillar": "equal_economy",
"vignette": "Carla Bianchi, Head of People at a Bologna-based engineering firm with 510 employees, has completed the firm's Pay Transparency Directive readiness audit. The audit reveals two intertwined patterns: a 9% unexplained gender pay gap concentrated in the operations division, and an underlying job-grading methodology in which the operations division's female-dominated coordination roles are systematically classified one band below the male-dominated technical roles they support. Carla must propose a remediation plan to the board.",
"gold": "Re-evaluate the operations division's job-grading methodology with a documented gender-neutral job-evaluation framework, regrade the affected coordination roles with retroactive pay adjustment for the past 24 months, and integrate the regraded methodology into the firm's joint pay assessment under Article 10 of Directive (EU) 2023/970.",
"partial_scope": "Build a documented 24-month banded remediation plan with quarterly salary adjustments for the affected coordination roles in line with the Pay Transparency Directive's reporting obligations, leaving the underlying job-grading methodology unchanged to preserve continuity of classification across the firm.",
"wrong_anchor": "Adopt a documented remediation plan with retroactive pay adjustment in alignment with Article 11 of the Work-Life Balance Directive (EU) 2019/1158 prohibiting detriment based on the exercise of leave rights, and integrate the remediation into the firm's annual sustainability disclosure.",
"procedural_substitution": "Introduce a documented joint-pay-assessment governance committee chaired by the head of HR with works-council representation, tasked under Article 10 of Directive (EU) 2023/970 with reviewing the operations-division pay gap and recommending corrective measures within 18 months.",
},

{
"pillar": "equal_economy",
"vignette": "Henrik Lindgren, Compensation Director at a Stockholm-based bank with 1,200 employees, faces a parental-leave issue: women returning from maternity leave are reassigned to lower-revenue client portfolios, and bonus pools for those portfolios are 38% smaller. The raw pay gap of 4.2% falls below the Pay Transparency Directive's 5% reporting threshold, masking the underlying portfolio-reassignment pattern.",
"gold": "Address the portfolio-reassignment pattern as detriment under Article 12 of the Work-Life Balance Directive (EU) 2019/1158, remediate both the portfolio assignments and the consequent bonus differentials with retroactive correction over the prior 24 months, and integrate portfolio-allocation oversight into the firm's returners' protection protocol.",
"partial_scope": "Remediate the bonus differentials for the affected returners with a one-off corrective top-up calibrated to the historical portfolio-revenue gap, and document the rationale in the firm's pay-transparency working papers under Directive (EU) 2023/970.",
"wrong_anchor": "Conduct a voluntary joint pay assessment under Article 10 of Directive (EU) 2023/970 despite the sub-threshold raw gap, document the portfolio-reassignment pattern, and remediate the bonus differentials in line with the Pay Transparency Directive's reporting obligations.",
"procedural_substitution": "Establish a documented returners' protection review committee chaired by the head of People with quarterly reporting to the executive committee, tasked with reviewing portfolio assignments of returning employees against the Work-Life Balance Directive's anti-detriment provisions.",
},

{
"pillar": "equal_economy",
"vignette": "Aleksandra Nowak, HR Director at a Warsaw-based construction conglomerate with 2,800 employees, identifies that the group's sub-contractor selection criteria allocate 70% of weighting to lowest-bid pricing, producing wage suppression at sub-contractor level — disproportionately affecting women cleaners and canteen staff who form 84% of the affected subcontracted workforce.",
"gold": "Restructure the sub-contractor selection framework to incorporate documented decent-work and equal-pay-for-work-of-equal-value criteria — including living-wage thresholds and gender-pay-gap reporting at sub-contractor level — in line with the value-chain provisions of Directive (EU) 2024/1760 (CSDDD) and the equal-pay principle of Directive (EU) 2023/970.",
"partial_scope": "Tighten the firm's existing sub-contractor selection criteria by requiring all sub-contractors to certify compliance with the equal-pay-for-work-of-equal-value principle of Article 4 of Directive (EU) 2023/970 in their offer documentation.",
"wrong_anchor": "Restructure the sub-contractor selection framework to incorporate documented decent-work and gender-pay-gap reporting criteria in alignment with the value-chain reporting requirements of Directive (EU) 2022/2464 (CSRD) and the firm's broader ESRS-aligned sustainability disclosure.",
"procedural_substitution": "Adopt a documented sub-contractor governance charter requiring tier-1 sub-contractors to undergo annual independent decent-work audits, with audit findings reviewed by the firm's vendor-management committee against CSDDD-aligned criteria.",
},

{
"pillar": "equal_economy",
"vignette": "Sara Kjær, People Operations Lead at a Copenhagen-based fintech with 180 employees, faces a complaint that the firm's algorithmic recruitment vendor encodes a 22% under-selection of female candidates for senior engineering roles. The procurement contract includes no fairness-audit clause. The AI Act risk-classification deadline approaches.",
"gold": "Suspend the algorithmic recruitment system pending a documented fundamental-rights and bias impact assessment under Article 27 of Regulation (EU) 2024/1689 (the AI Act, classifying recruitment systems as high-risk under Annex III), renegotiate the vendor contract to include audit rights and bias-mitigation obligations, and document the assessment outcomes before resuming use.",
"partial_scope": "Continue the algorithmic recruitment system in parallel with human-led shortlisting for senior engineering roles, document the dual-track outcomes for the next two hiring cycles, and align the documentation with the AI Act's high-risk-system transparency obligations.",
"wrong_anchor": "Conduct a documented Data Protection Impact Assessment under Article 35 GDPR for the algorithmic recruitment system, renegotiate the vendor contract to include audit rights, and document the assessment outcomes before resuming use.",
"procedural_substitution": "Adopt a documented AI-recruitment governance framework requiring fundamental-rights and bias review by an internal cross-functional committee for all high-risk AI systems used in HR, with the recruitment system as the first scoped system under the framework.",
},

{
"pillar": "equal_economy",
"vignette": "Andreas Sørensen, Head of Reward at a Bergen-based offshore-services firm with 740 employees, finds that the firm's 28-on / 28-off offshore-rotation pattern is incompatible with shared care responsibilities; 11 women have rotated off offshore roles in 18 months citing schedule incompatibility, and offshore-pay premiums are 42% above onshore equivalents — a structural pay gap that compounds the pattern.",
"gold": "Pilot a documented split-rotation pattern (14 on / 14 off) for offshore roles where operationally viable, ring-fence offshore-equivalent pay premiums for split-rotation participants in line with Article 9 of the Work-Life Balance Directive (EU) 2019/1158 (right to request flexible-working arrangements) and the equal-pay principle of Article 157 TFEU, and document the trial methodology and outcomes.",
"partial_scope": "Introduce a documented right-to-request split-rotation arrangement for offshore workers in line with Article 9 of the Work-Life Balance Directive (EU) 2019/1158, with each request evaluated on operational feasibility by the offshore operations director.",
"wrong_anchor": "Pilot a documented split-rotation pattern (14 on / 14 off) for offshore roles with offshore-equivalent pay premiums for participants, in line with Article 4 of Directive (EU) 2023/970 on the equal-pay-for-work-of-equal-value principle, and document the trial methodology.",
"procedural_substitution": "Convene a documented joint working group with the works council and offshore-supervisor representation, tasked with developing operational-feasibility criteria for offshore split-rotation arrangements aligned with the Work-Life Balance Directive, with recommendations due in 12 months.",
},

{
"pillar": "equal_economy",
"vignette": "Réka Tóth, HR Manager at a Budapest-based media group with 670 employees, finds that the group's freelance pool is bimodal: men get 71% of high-paying long-form contracts, women get 78% of low-paying short-form work. The freelance pool falls outside the Pay Transparency Directive's employee scope but inside the CSRD value-chain reporting boundary.",
"gold": "Establish a documented gender-neutral commissioning rubric tying contract type to deliverable specification rather than commissioner discretion, audit the past 24 months of commissioning decisions for gender disparity and remediate identified gaps through targeted commissioning, and disclose the rubric and outcomes under the group's CSRD value-chain reporting in alignment with the Strategy's mainstreaming approach.",
"partial_scope": "Introduce a documented gender-neutral commissioning rubric for new freelance engagements tying contract type to deliverable specification, and disclose the rubric under the group's CSRD value-chain reporting in alignment with the Strategy's mainstreaming approach.",
"wrong_anchor": "Establish a documented gender-neutral commissioning rubric for freelance engagements, audit the past 24 months of commissioning decisions for gender disparity, and remediate identified gaps under the equal-pay principle of Article 4 of Directive (EU) 2023/970.",
"procedural_substitution": "Adopt a documented freelance-commissioning governance charter requiring editors to submit annual commissioning-pattern reviews to the head of editorial, with gender disaggregation as a standing item in the review template under the group's CSRD value-chain reporting framework.",
},

{
"pillar": "equal_economy",
"vignette": "Lukas Brandt, HR Director at a Munich-based aerospace supplier with 920 employees, identifies two compounding issues: the firm's apprenticeship programme has admitted only 12% women over five cohorts because applications require a baseline physics qualification documented as a barrier to female applicants, and two pregnant apprentices have left citing inflexible workshop schedules.",
"gold": "Replace the physics-qualification screening with a competence-based aptitude assessment validated for indirect-discrimination risk, introduce documented flexible-scheduling protections for pregnant apprentices in line with Council Directive 92/85/EEC and the Work-Life Balance Directive (EU) 2019/1158, and report the redesigned programme's gender-balance trajectory in the firm's annual sustainability disclosure.",
"partial_scope": "Replace the physics-qualification screening with a competence-based aptitude assessment validated for indirect-discrimination risk, and report the redesigned programme's gender-balance trajectory in the firm's annual sustainability disclosure.",
"wrong_anchor": "Replace the physics-qualification screening with a competence-based aptitude assessment validated for indirect-discrimination risk in line with Article 4 of Directive 2006/54/EC, introduce documented flexible-scheduling protections for pregnant apprentices in line with Article 4 of Directive 2006/54/EC, and report the redesigned programme's gender-balance trajectory annually.",
"procedural_substitution": "Adopt a documented apprenticeship-equity review framework with annual screening-criteria audit and pregnancy-accommodation case review, conducted by a cross-functional committee chaired by the head of People with reporting to the firm's CSR committee.",
},

{
"pillar": "equal_economy",
"vignette": "Inês Carvalho, People Lead at a Lisbon-based hospitality group with 1,800 employees across 12 properties, identifies that tip arrangements vary across properties: at six properties tips are pooled, at six others tips accrue individually. Female-dominated housekeeping and back-of-house staff at individual-tip properties earn 22% less than peers at pooled-tip properties for equivalent hours.",
"gold": "Bring tip arrangements within the scope of the group's pay-structures review under Article 4 of Directive (EU) 2023/970, harmonise tip-pooling rules across properties with documented gender-impact analysis, and integrate the harmonised arrangement into the group's collective bargaining negotiations as a non-discretionary element of remuneration.",
"partial_scope": "Mandate tip-pooling as the standard arrangement across all twelve properties effective from the next fiscal year, in alignment with the equal-pay principle of Article 4 of Directive (EU) 2023/970, with general managers responsible for implementation.",
"wrong_anchor": "Harmonise tip-pooling rules across all twelve properties with documented gender-impact analysis, in alignment with the gender-mainstreaming provisions of the Strategy and the Work-Life Balance Directive's broader commitment to equitable treatment.",
"procedural_substitution": "Establish a documented cross-property tip-arrangements review committee with works-council representation, tasked under Article 4 of Directive (EU) 2023/970 with reviewing tip arrangements property-by-property and recommending harmonisation measures within 18 months.",
},

{
"pillar": "equal_economy",
"vignette": "Caterina Russo, HR Director at a Milan-based luxury-goods manufacturer with 1,100 employees, identifies that the firm's piece-rate compensation system in the leather-goods division — used by 280 stitchers and finishers, 92% women — produces hourly earnings 18% below the firm's male-dominated cutting and quality-control departments doing comparably skilled work.",
"gold": "Re-evaluate the piece-rate system using a documented gender-neutral job-evaluation methodology that establishes equivalence of skill, effort, responsibility and working conditions across the leather-goods, cutting and quality-control departments, regrade the affected roles with retroactive adjustment in line with Article 4 of Directive (EU) 2023/970, and negotiate the methodology jointly with the works council.",
"partial_scope": "Adjust the leather-goods division piece-rate to close the 18% hourly-earnings gap with the firm's male-dominated cutting and quality-control departments, in line with the equal-pay-for-work-of-equal-value principle of Article 4 of Directive (EU) 2023/970, and negotiate the adjustment with the works council.",
"wrong_anchor": "Re-evaluate the piece-rate system using a documented gender-neutral job-evaluation methodology and regrade the affected roles in alignment with the equal-treatment principle of Article 14 of Directive 2006/54/EC, and integrate the methodology into the firm's annual sustainability disclosure.",
"procedural_substitution": "Convene a documented job-evaluation working group with the works council, tasked under Article 4 of Directive (EU) 2023/970 with developing a gender-neutral job-evaluation methodology for the leather-goods, cutting and quality-control departments with recommendations due in 12 months.",
},

{
"pillar": "equal_economy",
"vignette": "Diogo Almeida, Head of People at a Porto-based logistics firm with 540 employees, finds that the firm's standard contract includes an unbroken-continuity-of-service clause for share-plan eligibility, with the consequence that 91% of employees ineligible for the share plan after parental leave are women. The next share-plan grant cycle is in four months.",
"gold": "Amend the standard contract's continuity-of-service clause to expressly preserve share-plan eligibility through periods of statutory leave under Article 12 of the Work-Life Balance Directive (EU) 2019/1158 (protection from less favourable treatment), grant catch-up share-plan participation to affected returners over the past 24 months, and disclose the change in the firm's next annual remuneration report.",
"partial_scope": "Amend the standard contract's continuity-of-service clause to expressly preserve share-plan eligibility through periods of statutory leave under Article 12 of the Work-Life Balance Directive (EU) 2019/1158, with the amendment taking effect from the next share-plan grant cycle.",
"wrong_anchor": "Amend the standard contract's continuity-of-service clause to expressly preserve share-plan eligibility through periods of statutory leave in alignment with Article 4 of Directive (EU) 2023/970 on the equal-pay-for-work-of-equal-value principle, and grant catch-up share-plan participation to affected returners.",
"procedural_substitution": "Adopt a documented returner-protection governance protocol requiring the People function to review share-plan eligibility decisions for employees returning from statutory leave, with quarterly reporting to the remuneration committee under the Work-Life Balance Directive's anti-detriment provisions.",
},

{
"pillar": "equal_economy",
"vignette": "Marta Schneider, HR Director at a Vienna-based pharma SME with 240 employees, finds that the firm's overtime-pay policy excludes part-time workers (78% women) even when their hours exceed contracted thresholds — an arrangement unchanged since the firm was founded. Two affected employees have filed equal-treatment complaints with the national equality body.",
"gold": "Extend overtime-pay eligibility to all workers exceeding contracted hours regardless of contract type, in line with Clause 4 of the Part-Time Work Directive 97/81/EC (principle of non-discrimination) and the equal-pay principle of Article 157 TFEU, and back-pay affected employees over the past 24 months with documented case-by-case reconciliation.",
"partial_scope": "Extend overtime-pay eligibility prospectively to all part-time workers exceeding contracted hours, in line with Clause 4 of the Part-Time Work Directive 97/81/EC, and disclose the change in the firm's annual sustainability disclosure.",
"wrong_anchor": "Extend overtime-pay eligibility to all workers exceeding contracted hours regardless of contract type, in alignment with Article 4 of Directive (EU) 2023/970 on the equal-pay-for-work-of-equal-value principle, and back-pay affected employees over the past 24 months.",
"procedural_substitution": "Adopt a documented overtime-pay governance protocol requiring quarterly review of overtime-pay allocation by contract type, with works-council reporting under the Part-Time Work Directive's non-discrimination principle, and submit findings to the executive committee for corrective recommendations.",
},

{
"pillar": "equal_economy",
"vignette": "Olivia Andersen, People Director at an Oslo fintech with 180 employees, identifies that the firm's standard contract specifies a 'preferred availability' clause that disproportionately disadvantages caregivers (predominantly women), and that exit data show 14 women leaving in the past 18 months citing schedule rigidity. The firm has just received its first CSRD-aligned ESRS S1 audit.",
"gold": "Remove the 'preferred availability' clause from standard contracts, introduce a documented right to request flexible-working arrangements aligned with Article 9 of the Work-Life Balance Directive (EU) 2019/1158, offer existing staff a 90-day window to amend their contracts, and integrate flexible-working-arrangement uptake and gender breakdown into the firm's ESRS S1 disclosure.",
"partial_scope": "Remove the 'preferred availability' clause from standard contracts and disclose the change in the firm's ESRS S1 disclosure under the CSRD framework, applying the change to all new hires from the date of the amendment.",
"wrong_anchor": "Remove the 'preferred availability' clause from standard contracts in alignment with the anti-detriment provisions of Article 12 of the Work-Life Balance Directive (EU) 2019/1158, offer existing staff a 90-day window to amend their contracts, and integrate the change into the firm's ESRS S1 disclosure.",
"procedural_substitution": "Convene a documented working group with employee representatives to review the firm's flexible-working framework against Article 9 of the Work-Life Balance Directive (EU) 2019/1158, with recommendations on contract-clause amendments due within 12 months and reporting under the firm's ESRS S1 framework.",
},

{
"pillar": "equal_economy",
"vignette": "Klaus Berger, Head of Total Rewards at a Frankfurt-based asset manager with 880 employees, finds that the firm's discretionary year-end equity grants have been distributed 65/35 in favour of men over the past three cycles despite comparable role distributions, and that no allocation criteria are currently documented. The Pay Transparency Directive readiness deadline approaches.",
"gold": "Issue documented equity-allocation criteria tied to role, tenure and performance, audit and remediate the past three years of grants for unexplained gender variance with corrective top-up to under-allocated employees, and integrate equity-grant distribution by gender into the firm's joint pay assessment under Article 10 of Directive (EU) 2023/970.",
"partial_scope": "Issue documented equity-allocation criteria tied to role, tenure and performance, applicable to the next equity-grant cycle and beyond, and integrate equity-grant distribution by gender into the firm's joint pay assessment under Article 10 of Directive (EU) 2023/970.",
"wrong_anchor": "Issue documented equity-allocation criteria tied to role, tenure and performance, audit and remediate the past three years of grants for unexplained gender variance with corrective top-up to under-allocated employees, in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters.",
"procedural_substitution": "Adopt a documented equity-grant governance charter requiring the remuneration committee to review annual grant distributions for gender variance under Article 10 of Directive (EU) 2023/970, with works-council input on grant-criteria methodology and quarterly reporting to the executive committee.",
},

{
"pillar": "equal_economy",
"vignette": "Eleni Vasilakis, HR Lead at a Thessaloniki-based shipping firm with 510 employees, finds that the annual sales-commission scheme disproportionately rewards account types historically held by male sales staff, and that the 70/30 commission split has not been reviewed in eight years despite shifts in team gender composition.",
"gold": "Recalibrate the commission scheme on the basis of a documented account-difficulty rubric ensuring equivalent-effort accounts attract equivalent commission rates, audit and remediate past commission outcomes for unexplained gender variance, and integrate the recalibrated scheme into the firm's joint pay assessment process under Article 10 of Directive (EU) 2023/970.",
"partial_scope": "Recalibrate the commission scheme on the basis of a documented account-difficulty rubric ensuring equivalent-effort accounts attract equivalent commission rates, effective from the next commission cycle, with disclosure under Article 10 of Directive (EU) 2023/970.",
"wrong_anchor": "Recalibrate the commission scheme on the basis of a documented account-difficulty rubric and audit past commission outcomes for unexplained gender variance, in alignment with Article 14 of Directive 2006/54/EC on equal treatment, and disclose the recalibrated scheme in the firm's annual sustainability disclosure.",
"procedural_substitution": "Convene a documented commission-design working group with sales-team and works-council representation, tasked under Article 10 of Directive (EU) 2023/970 with reviewing commission-allocation outcomes for gender variance and recommending recalibration measures within 12 months.",
},

{
"pillar": "equal_economy",
"vignette": "Sigrid Aas, HR Director at an Oslo professional-services firm with 600 employees, learns that female partners are 24% of the partnership but receive 12% of public-speaking invitations the firm allocates annually — a visibility gap with downstream effects on partner-track progression for the firm's senior associates.",
"gold": "Establish a documented public-speaking-allocation process tied to expertise areas with at least 40% of speaking slots ring-fenced for partners of the under-represented sex, audit the past two years of speaking-slot allocation for unexplained variance and rebalance, and integrate visibility-allocation outcomes into the partnership-governance annual review under the Strategy's leadership-participation mainstreaming framework.",
"partial_scope": "Establish a documented public-speaking-allocation process tied to expertise areas with at least 40% of speaking slots ring-fenced for partners of the under-represented sex, effective from the next speaking-allocation cycle, in alignment with the Strategy's leadership-participation framework.",
"wrong_anchor": "Establish a documented public-speaking-allocation process with at least 40% of speaking slots ring-fenced for partners of the under-represented sex, in alignment with Article 5 of Directive (EU) 2022/2381 on gender-balanced selection of directors, and rebalance past allocations.",
"procedural_substitution": "Adopt a documented partnership-visibility governance charter requiring the firm's marketing function to report annual speaking-slot allocation by partner gender to the partnership board, with corrective recommendations integrated into the firm's annual people-strategy review.",
},

# =============================================================================
# PILLAR 2 - leadership_participation (n=15)
# =============================================================================

{
"pillar": "leadership_participation",
"vignette": "Marta Sánchez, Head of Corporate Governance at a Barcelona-listed industrials firm, has reviewed the board composition ahead of the 2026 Women on Boards Directive deadline. Of nine non-executive directors, two are women — 22% representation, well short of the 40% target. The chair has proposed appointing two female non-executive directors over the next 18 months.",
"gold": "Build a documented board-renewal plan bringing non-executive director composition to at least 40% of the under-represented sex by 30 June 2026 in line with Article 5 of Directive (EU) 2022/2381, with a documented gender-neutral director-skills matrix and gender-balanced shortlist requirements under Article 4 governing the appointment process, and annual disclosure of progress in the corporate governance statement.",
"partial_scope": "Appoint two female non-executive directors over the next 18 months to reach the 40% non-executive director target ahead of the 30 June 2026 deadline of Directive (EU) 2022/2381, with the appointments disclosed in the corporate governance statement.",
"wrong_anchor": "Build a documented board-renewal plan bringing non-executive director composition to at least 40% of the under-represented sex by 30 June 2026 in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters, with the renewal plan disclosed in the corporate governance statement.",
"procedural_substitution": "Adopt a documented nominations-committee charter requiring gender-balanced shortlists and competence-based selection criteria for all director appointments under Article 5 of Directive (EU) 2022/2381, with the charter approved at the next AGM and progress reporting in the corporate governance statement.",
},

{
"pillar": "leadership_participation",
"vignette": "Sigrid Lindqvist, Company Secretary at a Stockholm-listed multinational holding (board 12 members, 33% female non-executive directors), is preparing the firm's response to the planned merger with a smaller listed firm whose board is 8% female. The merger draft term sheet preserves the smaller firm's board representation as a 'cultural continuity' clause; institutional shareholders representing 18% of equity have flagged concerns.",
"gold": "Renegotiate the merger term sheet to require the combined-entity board to reach 40% representation of the under-represented sex by 30 June 2026 in line with Article 5 of Directive (EU) 2022/2381, replace the 'cultural continuity' clause with a documented integration-plan committee tasked with combined-entity director recruitment under Article 4 (gender-neutral selection criteria), and disclose the trajectory to the merger-approval shareholder meeting.",
"partial_scope": "Renegotiate the merger term sheet to require the combined-entity board to reach 40% representation of the under-represented sex by 30 June 2026 in line with Article 5 of Directive (EU) 2022/2381, with the existing nominations committees of both firms retained pending the natural integration cycle.",
"wrong_anchor": "Renegotiate the merger term sheet to require the combined-entity board to reach 40% representation of the under-represented sex by 30 June 2026 in alignment with Article 14 of Directive 2006/54/EC on equal treatment, and replace the 'cultural continuity' clause with an integration-plan committee tasked with combined-entity director recruitment.",
"procedural_substitution": "Establish a documented merger-integration nominations sub-committee co-chaired by the chairs of both nominations committees, tasked under Article 4 of Directive (EU) 2022/2381 with developing gender-neutral selection criteria for combined-entity director appointments with recommendations due ahead of the integration date.",
},

{
"pillar": "leadership_participation",
"vignette": "Aurélie Fontaine, Chief of Staff at a Paris-listed insurance group, finds that the nominations committee has interpreted Article 5 of the Women on Boards Directive as permitting a 'qualifications equivalence' override that has been used to justify three consecutive male appointments since 2023. The CEO has signalled support for a fourth such appointment at the next AGM.",
"gold": "Reject the proposed fourth appointment, issue an updated nominations-committee charter clarifying that Article 5(2) of Directive (EU) 2022/2381 requires equal-qualification candidates of the under-represented sex to be given priority, document the appointment rationale for every director nomination going forward as required by Article 5(4), and disclose the corrected interpretation in the corporate governance statement.",
"partial_scope": "Reject the proposed fourth appointment and document the appointment rationale for every director nomination going forward as required by Article 5(4) of Directive (EU) 2022/2381, with disclosure in the corporate governance statement.",
"wrong_anchor": "Reject the proposed fourth appointment and issue an updated nominations-committee charter clarifying that gender-balanced shortlists are required for all director appointments in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters.",
"procedural_substitution": "Adopt a documented nominations-committee charter governing the application of Article 5 of Directive (EU) 2022/2381, with mandatory legal-opinion sign-off for any 'qualifications equivalence' override and quarterly reporting to the corporate governance committee.",
},

{
"pillar": "leadership_participation",
"vignette": "Mohammad Al-Rashid, Head of Talent at a Dublin-listed pharmaceutical group, finds that the main board has reached 41% female representation but the executive committee remains 11% female (1 of 9), and the natural successor pool — 28 director-1 leaders — is 14% female. A shareholder ESG-engagement letter has cited the inversion as cosmetic compliance.",
"gold": "Establish a documented executive-committee succession plan targeting at least 40% representation of the under-represented sex by 2028 mirroring the Women on Boards Directive trajectory at executive level, implement a structured pipeline-development programme for the senior women in the director-1 cohort, and disclose succession-pipeline gender data annually under ESRS S1 of the firm's CSRD report.",
"partial_scope": "Commit to filling the next two executive-committee vacancies with female candidates as natural attrition occurs, document the commitment in the firm's corporate governance statement, and disclose the executive-committee composition under ESRS S1 of the firm's CSRD report.",
"wrong_anchor": "Establish a documented executive-committee succession plan targeting at least 40% representation of the under-represented sex by 2028 in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies, and disclose succession-pipeline gender data annually.",
"procedural_substitution": "Adopt a documented executive-committee succession-planning governance protocol requiring annual review of pipeline composition by gender, with the human-resources committee of the board tasked with oversight and quarterly reporting to the main board under ESRS S1 of the firm's CSRD report.",
},

{
"pillar": "leadership_participation",
"vignette": "Tomáš Procházka, Head of Group Governance at a Prague-listed industrial group, observes that the parent board's non-executive director composition is at 38% (one short of the directive target, one term expiring in 2026), but the group's three operating-subsidiary boards (through which operational power flows) have between 0 and 18% female non-executive directors. The directive applies to the listed parent only; the CSRD report consolidates governance disclosure across the structure.",
"gold": "Extend the spirit of Directive (EU) 2022/2381 voluntarily to the operating-subsidiary boards by adopting documented gender-balance targets at subsidiary level mirroring the 40% non-executive-director target, replace the upcoming parent-board vacancy with a director of the under-represented sex to clear the directive threshold, and integrate the subsidiary-level targets into the group's CSRD ESRS S1 disclosure on workforce diversity.",
"partial_scope": "Replace the upcoming parent-board vacancy with a director of the under-represented sex to clear the 40% threshold under Article 5 of Directive (EU) 2022/2381, with disclosure of the appointment in the corporate governance statement and the firm's ESRS S1 disclosure.",
"wrong_anchor": "Extend the spirit of Directive (EU) 2022/2381 voluntarily to the operating-subsidiary boards by adopting documented gender-balance targets at subsidiary level, replace the upcoming parent-board vacancy with a director of the under-represented sex, and integrate the subsidiary-level targets into the firm's ESRS G1 disclosure on business conduct under the CSRD framework.",
"procedural_substitution": "Adopt a documented group-governance charter setting parent-board and operating-subsidiary gender-balance targets aligned with the spirit of Directive (EU) 2022/2381, with the group nominations committee tasked with oversight and quarterly reporting to the parent board under ESRS S1.",
},

{
"pillar": "leadership_participation",
"vignette": "Lukas Brandt, Head of Corporate Governance at a Vienna-listed energy utility, identifies that the supervisory board has reached 40% female representation but the management board (Vorstand) — which under Austrian dual-board governance carries primary executive authority — is 0% female (4 men). Three management-board terms expire over the next 24 months.",
"gold": "Adopt a documented management-board renewal plan targeting at least 40% representation of the under-represented sex on the management board by the conclusion of the three upcoming term expiries, in alignment with the spirit of Directive (EU) 2022/2381 and the EU Strategy's commitment to gender-balanced leadership in management positions, with the supervisory board approving each appointment and disclosure in the corporate governance statement.",
"partial_scope": "Commit to appointing a female candidate to the first of the three upcoming management-board vacancies in alignment with the spirit of Directive (EU) 2022/2381, with the supervisory board overseeing the appointment process and disclosure in the corporate governance statement.",
"wrong_anchor": "Adopt a documented management-board renewal plan targeting at least 40% representation of the under-represented sex by the conclusion of the three upcoming term expiries, in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters, with disclosure in the corporate governance statement.",
"procedural_substitution": "Adopt a documented Vorstand-succession governance protocol requiring the supervisory board to develop a gender-balance trajectory for the management board across the three upcoming term expiries, with annual progress reporting in the firm's corporate governance statement.",
},

{
"pillar": "leadership_participation",
"vignette": "Patrik Novák, Group HR Director at a Bratislava-listed IT-services firm, finds that the firm has used the directive's alternative reporting regime under Article 6 (procedural-only) for the past two cycles. The chosen procedural targets — gender-balanced shortlists, structured interviews — have been formally adopted but audit shows zero gender-balanced shortlists submitted in the past 12 months. The 30 June 2026 substantive deadline approaches.",
"gold": "Switch from the Article 6 procedural-only regime to substantive 40% target compliance under Article 5 of Directive (EU) 2022/2381 given the documented implementation gap, develop a board-renewal plan to reach the 40% target by 30 June 2026 with quarterly progress reporting to the nominations committee, and disclose both the regime change and the underlying implementation gap in the corporate governance statement.",
"partial_scope": "Tighten the existing Article 6 procedural commitments by adding an enforcement mechanism requiring the company secretary to validate every shortlist against the gender-balance requirement under Article 6 of Directive (EU) 2022/2381, with non-compliance reported to the nominations committee.",
"wrong_anchor": "Switch from the Article 6 procedural-only regime to substantive 40% target compliance under Article 5 of Directive (EU) 2022/2381 by adopting a board-renewal plan in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters, with quarterly progress reporting to the nominations committee.",
"procedural_substitution": "Adopt a documented enforcement protocol for the existing Article 6 procedural commitments, with the company secretary tasked with quarterly validation of nominations-committee compliance against the gender-balanced-shortlist and structured-interview requirements, and reporting in the corporate governance statement.",
},

{
"pillar": "leadership_participation",
"vignette": "Magdalena Walczak, Chief of Staff at a Warsaw-listed retail group, identifies a pattern across 11 listed firms in the sector: all 11 boards are converging on Article 5 compliance via a small pool of around 40 'professional non-executive directors' of the under-represented sex, who hold an average of 2.3 directorships each. The firm's nominations committee has identified one such director for the next vacancy. Her existing portfolio is at the conventional boundary of board commitment.",
"gold": "Decline the proposed appointment in favour of a documented broadened director-search process surfacing candidates from sources beyond the existing 'professional non-executive director' pool — operational leadership, sector-adjacent expertise, candidates from below the conventional board-experience threshold — in line with Article 4(2)(b) of Directive (EU) 2022/2381 (selection based on a comparative analysis of qualifications) rather than reliance on a narrow existing-director pool.",
"partial_scope": "Proceed with the proposed appointment given the candidate's qualifications and broaden the director-search firm panel for the subsequent vacancy to bring in alternative candidate sources, in alignment with the gender-neutral selection requirement of Article 4 of Directive (EU) 2022/2381.",
"wrong_anchor": "Decline the proposed appointment in favour of a documented broadened director-search process surfacing candidates from operational leadership and sector-adjacent expertise, in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters and the firm's CSRD-aligned governance disclosure.",
"procedural_substitution": "Adopt a documented director-search-process charter for the nominations committee requiring engagement of at least two executive-search firms with explicit diverse-candidate-pool mandates under Article 4 of Directive (EU) 2022/2381, with the charter applicable to the proposed appointment and all subsequent director vacancies.",
},

{
"pillar": "leadership_participation",
"vignette": "Eleni Christou, Head of People at an Athens-listed retail group with 6,200 employees, reviews two concurrent issues: the firm's franchise network of 340 outlets operates under a 'preferred manager profile' template producing a 22% female franchise-manager rate against 51% female applicants, and the directly-owned-store regional-manager appointments have an 18% female rate against a 49% female store-manager candidate pool.",
"gold": "Replace the 'preferred manager profile' template with a documented competence-based selection rubric mirroring the spirit of Article 4 of Directive (EU) 2022/2381 (gender-neutral selection criteria) at all leadership tiers below board level, audit the past three years' franchise and regional-manager appointments for unexplained variance with remediation through targeted promotion in the next cycle, and integrate the leadership-pipeline gender data into the firm's annual sustainability statement.",
"partial_scope": "Replace the 'preferred manager profile' template with a documented competence-based selection rubric for franchise-manager appointments mirroring the spirit of Article 4 of Directive (EU) 2022/2381, effective from the next franchise-renewal cycle, with disclosure in the firm's annual sustainability statement.",
"wrong_anchor": "Replace the 'preferred manager profile' template with a documented competence-based selection rubric at all leadership tiers below board level, in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters, and disclose the leadership-pipeline gender data in the firm's annual sustainability statement.",
"procedural_substitution": "Adopt a documented franchise-and-regional-manager-appointment governance charter requiring gender-balanced shortlists and documented selection rationale for every appointment, with the head of franchise operations reporting quarterly to the executive committee against the spirit of Article 4 of Directive (EU) 2022/2381.",
},

{
"pillar": "leadership_participation",
"vignette": "Catherine O'Brien, Head of Group Strategy at a Dublin-listed financial-services group, observes that the executive-development programme — which feeds the C-suite — has admitted 23% women over five cohorts. Women admitted have an 81% completion rate against 68% male, but women's post-completion C-suite placement rate is 11% against a 43% male rate. Internal HR attributes the placement gap to informal sponsor-allocation at executive-committee level.",
"gold": "Restructure the executive-development programme to include a documented post-completion sponsorship-allocation protocol with gender-balanced sponsor-mentee matching at executive-committee level, target placement-rate parity by 2027 mirroring the European Commission's 50% gender-balance internal benchmark, and disclose programme outcomes by gender in the firm's annual sustainability statement under ESRS S1.",
"partial_scope": "Introduce a documented post-completion sponsorship-allocation protocol with gender-balanced sponsor-mentee matching at executive-committee level, effective from the next executive-development programme cohort, with disclosure in the firm's annual sustainability statement under ESRS S1.",
"wrong_anchor": "Restructure the executive-development programme to include a documented post-completion sponsorship-allocation protocol with gender-balanced sponsor-mentee matching at executive-committee level, in alignment with Article 5 of Directive (EU) 2022/2381 on gender-balanced selection of directors, with disclosure under ESRS S1.",
"procedural_substitution": "Adopt a documented executive-development-programme governance protocol requiring the head of People to convene an annual sponsor-allocation review with executive-committee participation, mirroring the European Commission's 50% gender-balance internal benchmark, with reporting under ESRS S1 of the firm's CSRD report.",
},

{
"pillar": "leadership_participation",
"vignette": "Jakob Hansen, Company Secretary at a Copenhagen-listed shipping group, faces a tactical dilemma: the board has 36% female non-executive directors with one upcoming vacancy. The chairman favours appointing a male candidate with deep maritime-regulatory expertise, arguing the next vacancy will allow easy compliance with Article 5 by the directive deadline. The nominations-committee minority has objected that this tactical approach inverts the directive's intent.",
"gold": "Decline the chairman's proposed appointment for the current vacancy, document the rationale by reference to Article 4(2) of Directive (EU) 2022/2381 (gender-neutral selection at every appointment, not aggregated across a sequence), develop a director-skills matrix for the joint vacancies allowing maritime-regulatory expertise to be sourced from a candidate of the under-represented sex, and disclose the rationale in the corporate governance statement.",
"partial_scope": "Proceed with the chairman's proposed appointment given the strategic relevance of maritime-regulatory expertise, document the appointment rationale comprehensively per Article 5(4) of Directive (EU) 2022/2381, and commit to filling the next vacancy with a candidate of the under-represented sex.",
"wrong_anchor": "Decline the chairman's proposed appointment for the current vacancy and develop a director-skills matrix for the joint vacancies allowing maritime-regulatory expertise to be sourced from a candidate of the under-represented sex, in alignment with Article 14 of Directive 2006/54/EC on equal treatment.",
"procedural_substitution": "Adopt a documented nominations-committee charter governing director-skills matrix development and the application of Article 4 of Directive (EU) 2022/2381 to every individual appointment decision, with the charter approved at the next nominations-committee meeting and applicable to the current vacancy.",
},

{
"pillar": "leadership_participation",
"vignette": "Camille Dubois, Group HR Lead at a Paris-headquartered listed retailer, reviews succession-planning data: of 15 senior-leader retirements expected in the next five years, only two have a documented female successor identified, despite a balanced talent-pool composition at director-1 level. The chairman has asked for a 'pipeline strategy' recommendation.",
"gold": "Mandate gender-balanced succession panels for every senior role, require at least one qualified candidate of the under-represented sex to be documented per role with structured assessment against role criteria, and integrate succession-pipeline gender metrics into the annual people-strategy review reported to the board under ESRS S1 of the firm's CSRD report.",
"partial_scope": "Mandate gender-balanced succession panels for every senior role and require at least one qualified candidate of the under-represented sex per role, applicable to all succession-planning cycles starting from the next planning round, with disclosure under ESRS S1.",
"wrong_anchor": "Mandate gender-balanced succession panels for every senior role and require at least one qualified candidate of the under-represented sex per role, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies, with disclosure under ESRS S1.",
"procedural_substitution": "Adopt a documented succession-planning governance protocol requiring senior-role talent reviews to include gender-balance discussion as a standing agenda item, with the head of talent reporting succession-pipeline gender metrics quarterly to the executive committee under ESRS S1.",
},

{
"pillar": "leadership_participation",
"vignette": "Iulia Stancu, HR Director at a Bucharest-listed bank, finds that the bank's branch-manager appointments over the past five years have gone to men 71% of the time, despite an internal candidate pool that is 52% female, with no documented record of selection rationale.",
"gold": "Introduce a documented branch-manager-appointment process requiring gender-balanced shortlists and structured interview rubrics, audit the past three years' appointments for unexplained variance with remediation through targeted promotion in the next cycle, and integrate appointment-outcome gender data into the firm's annual sustainability statement under ESRS S1 of the CSRD framework.",
"partial_scope": "Introduce a documented branch-manager-appointment process requiring gender-balanced shortlists and structured interview rubrics, effective from the next branch-manager-appointment cycle, with appointment-outcome gender data disclosed under ESRS S1.",
"wrong_anchor": "Introduce a documented branch-manager-appointment process requiring gender-balanced shortlists and structured interview rubrics, audit the past three years' appointments for unexplained variance with remediation, and disclose the data under Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies.",
"procedural_substitution": "Adopt a documented branch-manager-appointment governance charter requiring the head of People to validate every branch-manager appointment against gender-balanced-shortlist criteria, with quarterly reporting to the executive committee and disclosure under ESRS S1.",
},

{
"pillar": "leadership_participation",
"vignette": "Paolo Conti, Head of Talent at a Rome-listed utility, identifies that the firm's executive-development programme — a key feeder for senior leadership — has admitted only 18% women over the past four cohorts despite gender-balanced applications. The selection panel is exclusively male.",
"gold": "Reconstitute the selection panel to ensure gender-balanced membership, introduce a documented selection rubric tied to leadership competencies validated for indirect-discrimination risk, target gender-balanced cohorts of the executive-development programme aligned with the Commission's 50%-by-2024 internal benchmark for management-level gender balance, and integrate cohort outcomes into the firm's ESRS S1 disclosure.",
"partial_scope": "Reconstitute the selection panel to ensure gender-balanced membership and target gender-balanced cohorts of the executive-development programme aligned with the Commission's 50%-by-2024 internal benchmark, effective from the next cohort intake, with disclosure under ESRS S1.",
"wrong_anchor": "Reconstitute the selection panel to ensure gender-balanced membership and introduce a documented selection rubric tied to leadership competencies, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors, with cohort outcomes disclosed under ESRS S1.",
"procedural_substitution": "Adopt a documented executive-development-programme selection charter requiring gender-balanced selection panels and structured rubric assessment for all cohort selections, mirroring the Commission's 50%-by-2024 management-level benchmark, with reporting under ESRS S1.",
},

{
"pillar": "leadership_participation",
"vignette": "Tomáš Novák, Head of Corporate Strategy at a Prague-listed manufacturer, finds that the firm's strategic-planning workshops — which materially shape resource allocation — are systematically attended by 90% male senior leaders, despite a 30% female senior-leadership composition, due to invitation patterns set by the COO.",
"gold": "Reform the strategic-planning workshop invitation process to ensure all senior leaders of equivalent seniority are invited regardless of gender, document the revised invitation criteria, audit and rebalance past workshop attendance and contribution patterns by gender as a standing item in the executive-committee review under ESRS S1 of the firm's CSRD report.",
"partial_scope": "Reform the strategic-planning workshop invitation process to ensure all senior leaders of equivalent seniority are invited regardless of gender, effective from the next strategic-planning cycle, with attendance disclosed under ESRS S1.",
"wrong_anchor": "Reform the strategic-planning workshop invitation process to ensure all senior leaders of equivalent seniority are invited regardless of gender and document the revised invitation criteria, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies.",
"procedural_substitution": "Adopt a documented strategic-planning-workshop governance protocol requiring the COO's office to maintain an attendance register disaggregated by gender, with quarterly reporting to the executive committee under ESRS S1 of the firm's CSRD report.",
},

# =============================================================================
# PILLAR 3 - violence_stereotypes (n=15)
# =============================================================================

{
"pillar": "violence_stereotypes",
"vignette": "Andrei Popescu, Director of Legal & Compliance at a Bucharest-headquartered logistics firm with 1,800 employees across three sites, has received an internal report indicating six allegations of workplace sexual harassment in the past 12 months. The grievance procedure references only 'inappropriate behaviour' and provides no specific channel for harassment cases.",
"gold": "Adopt a documented anti-harassment policy aligned with ILO Convention No. 190 on Violence and Harassment in the World of Work, including a confidential reporting channel bypassing the chain of command, named investigation owners with trained interviewers, documented victim-support provisions, and mandatory annual training for all line managers, with implementation tracked through quarterly incident-resolution reporting to the audit committee.",
"partial_scope": "Adopt a documented anti-harassment policy aligned with ILO Convention No. 190 on Violence and Harassment in the World of Work, including a confidential reporting channel and named investigation owners, applicable to all reported incidents from the date of adoption.",
"wrong_anchor": "Adopt a documented anti-harassment policy aligned with the Victims' Rights Directive 2012/29/EU on minimum standards on the rights, support and protection of victims of crime, including a confidential reporting channel and named investigation owners, with implementation tracked through quarterly reporting.",
"procedural_substitution": "Adopt a documented anti-harassment governance charter aligned with ILO Convention No. 190 on Violence and Harassment in the World of Work, with the head of HR tasked with quarterly review of harassment-incident handling and reporting to the audit committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Margit Kovács, Head of Compliance at a Budapest-headquartered telecom group with 4,800 employees across Hungary, Romania, and Bulgaria, faces a senior male engineering director the subject of seven harassment complaints from three female reports across two countries. The Hungarian transposition of Directive (EU) 2024/1385 is operative; the Romanian transposition delays the cyberviolence provisions; the Bulgarian transposition is incomplete. One complainant has been informally encouraged by HR to accept a performance-based settlement with a confidentiality clause.",
"gold": "Apply the firm's internal harassment policy at the highest of the applicable national standards across all three jurisdictions, withdraw any settlement offer that includes confidentiality clauses on the underlying conduct (which Article 19 of Directive (EU) 2024/1385 requires Member States to prohibit), open a formal investigation suspending the engineering director's line authority pending outcome, and engage trauma-informed support for the complainants in alignment with the Victims' Rights Directive 2012/29/EU.",
"partial_scope": "Withdraw the settlement offer that includes confidentiality clauses on the underlying conduct (which Article 19 of Directive (EU) 2024/1385 requires Member States to prohibit) and open a formal investigation in line with the firm's existing harassment policy, with trauma-informed support engaged for the complainants.",
"wrong_anchor": "Apply the firm's internal harassment policy at the highest of the applicable national standards across all three jurisdictions, withdraw any settlement offer that includes confidentiality clauses on the underlying conduct in alignment with Article 10 of ILO Convention No. 190 on safe and effective dispute mechanisms, open a formal investigation, and engage trauma-informed support.",
"procedural_substitution": "Convene a documented cross-jurisdiction harassment-response committee with HR leads from all three operating companies, tasked with developing harmonised investigation protocols aligned with Directive (EU) 2024/1385 and the Victims' Rights Directive 2012/29/EU, with recommendations due within 90 days.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Cristina Ferreira, Compliance Officer at a Porto-based construction group with 2,100 directly-employed staff and 6,400 sub-contractor workers across 18 sites, has received a complaint that female sub-contractor cleaners on three sites are subject to sustained sexual harassment by sub-contractor supervisors. The firm's harassment policy applies only to directly-employed staff; the sub-contractor agreements include a generic 'compliance with applicable law' clause.",
"gold": "Extend the firm's harassment policy to cover all sub-contractor workers on firm-controlled sites in alignment with Article 7 of ILO Convention No. 190 (covering all workers regardless of contractual status), introduce an independent-investigation channel for sub-contractor harassment reports, embed harassment-protection obligations into the sub-contractor agreement template, and document the chain of responsibility under the value-chain due-diligence provisions of Directive (EU) 2024/1760 (CSDDD).",
"partial_scope": "Embed harassment-protection obligations into the sub-contractor agreement template in alignment with Article 7 of ILO Convention No. 190, with renewed sub-contractor agreements adopting the updated template at their natural renewal date.",
"wrong_anchor": "Extend the firm's harassment policy to cover all sub-contractor workers on firm-controlled sites in alignment with the value-chain disclosure provisions of Directive (EU) 2022/2464 (CSRD), introduce an independent-investigation channel, and embed harassment-protection obligations into the sub-contractor agreement template.",
"procedural_substitution": "Adopt a documented sub-contractor harassment-governance charter aligned with ILO Convention No. 190, with the head of compliance tasked with quarterly review of sub-contractor harassment-incident handling and reporting to the audit committee under the CSDDD framework.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Lina Sandberg, Trust & Safety Lead at a Gothenburg-based social-media platform with 2.4 million EU users, reviews two compounding signals: female users report receiving online sexual harassment at 4x the rate of male users, and the platform's automated content-moderation system has a 31% false-negative rate on intimate-image abuse reports involving women, against 8% for equivalent reports involving men. The platform is preparing for both Directive (EU) 2024/1385 transposition deadlines and the DSA Article 35 risk-mitigation obligations.",
"gold": "Conduct a documented risk assessment of the content-moderation system's gendered false-negative rate as a high-risk AI system under Annex III of Regulation (EU) 2024/1689 (the AI Act), retrain the moderation model with a balanced training corpus and human-review escalation for intimate-image abuse cases, integrate the mitigation into the platform's DSA Article 35 systemic-risk-mitigation report, and align with the cyberviolence provisions of Directive (EU) 2024/1385.",
"partial_scope": "Retrain the moderation model with a balanced training corpus to address the 31% false-negative rate on intimate-image abuse reports involving women, in alignment with the cyberviolence provisions of Directive (EU) 2024/1385, and integrate the mitigation into the platform's DSA Article 35 systemic-risk-mitigation report.",
"wrong_anchor": "Conduct a documented Data Protection Impact Assessment of the content-moderation system's gendered false-negative rate under Article 35 GDPR, retrain the moderation model, and integrate the mitigation into the platform's DSA Article 35 systemic-risk-mitigation report.",
"procedural_substitution": "Adopt a documented content-moderation governance protocol requiring the trust-and-safety committee to review the moderation system's gendered false-negative-rate metrics quarterly, with reporting under the platform's DSA Article 35 systemic-risk-mitigation framework and Article 27 fundamental-rights impact assessment of the AI Act.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Eva Janssen, HR Director at an Amsterdam-based hospital group with 11,800 employees, identifies that 38% of female nursing staff report having experienced patient-perpetrated sexual harassment in the past 12 months, that 92% of those incidents went unreported through formal channels, and that the group's existing patient-incident reporting workflow categorises such events under 'patient agitation' alongside non-gendered behaviours.",
"gold": "Reclassify patient-perpetrated sexual harassment as a distinct workplace-safety incident category in the patient-incident reporting workflow, introduce a documented response protocol including trained patient-incident response leads, post-incident counselling, and an explicit nurse-led right to refuse to provide non-emergency care to patients with documented incidents, in alignment with Article 7 of ILO Convention No. 190 on third-party violence and the workplace-safety provisions of EU Framework Directive 89/391/EEC.",
"partial_scope": "Reclassify patient-perpetrated sexual harassment as a distinct workplace-safety incident category in the patient-incident reporting workflow and introduce a documented response protocol including trained patient-incident response leads and post-incident counselling, in alignment with Article 7 of ILO Convention No. 190 on third-party violence.",
"wrong_anchor": "Reclassify patient-perpetrated sexual harassment as a distinct workplace-safety incident category and introduce a documented response protocol, in alignment with the cyberviolence and offline-violence provisions of Directive (EU) 2024/1385 on combating violence against women and domestic violence.",
"procedural_substitution": "Adopt a documented patient-incident-response governance charter recognising patient-perpetrated sexual harassment as a distinct incident category under ILO Convention No. 190, with the head of nursing tasked with quarterly review of incident-response handling and reporting to the executive committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Henrik Johansen, HR Director at an Oslo-based offshore-vessel-operations firm with 380 employees, learns that female cadets on long offshore deployments report a pattern of 'normalised banter' that escalates to sexual harassment in approximately 22% of deployments. The grievance procedure requires reports to be made to the vessel master, frequently the perpetrator's social peer or implicit superior.",
"gold": "Establish a documented offshore-harassment reporting protocol bypassing the vessel-master line, including a confidential 24/7 shore-based reporting channel, mandatory shore-side investigation for reports involving senior crew, immediate cadet-rotation-out protections, and integration with the ISM Code's safety-management framework, in alignment with Article 10 of ILO Convention No. 190 on safe and effective dispute mechanisms.",
"partial_scope": "Add a confidential 24/7 shore-based reporting channel as a parallel route to the existing grievance procedure, in alignment with Article 10 of ILO Convention No. 190 on safe and effective dispute mechanisms, with cadets and crew briefed on the parallel route during onboarding.",
"wrong_anchor": "Establish a documented offshore-harassment reporting protocol bypassing the vessel-master line, with a confidential 24/7 shore-based reporting channel and immediate cadet-rotation-out protections, in alignment with the Victims' Rights Directive 2012/29/EU on minimum standards on the rights, support and protection of victims of crime.",
"procedural_substitution": "Adopt a documented offshore-harassment-response charter aligned with ILO Convention No. 190 and the ISM Code, with the head of fleet operations tasked with quarterly review of grievance-handling and reporting to the executive committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Anna Sokolova, Communications Director at a Riga-based media company, finds that two female journalists have received targeted online harassment campaigns following politically sensitive articles, including doxxing and threats of sexual violence. The firm has no documented protocol for online violence affecting employees.",
"gold": "Adopt a documented protocol for online-harassment incidents involving employees, including legal-support coverage, platform-takedown coordination via Article 16 of the Digital Services Act, counselling provision aligned with the Victims' Rights Directive 2012/29/EU, and trauma-informed editorial-leadership liaison, in alignment with the cyberviolence provisions of Directive (EU) 2024/1385 on combating violence against women and domestic violence.",
"partial_scope": "Adopt a documented protocol for online-harassment incidents involving employees, including legal-support coverage and platform-takedown coordination, in alignment with the cyberviolence provisions of Directive (EU) 2024/1385 on combating violence against women and domestic violence.",
"wrong_anchor": "Adopt a documented protocol for online-harassment incidents involving employees, including legal-support coverage and platform-takedown coordination, in alignment with ILO Convention No. 190 on Violence and Harassment in the World of Work and the firm's workplace-safety framework.",
"procedural_substitution": "Adopt a documented editorial-safety governance charter aligned with Directive (EU) 2024/1385, with the head of editorial tasked with quarterly review of online-harassment incidents involving journalists and reporting to the executive committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Anneli Korhonen, Head of Editorial at a Helsinki-based public-broadcasting service, faces two interlocking issues following the broadcaster's investigative coverage of organised-crime networks: three female reporters have received targeted online-harassment campaigns including doxxing, deepfake intimate-image generation, and coordinated platform reporting that has led to temporary social-media suspension.",
"gold": "Update the safety-of-journalists protocol to address gendered online violence as a distinct workplace-safety issue, including legal-support coverage, platform-takedown coordination via Article 16 of the Digital Services Act, deepfake-removal procedures under Article 5 of Directive (EU) 2024/1385 (criminalisation of non-consensual intimate-image dissemination including deepfakes), and trauma-informed counselling provision aligned with the Victims' Rights Directive 2012/29/EU.",
"partial_scope": "Update the safety-of-journalists protocol to address gendered online violence with legal-support coverage and platform-takedown coordination via Article 16 of the Digital Services Act, applicable to the three affected reporters and any subsequent incidents.",
"wrong_anchor": "Update the safety-of-journalists protocol to address gendered online violence as a distinct workplace-safety issue, including legal-support coverage and platform-takedown coordination, in alignment with ILO Convention No. 190 on Violence and Harassment in the World of Work and the broadcaster's workplace-safety framework.",
"procedural_substitution": "Adopt a documented safety-of-journalists governance protocol addressing gendered online violence as a distinct workplace-safety issue, with the head of editorial tasked with quarterly review of online-harassment incidents and reporting to the broadcaster's editorial-standards committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Pierre Lambert, Workplace Safety Manager at a Lyon-based industrial-services firm with 320 employees, identifies that the firm's late-shift operations expose women to safety risks: lone working, poorly lit access routes, and no documented protocol for incidents of harassment or assault during transit between site and parking.",
"gold": "Introduce a documented late-shift safety protocol covering lighting upgrade and paired-working arrangements, an incident-reporting channel with named investigation owners, and trauma-informed post-incident support, in alignment with the workplace-safety provisions of ILO Convention No. 190 and the firm's duty of care under EU Framework Directive 89/391/EEC on the introduction of measures to encourage improvements in the safety and health of workers at work.",
"partial_scope": "Upgrade the lighting on access routes between the late-shift site and parking and introduce paired-working arrangements for late-shift workers, in alignment with the firm's duty of care under EU Framework Directive 89/391/EEC on the introduction of measures to encourage improvements in the safety and health of workers at work.",
"wrong_anchor": "Introduce a documented late-shift safety protocol covering lighting, paired-working arrangements, and an incident-reporting channel, in alignment with the third-party-violence provisions of the Victims' Rights Directive 2012/29/EU on minimum standards on the rights, support and protection of victims of crime.",
"procedural_substitution": "Adopt a documented late-shift safety governance charter aligned with ILO Convention No. 190 and EU Framework Directive 89/391/EEC, with the workplace-safety officer tasked with quarterly review of late-shift incident-handling and reporting to the executive committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Kai Brandt, Head of People at a Berlin-headquartered pharmaceutical group with 5,400 employees across the EU, faces a recurrent issue: senior male sales representatives in the German and Italian markets habitually entertain customers — predominantly male physicians — at venues where female sales representatives report repeated sexual-harassment incidents involving customers. A female sales representative has just resigned citing the dynamic.",
"gold": "Issue a documented group-wide customer-entertainment policy requiring all firm-organised customer events to take place at venues meeting documented respect-and-safety standards, ban firm-sponsored attendance at venues with documented harassment risk, extend the firm's harassment policy to cover firm-sanctioned customer-entertainment activities in alignment with ILO Convention No. 190's broad workplace definition, and engage the works councils in both markets on policy implementation.",
"partial_scope": "Issue venue-selection guidance through the firm's commercial-operations function, recommending that customer events take place at venues without documented harassment risk in alignment with ILO Convention No. 190, with sales-representative discretion preserved on customer-entertainment formats and frequency.",
"wrong_anchor": "Issue a documented group-wide customer-entertainment policy requiring all firm-organised customer events to take place at venues meeting documented respect-and-safety standards, extending the firm's harassment policy to firm-sanctioned customer-entertainment activities in alignment with the third-party-violence provisions of the Victims' Rights Directive 2012/29/EU.",
"procedural_substitution": "Adopt a documented customer-entertainment governance charter aligned with ILO Convention No. 190's broad workplace definition, with the head of commercial operations tasked with venue-risk review and quarterly reporting to the audit committee, in cooperation with the works councils in both markets.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Marc Vermeulen, HR Director at an Antwerp-based law firm with 250 employees including support staff, identifies that the firm's longstanding 'partner-track culture' includes informal late-night networking events at which inappropriate behaviour by senior partners has been historically tolerated, with two associates resigning in the past year citing this dynamic.",
"gold": "Adopt a documented partner-conduct standard extending the firm's harassment policy to all firm-sanctioned networking activities, conduct anonymous culture-survey diagnostics with action commitments tied to findings, tie partner profit-share allocation to documented compliance with the conduct standard, and align with ILO Convention No. 190's broad workplace definition extending to all work-related activities.",
"partial_scope": "Adopt a documented partner-conduct standard extending the firm's harassment policy to all firm-sanctioned networking activities in alignment with ILO Convention No. 190's broad workplace definition, with the conduct standard applicable to all partners from the date of adoption.",
"wrong_anchor": "Adopt a documented partner-conduct standard extending the firm's harassment policy to all firm-sanctioned networking activities and conduct anonymous culture-survey diagnostics, in alignment with the Victims' Rights Directive 2012/29/EU on minimum standards on the rights, support and protection of victims of crime.",
"procedural_substitution": "Adopt a documented partnership-conduct governance charter aligned with ILO Convention No. 190's broad workplace definition, with the managing partner tasked with annual anonymous culture-survey diagnostics and reporting to the partnership board.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Federica Ricci, Director of Marketing at a Florence-based fashion retailer with 1,400 employees, faces an internal-stakeholder split over the firm's autumn campaign creative brief, which features sexualised imagery of young female models in workplace office settings. Internal HR data show the firm has had 14 sexual-harassment incidents in 24 months; an internal employee survey links the imagery to a 'culture of objectification.' The chief creative officer argues the imagery is central to commercial performance.",
"gold": "Veto the autumn campaign creative in its current form, adopt a documented marketing-content review policy aligned with the EU Strategy's commitment to challenging gender stereotypes in advertising and Article 6 of Directive 2010/13/EU (AVMSD) on respect for human dignity in commercial communications, integrate the policy into creative-brief sign-off as a binding gate, and engage the chief creative officer on the policy applying equally to heritage-brand and new-campaign work.",
"partial_scope": "Veto the autumn campaign creative in its current form and adopt a documented marketing-content review policy aligned with the EU Strategy's commitment to challenging gender stereotypes in advertising, with the policy taking effect from the next creative-brief sign-off.",
"wrong_anchor": "Veto the autumn campaign creative in its current form and adopt a documented marketing-content review policy aligned with the EU Strategy's commitment to challenging gender stereotypes, in alignment with the GDPR Article 9 protections on special-category data and the firm's brand-protection framework.",
"procedural_substitution": "Adopt a documented marketing-content review governance charter aligned with the EU Strategy's commitment to challenging gender stereotypes and Article 6 of Directive 2010/13/EU (AVMSD), with the head of marketing tasked with creative-brief review and quarterly reporting to the executive committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Helena Nilsson, Head of Compliance at a Gothenburg-based logistics firm with 590 employees, finds that the company's grievance procedure currently routes all harassment complaints through the line manager, but 80% of complaints involve the line manager themselves or a peer-relationship.",
"gold": "Replace the line-manager-only grievance route with a documented dual-channel procedure offering an alternative confidential reporting line outside the chain of command, with named investigation owners trained in trauma-informed interviewing and documented victim-support coordination, in alignment with Article 10 of ILO Convention No. 190 on safe and effective dispute mechanisms.",
"partial_scope": "Add a documented alternative confidential reporting line outside the chain of command as a parallel route to the existing grievance procedure, in alignment with Article 10 of ILO Convention No. 190 on safe and effective dispute mechanisms, with employees briefed on the parallel route during onboarding.",
"wrong_anchor": "Replace the line-manager-only grievance route with a documented dual-channel procedure offering an alternative confidential reporting line outside the chain of command, in alignment with the Victims' Rights Directive 2012/29/EU on minimum standards on the rights, support and protection of victims of crime.",
"procedural_substitution": "Adopt a documented harassment-grievance governance charter aligned with Article 10 of ILO Convention No. 190 on safe and effective dispute mechanisms, with the head of HR tasked with quarterly review of grievance-handling and reporting to the audit committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Tomáš Bednár, Head of HR at a Prague-based logistics firm with 1,650 employees, learns that the firm's third-party recruitment vendor — used for high-volume warehouse hiring — has been screening female applicants for marital status and pregnancy intentions in informal pre-screening calls, a practice that violates EU equal-treatment law. The vendor's contract is on auto-renewal in 60 days.",
"gold": "Suspend the vendor's pre-screening operations pending a documented compliance investigation, terminate the vendor contract for material breach if the investigation confirms the practice, replace the vendor's pre-screening with a documented competence-only screening framework consistent with Article 4 of Directive 2006/54/EC (Recast Equal Treatment Directive), report the incident to the firm's compliance committee and external auditor, and offer trauma-informed support to affected applicants where identifiable.",
"partial_scope": "Suspend the vendor's pre-screening operations pending a documented compliance investigation and replace the vendor's pre-screening with a documented competence-only screening framework consistent with Article 4 of Directive 2006/54/EC, with the vendor contract renewed or terminated based on investigation outcomes.",
"wrong_anchor": "Suspend the vendor's pre-screening operations pending a documented compliance investigation and replace the vendor's pre-screening with a documented competence-only screening framework, in alignment with Article 4 of Directive (EU) 2023/970 on the equal-pay-for-work-of-equal-value principle.",
"procedural_substitution": "Adopt a documented third-party-recruitment-vendor governance charter requiring all recruitment vendors to certify compliance with Article 4 of Directive 2006/54/EC and undergo annual compliance audits, with the head of HR tasked with vendor compliance review and quarterly reporting to the audit committee.",
},

{
"pillar": "violence_stereotypes",
"vignette": "Maria Antoniou, Head of Security at a Larnaca-based hospitality group with 1,200 employees, learns that two female employees have disclosed they are experiencing domestic violence at home. The firm has no documented support framework, and both employees fear job impact if they request schedule changes.",
"gold": "Adopt a documented domestic-violence workplace-support policy including paid safe leave, scheduling and location flexibility, confidentiality protections, and named HR contacts trained in trauma-informed support, in alignment with the workplace-support provisions of Directive (EU) 2024/1385 on combating violence against women and domestic violence and the Work-Life Balance Directive (EU) 2019/1158's right-to-request flexible-working framework.",
"partial_scope": "Adopt a documented domestic-violence workplace-support policy including paid safe leave and scheduling flexibility, in alignment with the workplace-support provisions of Directive (EU) 2024/1385 on combating violence against women and domestic violence.",
"wrong_anchor": "Adopt a documented domestic-violence workplace-support policy including paid safe leave, scheduling and location flexibility, and confidentiality protections, in alignment with the Victims' Rights Directive 2012/29/EU on minimum standards on the rights, support and protection of victims of crime and the firm's broader workplace-safety framework.",
"procedural_substitution": "Adopt a documented domestic-violence workplace-support governance charter aligned with Directive (EU) 2024/1385, with the head of HR tasked with managing case-by-case responses to domestic-violence disclosures and quarterly reporting to the executive committee.",
},

# =============================================================================
# PILLAR 4 - mainstreaming_intersectionality (n=15)
# =============================================================================

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Elena Marchetti, Programme Director at a Florence-based research institute applying for Horizon Europe funding, finds that the institute has no Gender Equality Plan in place, despite the eligibility requirement for public-research applicants since 2022. The institute's 14-page draft 'diversity statement' does not meet the GEP criteria.",
"gold": "Develop and publish a Gender Equality Plan meeting the five mandatory Horizon Europe criteria — public document, dedicated resources, data collection and monitoring, training, and gender-balance targets — before submitting the application, with documented monitoring indicators and named GEP-implementation officer, in alignment with the Horizon Europe GEP eligibility requirement.",
"partial_scope": "Develop and publish a Gender Equality Plan meeting four of the five mandatory Horizon Europe criteria — public document, dedicated resources, data collection and monitoring, and training — before submitting the application, with gender-balance targets to be developed in the institute's next strategic-planning cycle.",
"wrong_anchor": "Develop and publish a Gender Equality Plan meeting the five mandatory criteria — public document, dedicated resources, data collection and monitoring, training, and gender-balance targets — in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters, and submit the GEP alongside the funding application.",
"procedural_substitution": "Adopt a documented Gender Equality Plan governance charter aligned with the Horizon Europe GEP eligibility framework, with the head of research tasked with annual GEP review and quarterly reporting to the institute's executive committee.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Hanna Lehtinen, Sustainability Lead at an Espoo-based clean-energy firm with 410 employees, is preparing the firm's response to a public-tender requirement on the gender dimension of the proposed Green Deal-aligned project. The current proposal has no documented gender-impact assessment.",
"gold": "Conduct a documented gender-impact assessment of the proposed project identifying differential impacts on women, men, and non-binary stakeholders across the energy-transition activities, integrate documented mitigations into the project plan with gender-disaggregated outcome indicators, and align with the gender-mainstreaming provisions of the European Green Deal and the EU Strategy's commitment to gender mainstreaming in the green transition.",
"partial_scope": "Conduct a documented gender-impact assessment of the proposed project identifying differential impacts on women, men, and non-binary stakeholders across the energy-transition activities, with the assessment findings included in the tender response in alignment with the EU Strategy's gender-mainstreaming framework.",
"wrong_anchor": "Conduct a documented gender-impact assessment of the proposed project and integrate documented mitigations into the project plan, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies and the firm's broader governance disclosure.",
"procedural_substitution": "Adopt a documented gender-impact-assessment governance charter aligned with the gender-mainstreaming provisions of the European Green Deal, with the head of sustainability tasked with annual review of project-level gender-impact assessments and reporting to the executive committee.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Marta Vukmir, Head of People Analytics at a Zagreb-based banking group with 3,400 employees across Croatia, Slovenia and Bosnia, is preparing the group's CSRD-aligned ESRS S1 disclosure on workforce diversity. The current plan reports on gender alone; senior leadership has resisted disaggregation by ethnicity (Roma, Bosniak, Albanian minorities) and disability on cost grounds. Internal data show Roma women face documented compounding barriers in branch-level promotion.",
"gold": "Adopt intersectional disaggregation (gender x ethnicity x disability) in the ESRS S1 disclosure with safeguarded data-collection protocols compliant with Article 9 GDPR (special-category data), align the disclosure framework with the EU Strategy's intersectional commitment to the situation of Roma women, integrate the intersectional findings into the bank's anti-discrimination training, and disclose remediation actions in the ESRS S1 narrative.",
"partial_scope": "Adopt intersectional disaggregation (gender x ethnicity x disability) in the ESRS S1 disclosure with safeguarded data-collection protocols compliant with Article 9 GDPR (special-category data), aligned with the EU Strategy's intersectional commitment to the situation of Roma women.",
"wrong_anchor": "Adopt intersectional disaggregation (gender x ethnicity x disability) in the ESRS S1 disclosure with safeguarded data-collection protocols compliant with Article 9 GDPR (special-category data), in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters.",
"procedural_substitution": "Adopt a documented intersectional-disclosure governance charter aligned with Article 9 GDPR and the EU Strategy's intersectional commitment to the situation of Roma women, with the head of People Analytics tasked with annual review of intersectional data-collection protocols and reporting to the audit committee.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Elena Rusu, Sustainability Director at a Bucharest-based industrial conglomerate, faces a layered CSRD challenge: the firm's value chain includes Bangladeshi garment suppliers (predominantly women workers), Romanian agricultural seasonal labour (mixed migrant workforce), and Italian luxury sub-contractors (older female craftworkers). The current materiality assessment treats gender equality as a workforce metric for direct employees only.",
"gold": "Expand the materiality assessment to include intersectional gender-equality impacts across the full value chain — gender x migration status (Bangladeshi/Romanian agricultural), gender x age (Italian craftworkers), gender x ethnicity — integrate findings into supplier-engagement protocols with documented gender-disaggregated outcome indicators, and disclose results under the value-chain reporting requirements of ESRS S2 of the CSRD and the human-rights due-diligence obligations of Directive (EU) 2024/1760 (CSDDD).",
"partial_scope": "Expand the materiality assessment to include intersectional gender-equality impacts across tier-1 suppliers — gender x migration status, gender x age, gender x ethnicity — and integrate findings into supplier-engagement protocols, in alignment with ESRS S2 of the CSRD.",
"wrong_anchor": "Expand the materiality assessment to include intersectional gender-equality impacts across the full value chain, integrate findings into supplier-engagement protocols with documented gender-disaggregated outcome indicators, and disclose results under ESRS S1 of the CSRD on direct workforce reporting and the firm's broader governance framework.",
"procedural_substitution": "Adopt a documented value-chain intersectional-impact governance charter aligned with ESRS S2 of the CSRD and Directive (EU) 2024/1760 (CSDDD), with the head of sustainability tasked with annual review of supplier-engagement protocols and reporting to the audit committee.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Jens Mortensen, Strategic Planning Lead at a Copenhagen-based regional health agency, is reviewing two policy strands due for refresh: the cardiovascular-care pathway (which published evidence shows under-recognises symptoms in women, particularly older women and women of South Asian descent) and the perinatal mental-health pathway (which under-serves teen mothers and migrant mothers).",
"gold": "Restructure both pathways using an intersectional design framework (gender x age x ethnicity) with documented disaggregated outcome metrics, train clinical staff on intersectional symptom recognition, integrate the outcome data into the agency's quality-improvement cycle, and align the redesign with the EU Strategy's gender-mainstreaming approach to health policy and the EU's commitment to the Beijing Platform for Action's intersectional health framework.",
"partial_scope": "Restructure the cardiovascular-care pathway using an intersectional design framework (gender x age x ethnicity) with documented disaggregated outcome metrics and train clinical staff on intersectional symptom recognition, in alignment with the EU Strategy's gender-mainstreaming approach to health policy.",
"wrong_anchor": "Restructure both pathways using an intersectional design framework (gender x age x ethnicity) with documented disaggregated outcome metrics and train clinical staff on intersectional symptom recognition, in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters.",
"procedural_substitution": "Adopt a documented intersectional-pathway-design governance charter aligned with the EU Strategy's gender-mainstreaming approach to health policy and the Beijing Platform for Action, with the chief clinical officer tasked with annual review of pathway outcomes by intersectional category and reporting to the agency's quality-improvement committee.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Anna Lehtinen, Programme Director at a Helsinki-based vocational-training agency, faces a structural challenge: the agency's reskilling programmes for the green transition target unemployed workers from carbon-intensive industries, but the participant pool is 91% male, reflecting the gender composition of the affected industries. Adjacent sectors (administration, logistics) where women are concentrated are not currently in the agency's outreach scope.",
"gold": "Expand the agency's reskilling-programme outreach scope to include workers in adjacent sectors affected by carbon-intensive-industry decline (administration, logistics, retail) where women are concentrated, redesign programme-eligibility criteria with intersectional consideration of gender x age x prior-sector, and integrate the redesign into the agency's ESF+ gender-mainstreaming compliance and the Just Transition Fund's gender-equality provisions under Regulation (EU) 2021/1056.",
"partial_scope": "Expand the agency's reskilling-programme outreach scope to include workers in adjacent sectors affected by carbon-intensive-industry decline (administration, logistics, retail) where women are concentrated, in alignment with the Just Transition Fund's gender-equality provisions under Regulation (EU) 2021/1056.",
"wrong_anchor": "Expand the agency's reskilling-programme outreach scope to include workers in adjacent sectors, redesign programme-eligibility criteria with intersectional consideration of gender x age x prior-sector, and integrate the redesign into the agency's compliance with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies.",
"procedural_substitution": "Adopt a documented reskilling-programme governance charter aligned with the agency's ESF+ gender-mainstreaming framework and the Just Transition Fund's gender-equality provisions under Regulation (EU) 2021/1056, with the programme director tasked with annual review of outreach-scope and reporting to the ESF+ managing authority.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Kornelia Müller, Head of Procurement at a Vienna-based federal-state authority, is overseeing the procurement of an AI-driven welfare-eligibility-assessment system covering 280,000 beneficiaries. Vendor proposals show a 14-percentage-point gendered false-rejection differential, with a further intersectional differential affecting women with disabilities (additional 9 points) and migrant women (additional 11 points).",
"gold": "Reject the lead vendor's proposal in its current form, require all final-stage vendors to submit a documented intersectional fundamental-rights impact assessment under Article 27 of Regulation (EU) 2024/1689 (the AI Act, classifying welfare-eligibility-assessment systems as high-risk under Annex III) specifying mitigation across gender, disability and migration axes, integrate the requirement into the procurement framework alongside the EU Strategy's intersectional gender-mainstreaming commitments, and require post-deployment monitoring with named accountability.",
"partial_scope": "Reject the lead vendor's proposal in its current form and require all final-stage vendors to submit a documented fundamental-rights impact assessment under Article 27 of Regulation (EU) 2024/1689 (the AI Act) specifying gender-axis mitigation, with disability and migration axes addressed in the post-deployment monitoring phase.",
"wrong_anchor": "Reject the lead vendor's proposal in its current form and require all final-stage vendors to submit a documented intersectional Data Protection Impact Assessment under Article 35 GDPR specifying mitigation across gender, disability and migration axes, with named accountability for post-deployment monitoring.",
"procedural_substitution": "Adopt a documented AI-procurement governance charter requiring all high-risk AI systems to undergo intersectional fundamental-rights impact assessment under Article 27 of Regulation (EU) 2024/1689 (the AI Act), with the head of procurement tasked with annual review of vendor-assessment outcomes and reporting to the audit committee.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Bartosz Lewandowski, Innovation Director at a Wrocław-based smart-city public-private partnership, faces a tension: the partnership's predictive-policing pilot has produced documented over-targeting of Roma women in three districts, an intersectional pattern not visible in the original gender-mainstreaming impact assessment which considered only the gender axis. The policing partner argues the pilot's overall accuracy metrics justify continuation.",
"gold": "Suspend the predictive-policing pilot pending a documented intersectional fundamental-rights impact assessment under Article 27 of Regulation (EU) 2024/1689 (the AI Act, with predictive-policing prohibited or high-risk under Annex II–III depending on use case), engage civil-society representatives in the redesign, align with both the EU Strategy's intersectional gender-mainstreaming framework and the EU Roma Strategic Framework on equality, inclusion and participation, and document a public mitigation plan before any resumption.",
"partial_scope": "Recalibrate the predictive-policing model with additional Roma-specific training data to address the documented over-targeting pattern, conduct a documented fundamental-rights impact assessment under Article 27 of Regulation (EU) 2024/1689 (the AI Act), and maintain pilot operational continuity through the recalibration period.",
"wrong_anchor": "Suspend the predictive-policing pilot pending a documented intersectional Data Protection Impact Assessment under Article 35 GDPR, engage civil-society representatives in the redesign, and align with the EU Strategy's intersectional gender-mainstreaming framework and the EU Roma Strategic Framework.",
"procedural_substitution": "Adopt a documented predictive-policing-governance charter aligned with Article 27 of Regulation (EU) 2024/1689 (the AI Act) and the EU Roma Strategic Framework, with the innovation director tasked with annual review of pilot outcomes by intersectional category and reporting to the municipal stakeholders.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Sandra Costa, Sustainability Officer at a Lisbon-based luxury-tourism group with 3,200 employees and a 14,000-strong supplier base across Portugal, Cape Verde and São Tomé, has identified that women in the group's African supplier base face compounding climate-vulnerability and economic-vulnerability that an apparently gender-neutral climate-resilience programme funded by the group does not reach because the programme operates through male village-head intermediaries.",
"gold": "Restructure the climate-resilience programme to operate through women's-cooperative intermediaries with documented gender-disaggregated outcome metrics, integrate the redesign into the group's CSRD ESRS E1 (climate) and S2 (value chain) disclosures, align the methodology with both the Gender Action Plan III's gender-responsive climate-action framework and the EU Strategy's intersectional commitment to the situation of women in low-income partner countries, and document baseline-and-target indicators per delivery cooperative.",
"partial_scope": "Add a women's-cooperative co-implementation track alongside the existing male-intermediary delivery channel for the climate-resilience programme, integrate the dual-track into the group's CSRD ESRS E1 (climate) and S2 (value chain) disclosures, and align with the Gender Action Plan III's gender-responsive climate-action framework.",
"wrong_anchor": "Restructure the climate-resilience programme to operate through women's-cooperative intermediaries with documented gender-disaggregated outcome metrics, integrate the redesign into the group's CSRD ESRS E1 (climate) and S2 (value chain) disclosures, and align with ESRS S1 of the CSRD on direct workforce reporting and the group's broader workforce-diversity framework.",
"procedural_substitution": "Adopt a documented climate-resilience-programme governance charter aligned with the Gender Action Plan III's gender-responsive climate-action framework, with the head of sustainability tasked with annual review of programme delivery channels and reporting to the audit committee under ESRS E1 and S2.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Maria Schmidt, Head of EU Affairs at a Brussels-based industry association representing 220 member firms across the construction sector, is coordinating the association's response to the Commission's revision of the Construction Products Regulation. The current draft response emphasises competitiveness and red-tape concerns; the gender dimension of construction-product safety (e.g. PPE design defaulting to male-body specifications, with documented injury implications for female construction workers) is absent from the draft.",
"gold": "Expand the association's consultation response to include the gender dimension of construction-product safety — including PPE design specifications that account for female-body morphology — anchor the response in Article 8 TFEU (gender-mainstreaming clause), the EU Strategy's commitment to addressing gender-blind product design, and EU Framework Directive 89/391/EEC on the introduction of measures to encourage improvements in the safety and health of workers, and request gender-disaggregated injury-data reporting requirements in the revised regulation.",
"partial_scope": "Expand the association's consultation response to request gender-disaggregated injury-data reporting requirements in the revised Construction Products Regulation, anchor the request in Article 8 TFEU (gender-mainstreaming clause), and submit the expanded response to the consultation.",
"wrong_anchor": "Expand the association's consultation response to include the gender dimension of construction-product safety — including PPE design specifications that account for female-body morphology — anchor the response in Article 14 of Directive 2006/54/EC on equal treatment in occupational matters and the EU Strategy's commitment to addressing gender-blind product design.",
"procedural_substitution": "Adopt a documented association-position governance charter aligned with Article 8 TFEU (gender-mainstreaming clause) and the EU Strategy's commitment to addressing gender-blind product design, with the head of EU affairs tasked with annual review of consultation responses for gender-mainstreaming alignment and reporting to the association board.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Eleni Vasilakis, Programme Director at a Thessaloniki-based EU-funded migration-integration programme, faces an intersectional challenge: the programme's standard intervention package — language training, employment placement, social-services referral — is poorly accessed by women migrants from third countries with documented patterns of restricted-mobility, intra-household decision-making constraints, and gender-based-violence vulnerability. Outcome data show 11% female participation against a regional female-migrant population of 47%.",
"gold": "Redesign the intervention package with documented intersectional sensitivity (gender x migration status x GBV vulnerability), introduce home-based and women-only delivery formats, integrate GBV-screening with referral pathways consistent with Directive (EU) 2024/1385 and the Victims' Rights Directive 2012/29/EU, and align the redesign with the Gender Action Plan III's intersectional approach and the EU Strategy's commitment to migrant women's integration with documented participation and placement targets.",
"partial_scope": "Redesign the intervention package with documented intersectional sensitivity (gender x migration status), introduce home-based and women-only delivery formats, and align the redesign with the Gender Action Plan III's intersectional approach and the EU Strategy's commitment to migrant women's integration, with GBV-screening to be integrated in the subsequent programme cycle.",
"wrong_anchor": "Redesign the intervention package with documented intersectional sensitivity (gender x migration status x GBV vulnerability), introduce home-based and women-only delivery formats, integrate GBV-screening with referral pathways, and align with the Recast Equal Treatment Directive 2006/54/EC and the firm's broader anti-discrimination framework.",
"procedural_substitution": "Adopt a documented intersectional-intervention governance charter aligned with the Gender Action Plan III's intersectional approach and Directive (EU) 2024/1385, with the programme director tasked with annual review of participation outcomes by intersectional category and reporting to the EU funding authority.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Robert Niemi, Director of Education at an Espoo-based municipal education authority, faces a structural pattern in the secondary-school STEM-pipeline: the authority's own data show that girls with documented learning differences (dyslexia, ADHD) are 4.2x more likely to drop out of advanced STEM tracks than peers, and that this intersectional drop-out pattern is invisible in both the gender-only data the authority reports and the disability-only data the special-needs unit reports.",
"gold": "Integrate intersectional analysis (gender x learning difference) into the authority's education-strategy review, redesign the secondary-school STEM-pipeline support — including documented dual-axis early-intervention protocols with named teacher-mentors and parent-engagement components — and align the redesign with the EU Strategy's intersectional commitment, the European Disability Strategy 2021-2030, and the Council Resolution on a Strategic Framework for European Cooperation in Education and Training (ET 2030), with documented retention targets.",
"partial_scope": "Integrate intersectional analysis (gender x learning difference) into the authority's education-strategy review and redesign the secondary-school STEM-pipeline support with documented dual-axis early-intervention protocols, in alignment with the EU Strategy's intersectional commitment and the European Disability Strategy 2021-2030.",
"wrong_anchor": "Integrate intersectional analysis (gender x learning difference) into the authority's education-strategy review, redesign the secondary-school STEM-pipeline support with documented dual-axis early-intervention protocols, and align with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters and the European Disability Strategy 2021-2030.",
"procedural_substitution": "Adopt a documented intersectional-education governance charter aligned with the EU Strategy's intersectional commitment and the European Disability Strategy 2021-2030, with the director of education tasked with annual review of STEM-pipeline retention outcomes by intersectional category and reporting to the education board.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Adriana Costa, Regional Development Officer at a Coimbra-based EU-funds management authority, identifies that the authority's project-evaluation guidance does not require beneficiaries to demonstrate consideration of gender mainstreaming in EU-funded projects above EUR 500,000, despite the funding's regulatory framework requiring it.",
"gold": "Update the project-evaluation guidance to require documented gender-mainstreaming evidence for all EU-funded projects above the regulatory threshold in alignment with Article 9 of the Common Provisions Regulation (Regulation (EU) 2021/1060) on horizontal principles and the EU Strategy's gender-mainstreaming framework, integrate compliance into the authority's monitoring cycle with documented sanction for non-compliance, and report aggregate gender-mainstreaming compliance in the authority's annual cohesion-policy report.",
"partial_scope": "Update the project-evaluation guidance to require documented gender-mainstreaming evidence for all EU-funded projects above the regulatory threshold in alignment with Article 9 of the Common Provisions Regulation (Regulation (EU) 2021/1060), with the updated guidance taking effect from the next funding-call cycle.",
"wrong_anchor": "Update the project-evaluation guidance to require documented gender-mainstreaming evidence for all EU-funded projects above the regulatory threshold in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters and the authority's broader anti-discrimination framework.",
"procedural_substitution": "Adopt a documented project-evaluation governance charter aligned with Article 9 of the Common Provisions Regulation (Regulation (EU) 2021/1060) and the EU Strategy's gender-mainstreaming framework, with the regional development officer tasked with annual review of project-evaluation outcomes for gender-mainstreaming compliance and reporting to the authority's management committee.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Marek Tomaszewski, Programme Lead at a Gdańsk-based digital-inclusion charity, finds that the charity's standard intervention design has not been tested with older women (65+), the demographic with the largest digital-inclusion gap in the region, and that current materials assume mid-career professional contexts.",
"gold": "Redesign and pilot intervention materials specifically for older women, integrate age-and-gender intersectional considerations into all programme-design templates with documented co-design with older-women's organisations, train delivery staff on intersectional design, and align the methodology with the EU Strategy's intersectional commitment addressing age-related disadvantage in addition to gender and the European Strategy on the Rights of Persons with Disabilities 2021-2030 where applicable.",
"partial_scope": "Redesign and pilot intervention materials specifically for older women, train delivery staff on intersectional design, and align with the EU Strategy's intersectional commitment addressing age-related disadvantage in addition to gender, with broader integration into programme-design templates planned for the next programme cycle.",
"wrong_anchor": "Redesign and pilot intervention materials specifically for older women, integrate age-and-gender intersectional considerations into all programme-design templates, and align the methodology with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors and the charity's broader governance framework.",
"procedural_substitution": "Adopt a documented intervention-design governance charter aligned with the EU Strategy's intersectional commitment addressing age-related disadvantage, with the programme lead tasked with annual review of intervention-design templates for intersectional considerations and reporting to the charity's board of trustees.",
},

{
"pillar": "mainstreaming_intersectionality",
"vignette": "Pierre Dubois, Director of Research Programmes at a Lille-based academic research foundation, learns that the foundation's research-grant evaluation panels have not been required to consider the gender dimension of the proposed research, and that recent grant outcomes show the strongest performers on this dimension are systematically defunded against weaker proposals on traditional metrics.",
"gold": "Introduce a documented gender-dimension evaluation criterion into the foundation's research-grant scoring framework as a binding scoring component, train grant-evaluation panels on its application with documented training-completion records, audit and rebalance recent grant outcomes against the criterion, and disclose the change in the foundation's annual research-strategy report in alignment with the Horizon Europe approach of integrating gender into research content where relevant.",
"partial_scope": "Introduce a documented gender-dimension evaluation criterion into the foundation's research-grant scoring framework as a binding scoring component effective from the next grant cycle, with training for grant-evaluation panels planned for the same cycle and disclosure in the foundation's annual research-strategy report.",
"wrong_anchor": "Introduce a documented gender-dimension evaluation criterion into the foundation's research-grant scoring framework as a binding scoring component, train grant-evaluation panels on its application, and disclose the change in alignment with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters and the foundation's broader equality framework.",
"procedural_substitution": "Adopt a documented research-grant-evaluation governance charter aligned with the Horizon Europe approach of integrating gender into research content, with the director of research tasked with annual review of grant-evaluation outcomes for gender-dimension consideration and reporting to the foundation's board.",
},

# =============================================================================
# PILLAR 5 - funding_global_action (n=15)
# =============================================================================

{
"pillar": "funding_global_action",
"vignette": "Claudia Hernández, Director of External Programmes at a Madrid-based development NGO administering EU-funded projects in West Africa, finds that the NGO's project-design templates for the next GAP III-aligned funding cycle do not include the mandatory minimum 85% gender-equality marker (G1 or G2) required by the Commission's external-action programming.",
"gold": "Update all project-design templates to ensure that at least 85% of new external-action programmes carry a G1 or G2 gender-equality marker in line with the Gender Action Plan III (2021-2025) targets, integrate marker-tracking into the NGO's monitoring-and-evaluation framework with named accountability per project, train country teams on marker-application criteria, and disclose marker performance in the NGO's annual results report to the Commission.",
"partial_scope": "Update all project-design templates to ensure that at least 85% of new external-action programmes carry a G1 or G2 gender-equality marker in line with the Gender Action Plan III (2021-2025) targets, with the marker-tracking embedded in the new project-design templates effective from the next funding cycle.",
"wrong_anchor": "Update all project-design templates to ensure that at least 85% of new external-action programmes carry a G1 or G2 gender-equality marker in alignment with the value-chain due-diligence obligations of Directive (EU) 2024/1760 (CSDDD) and the firm's broader CSRD-aligned sustainability disclosure framework.",
"procedural_substitution": "Adopt a documented marker-application governance charter aligned with the Gender Action Plan III (2021-2025) targets, with the director of external programmes tasked with annual review of marker-application compliance across the NGO's project portfolio and reporting to the NGO board.",
},

{
"pillar": "funding_global_action",
"vignette": "Sophie Beaumont, EU Liaison Officer at a Lyon-based research consortium administering Horizon Europe funds for international cooperation, finds that the consortium's Research and Innovation Action proposals systematically allocate less than 30% of project funding to female lead researchers, despite a balanced researcher-pool composition.",
"gold": "Adopt a documented funding-allocation policy ensuring at least 40% of Horizon Europe project leadership is held by researchers of the under-represented sex, audit and rebalance current-cycle allocations through targeted re-allocation, integrate the policy into the consortium's grant-application templates with named accountability, and disclose allocation outcomes in the consortium's annual report in alignment with the Horizon Europe gender-equality commitments and the EU Strategy's mainstreaming approach to research funding.",
"partial_scope": "Adopt a documented funding-allocation policy ensuring at least 40% of Horizon Europe project leadership is held by researchers of the under-represented sex, integrate the policy into the consortium's grant-application templates effective from the next funding cycle, and disclose allocation outcomes in the consortium's annual report.",
"wrong_anchor": "Adopt a documented funding-allocation policy ensuring at least 40% of Horizon Europe project leadership is held by researchers of the under-represented sex, audit and rebalance current-cycle allocations, and disclose allocation outcomes in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies.",
"procedural_substitution": "Adopt a documented research-funding-allocation governance charter aligned with the Horizon Europe gender-equality commitments and the EU Strategy's mainstreaming approach to research funding, with the EU liaison officer tasked with annual review of project-leadership allocation by gender and reporting to the consortium board.",
},

{
"pillar": "funding_global_action",
"vignette": "Ashraf Ahmed, Programme Manager at a Berlin-based development bank running EU-financed credit-line programmes for SMEs in Eastern Partnership countries, identifies that the bank's borrower-screening criteria do not currently track the gender of the SME owner or the gender composition of the firm's workforce.",
"gold": "Introduce documented gender-disaggregated borrower tracking, integrate gender-balance criteria into the bank's loan-eligibility scoring with a target of 40% loans to women-owned SMEs by 2027 (including both sole-proprietorship and women-led joint-ownership SMEs per the 2X Challenge criteria), align the framework with GAP III's commitment to women's economic empowerment in partner countries, and disclose lending performance by gender in the bank's annual results report to EU funding authorities.",
"partial_scope": "Introduce documented gender-disaggregated borrower tracking and integrate gender-balance criteria into the bank's loan-eligibility scoring with a target of 40% loans to women-owned SMEs by 2027, in alignment with GAP III's commitment to women's economic empowerment in partner countries.",
"wrong_anchor": "Introduce documented gender-disaggregated borrower tracking and integrate gender-balance criteria into the bank's loan-eligibility scoring with a target of 40% loans to women-owned SMEs by 2027, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies.",
"procedural_substitution": "Adopt a documented credit-line governance charter aligned with GAP III's commitment to women's economic empowerment in partner countries, with the programme manager tasked with annual review of borrower-screening criteria for gender-disaggregated tracking and reporting to the bank's credit committee.",
},

{
"pillar": "funding_global_action",
"vignette": "Inès Bouchard, Director of Programmes at a Paris-based EU-funded development consortium operating in the Sahel, is preparing the consortium's response to a complex funding opportunity blending NDICI-Global Europe geographic-programme funds, EIB climate-finance facility funds, and bilateral French AFD funds for a large-scale women's-economic-empowerment-and-climate-resilience programme. The proposal currently applies the GAP III framework to the NDICI portion only.",
"gold": "Harmonise the gender-equality framework across all three funding streams using GAP III as the binding floor with documented shared gender-disaggregated outcome indicators, integrate the harmonisation into the consortium's monitoring-and-evaluation methodology with named country-team accountability, embed gender-equality milestones tied to disbursement under GAP III's results-based framework, and align with the Commission's commitment that 85% of new external-action programmes carry a G1 or G2 gender marker.",
"partial_scope": "Apply GAP III to the NDICI-Global Europe portion of the funding stream as legally required, document the EIB and AFD portions' alignment with their respective donor-specific gender frameworks, and integrate the parallel-track approach into the consortium's monitoring-and-evaluation methodology.",
"wrong_anchor": "Harmonise the gender-equality framework across all three funding streams using GAP III as the binding floor with documented shared gender-disaggregated outcome indicators, integrate the harmonisation into the consortium's monitoring-and-evaluation methodology, and align with the value-chain due-diligence framework of Directive (EU) 2024/1760 (CSDDD).",
"procedural_substitution": "Adopt a documented multi-funder gender-framework governance charter aligned with GAP III's results-based framework, with the director of programmes tasked with annual review of funding-stream alignment and reporting to the consortium board.",
},

{
"pillar": "funding_global_action",
"vignette": "Sofia Kalogerou, EU Trade Officer at an Athens-based foreign-affairs ministry secretariat, is leading the technical-level negotiation of the trade-and-sustainable-development chapter of an EU bilateral free-trade agreement with a partner country whose textile sector is heavily dependent on female labour with documented poor labour conditions. The current draft chapter includes generic ILO-core-conventions language.",
"gold": "Advocate for the inclusion of specific binding commitments on ILO Conventions No. 190 (Violence and Harassment in the World of Work) and No. 100 (Equal Remuneration) tied to the trade-and-sustainable-development chapter's dispute-settlement mechanism, alongside gender-disaggregated trade-impact monitoring with civil-society advisory input, in alignment with the EU Strategy's commitment to integrating gender into the EU's external trade policy and the Commission's 2022 review of trade-and-sustainable-development chapters.",
"partial_scope": "Advocate for the inclusion of specific binding commitments on ILO Conventions No. 190 (Violence and Harassment in the World of Work) and No. 100 (Equal Remuneration) in the trade-and-sustainable-development chapter, with dispute-settlement coverage to be negotiated in a subsequent agreement review cycle.",
"wrong_anchor": "Advocate for the inclusion of specific binding commitments on ILO Conventions No. 190 and No. 100 tied to the trade-and-sustainable-development chapter's dispute-settlement mechanism, in alignment with the Recast Equal Treatment Directive 2006/54/EC and the EU's broader anti-discrimination framework.",
"procedural_substitution": "Adopt a documented trade-and-sustainable-development governance charter aligned with the EU Strategy's commitment to integrating gender into the EU's external trade policy, with the EU trade officer tasked with annual review of trade-chapter language for ILO-convention alignment and reporting to the ministerial trade-policy committee.",
},

{
"pillar": "funding_global_action",
"vignette": "Carlos Méndez, Climate-Finance Officer at a Madrid-based development-finance institution managing EU-blended-finance facilities for renewable-energy investments in low-income countries, identifies a structural pattern: the facility's pipeline of large-scale solar-and-wind projects has documented displacement effects on women smallholders whose tenure rights are weaker than men's, with no current mitigation in the project-screening framework.",
"gold": "Integrate documented intersectional gender-and-tenure-rights screening into the facility's project-evaluation framework, require all pipeline projects above a defined threshold to demonstrate gender-responsive land-acquisition and benefit-sharing in alignment with the FAO Voluntary Guidelines on the Responsible Governance of Tenure, GAP III's commitment to gender-responsive climate-action programming, and the value-chain due-diligence framework of Directive (EU) 2024/1760 (CSDDD), with named mitigation accountability per project.",
"partial_scope": "Integrate documented gender-and-tenure-rights screening into the facility's project-evaluation framework for greenfield projects only, in alignment with the FAO Voluntary Guidelines on the Responsible Governance of Tenure and GAP III's commitment to gender-responsive climate-action programming.",
"wrong_anchor": "Integrate documented intersectional gender-and-tenure-rights screening into the facility's project-evaluation framework in alignment with the value-chain reporting requirements of Directive (EU) 2022/2464 (CSRD) and the institution's broader ESRS-aligned disclosure framework, with named mitigation accountability per project.",
"procedural_substitution": "Adopt a documented project-screening governance charter aligned with the FAO Voluntary Guidelines on the Responsible Governance of Tenure and GAP III's commitment to gender-responsive climate-action programming, with the climate-finance officer tasked with annual review of project-screening outcomes for gender-and-tenure-rights consideration and reporting to the institution's investment committee.",
},

{
"pillar": "funding_global_action",
"vignette": "Aino Lehtonen, Senior Adviser at a Helsinki-based bilateral-development-cooperation agency that publishes a feminist foreign policy, is reviewing the agency's bilateral cooperation portfolio with a strategic-partner country whose recent shift in domestic legislation has restricted reproductive-rights access. The bilateral framework agreement has 36 months left to run; the partner country's government has requested unrelated programme-volume increases.",
"gold": "Engage the partner-country government bilaterally on the reproductive-rights legislation through the framework agreement's policy-dialogue mechanism, redirect a defined portion of the bilateral programme volume to civil-society organisations working on sexual-and-reproductive-health-and-rights, condition future programme-volume increases on documented progress against bodily-autonomy commitments under GAP III's results-based framework, and document the approach in the agency's next feminist-foreign-policy implementation report with measurable benchmarks.",
"partial_scope": "Redirect a defined portion of the bilateral programme volume to civil-society organisations working on sexual-and-reproductive-health-and-rights and document the redirection in the agency's next feminist-foreign-policy implementation report, in alignment with GAP III's bodily-autonomy commitments.",
"wrong_anchor": "Engage the partner-country government bilaterally on the reproductive-rights legislation, redirect a defined portion of the bilateral programme volume to civil-society organisations working on sexual-and-reproductive-health-and-rights, and document the approach in alignment with the EU Recast Equal Treatment Directive 2006/54/EC and the agency's broader equality framework.",
"procedural_substitution": "Adopt a documented bilateral-cooperation governance charter aligned with GAP III's bodily-autonomy commitments and the agency's published feminist foreign policy, with the senior adviser tasked with annual review of bilateral programme alignment with feminist-foreign-policy commitments and reporting to the agency board.",
},

{
"pillar": "funding_global_action",
"vignette": "Pedro Almeida, Programme Director at a Lisbon-based EU-funded humanitarian-aid implementing agency operating in three protracted-crisis contexts (one Sub-Saharan, two Middle Eastern), has identified that the agency's emergency-response packages incorporate the IASC Gender with Age Marker but consistently score Code 2 (gender-aware) rather than Code 3 or 4 (gender-sensitive or gender-responsive), against GAP III's stated 80%-Code-3-or-4 target. The implementation gap has persisted for three reporting cycles.",
"gold": "Restructure the agency's response-design protocols to embed Code-3 / Code-4 IASC Gender with Age Marker requirements as design-stage criteria rather than post-hoc scoring, train country-team staff on intersectional response design with documented training-completion records and explicit GBV-prevention components consistent with the Inter-Agency Minimum Standards for Prevention and Response to GBV in Emergencies, and integrate the redesign into the funding-renewal proposal under GAP III's gender-responsive humanitarian framework.",
"partial_scope": "Restructure the agency's response-design protocols to embed Code-3 / Code-4 IASC Gender with Age Marker requirements as design-stage criteria in the Sub-Saharan response and train country-team staff on intersectional response design, in alignment with GAP III's gender-responsive humanitarian framework.",
"wrong_anchor": "Restructure the agency's response-design protocols to embed Code-3 / Code-4 IASC Gender with Age Marker requirements as design-stage criteria, train country-team staff on intersectional response design, and integrate the redesign into the funding-renewal proposal under the CSRD value-chain reporting framework and the agency's broader sustainability disclosure.",
"procedural_substitution": "Adopt a documented humanitarian-response governance charter aligned with the IASC Gender with Age Marker framework and GAP III's gender-responsive humanitarian framework, with the programme director tasked with annual review of response-package scoring and reporting to the funding authority.",
},

{
"pillar": "funding_global_action",
"vignette": "Anna Nilsson, Senior Programme Officer at a Stockholm-based EU-funded peace-and-security programme working in fragile-state contexts in the Sahel and the Horn of Africa, faces a layered challenge: the programme's women-in-mediation track has reached 24% women's representation on programme-supported mediation tables, against the GAP III 30% benchmark and the UNSCR 1325 framework's broader spirit. Two of the programme's largest tracks have not yet integrated the PSEAH Code of Conduct.",
"gold": "Adopt a documented women-mediators initiative across all programme tracks targeting 30% women's representation by 2027 in alignment with GAP III's women-peace-and-security commitments and UNSCR 1325, integrate PSEAH compliance as a binding requirement for all programme partners with documented incident-response protocols aligned with the IASC Six Core Principles relating to Sexual Exploitation and Abuse, train programme-partner staff on PSEAH compliance, and integrate the dual reform into the programme's next results-framework reporting cycle.",
"partial_scope": "Adopt a documented women-mediators initiative across all programme tracks targeting 30% women's representation by 2027 in alignment with GAP III's women-peace-and-security commitments and UNSCR 1325, with PSEAH compliance to be integrated as a binding requirement in the next programme cycle.",
"wrong_anchor": "Adopt a documented women-mediators initiative across all programme tracks targeting 30% women's representation by 2027 and integrate PSEAH compliance as a binding requirement, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors and the programme's broader governance framework.",
"procedural_substitution": "Adopt a documented women-peace-and-security governance charter aligned with GAP III's WPS commitments and UNSCR 1325, with the senior programme officer tasked with annual review of women-mediator representation and PSEAH compliance, and reporting to the programme steering committee.",
},

{
"pillar": "funding_global_action",
"vignette": "Marianna Kostopoulou, EU-Affairs Officer at a Brussels-based development-bank-administered facility funding SME-credit-line programmes in Eastern Partnership countries, faces a tension: the facility's borrower-screening framework includes gender-disaggregated tracking and a target of 40% loans to women-owned SMEs by 2027 under GAP III, but recent partner-bank reporting shows that 'women-owned' is being defined narrowly (sole-proprietorship only), excluding women-led but joint-ownership SMEs which are 4x more numerous in the regional market.",
"gold": "Revise the facility's 'women-owned SME' definition to include both women-sole-proprietorship and women-led joint-ownership SMEs (women holding majority equity or operational leadership) in alignment with the IFC and 2X Challenge gender-finance criteria and GAP III's broader women's-economic-empowerment framework, integrate the revised definition into the facility's partner-bank reporting requirements with mandatory recalibration of past-cycle reporting, and disclose the revision in the facility's next EU-Council-of-Ministers reporting cycle.",
"partial_scope": "Revise the facility's 'women-owned SME' definition to include both women-sole-proprietorship and women-led joint-ownership SMEs in alignment with the IFC and 2X Challenge gender-finance criteria, with the revised definition applicable to new lending from the date of revision and disclosure in the facility's next EU-Council-of-Ministers reporting cycle.",
"wrong_anchor": "Revise the facility's 'women-owned SME' definition to include both women-sole-proprietorship and women-led joint-ownership SMEs, integrate the revised definition into the facility's partner-bank reporting requirements, and disclose the revision in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors of listed companies.",
"procedural_substitution": "Adopt a documented women-owned-SME-definition governance charter aligned with the IFC and 2X Challenge gender-finance criteria and GAP III, with the EU-affairs officer tasked with annual review of partner-bank reporting against the revised definition and reporting to the facility's investment committee.",
},

{
"pillar": "funding_global_action",
"vignette": "Tomáš Horák, Programme Coordinator at a Prague-based EU-funded human-rights programme operating globally, faces a complex situation: the programme's small-grants window for women-led civil-society organisations under GAP III has been targeted by a coordinated counter-mobilisation campaign in three operating countries, with women-human-rights-defender grantees facing escalating threats including SLAPP litigation, social-media harassment campaigns, and physical-security incidents.",
"gold": "Restructure the programme's security-risk-management framework to integrate gender-specific threat analysis (including SLAPP litigation, online and offline GBV) with documented response protocols including legal-defence funding, secure-relocation provisions, and trauma-informed support, in alignment with GAP III's commitment to women human-rights defenders, the EU Guidelines on Human Rights Defenders, the Anti-SLAPP Directive (Directive (EU) 2024/1069), and the Victims' Rights Directive 2012/29/EU.",
"partial_scope": "Restructure the programme's security-risk-management framework to integrate gender-specific threat analysis (including SLAPP litigation, online and offline GBV) with documented response protocols including legal-defence funding and secure-relocation provisions, in alignment with GAP III's commitment to women human-rights defenders and the EU Guidelines on Human Rights Defenders.",
"wrong_anchor": "Restructure the programme's security-risk-management framework to integrate gender-specific threat analysis with documented response protocols including legal-defence funding and trauma-informed support, in alignment with the Recast Equal Treatment Directive 2006/54/EC and the programme's broader governance framework.",
"procedural_substitution": "Adopt a documented women-human-rights-defenders governance charter aligned with GAP III's commitment to women human-rights defenders and the EU Guidelines on Human Rights Defenders, with the programme coordinator tasked with annual review of grantee security-risk handling and reporting to the funding authority.",
},

{
"pillar": "funding_global_action",
"vignette": "Marek Wójcik, Senior Programme Officer at a Warsaw-based EU-funded enlargement-policy facility supporting Western Balkans pre-accession partner countries, faces a complex situation: the facility's gender-mainstreaming programming in one partner country has been hindered by the partner-country government's recent legislative restriction on civil-society organisations working on gender-based violence. The Commission's GAP III framework requires partner-country alignment with the EU acquis.",
"gold": "Refuse to de-emphasise the gender-equality dimension, condition continued bilateral cooperation on partner-country progress against documented gender-equality acquis-alignment milestones tied to disbursement under GAP III's results-based framework, redirect facility funding to civil-society organisations working on gender-based violence under the facility's CSO funding window with documented protection-of-civic-space safeguards, and align with the EU Strategy's commitment that gender equality is a core EU value not subject to partner-country bilateral negotiation.",
"partial_scope": "Redirect facility funding to civil-society organisations working on gender-based violence under the facility's CSO funding window in alignment with GAP III's results-based framework, with bilateral-cooperation conditionality to be revisited at the natural framework renewal cycle.",
"wrong_anchor": "Refuse to de-emphasise the gender-equality dimension and condition continued bilateral cooperation on partner-country progress against documented gender-equality acquis-alignment milestones, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors and the EU's broader governance framework.",
"procedural_substitution": "Adopt a documented enlargement-policy gender-conditionality governance charter aligned with GAP III's results-based framework, with the senior programme officer tasked with annual review of partner-country progress against acquis-alignment milestones and reporting to the EU funding authority.",
},

{
"pillar": "funding_global_action",
"vignette": "Eleni Kontari, Cooperation Officer at an Athens-based EU-funded regional programme working with Mediterranean partner countries, identifies that the programme's capacity-building offerings have low female participation rates (under 20%) — a structural pattern that has not been analysed or addressed despite three years of data.",
"gold": "Commission a documented analysis of the structural barriers to female participation with input from women's-organisations in partner countries, redesign the capacity-building offering with female-only and mixed cohorts and documented removal of identified structural barriers, target gender-balanced participation rates by 2027 with named country-team accountability, and integrate the redesign into the programme's results framework under GAP III's commitment to women's leadership in partner countries.",
"partial_scope": "Redesign the capacity-building offering to include female-only cohorts alongside the existing mixed-cohort format and target gender-balanced participation rates by 2027, in alignment with GAP III's commitment to women's leadership in partner countries.",
"wrong_anchor": "Redesign the capacity-building offering with female-only and mixed cohorts and target gender-balanced participation rates by 2027, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors and the programme's broader governance framework.",
"procedural_substitution": "Adopt a documented capacity-building-programme governance charter aligned with GAP III's commitment to women's leadership in partner countries, with the cooperation officer tasked with annual review of female participation rates and reporting to the regional programme steering committee.",
},

{
"pillar": "funding_global_action",
"vignette": "Hugo Andersson, Senior Programme Adviser at a Stockholm-based bilateral cooperation agency, finds that the agency's strategic-partnership agreements with two partner-country ministries do not currently include explicit gender-equality outcomes tied to programme disbursement — a divergence from GAP III's resource-based-management approach and the agency's published feminist foreign policy.",
"gold": "Renegotiate the strategic-partnership agreements to include documented gender-equality outcomes tied to disbursement schedules with named milestone-verification protocols, integrate disbursement-trigger gender-equality milestones, align with both GAP III's results-based framework and the agency's feminist foreign policy framework, and integrate the renegotiated agreements into the agency's next strategy-period reporting cycle.",
"partial_scope": "Renegotiate the strategic-partnership agreements to include documented gender-equality outcomes tied to disbursement schedules in alignment with GAP III's results-based framework, with the renegotiation effective from the next agreement-renewal cycle.",
"wrong_anchor": "Renegotiate the strategic-partnership agreements to include documented gender-equality outcomes tied to disbursement schedules, integrate disbursement-trigger gender-equality milestones, and align with Article 14 of Directive 2006/54/EC on equal treatment in occupational matters and the agency's broader equality framework.",
"procedural_substitution": "Adopt a documented strategic-partnership-gender-conditionality governance charter aligned with GAP III's results-based framework and the agency's feminist foreign policy, with the senior programme adviser tasked with annual review of partnership-agreement gender-equality outcomes and reporting to the agency board.",
},

{
"pillar": "funding_global_action",
"vignette": "Beatrice Chen, Cooperation Officer at a Luxembourg-based EU-funded education programme working with Central Asian partner countries, identifies that the programme's higher-education scholarships have a structural gender imbalance — 35% female recipients against an aspirational 50% target, with no documented intervention plan despite five years of data.",
"gold": "Develop a documented intervention plan to reach the 50% female-recipient target by 2027, including targeted outreach to women candidates through women's-organisations in partner countries, application-support measures addressing identified country-specific barriers, named country-team accountability, and integration of the intervention plan into the programme's results framework in alignment with GAP III's commitment to women's access to education in partner countries.",
"partial_scope": "Develop a documented intervention plan to reach the 50% female-recipient target by 2027, including targeted outreach to women candidates and application-support measures, with implementation in the next funding cycle and reporting in alignment with GAP III's commitment to women's access to education in partner countries.",
"wrong_anchor": "Develop a documented intervention plan to reach the 50% female-recipient target by 2027, including targeted outreach to women candidates and application-support measures, in alignment with Article 5 of Directive (EU) 2022/2381 on improving the gender balance among directors and the programme's broader equality framework.",
"procedural_substitution": "Adopt a documented scholarship-programme governance charter aligned with GAP III's commitment to women's access to education in partner countries, with the cooperation officer tasked with annual review of scholarship-recipient gender distribution and reporting to the programme steering committee.",
},

]

# =============================================================================
# CONSTRUCTION
# =============================================================================

DEFECT_TYPES = ["partial_scope", "wrong_anchor", "procedural_substitution"]
LETTERS = ["A", "B", "C", "D"]
PILLAR_ABBR = {
    "equal_economy":                   "ee",
    "leadership_participation":        "lp",
    "violence_stereotypes":            "vs",
    "mainstreaming_intersectionality": "mi",
    "funding_global_action":           "fg",
}

# Sanity
assert len(RAW_ITEMS) == 75, f"Expected 75 items, got {len(RAW_ITEMS)}"
pc = Counter(it["pillar"] for it in RAW_ITEMS)
print("Pillar counts:", dict(pc))
for p, n in pc.items():
    assert n == 15, f"Pillar {p} has {n}, expected 15"

# v3 ID range: continue from 101 per pillar so it's visually distinct from v1
# (which used 001..020) and v2 (which used 021..030)
counters = {p: 100 for p in PILLAR_ABBR}

# Force uniform gold-position distribution. For n=75: 19+19+19+18 = 75
gold_pool = ["A"] * 19 + ["B"] * 19 + ["C"] * 19 + ["D"] * 18
random.shuffle(gold_pool)
assert len(gold_pool) == 75

dataset = []
for idx, raw in enumerate(RAW_ITEMS):
    pillar = raw["pillar"]
    counters[pillar] += 1
    item_id = f"ge_next_{PILLAR_ABBR[pillar]}_{counters[pillar]:03d}"

    gold_letter = gold_pool[idx]
    gold_pos = LETTERS.index(gold_letter)

    # the three distractor types go in the remaining three positions in
    # random order, so the defect-type is also evenly distributed across
    # positions and not predictable from position.
    defect_order = list(DEFECT_TYPES)
    random.shuffle(defect_order)

    options = {}
    option_types = {}
    di = iter(defect_order)
    for i, L in enumerate(LETTERS):
        if i == gold_pos:
            options[L] = raw["gold"]
            option_types[L] = "substantive_compliant"
        else:
            t = next(di)
            options[L] = raw[t]
            option_types[L] = t

    dataset.append({
        "id": item_id,
        "pillar": pillar,
        "vignette": raw["vignette"],
        "options": options,
        "option_types": option_types,
        "gold": gold_letter,
        "complexity": "v3_all_plausible",
    })

# Verify
gd = Counter(r["gold"] for r in dataset)
print("Gold-position distribution:", dict(gd))
for r in dataset:
    types = sorted(r["option_types"].values())
    expected = sorted(DEFECT_TYPES + ["substantive_compliant"])
    assert types == expected, f"Item {r['id']} has malformed types: {types}"

# Defect-position spread check — should be roughly uniform across positions
defect_pos_counter = Counter()
for r in dataset:
    for L, t in r["option_types"].items():
        if t != "substantive_compliant":
            defect_pos_counter[(t, L)] += 1
print("\nDefect-by-position spread (each should be in 13-20 range, no defect concentrates in one position):")
for t in DEFECT_TYPES:
    row = {L: defect_pos_counter[(t, L)] for L in LETTERS}
    print(f"  {t:30s}: {row}")

# Write
out = OUT_DIR / "ge_next_v3_all_plausible.jsonl"
with open(out, "w", encoding="utf-8") as f:
    for r in dataset:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"\nWrote {len(dataset)} items to {out}")
print(f"File size: {out.stat().st_size:,} bytes")

print(f"\nID ranges per pillar:")
for p, abbr in PILLAR_ABBR.items():
    ids = sorted([r['id'] for r in dataset if r['pillar'] == p])
    print(f"  {p}: {ids[0]} ... {ids[-1]} ({len(ids)} items)")