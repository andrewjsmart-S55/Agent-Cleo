# DecideWright Comprehensive Risk Analysis Survey Framework

## Overview

This document outlines four versions of the DecideWright Quantitative Risk Analysis (QRA) survey system designed to assess business risks across the 16 dimensions of the Value Orchestration Canvas (VOC). The survey system adapts based on business model and geographic operations to provide relevant, actionable risk insights.

### Survey Versions

1. **Initial Survey - Scale Version**: Quick assessment using 1-5 scales (2 risk factors per dimension = 32 questions)
2. **Initial Survey - Data Version**: Quick assessment using quantitative data (2 risk factors per dimension = 32 questions)
3. **Detailed Survey - Scale Version**: Comprehensive assessment using 1-5 scales (4 risk factors per dimension = 64 questions)
4. **Detailed Survey - Data Version**: Comprehensive assessment using quantitative data (4 risk factors per dimension = 64 questions)

### Risk Exposure Metrics Calculated

All surveys generate the following quantitative risk metrics through multivariate analysis and Monte Carlo simulation:

1. **Opex at Risk** - Operating expenditure exposure
2. **Capex at Risk** - Capital expenditure exposure
3. **Stratex at Risk** - Strategic expenditure exposure
4. **Revenue at Risk** - Revenue stream vulnerability
5. **Productivity Time at Risk** - Time/efficiency losses
6. **Service Availability at Risk** OR **Product at Risk** (business model dependent)
7. **Reputation at Risk** - Brand and reputation damage exposure
8. **Enterprise Value at Risk** - Overall enterprise value vulnerability

---

## Section 1: Company Registration & Basic Information

### 1.1 Company Registration
- **Company Name**: [Text field]
- **Industry**: [Dropdown - GICS classification]
- **Company Size**:
  - [ ] Micro (1-10 employees)
  - [ ] Small (11-50 employees)
  - [ ] Medium (51-250 employees)
  - [ ] Large (251-1000 employees)
  - [ ] Enterprise (1000+ employees)

### 1.2 Business Model Selection
**Primary Business Model**: [Dropdown]
1. Transaction/Sales (Retail, E-commerce)
2. Fee-for-Service (Consulting, Professional Services)
3. Subscription/Recurring Revenue (SaaS, Memberships)
4. B2B Sales/Wholesale
5. Manufacturing/Production
6. Platform/Marketplace
7. Advertising/Media
8. Franchise
9. Freemium
10. Licensing/IP

### 1.3 Geographic Operations
- **Headquarters Country**: [Dropdown - all countries]
- **Headquarters Region**: [Auto-populated based on country]
  - Europe
  - North America
  - South America
  - Asia
  - Oceania
  - Africa

- **Operational Regions** (Select all that apply):
  - [ ] Europe
  - [ ] North America
  - [ ] South America
  - [ ] Asia
  - [ ] Oceania
  - [ ] Africa

### 1.4 IT Operations & Infrastructure
- **Primary IT Infrastructure**:
  - [ ] On-premises
  - [ ] Cloud-based
  - [ ] Hybrid
  - [ ] Managed by third party

- **Critical Systems Count**: [Number field]
- **IT Team Size**: [Number field]

---

## Section 2: INITIAL SURVEY - SCALE VERSION (1-5)

**Instructions**: For each risk factor, rate your organization on a scale of 1-5, where:
- **1 = Very Low Risk** (Excellent controls, minimal exposure)
- **2 = Low Risk** (Good controls, limited exposure)
- **3 = Medium Risk** (Adequate controls, moderate exposure)
- **4 = High Risk** (Weak controls, significant exposure)
- **5 = Very High Risk** (Poor/no controls, critical exposure)

### DOMAIN 1: ENABLERS

#### Dimension 1: Brand

**1.1 Brand Awareness Risk**
*How vulnerable is your organization to low brand recognition in your target markets?*
- [ ] 1 - Very Low Risk (Dominant brand recognition >80%)
- [ ] 2 - Low Risk (Strong recognition 60-80%)
- [ ] 3 - Medium Risk (Moderate recognition 40-60%)
- [ ] 4 - High Risk (Limited recognition 20-40%)
- [ ] 5 - Very High Risk (Minimal recognition <20%)

**1.2 Brand Reputation Risk**
*How exposed is your brand to reputational damage from negative events or customer experiences?*
- [ ] 1 - Very Low Risk (Excellent reputation management, proactive monitoring)
- [ ] 2 - Low Risk (Good reputation systems, regular monitoring)
- [ ] 3 - Medium Risk (Basic reputation management)
- [ ] 4 - High Risk (Limited reputation monitoring)
- [ ] 5 - Very High Risk (No reputation management, recent crises)

#### Dimension 2: Culture

**2.1 Employee Engagement Risk**
*How vulnerable is your organization to low employee engagement and motivation?*
- [ ] 1 - Very Low Risk (Highly engaged workforce, >80% engagement)
- [ ] 2 - Low Risk (Engaged workforce, 65-80% engagement)
- [ ] 3 - Medium Risk (Moderate engagement, 50-65%)
- [ ] 4 - High Risk (Low engagement, 35-50%)
- [ ] 5 - Very High Risk (Disengaged workforce, <35%)

**2.2 Culture-Strategy Alignment Risk**
*How misaligned is your organizational culture with your strategic objectives?*
- [ ] 1 - Very Low Risk (Perfect alignment, culture drives strategy)
- [ ] 2 - Low Risk (Strong alignment, minor gaps)
- [ ] 3 - Medium Risk (Moderate alignment, some conflicts)
- [ ] 4 - High Risk (Poor alignment, significant conflicts)
- [ ] 5 - Very High Risk (Complete misalignment, culture blocks strategy)

#### Dimension 3: Technology

**3.1 Technology Reliability Risk**
*How vulnerable is your organization to technology failures and downtime?*
- [ ] 1 - Very Low Risk (99.99%+ uptime, redundant systems)
- [ ] 2 - Low Risk (99.9% uptime, good backup systems)
- [ ] 3 - Medium Risk (99% uptime, basic backups)
- [ ] 4 - High Risk (95-99% uptime, frequent issues)
- [ ] 5 - Very High Risk (<95% uptime, critical failures)

**3.2 Cybersecurity Posture Risk**
*How exposed is your organization to cyber threats and data breaches?*
- [ ] 1 - Very Low Risk (Enterprise-grade security, SOC 2/ISO 27001 certified)
- [ ] 2 - Low Risk (Strong security controls, regular audits)
- [ ] 3 - Medium Risk (Basic security measures)
- [ ] 4 - High Risk (Minimal security, known vulnerabilities)
- [ ] 5 - Very High Risk (No security program, recent breaches)

#### Dimension 4: People

**4.1 Key Person Dependency Risk**
*How vulnerable is your organization to the loss of key individuals?*
- [ ] 1 - Very Low Risk (No single points of failure, deep bench)
- [ ] 2 - Low Risk (Limited dependencies, good succession plans)
- [ ] 3 - Medium Risk (Some key dependencies, basic succession plans)
- [ ] 4 - High Risk (High dependencies on few individuals)
- [ ] 5 - Very High Risk (Critical dependencies, no succession planning)

**4.2 Talent Retention Risk**
*How vulnerable is your organization to losing critical talent?*
- [ ] 1 - Very Low Risk (Retention >95%, highly competitive packages)
- [ ] 2 - Low Risk (Retention 90-95%, good packages)
- [ ] 3 - Medium Risk (Retention 80-90%, market-rate packages)
- [ ] 4 - High Risk (Retention 70-80%, below-market packages)
- [ ] 5 - Very High Risk (Retention <70%, high turnover)

#### Dimension 5: Third Parties

**5.1 Supplier Dependency Risk**
*How vulnerable is your organization to supplier failures or disruptions?*
- [ ] 1 - Very Low Risk (Diversified supplier base, multiple alternatives)
- [ ] 2 - Low Risk (Multiple suppliers, good alternatives)
- [ ] 3 - Medium Risk (Limited suppliers, some alternatives)
- [ ] 4 - High Risk (Few suppliers, limited alternatives)
- [ ] 5 - Very High Risk (Single suppliers for critical inputs)

**5.2 Third-Party Reliability Risk**
*How exposed is your organization to third-party service failures?*
- [ ] 1 - Very Low Risk (Enterprise SLAs, proven reliability >99.9%)
- [ ] 2 - Low Risk (Strong SLAs, good reliability 99-99.9%)
- [ ] 3 - Medium Risk (Standard SLAs, moderate reliability 95-99%)
- [ ] 4 - High Risk (Weak SLAs, frequent issues)
- [ ] 5 - Very High Risk (No SLAs, unreliable partners)

### DOMAIN 2: EXECUTION

#### Dimension 6: Processes

**6.1 Process Efficiency Risk**
*How vulnerable is your organization to inefficient processes and waste?*
- [ ] 1 - Very Low Risk (Lean processes, continuous improvement culture)
- [ ] 2 - Low Risk (Efficient processes, regular optimization)
- [ ] 3 - Medium Risk (Adequate processes, some inefficiencies)
- [ ] 4 - High Risk (Inefficient processes, significant waste)
- [ ] 5 - Very High Risk (Highly inefficient, no process management)

**6.2 Process Documentation Risk**
*How exposed is your organization to undocumented or unclear processes?*
- [ ] 1 - Very Low Risk (All critical processes documented and current)
- [ ] 2 - Low Risk (Most processes documented)
- [ ] 3 - Medium Risk (Some documentation, gaps exist)
- [ ] 4 - High Risk (Minimal documentation, tribal knowledge)
- [ ] 5 - Very High Risk (No documentation, chaos)

#### Dimension 7: Change

**7.1 Change Readiness Risk**
*How vulnerable is your organization to change initiatives failing due to lack of readiness?*
- [ ] 1 - Very Low Risk (High change maturity, strong change culture)
- [ ] 2 - Low Risk (Good change readiness, structured approach)
- [ ] 3 - Medium Risk (Moderate readiness, some resistance)
- [ ] 4 - High Risk (Low readiness, significant resistance)
- [ ] 5 - Very High Risk (Change-averse culture, consistent failures)

**7.2 Change Failure Rate Risk**
*How exposed is your organization to failed change initiatives?*
- [ ] 1 - Very Low Risk (Success rate >90%)
- [ ] 2 - Low Risk (Success rate 75-90%)
- [ ] 3 - Medium Risk (Success rate 50-75%)
- [ ] 4 - High Risk (Success rate 25-50%)
- [ ] 5 - Very High Risk (Success rate <25%)

#### Dimension 8: Innovation

**8.1 Innovation Investment Risk**
*How vulnerable is your organization to under-investment in innovation?*
- [ ] 1 - Very Low Risk (>15% revenue to R&D/innovation)
- [ ] 2 - Low Risk (10-15% to innovation)
- [ ] 3 - Medium Risk (5-10% to innovation)
- [ ] 4 - High Risk (2-5% to innovation)
- [ ] 5 - Very High Risk (<2% to innovation)

**8.2 Innovation Success Rate Risk**
*How exposed is your organization to failed innovation efforts?*
- [ ] 1 - Very Low Risk (>50% of innovations successful)
- [ ] 2 - Low Risk (30-50% success rate)
- [ ] 3 - Medium Risk (15-30% success rate)
- [ ] 4 - High Risk (5-15% success rate)
- [ ] 5 - Very High Risk (<5% success rate)

#### Dimension 9: Products & Services

**9.1 Product Quality Risk**
*How vulnerable is your organization to product/service quality issues?*
- [ ] 1 - Very Low Risk (Defect rate <0.1%, world-class quality)
- [ ] 2 - Low Risk (Defect rate 0.1-0.5%, high quality)
- [ ] 3 - Medium Risk (Defect rate 0.5-2%, acceptable quality)
- [ ] 4 - High Risk (Defect rate 2-5%, quality issues)
- [ ] 5 - Very High Risk (Defect rate >5%, serious quality problems)

**9.2 Product-Market Fit Risk**
*How exposed is your organization to poor product-market fit?*
- [ ] 1 - Very Low Risk (Perfect fit, high demand, >40% market share)
- [ ] 2 - Low Risk (Strong fit, good demand, 20-40% share)
- [ ] 3 - Medium Risk (Adequate fit, moderate demand, 10-20% share)
- [ ] 4 - High Risk (Weak fit, low demand, 5-10% share)
- [ ] 5 - Very High Risk (Poor fit, minimal demand, <5% share)

### DOMAIN 3: VALUE

#### Dimension 10: Annual Results

**10.1 Revenue Stability Risk**
*How vulnerable is your organization to revenue volatility and unpredictability?*
- [ ] 1 - Very Low Risk (Highly predictable, <5% variance)
- [ ] 2 - Low Risk (Predictable, 5-10% variance)
- [ ] 3 - Medium Risk (Moderate stability, 10-20% variance)
- [ ] 4 - High Risk (Volatile, 20-40% variance)
- [ ] 5 - Very High Risk (Highly volatile, >40% variance)

**10.2 Profitability Risk**
*How exposed is your organization to profitability erosion?*
- [ ] 1 - Very Low Risk (Highly profitable, >20% net margin)
- [ ] 2 - Low Risk (Profitable, 10-20% net margin)
- [ ] 3 - Medium Risk (Marginally profitable, 5-10% net margin)
- [ ] 4 - High Risk (Break-even, 0-5% net margin)
- [ ] 5 - Very High Risk (Unprofitable, negative margins)

#### Dimension 11: Strategic Goals

**11.1 Goal Achievement Rate Risk**
*How vulnerable is your organization to missing strategic objectives?*
- [ ] 1 - Very Low Risk (Consistently achieve >90% of goals)
- [ ] 2 - Low Risk (Achieve 75-90% of goals)
- [ ] 3 - Medium Risk (Achieve 50-75% of goals)
- [ ] 4 - High Risk (Achieve 25-50% of goals)
- [ ] 5 - Very High Risk (Achieve <25% of goals)

**11.2 Strategy Clarity Risk**
*How exposed is your organization to unclear or poorly communicated strategy?*
- [ ] 1 - Very Low Risk (Crystal clear strategy, >90% understand)
- [ ] 2 - Low Risk (Clear strategy, 75-90% understand)
- [ ] 3 - Medium Risk (Somewhat clear, 50-75% understand)
- [ ] 4 - High Risk (Unclear, 25-50% understand)
- [ ] 5 - Very High Risk (No clear strategy, <25% understand)

#### Dimension 12: Reputation

**12.1 Customer Satisfaction Risk**
*How vulnerable is your organization to customer dissatisfaction?*
- [ ] 1 - Very Low Risk (CSAT >90%, NPS >50)
- [ ] 2 - Low Risk (CSAT 80-90%, NPS 30-50)
- [ ] 3 - Medium Risk (CSAT 70-80%, NPS 10-30)
- [ ] 4 - High Risk (CSAT 60-70%, NPS 0-10)
- [ ] 5 - Very High Risk (CSAT <60%, NPS <0)

**12.2 Stakeholder Perception Risk**
*How exposed is your organization to negative stakeholder perceptions?*
- [ ] 1 - Very Low Risk (Excellent reputation with all stakeholders)
- [ ] 2 - Low Risk (Good reputation, minor concerns)
- [ ] 3 - Medium Risk (Mixed reputation, some issues)
- [ ] 4 - High Risk (Poor reputation, significant concerns)
- [ ] 5 - Very High Risk (Damaged reputation, crisis level)

### DOMAIN 4: ECONOMICS

#### Dimension 13: Financials

**13.1 Financial Health Risk**
*How vulnerable is your organization to financial distress?*
- [ ] 1 - Very Low Risk (Strong ratios, >12 months runway)
- [ ] 2 - Low Risk (Good ratios, 9-12 months runway)
- [ ] 3 - Medium Risk (Adequate ratios, 6-9 months runway)
- [ ] 4 - High Risk (Weak ratios, 3-6 months runway)
- [ ] 5 - Very High Risk (Critical ratios, <3 months runway)

**13.2 Funding Adequacy Risk**
*How exposed is your organization to insufficient capital?*
- [ ] 1 - Very Low Risk (Over-capitalized, multiple funding sources)
- [ ] 2 - Low Risk (Well-capitalized, good access to capital)
- [ ] 3 - Medium Risk (Adequately capitalized, some access)
- [ ] 4 - High Risk (Under-capitalized, limited access)
- [ ] 5 - Very High Risk (Critically under-capitalized, no access)

#### Dimension 14: Business Model

**14.1 Business Model Resilience Risk**
*How vulnerable is your business model to disruption?*
- [ ] 1 - Very Low Risk (Proven resilient, adapted successfully)
- [ ] 2 - Low Risk (Resilient, minor adaptations needed)
- [ ] 3 - Medium Risk (Moderately resilient, some vulnerabilities)
- [ ] 4 - High Risk (Fragile, significant vulnerabilities)
- [ ] 5 - Very High Risk (Threatened, fundamental challenges)

**14.2 Revenue Diversity Risk**
*How exposed is your organization to revenue concentration?*
- [ ] 1 - Very Low Risk (Highly diversified, no customer >5%)
- [ ] 2 - Low Risk (Diversified, largest customer 5-10%)
- [ ] 3 - Medium Risk (Moderate diversity, largest 10-20%)
- [ ] 4 - High Risk (Concentrated, largest 20-40%)
- [ ] 5 - Very High Risk (Highly concentrated, largest >40%)

#### Dimension 15: External Environment

**15.1 Market Volatility Risk**
*How vulnerable is your organization to market fluctuations?*
- [ ] 1 - Very Low Risk (Stable market, predictable demand)
- [ ] 2 - Low Risk (Mostly stable, minor fluctuations)
- [ ] 3 - Medium Risk (Moderate volatility)
- [ ] 4 - High Risk (High volatility, unpredictable)
- [ ] 5 - Very High Risk (Extreme volatility, constant disruption)

**15.2 Regulatory Risk**
*How exposed is your organization to regulatory changes?*
- [ ] 1 - Very Low Risk (Stable regulations, good compliance)
- [ ] 2 - Low Risk (Predictable regulations, compliant)
- [ ] 3 - Medium Risk (Some regulatory uncertainty)
- [ ] 4 - High Risk (Significant regulatory changes expected)
- [ ] 5 - Very High Risk (Major regulatory threats, non-compliance)

#### Dimension 16: Governance

**16.1 Governance Structure Risk**
*How vulnerable is your organization to governance failures?*
- [ ] 1 - Very Low Risk (Exemplary governance, independent board)
- [ ] 2 - Low Risk (Strong governance, clear oversight)
- [ ] 3 - Medium Risk (Adequate governance, some gaps)
- [ ] 4 - High Risk (Weak governance, significant gaps)
- [ ] 5 - Very High Risk (Poor governance, no oversight)

**16.2 Compliance Posture Risk**
*How exposed is your organization to compliance violations?*
- [ ] 1 - Very Low Risk (Full compliance, robust programs)
- [ ] 2 - Low Risk (Compliant, good programs)
- [ ] 3 - Medium Risk (Mostly compliant, some gaps)
- [ ] 4 - High Risk (Compliance issues, weak programs)
- [ ] 5 - Very High Risk (Non-compliant, major violations)

---

## Section 3: INITIAL SURVEY - DATA VERSION

**Instructions**: For each risk factor, provide actual quantitative data. If data is not available, you can estimate or use the scale fallback option.

### DOMAIN 1: ENABLERS

#### Dimension 1: Brand

**1.1 Brand Awareness Risk**

*Unaided brand awareness in primary market:*
- **Percentage**: [___]%
- **OR** If not measured, rate awareness:
  - [ ] Very High (>80%) = Score 1
  - [ ] High (60-80%) = Score 2
  - [ ] Medium (40-60%) = Score 3
  - [ ] Low (20-40%) = Score 4
  - [ ] Very Low (<20%) = Score 5

*Top-of-mind brand awareness:*
- **Percentage**: [___]%
- **OR** If not measured, select: [Same scale as above]

**1.2 Brand Reputation Risk**

*Net Promoter Score (NPS):*
- **Score**: [___] (Range: -100 to +100)
- **OR** If not measured:
  - [ ] Excellent (>50) = Score 1
  - [ ] Good (30-50) = Score 2
  - [ ] Fair (10-30) = Score 3
  - [ ] Poor (0-10) = Score 4
  - [ ] Critical (<0) = Score 5

*Number of reputation incidents in past 12 months:*
- **Count**: [___] incidents
- **Severity of most recent incident**:
  - [ ] None = Score 1
  - [ ] Minor = Score 2
  - [ ] Moderate = Score 3
  - [ ] Serious = Score 4
  - [ ] Critical = Score 5

#### Dimension 2: Culture

**2.1 Employee Engagement Risk**

*Employee engagement score:*
- **Percentage**: [___]%
- **OR** If not measured:
  - [ ] Very High (>80%) = Score 1
  - [ ] High (65-80%) = Score 2
  - [ ] Medium (50-65%) = Score 3
  - [ ] Low (35-50%) = Score 4
  - [ ] Very Low (<35%) = Score 5

*Employee turnover rate (annual):*
- **Percentage**: [___]%
- **Industry benchmark for your sector**: [___]%

**2.2 Culture-Strategy Alignment Risk**

*Percentage of employees who can articulate company strategy:*
- **Percentage**: [___]%
- **OR** If not measured:
  - [ ] Very High (>80%) = Score 1
  - [ ] High (65-80%) = Score 2
  - [ ] Medium (50-65%) = Score 3
  - [ ] Low (35-50%) = Score 4
  - [ ] Very Low (<35%) = Score 5

*Number of cultural barriers identified to strategy execution:*
- **Count**: [___] barriers

#### Dimension 3: Technology

**3.1 Technology Reliability Risk**

*System uptime (annual average):*
- **Percentage**: [___]%
- **Target uptime**: [___]%

*Number of critical system failures in past 12 months:*
- **Count**: [___] failures
- **Average downtime per incident**: [___] hours

*Mean Time To Repair (MTTR):*
- **Hours**: [___] hours
- **OR** If not tracked:
  - [ ] Excellent (<1 hour) = Score 1
  - [ ] Good (1-4 hours) = Score 2
  - [ ] Fair (4-8 hours) = Score 3
  - [ ] Poor (8-24 hours) = Score 4
  - [ ] Critical (>24 hours) = Score 5

**3.2 Cybersecurity Posture Risk**

*Security incidents in past 12 months:*
- **Count**: [___] incidents
- **Number resulting in data breach**: [___]

*Percentage of systems with current security patches:*
- **Percentage**: [___]%

*Last security audit/penetration test:*
- **Date**: [MM/YYYY]
- **Critical findings**: [___] (count)

*Cybersecurity certifications held:*
- [ ] ISO 27001
- [ ] SOC 2
- [ ] PCI DSS
- [ ] Other: [___]
- [ ] None

#### Dimension 4: People

**4.1 Key Person Dependency Risk**

*Number of roles with single-person dependencies:*
- **Count**: [___] roles
- **Total critical roles**: [___]

*Percentage of critical knowledge documented:*
- **Percentage**: [___]%
- **OR** If not assessed:
  - [ ] Very High (>80%) = Score 1
  - [ ] High (60-80%) = Score 2
  - [ ] Medium (40-60%) = Score 3
  - [ ] Low (20-40%) = Score 4
  - [ ] Very Low (<20%) = Score 5

**4.2 Talent Retention Risk**

*Annual employee retention rate:*
- **Percentage**: [___]%
- **Retention rate for high performers**: [___]%

*Average tenure of key employees:*
- **Years**: [___] years

*Percentage of positions filled internally:*
- **Percentage**: [___]%

#### Dimension 5: Third Parties

**5.1 Supplier Dependency Risk**

*Number of critical single-source suppliers:*
- **Count**: [___] suppliers
- **Total critical suppliers**: [___]

*Percentage of spend with top supplier:*
- **Percentage**: [___]%
- **Top 3 suppliers**: [___]%

*Average time to switch suppliers:*
- **Months**: [___] months

**5.2 Third-Party Reliability Risk**

*Number of third-party service disruptions in past 12 months:*
- **Count**: [___] disruptions
- **Total downtime caused**: [___] hours

*Percentage of third parties with SLAs:*
- **Percentage**: [___]%

*Average third-party SLA compliance:*
- **Percentage**: [___]%

### DOMAIN 2: EXECUTION

#### Dimension 6: Processes

**6.1 Process Efficiency Risk**

*Overall process efficiency rating:*
- **Percentage**: [___]% efficient
- **OR** Waste/rework percentage: [___]%

*Average cycle time vs. industry benchmark:*
- **Your cycle time**: [___] days
- **Industry benchmark**: [___] days
- **Variance**: [___]%

*Number of process bottlenecks identified:*
- **Count**: [___] bottlenecks

**6.2 Process Documentation Risk**

*Percentage of critical processes documented:*
- **Percentage**: [___]%

*Last process documentation review:*
- **Date**: [MM/YYYY]
- **Frequency of reviews**: [___] (times per year)

*Number of processes with outdated documentation:*
- **Count**: [___] processes

#### Dimension 7: Change

**7.1 Change Readiness Risk**

*Change readiness assessment score:*
- **Score**: [___]/100
- **OR** If not assessed:
  - [ ] Very High (>80) = Score 1
  - [ ] High (65-80) = Score 2
  - [ ] Medium (50-65) = Score 3
  - [ ] Low (35-50) = Score 4
  - [ ] Very Low (<35) = Score 5

*Percentage of employees who received change management training:*
- **Percentage**: [___]%

**7.2 Change Failure Rate Risk**

*Number of change initiatives in past 12 months:*
- **Initiated**: [___]
- **Completed successfully**: [___]
- **Failed or abandoned**: [___]
- **Success rate**: [___]%

*Average time overrun for change projects:*
- **Percentage**: [___]% over planned timeline

#### Dimension 8: Innovation

**8.1 Innovation Investment Risk**

*Annual R&D/innovation spending:*
- **Amount**: $[___]
- **As percentage of revenue**: [___]%

*Number of innovation initiatives underway:*
- **Count**: [___] initiatives

**8.2 Innovation Success Rate Risk**

*Innovation projects launched in past 3 years:*
- **Total launched**: [___]
- **Commercially successful**: [___]
- **Success rate**: [___]%

*Time from concept to market:*
- **Average months**: [___] months
- **Industry benchmark**: [___] months

#### Dimension 9: Products & Services

**9.1 Product Quality Risk**

*Product/service defect rate:*
- **Percentage**: [___]%
- **OR** Defects per thousand: [___]

*Customer complaints per 1000 transactions:*
- **Count**: [___]

*Return/refund rate:*
- **Percentage**: [___]%

**9.2 Product-Market Fit Risk**

*Market share in primary segment:*
- **Percentage**: [___]%

*Customer acquisition cost (CAC):*
- **Amount**: $[___]

*Customer lifetime value (LTV):*
- **Amount**: $[___]
- **LTV:CAC ratio**: [___]:1

*Product/service adoption rate:*
- **Percentage**: [___]% of target market

### DOMAIN 3: VALUE

#### Dimension 10: Annual Results

**10.1 Revenue Stability Risk**

*Annual revenue:*
- **Current year**: $[___]
- **Previous year**: $[___]
- **Variance**: [___]%

*Revenue predictability:*
- **Percentage of recurring revenue**: [___]%
- **Average revenue variance**: [___]%

*Largest customer as percentage of revenue:*
- **Percentage**: [___]%

**10.2 Profitability Risk**

*Current profitability metrics:*
- **Gross margin**: [___]%
- **Operating margin (EBITDA)**: [___]%
- **Net profit margin**: [___]%

*Trend vs. previous year:*
- [ ] Improving
- [ ] Stable
- [ ] Declining

*Cash burn rate (if applicable):*
- **Monthly**: $[___]
- **Runway**: [___] months

#### Dimension 11: Strategic Goals

**11.1 Goal Achievement Rate Risk**

*Strategic goals set for current year:*
- **Total goals**: [___]
- **On track to achieve**: [___]
- **Behind schedule**: [___]
- **Achievement rate**: [___]%

*Historical goal achievement rate:*
- **Past year**: [___]%
- **Past 3 years average**: [___]%

**11.2 Strategy Clarity Risk**

*Strategy communication effectiveness:*
- **Percentage of employees who can state top 3 strategic priorities**: [___]%

*Strategy refresh frequency:*
- **Last strategy review**: [MM/YYYY]
- **Review frequency**: [___] (times per year)

*Number of strategic pivots in past 3 years:*
- **Count**: [___] pivots

#### Dimension 12: Reputation

**12.1 Customer Satisfaction Risk**

*Customer satisfaction score (CSAT):*
- **Score**: [___]%

*Net Promoter Score (NPS):*
- **Score**: [___] (Range: -100 to +100)

*Customer churn rate (annual):*
- **Percentage**: [___]%

**12.2 Stakeholder Perception Risk**

*Online reputation score:*
- **Average rating**: [___]/5
- **Number of reviews**: [___]

*Media mentions sentiment:*
- **Positive**: [___]%
- **Neutral**: [___]%
- **Negative**: [___]%

*Stakeholder satisfaction scores:*
- **Investors**: [___]/10
- **Employees**: [___]/10
- **Partners**: [___]/10
- **Community**: [___]/10

### DOMAIN 4: ECONOMICS

#### Dimension 13: Financials

**13.1 Financial Health Risk**

*Key financial ratios:*
- **Current ratio**: [___]
- **Quick ratio**: [___]
- **Debt-to-equity ratio**: [___]

*Working capital:*
- **Amount**: $[___]
- **As months of operating expenses**: [___] months

*Credit rating (if applicable):*
- **Rating**: [___]
- **Outlook**: [ ] Positive [ ] Stable [ ] Negative

**13.2 Funding Adequacy Risk**

*Current cash and equivalents:*
- **Amount**: $[___]

*Cash runway at current burn rate:*
- **Months**: [___] months

*Available credit facilities:*
- **Total available**: $[___]
- **Currently utilized**: $[___]

*Next funding requirement:*
- **Expected date**: [MM/YYYY]
- **Amount needed**: $[___]

#### Dimension 14: Business Model

**14.1 Business Model Resilience Risk**

*Years operating with current business model:*
- **Years**: [___]

*Business model disruptions faced (past 3 years):*
- **Count**: [___]
- **Successfully adapted**: [ ] Yes [ ] No [ ] Partially

*Competitive moat strength:*
- **Score**: [___]/10
- **OR** Rate strength:
  - [ ] Very Strong (defensible) = Score 1
  - [ ] Strong = Score 2
  - [ ] Moderate = Score 3
  - [ ] Weak = Score 4
  - [ ] Very Weak (easily disrupted) = Score 5

**14.2 Revenue Diversity Risk**

*Revenue concentration:*
- **Largest customer**: [___]%
- **Top 5 customers**: [___]%
- **Top 10 customers**: [___]%

*Number of revenue streams:*
- **Count**: [___] distinct streams

*Geographic revenue distribution:*
- **Primary region**: [___]%
- **Secondary region**: [___]%
- **Other regions**: [___]%

#### Dimension 15: External Environment

**15.1 Market Volatility Risk**

*Market growth rate:*
- **Current year**: [___]%
- **Volatility (std deviation)**: [___]%

*Demand predictability:*
- **Forecast accuracy**: [___]%
- **Lead time visibility**: [___] months

*Number of market disruptions (past 12 months):*
- **Count**: [___] disruptions

**15.2 Regulatory Risk**

*Current regulatory compliance status:*
- **Number of applicable regulations**: [___]
- **Compliance rate**: [___]%

*Regulatory changes anticipated (next 12 months):*
- **Count**: [___] changes
- **Estimated compliance cost**: $[___]

*Recent regulatory violations:*
- **Count (past 3 years)**: [___]
- **Total fines/penalties**: $[___]

#### Dimension 16: Governance

**16.1 Governance Structure Risk**

*Board composition:*
- **Total board members**: [___]
- **Independent directors**: [___]
- **Board meetings per year**: [___]

*Board effectiveness score:*
- **Score**: [___]/10
- **OR** Rate effectiveness:
  - [ ] Excellent = Score 1
  - [ ] Good = Score 2
  - [ ] Fair = Score 3
  - [ ] Poor = Score 4
  - [ ] Inadequate = Score 5

**16.2 Compliance Posture Risk**

*Compliance program maturity:*
- **Years program in place**: [___]
- **Full-time compliance staff**: [___]

*Compliance audit results (most recent):*
- **Date**: [MM/YYYY]
- **Findings**: [___] issues
- **Critical findings**: [___]

*Compliance training completion rate:*
- **Percentage**: [___]%

---

## Section 4: DETAILED SURVEY - SCALE VERSION (1-5)

**Instructions**: For each risk factor, rate your organization on a scale of 1-5, where:
- **1 = Very Low Risk** (Excellent controls, minimal exposure)
- **2 = Low Risk** (Good controls, limited exposure)
- **3 = Medium Risk** (Adequate controls, moderate exposure)
- **4 = High Risk** (Weak controls, significant exposure)
- **5 = Very High Risk** (Poor/no controls, critical exposure)

### DOMAIN 1: ENABLERS

#### Dimension 1: Brand

**1.1 Brand Awareness Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**1.2 Brand Reputation Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**1.3 Brand Differentiation Risk**
*How vulnerable is your brand to being perceived as indistinguishable from competitors?*
- [ ] 1 - Very Low Risk (Highly differentiated, unique positioning)
- [ ] 2 - Low Risk (Well differentiated, clear unique value)
- [ ] 3 - Medium Risk (Some differentiation, not always clear)
- [ ] 4 - High Risk (Limited differentiation, similar to competitors)
- [ ] 5 - Very High Risk (No differentiation, commodity status)

**1.4 Brand Consistency Risk**
*How exposed is your organization to inconsistent brand experience across touchpoints?*
- [ ] 1 - Very Low Risk (Perfectly consistent, strong brand guidelines)
- [ ] 2 - Low Risk (Mostly consistent, minor variations)
- [ ] 3 - Medium Risk (Moderately consistent, some gaps)
- [ ] 4 - High Risk (Inconsistent, confusing experience)
- [ ] 5 - Very High Risk (Highly inconsistent, no brand standards)

#### Dimension 2: Culture

**2.1 Employee Engagement Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**2.2 Culture-Strategy Alignment Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**2.3 Leadership Effectiveness Risk**
*How vulnerable is your organization to ineffective leadership?*
- [ ] 1 - Very Low Risk (Exceptional leaders, high trust)
- [ ] 2 - Low Risk (Effective leaders, good trust)
- [ ] 3 - Medium Risk (Adequate leadership, moderate trust)
- [ ] 4 - High Risk (Weak leadership, low trust)
- [ ] 5 - Very High Risk (Poor leadership, no trust)

**2.4 Organizational Agility Risk**
*How exposed is your organization to inability to adapt quickly?*
- [ ] 1 - Very Low Risk (Highly agile, rapid adaptation)
- [ ] 2 - Low Risk (Agile, good adaptation capability)
- [ ] 3 - Medium Risk (Moderately agile, some bureaucracy)
- [ ] 4 - High Risk (Slow, significant bureaucracy)
- [ ] 5 - Very High Risk (Rigid, unable to adapt)

#### Dimension 3: Technology

**3.1 Technology Reliability Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**3.2 Cybersecurity Posture Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**3.3 Technical Debt Risk**
*How vulnerable is your organization to accumulated technical debt?*
- [ ] 1 - Very Low Risk (Minimal debt, modern architecture)
- [ ] 2 - Low Risk (Limited debt, manageable)
- [ ] 3 - Medium Risk (Moderate debt, some legacy systems)
- [ ] 4 - High Risk (Significant debt, aging systems)
- [ ] 5 - Very High Risk (Critical debt, obsolete systems)

**3.4 Technology Innovation Capability Risk**
*How exposed is your organization to inability to adopt new technologies?*
- [ ] 1 - Very Low Risk (Cutting-edge adopter, innovation leader)
- [ ] 2 - Low Risk (Early adopter, good innovation)
- [ ] 3 - Medium Risk (Mainstream adopter, moderate innovation)
- [ ] 4 - High Risk (Late adopter, limited innovation)
- [ ] 5 - Very High Risk (Laggard, no innovation capability)

#### Dimension 4: People

**4.1 Key Person Dependency Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**4.2 Talent Retention Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**4.3 Skills Gap Risk**
*How vulnerable is your organization to critical skills shortages?*
- [ ] 1 - Very Low Risk (No gaps, comprehensive skills)
- [ ] 2 - Low Risk (Minor gaps, mostly covered)
- [ ] 3 - Medium Risk (Some gaps, hiring/training needed)
- [ ] 4 - High Risk (Significant gaps, limiting capability)
- [ ] 5 - Very High Risk (Critical gaps, major capability issues)

**4.4 Succession Planning Risk**
*How exposed is your organization to lack of succession plans?*
- [ ] 1 - Very Low Risk (Robust plans for all key roles)
- [ ] 2 - Low Risk (Good plans for most key roles)
- [ ] 3 - Medium Risk (Plans for some key roles)
- [ ] 4 - High Risk (Few plans, major gaps)
- [ ] 5 - Very High Risk (No succession plans)

#### Dimension 5: Third Parties

**5.1 Supplier Dependency Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**5.2 Third-Party Reliability Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**5.3 Contract Terms Risk**
*How vulnerable is your organization to unfavorable third-party contract terms?*
- [ ] 1 - Very Low Risk (Favorable terms, strong protection)
- [ ] 2 - Low Risk (Good terms, adequate protection)
- [ ] 3 - Medium Risk (Fair terms, moderate protection)
- [ ] 4 - High Risk (Unfavorable terms, limited protection)
- [ ] 5 - Very High Risk (Very unfavorable, no protection)

**5.4 Third-Party Relationship Quality Risk**
*How exposed is your organization to poor third-party relationships?*
- [ ] 1 - Very Low Risk (Excellent relationships, strategic partners)
- [ ] 2 - Low Risk (Good relationships, collaborative)
- [ ] 3 - Medium Risk (Adequate relationships, transactional)
- [ ] 4 - High Risk (Poor relationships, contentious)
- [ ] 5 - Very High Risk (Hostile relationships, frequent disputes)

### DOMAIN 2: EXECUTION

#### Dimension 6: Processes

**6.1 Process Efficiency Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**6.2 Process Documentation Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**6.3 Process Automation Risk**
*How vulnerable is your organization to manual, error-prone processes?*
- [ ] 1 - Very Low Risk (Highly automated, minimal manual work)
- [ ] 2 - Low Risk (Well automated, some manual tasks)
- [ ] 3 - Medium Risk (Moderately automated, many manual tasks)
- [ ] 4 - High Risk (Limited automation, mostly manual)
- [ ] 5 - Very High Risk (No automation, all manual)

**6.4 Process Compliance Risk**
*How exposed is your organization to non-compliant processes?*
- [ ] 1 - Very Low Risk (All processes compliant, regular audits)
- [ ] 2 - Low Risk (Mostly compliant, occasional audits)
- [ ] 3 - Medium Risk (Compliant with gaps, irregular audits)
- [ ] 4 - High Risk (Compliance issues, rare audits)
- [ ] 5 - Very High Risk (Non-compliant, no audits)

#### Dimension 7: Change

**7.1 Change Readiness Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**7.2 Change Failure Rate Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**7.3 Change Velocity Risk**
*How vulnerable is your organization to slow change implementation?*
- [ ] 1 - Very Low Risk (Rapid change, agile)
- [ ] 2 - Low Risk (Good change speed)
- [ ] 3 - Medium Risk (Moderate speed, some delays)
- [ ] 4 - High Risk (Slow change, frequent delays)
- [ ] 5 - Very High Risk (Very slow, gridlock)

**7.4 Stakeholder Resistance Risk**
*How exposed is your organization to change resistance?*
- [ ] 1 - Very Low Risk (Embraced change culture)
- [ ] 2 - Low Risk (Limited resistance)
- [ ] 3 - Medium Risk (Moderate resistance)
- [ ] 4 - High Risk (Strong resistance)
- [ ] 5 - Very High Risk (Overwhelming resistance)

#### Dimension 8: Innovation

**8.1 Innovation Investment Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**8.2 Innovation Success Rate Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**8.3 R&D Effectiveness Risk**
*How vulnerable is your organization to ineffective R&D efforts?*
- [ ] 1 - Very Low Risk (Highly effective R&D, strong ROI)
- [ ] 2 - Low Risk (Effective R&D, good ROI)
- [ ] 3 - Medium Risk (Moderately effective, acceptable ROI)
- [ ] 4 - High Risk (Ineffective R&D, poor ROI)
- [ ] 5 - Very High Risk (Failed R&D, negative ROI)

**8.4 Market Responsiveness Risk**
*How exposed is your organization to slow market response?*
- [ ] 1 - Very Low Risk (First to market, rapid response)
- [ ] 2 - Low Risk (Fast follower, good response)
- [ ] 3 - Medium Risk (Moderate response, sometimes late)
- [ ] 4 - High Risk (Slow response, often late)
- [ ] 5 - Very High Risk (Very slow, always late to market)

#### Dimension 9: Products & Services

**9.1 Product Quality Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**9.2 Product-Market Fit Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**9.3 Product Lifecycle Risk**
*How vulnerable is your organization to product obsolescence?*
- [ ] 1 - Very Low Risk (Continuous innovation, long runway)
- [ ] 2 - Low Risk (Regular updates, good runway)
- [ ] 3 - Medium Risk (Periodic updates, moderate runway)
- [ ] 4 - High Risk (Rare updates, aging products)
- [ ] 5 - Very High Risk (No updates, obsolete products)

**9.4 Competitive Positioning Risk**
*How exposed is your organization to competitive displacement?*
- [ ] 1 - Very Low Risk (Market leader, strong moat)
- [ ] 2 - Low Risk (Strong position, defensible)
- [ ] 3 - Medium Risk (Competitive position, some threats)
- [ ] 4 - High Risk (Weak position, significant threats)
- [ ] 5 - Very High Risk (Vulnerable position, imminent threats)

### DOMAIN 3: VALUE

#### Dimension 10: Annual Results

**10.1 Revenue Stability Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**10.2 Profitability Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**10.3 Cash Flow Risk**
*How vulnerable is your organization to cash flow problems?*
- [ ] 1 - Very Low Risk (Strong positive cash flow)
- [ ] 2 - Low Risk (Positive cash flow)
- [ ] 3 - Medium Risk (Break-even cash flow)
- [ ] 4 - High Risk (Negative cash flow, managed)
- [ ] 5 - Very High Risk (Severe cash flow crisis)

**10.4 Growth Trajectory Risk**
*How exposed is your organization to growth stagnation or decline?*
- [ ] 1 - Very Low Risk (Strong growth >20% YoY)
- [ ] 2 - Low Risk (Good growth 10-20% YoY)
- [ ] 3 - Medium Risk (Moderate growth 5-10% YoY)
- [ ] 4 - High Risk (Slow growth 0-5% YoY)
- [ ] 5 - Very High Risk (No growth or declining)

#### Dimension 11: Strategic Goals

**11.1 Goal Achievement Rate Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**11.2 Strategy Clarity Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**11.3 Resource Alignment Risk**
*How vulnerable is your organization to misaligned resource allocation?*
- [ ] 1 - Very Low Risk (Perfect alignment with strategy)
- [ ] 2 - Low Risk (Strong alignment, minor gaps)
- [ ] 3 - Medium Risk (Moderate alignment, some gaps)
- [ ] 4 - High Risk (Poor alignment, major gaps)
- [ ] 5 - Very High Risk (Complete misalignment)

**11.4 Milestone Tracking Risk**
*How exposed is your organization to missed strategic milestones?*
- [ ] 1 - Very Low Risk (All milestones on track)
- [ ] 2 - Low Risk (Most milestones on track)
- [ ] 3 - Medium Risk (Some milestones behind)
- [ ] 4 - High Risk (Many milestones behind)
- [ ] 5 - Very High Risk (All milestones missed)

#### Dimension 12: Reputation

**12.1 Customer Satisfaction Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**12.2 Stakeholder Perception Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**12.3 Crisis Preparedness Risk**
*How vulnerable is your organization to reputational crises?*
- [ ] 1 - Very Low Risk (Robust crisis plans, tested)
- [ ] 2 - Low Risk (Good crisis plans, practiced)
- [ ] 3 - Medium Risk (Basic crisis plans, untested)
- [ ] 4 - High Risk (Weak crisis plans, unprepared)
- [ ] 5 - Very High Risk (No crisis plans, vulnerable)

**12.4 Social Responsibility Risk**
*How exposed is your organization to ESG/CSR criticism?*
- [ ] 1 - Very Low Risk (Industry leader in ESG/CSR)
- [ ] 2 - Low Risk (Strong ESG/CSR program)
- [ ] 3 - Medium Risk (Basic ESG/CSR compliance)
- [ ] 4 - High Risk (Weak ESG/CSR, concerns raised)
- [ ] 5 - Very High Risk (Poor ESG/CSR, major issues)

### DOMAIN 4: ECONOMICS

#### Dimension 13: Financials

**13.1 Financial Health Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**13.2 Funding Adequacy Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**13.3 Debt Burden Risk**
*How vulnerable is your organization to excessive debt?*
- [ ] 1 - Very Low Risk (Minimal debt, strong coverage)
- [ ] 2 - Low Risk (Manageable debt, good coverage)
- [ ] 3 - Medium Risk (Moderate debt, adequate coverage)
- [ ] 4 - High Risk (High debt, weak coverage)
- [ ] 5 - Very High Risk (Excessive debt, no coverage)

**13.4 Financial Controls Risk**
*How exposed is your organization to financial control failures?*
- [ ] 1 - Very Low Risk (Robust controls, SOX compliant)
- [ ] 2 - Low Risk (Strong controls, regular audits)
- [ ] 3 - Medium Risk (Adequate controls, periodic audits)
- [ ] 4 - High Risk (Weak controls, rare audits)
- [ ] 5 - Very High Risk (Poor controls, control failures)

#### Dimension 14: Business Model

**14.1 Business Model Resilience Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**14.2 Revenue Diversity Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**14.3 Pricing Power Risk**
*How vulnerable is your organization to pricing pressure?*
- [ ] 1 - Very Low Risk (Strong pricing power, premium brand)
- [ ] 2 - Low Risk (Good pricing power, value brand)
- [ ] 3 - Medium Risk (Moderate pricing power, competitive)
- [ ] 4 - High Risk (Weak pricing power, price-taker)
- [ ] 5 - Very High Risk (No pricing power, commoditized)

**14.4 Business Model Scalability Risk**
*How exposed is your organization to scalability limitations?*
- [ ] 1 - Very Low Risk (Highly scalable, no constraints)
- [ ] 2 - Low Risk (Scalable, minor constraints)
- [ ] 3 - Medium Risk (Moderately scalable, some constraints)
- [ ] 4 - High Risk (Limited scalability, major constraints)
- [ ] 5 - Very High Risk (Not scalable, fundamental limits)

#### Dimension 15: External Environment

**15.1 Market Volatility Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**15.2 Regulatory Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**15.3 Competitive Pressure Risk**
*How vulnerable is your organization to competitive threats?*
- [ ] 1 - Very Low Risk (Dominant position, high barriers)
- [ ] 2 - Low Risk (Strong position, good barriers)
- [ ] 3 - Medium Risk (Competitive market, moderate barriers)
- [ ] 4 - High Risk (Intense competition, low barriers)
- [ ] 5 - Very High Risk (Hyper-competitive, no barriers)

**15.4 Economic Conditions Risk**
*How exposed is your organization to economic downturns?*
- [ ] 1 - Very Low Risk (Counter-cyclical or recession-proof)
- [ ] 2 - Low Risk (Resilient to downturns)
- [ ] 3 - Medium Risk (Moderately affected by cycles)
- [ ] 4 - High Risk (Highly cyclical)
- [ ] 5 - Very High Risk (Extremely vulnerable to downturns)

#### Dimension 16: Governance

**16.1 Governance Structure Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**16.2 Compliance Posture Risk**
- [ ] 1 - Very Low Risk
- [ ] 2 - Low Risk
- [ ] 3 - Medium Risk
- [ ] 4 - High Risk
- [ ] 5 - Very High Risk

**16.3 Board Effectiveness Risk**
*How vulnerable is your organization to ineffective board governance?*
- [ ] 1 - Very Low Risk (Highly effective, engaged board)
- [ ] 2 - Low Risk (Effective board, good oversight)
- [ ] 3 - Medium Risk (Adequate board, basic oversight)
- [ ] 4 - High Risk (Weak board, limited oversight)
- [ ] 5 - Very High Risk (Ineffective board, no oversight)

**16.4 Risk Management Maturity Risk**
*How exposed is your organization to immature risk management?*
- [ ] 1 - Very Low Risk (Enterprise risk management, mature)
- [ ] 2 - Low Risk (Good risk management, structured)
- [ ] 3 - Medium Risk (Basic risk management, developing)
- [ ] 4 - High Risk (Weak risk management, ad-hoc)
- [ ] 5 - Very High Risk (No risk management)

---

## Section 5: DETAILED SURVEY - DATA VERSION

**Instructions**: For each risk factor, provide actual quantitative data. If data is not available, you can estimate or use the scale fallback option.

### DOMAIN 1: ENABLERS

#### Dimension 1: Brand

**1.1 Brand Awareness Risk**

*Unaided brand awareness in primary market:*
- **Percentage**: [___]%
- **OR** If not measured: [Scale 1-5 as in Initial Survey]

*Top-of-mind brand awareness:*
- **Percentage**: [___]%

**1.2 Brand Reputation Risk**

*Net Promoter Score (NPS):*
- **Score**: [___] (Range: -100 to +100)

*Number of reputation incidents in past 12 months:*
- **Count**: [___] incidents
- **Severity of most recent incident**: [Same scale as Initial Survey]

**1.3 Brand Differentiation Risk**

*Brand differentiation score (market research):*
- **Score**: [___]/100
- **OR** If not measured:
  - [ ] Highly differentiated (>80) = Score 1
  - [ ] Differentiated (60-80) = Score 2
  - [ ] Somewhat differentiated (40-60) = Score 3
  - [ ] Limited differentiation (20-40) = Score 4
  - [ ] Not differentiated (<20) = Score 5

*Unique value propositions clearly communicated:*
- **Count**: [___] UVPs
- **Percentage of customers who can recall**: [___]%

*Brand positioning clarity index:*
- **Score**: [___]/10

**1.4 Brand Consistency Risk**

*Brand consistency audit score:*
- **Score**: [___]/100
- **Last audit date**: [MM/YYYY]

*Number of brand guideline violations (past 12 months):*
- **Count**: [___] violations

*Brand touchpoints audited:*
- **Total touchpoints**: [___]
- **Compliant touchpoints**: [___]
- **Compliance rate**: [___]%

#### Dimension 2: Culture

**2.1 Employee Engagement Risk**

*Employee engagement score:*
- **Percentage**: [___]%

*Employee turnover rate (annual):*
- **Percentage**: [___]%
- **Industry benchmark**: [___]%

**2.2 Culture-Strategy Alignment Risk**

*Percentage of employees who can articulate company strategy:*
- **Percentage**: [___]%

*Number of cultural barriers identified to strategy execution:*
- **Count**: [___] barriers

**2.3 Leadership Effectiveness Risk**

*Leadership effectiveness score (360 review):*
- **Average score**: [___]/100
- **OR** If not measured: [Scale 1-5]

*Leadership trust index:*
- **Score**: [___]/10

*Leadership turnover rate (annual):*
- **Percentage**: [___]%

*Succession readiness for leadership roles:*
- **Percentage with ready successors**: [___]%

**2.4 Organizational Agility Risk**

*Time to implement strategic decisions:*
- **Average months**: [___] months

*Number of organizational layers:*
- **Count**: [___] layers

*Percentage of decisions made at front-line level:*
- **Percentage**: [___]%

*Agility assessment score:*
- **Score**: [___]/100
- **OR** If not measured: [Scale 1-5]

#### Dimension 3: Technology

**3.1 Technology Reliability Risk**

*System uptime (annual average):*
- **Percentage**: [___]%
- **Target uptime**: [___]%

*Number of critical system failures in past 12 months:*
- **Count**: [___] failures
- **Average downtime per incident**: [___] hours

*Mean Time To Repair (MTTR):*
- **Hours**: [___] hours

**3.2 Cybersecurity Posture Risk**

*Security incidents in past 12 months:*
- **Count**: [___] incidents
- **Number resulting in data breach**: [___]

*Percentage of systems with current security patches:*
- **Percentage**: [___]%

*Last security audit/penetration test:*
- **Date**: [MM/YYYY]
- **Critical findings**: [___] (count)

*Cybersecurity certifications held:*
- [ ] ISO 27001
- [ ] SOC 2
- [ ] PCI DSS
- [ ] Other: [___]
- [ ] None

**3.3 Technical Debt Risk**

*Technical debt as percentage of codebase:*
- **Percentage**: [___]%
- **OR** Estimated months to remediate: [___] months

*Number of legacy systems:*
- **Count**: [___] systems
- **Age of oldest critical system**: [___] years

*Technology refresh cycle:*
- **Average years**: [___] years
- **Industry standard**: [___] years

*Percentage of infrastructure beyond vendor support:*
- **Percentage**: [___]%

**3.4 Technology Innovation Capability Risk**

*Technology innovation budget as percentage of IT spend:*
- **Percentage**: [___]%

*Number of new technologies adopted (past 12 months):*
- **Count**: [___] technologies

*Time from technology evaluation to deployment:*
- **Average months**: [___] months

*Technology maturity assessment:*
- **Score**: [___]/100
- **OR** If not assessed: [Scale 1-5]

#### Dimension 4: People

**4.1 Key Person Dependency Risk**

*Number of roles with single-person dependencies:*
- **Count**: [___] roles
- **Total critical roles**: [___]

*Percentage of critical knowledge documented:*
- **Percentage**: [___]%

**4.2 Talent Retention Risk**

*Annual employee retention rate:*
- **Percentage**: [___]%
- **Retention rate for high performers**: [___]%

*Average tenure of key employees:*
- **Years**: [___] years

*Percentage of positions filled internally:*
- **Percentage**: [___]%

**4.3 Skills Gap Risk**

*Number of critical skills gaps identified:*
- **Count**: [___] gaps

*Percentage of roles with adequate skills coverage:*
- **Percentage**: [___]%

*Time to fill critical skill gaps:*
- **Average months**: [___] months

*Training investment per employee (annual):*
- **Amount**: $[___]
- **As percentage of payroll**: [___]%

**4.4 Succession Planning Risk**

*Percentage of key roles with succession plans:*
- **Percentage**: [___]%

*Number of succession plan gaps:*
- **Count**: [___] gaps

*Average readiness time for successors:*
- **Months**: [___] months

*Succession plan testing frequency:*
- **Times per year**: [___]

#### Dimension 5: Third Parties

**5.1 Supplier Dependency Risk**

*Number of critical single-source suppliers:*
- **Count**: [___] suppliers
- **Total critical suppliers**: [___]

*Percentage of spend with top supplier:*
- **Percentage**: [___]%
- **Top 3 suppliers**: [___]%

*Average time to switch suppliers:*
- **Months**: [___] months

**5.2 Third-Party Reliability Risk**

*Number of third-party service disruptions in past 12 months:*
- **Count**: [___] disruptions
- **Total downtime caused**: [___] hours

*Percentage of third parties with SLAs:*
- **Percentage**: [___]%

*Average third-party SLA compliance:*
- **Percentage**: [___]%

**5.3 Contract Terms Risk**

*Percentage of contracts with unfavorable terms:*
- **Percentage**: [___]%

*Number of contract disputes (past 12 months):*
- **Count**: [___] disputes

*Average contract lock-in period:*
- **Months**: [___] months

*Percentage of contracts with exit clauses:*
- **Percentage**: [___]%

**5.4 Third-Party Relationship Quality Risk**

*Third-party relationship satisfaction score:*
- **Average score**: [___]/10

*Number of strategic partnerships:*
- **Count**: [___] partnerships
- **Total third parties**: [___]

*Third-party relationship review frequency:*
- **Times per year**: [___]

*Number of third-party relationship issues (past 12 months):*
- **Count**: [___] issues

### DOMAIN 2: EXECUTION

#### Dimension 6: Processes

**6.1 Process Efficiency Risk**

*Overall process efficiency rating:*
- **Percentage**: [___]% efficient
- **OR** Waste/rework percentage: [___]%

*Average cycle time vs. industry benchmark:*
- **Your cycle time**: [___] days
- **Industry benchmark**: [___] days
- **Variance**: [___]%

*Number of process bottlenecks identified:*
- **Count**: [___] bottlenecks

**6.2 Process Documentation Risk**

*Percentage of critical processes documented:*
- **Percentage**: [___]%

*Last process documentation review:*
- **Date**: [MM/YYYY]
- **Frequency of reviews**: [___] (times per year)

*Number of processes with outdated documentation:*
- **Count**: [___] processes

**6.3 Process Automation Risk**

*Percentage of processes automated:*
- **Percentage**: [___]%

*Number of manual processes in critical path:*
- **Count**: [___] processes

*Automation ROI (if measured):*
- **ROI**: [___]%

*Average time saved per automated process:*
- **Hours per month**: [___] hours

**6.4 Process Compliance Risk**

*Percentage of processes compliance-reviewed:*
- **Percentage**: [___]%

*Number of compliance violations (past 12 months):*
- **Count**: [___] violations

*Last process compliance audit:*
- **Date**: [MM/YYYY]
- **Findings**: [___] issues

*Process compliance training completion rate:*
- **Percentage**: [___]%

#### Dimension 7: Change

**7.1 Change Readiness Risk**

*Change readiness assessment score:*
- **Score**: [___]/100

*Percentage of employees who received change management training:*
- **Percentage**: [___]%

**7.2 Change Failure Rate Risk**

*Number of change initiatives in past 12 months:*
- **Initiated**: [___]
- **Completed successfully**: [___]
- **Failed or abandoned**: [___]
- **Success rate**: [___]%

*Average time overrun for change projects:*
- **Percentage**: [___]% over planned timeline

**7.3 Change Velocity Risk**

*Average time from approval to implementation:*
- **Weeks**: [___] weeks

*Number of change initiatives in progress:*
- **Count**: [___] initiatives

*Change throughput (initiatives per quarter):*
- **Count**: [___] per quarter

*Change backlog size:*
- **Count**: [___] pending initiatives

**7.4 Stakeholder Resistance Risk**

*Stakeholder change acceptance rate:*
- **Percentage**: [___]%

*Number of change rollbacks due to resistance (past 12 months):*
- **Count**: [___] rollbacks

*Change communication effectiveness score:*
- **Score**: [___]/100

*Percentage of stakeholders actively supporting change:*
- **Percentage**: [___]%

#### Dimension 8: Innovation

**8.1 Innovation Investment Risk**

*Annual R&D/innovation spending:*
- **Amount**: $[___]
- **As percentage of revenue**: [___]%

*Number of innovation initiatives underway:*
- **Count**: [___] initiatives

**8.2 Innovation Success Rate Risk**

*Innovation projects launched in past 3 years:*
- **Total launched**: [___]
- **Commercially successful**: [___]
- **Success rate**: [___]%

*Time from concept to market:*
- **Average months**: [___] months
- **Industry benchmark**: [___] months

**8.3 R&D Effectiveness Risk**

*R&D ROI:*
- **ROI percentage**: [___]%

*Number of patents/IP generated (past 3 years):*
- **Count**: [___] patents/IP

*R&D project completion rate:*
- **Percentage**: [___]%

*Average R&D project duration:*
- **Months**: [___] months

**8.4 Market Responsiveness Risk**

*Time to respond to market changes:*
- **Average months**: [___] months

*Number of market opportunities missed (past 12 months):*
- **Count**: [___] opportunities

*Market intelligence gathering frequency:*
- **Times per month**: [___]

*Percentage of revenue from products launched in past 3 years:*
- **Percentage**: [___]%

#### Dimension 9: Products & Services

**9.1 Product Quality Risk**

*Product/service defect rate:*
- **Percentage**: [___]%
- **OR** Defects per thousand: [___]

*Customer complaints per 1000 transactions:*
- **Count**: [___]

*Return/refund rate:*
- **Percentage**: [___]%

**9.2 Product-Market Fit Risk**

*Market share in primary segment:*
- **Percentage**: [___]%

*Customer acquisition cost (CAC):*
- **Amount**: $[___]

*Customer lifetime value (LTV):*
- **Amount**: $[___]
- **LTV:CAC ratio**: [___]:1

*Product/service adoption rate:*
- **Percentage**: [___]% of target market

**9.3 Product Lifecycle Risk**

*Average product lifecycle:*
- **Years**: [___] years

*Number of products in decline phase:*
- **Count**: [___] products
- **Total products**: [___]

*Time since last major product update:*
- **Months**: [___] months

*Percentage of revenue from mature/declining products:*
- **Percentage**: [___]%

**9.4 Competitive Positioning Risk**

*Market position ranking:*
- **Rank**: #[___] in market
- **Total competitors**: [___]

*Competitive win rate:*
- **Percentage**: [___]%

*Number of key differentiators vs. competitors:*
- **Count**: [___] differentiators

*Relative price position:*
- **Percentage vs. market average**: [___]%

### DOMAIN 3: VALUE

#### Dimension 10: Annual Results

**10.1 Revenue Stability Risk**

*Annual revenue:*
- **Current year**: $[___]
- **Previous year**: $[___]
- **Variance**: [___]%

*Revenue predictability:*
- **Percentage of recurring revenue**: [___]%
- **Average revenue variance**: [___]%

*Largest customer as percentage of revenue:*
- **Percentage**: [___]%

**10.2 Profitability Risk**

*Current profitability metrics:*
- **Gross margin**: [___]%
- **Operating margin (EBITDA)**: [___]%
- **Net profit margin**: [___]%

*Trend vs. previous year:*
- [ ] Improving
- [ ] Stable
- [ ] Declining

*Cash burn rate (if applicable):*
- **Monthly**: $[___]
- **Runway**: [___] months

**10.3 Cash Flow Risk**

*Operating cash flow:*
- **Annual**: $[___]
- **Monthly average**: $[___]

*Free cash flow:*
- **Annual**: $[___]

*Cash conversion cycle:*
- **Days**: [___] days

*Percentage of revenue converted to cash:*
- **Percentage**: [___]%

**10.4 Growth Trajectory Risk**

*Revenue growth rate:*
- **YoY**: [___]%
- **3-year CAGR**: [___]%

*Customer growth rate:*
- **YoY**: [___]%

*Market growth rate:*
- **YoY**: [___]%

*Growth sustainability score:*
- **Score**: [___]/100
- **OR** If not assessed: [Scale 1-5]

#### Dimension 11: Strategic Goals

**11.1 Goal Achievement Rate Risk**

*Strategic goals set for current year:*
- **Total goals**: [___]
- **On track to achieve**: [___]
- **Behind schedule**: [___]
- **Achievement rate**: [___]%

*Historical goal achievement rate:*
- **Past year**: [___]%
- **Past 3 years average**: [___]%

**11.2 Strategy Clarity Risk**

*Strategy communication effectiveness:*
- **Percentage of employees who can state top 3 strategic priorities**: [___]%

*Strategy refresh frequency:*
- **Last strategy review**: [MM/YYYY]
- **Review frequency**: [___] (times per year)

*Number of strategic pivots in past 3 years:*
- **Count**: [___] pivots

**11.3 Resource Alignment Risk**

*Percentage of resources aligned to strategic priorities:*
- **Percentage**: [___]%

*Strategic initiative budget vs. total budget:*
- **Percentage**: [___]%

*Number of strategic initiatives under-resourced:*
- **Count**: [___] initiatives

*Resource reallocation frequency:*
- **Times per year**: [___]

**11.4 Milestone Tracking Risk**

*Number of strategic milestones:*
- **Total milestones**: [___]
- **On track**: [___]
- **Behind schedule**: [___]
- **Missed**: [___]

*Average milestone completion variance:*
- **Percentage behind/ahead of schedule**: [___]%

*Milestone tracking cadence:*
- **Reviews per month**: [___]

#### Dimension 12: Reputation

**12.1 Customer Satisfaction Risk**

*Customer satisfaction score (CSAT):*
- **Score**: [___]%

*Net Promoter Score (NPS):*
- **Score**: [___] (Range: -100 to +100)

*Customer churn rate (annual):*
- **Percentage**: [___]%

**12.2 Stakeholder Perception Risk**

*Online reputation score:*
- **Average rating**: [___]/5
- **Number of reviews**: [___]

*Media mentions sentiment:*
- **Positive**: [___]%
- **Neutral**: [___]%
- **Negative**: [___]%

*Stakeholder satisfaction scores:*
- **Investors**: [___]/10
- **Employees**: [___]/10
- **Partners**: [___]/10
- **Community**: [___]/10

**12.3 Crisis Preparedness Risk**

*Crisis management plan status:*
- **Last updated**: [MM/YYYY]
- **Last tested**: [MM/YYYY]

*Crisis team training frequency:*
- **Times per year**: [___]

*Number of potential crisis scenarios documented:*
- **Count**: [___] scenarios

*Crisis response time (target):*
- **Hours**: [___] hours

**12.4 Social Responsibility Risk**

*ESG rating (if available):*
- **Rating**: [___] (specify rating agency)

*Sustainability targets achievement:*
- **Percentage**: [___]%

*Number of ESG/CSR incidents (past 12 months):*
- **Count**: [___] incidents

*CSR budget as percentage of revenue:*
- **Percentage**: [___]%

### DOMAIN 4: ECONOMICS

#### Dimension 13: Financials

**13.1 Financial Health Risk**

*Key financial ratios:*
- **Current ratio**: [___]
- **Quick ratio**: [___]
- **Debt-to-equity ratio**: [___]

*Working capital:*
- **Amount**: $[___]
- **As months of operating expenses**: [___] months

*Credit rating (if applicable):*
- **Rating**: [___]
- **Outlook**: [ ] Positive [ ] Stable [ ] Negative

**13.2 Funding Adequacy Risk**

*Current cash and equivalents:*
- **Amount**: $[___]

*Cash runway at current burn rate:*
- **Months**: [___] months

*Available credit facilities:*
- **Total available**: $[___]
- **Currently utilized**: $[___]

*Next funding requirement:*
- **Expected date**: [MM/YYYY]
- **Amount needed**: $[___]

**13.3 Debt Burden Risk**

*Total debt:*
- **Amount**: $[___]
- **As multiple of EBITDA**: [___]x

*Debt service coverage ratio:*
- **Ratio**: [___]

*Interest coverage ratio:*
- **Ratio**: [___]

*Percentage of debt maturing in next 12 months:*
- **Percentage**: [___]%

**13.4 Financial Controls Risk**

*Last financial audit:*
- **Date**: [MM/YYYY]
- **Type**: [ ] Internal [ ] External [ ] Both

*Number of audit findings (most recent):*
- **Total findings**: [___]
- **Material weaknesses**: [___]

*Financial control testing frequency:*
- **Times per year**: [___]

*Percentage of financial processes with documented controls:*
- **Percentage**: [___]%

#### Dimension 14: Business Model

**14.1 Business Model Resilience Risk**

*Years operating with current business model:*
- **Years**: [___]

*Business model disruptions faced (past 3 years):*
- **Count**: [___]
- **Successfully adapted**: [ ] Yes [ ] No [ ] Partially

*Competitive moat strength:*
- **Score**: [___]/10

**14.2 Revenue Diversity Risk**

*Revenue concentration:*
- **Largest customer**: [___]%
- **Top 5 customers**: [___]%
- **Top 10 customers**: [___]%

*Number of revenue streams:*
- **Count**: [___] distinct streams

*Geographic revenue distribution:*
- **Primary region**: [___]%
- **Secondary region**: [___]%
- **Other regions**: [___]%

**14.3 Pricing Power Risk**

*Pricing vs. competitors:*
- **Percentage premium/discount**: [___]%

*Number of price increases (past 3 years):*
- **Count**: [___] increases
- **Average increase**: [___]%

*Customer price sensitivity:*
- **Churn from last price increase**: [___]%

*Gross margin trend:*
- **Current**: [___]%
- **3 years ago**: [___]%
- **Change**: [___]%

**14.4 Business Model Scalability Risk**

*Marginal cost of serving additional customer:*
- **Amount/Percentage**: $[___] or [___]%

*Revenue per employee:*
- **Amount**: $[___]

*Operating leverage:*
- **Score**: [___]/10
- **OR** Percentage of fixed costs: [___]%

*Capacity utilization:*
- **Percentage**: [___]%

#### Dimension 15: External Environment

**15.1 Market Volatility Risk**

*Market growth rate:*
- **Current year**: [___]%
- **Volatility (std deviation)**: [___]%

*Demand predictability:*
- **Forecast accuracy**: [___]%
- **Lead time visibility**: [___] months

*Number of market disruptions (past 12 months):*
- **Count**: [___] disruptions

**15.2 Regulatory Risk**

*Current regulatory compliance status:*
- **Number of applicable regulations**: [___]
- **Compliance rate**: [___]%

*Regulatory changes anticipated (next 12 months):*
- **Count**: [___] changes
- **Estimated compliance cost**: $[___]

*Recent regulatory violations:*
- **Count (past 3 years)**: [___]
- **Total fines/penalties**: $[___]

**15.3 Competitive Pressure Risk**

*Number of direct competitors:*
- **Count**: [___] competitors

*Market concentration (HHI if known):*
- **Index**: [___]

*Competitive intensity score:*
- **Score**: [___]/10

*Number of new entrants (past 12 months):*
- **Count**: [___] new entrants

**15.4 Economic Conditions Risk**

*Economic sensitivity:*
- **Revenue elasticity to GDP**: [___]

*Exposure to economic indicators:*
- **Primary indicator**: [___]
- **Correlation**: [___]%

*Geographic economic risk distribution:*
- **Percentage of revenue from stable economies**: [___]%
- **Percentage from emerging markets**: [___]%

*Recession preparedness score:*
- **Score**: [___]/100
- **OR** If not assessed: [Scale 1-5]

#### Dimension 16: Governance

**16.1 Governance Structure Risk**

*Board composition:*
- **Total board members**: [___]
- **Independent directors**: [___]
- **Board meetings per year**: [___]

*Board effectiveness score:*
- **Score**: [___]/10

**16.2 Compliance Posture Risk**

*Compliance program maturity:*
- **Years program in place**: [___]
- **Full-time compliance staff**: [___]

*Compliance audit results (most recent):*
- **Date**: [MM/YYYY]
- **Findings**: [___] issues
- **Critical findings**: [___]

*Compliance training completion rate:*
- **Percentage**: [___]%

**16.3 Board Effectiveness Risk**

*Board attendance rate:*
- **Percentage**: [___]%

*Board diversity metrics:*
- **Gender diversity**: [___]%
- **Age range**: [___] to [___] years
- **Industry expertise**: [___] different industries

*Board evaluation frequency:*
- **Times per year**: [___]

*Number of board committees:*
- **Count**: [___] committees

**16.4 Risk Management Maturity Risk**

*Enterprise risk management program age:*
- **Years**: [___] years

*Risk assessment frequency:*
- **Times per year**: [___]

*Number of risk owners assigned:*
- **Count**: [___] owners
- **Percentage of risks with owners**: [___]%

*Risk management framework:*
- [ ] ISO 31000
- [ ] COSO ERM
- [ ] Custom framework
- [ ] No formal framework

---

## Section 6: Adaptive Logic Documentation

### Business Model-Specific Adaptations

The survey system dynamically adjusts certain questions based on the selected business model:

#### 1. Transaction/Sales (Retail, E-commerce)
**Adapted dimensions:**
- **Products & Services**: Focus on inventory management, product quality, merchandising
- **Processes**: Emphasize supply chain, fulfillment, returns
- **External Environment**: Retail market trends, consumer behavior
- **Risk Metric**: **Product at Risk** (inventory obsolescence, quality issues)

#### 2. Fee-for-Service (Consulting, Professional Services)
**Adapted dimensions:**
- **People**: Focus on consultant utilization, expertise retention
- **Products & Services**: Service delivery quality, project success rate
- **Business Model**: Client concentration, pricing models
- **Risk Metric**: **Service Availability at Risk** (consultant availability, delivery capacity)

#### 3. Subscription/Recurring Revenue (SaaS, Memberships)
**Adapted dimensions:**
- **Annual Results**: Focus on MRR/ARR, churn rate, expansion revenue
- **Technology**: Platform uptime, scalability, feature velocity
- **Business Model**: Subscription metrics, LTV, CAC payback
- **Risk Metric**: **Service Availability at Risk** (platform uptime)

#### 4. B2B Sales/Wholesale
**Adapted dimensions:**
- **Third Parties**: Supplier relationships, distribution channels
- **Business Model**: Customer concentration, contract terms
- **External Environment**: B2B market dynamics, procurement trends
- **Risk Metric**: **Product at Risk** + **Revenue at Risk** (order concentration)

#### 5. Manufacturing/Production
**Adapted dimensions:**
- **Processes**: Production efficiency, quality control, safety
- **Third Parties**: Supply chain resilience, raw material sourcing
- **Technology**: Production systems, equipment reliability
- **Risk Metric**: **Product at Risk** (production quality, capacity)

#### 6. Platform/Marketplace
**Adapted dimensions:**
- **Technology**: Platform scalability, transaction processing
- **Products & Services**: Network effects, two-sided market dynamics
- **Business Model**: Take rate, platform liquidity
- **Risk Metric**: **Service Availability at Risk** (platform uptime)

#### 7. Advertising/Media
**Adapted dimensions:**
- **Brand**: Audience reach, content quality
- **Annual Results**: Ad revenue, audience metrics
- **External Environment**: Media consumption trends, advertiser demand
- **Risk Metric**: **Revenue at Risk** (advertiser concentration)

#### 8. Franchise
**Adapted dimensions:**
- **Third Parties**: Franchisee relationships, brand compliance
- **Governance**: Franchise agreement enforcement
- **Brand**: Brand consistency across franchises
- **Risk Metric**: **Reputation at Risk** (franchisee brand compliance)

#### 9. Freemium
**Adapted dimensions:**
- **Business Model**: Conversion rate, feature gating effectiveness
- **Technology**: Free tier infrastructure cost, scalability
- **Products & Services**: Premium feature development
- **Risk Metric**: **Opex at Risk** (free user infrastructure cost)

#### 10. Licensing/IP
**Adapted dimensions:**
- **Innovation**: IP portfolio strength, patent protection
- **Governance**: IP protection, licensing compliance
- **Business Model**: Royalty stream diversity, contract terms
- **Risk Metric**: **Revenue at Risk** (IP infringement, contract expiration)

### Geographic-Specific Adaptations

#### Regulatory Environment by Region:
- **Europe**: GDPR, strict labor laws, environmental regulations
- **North America**: SEC compliance (US), industry-specific regulations
- **South America**: Currency volatility, political stability
- **Asia**: Varied regulatory environments, data sovereignty
- **Oceania**: Sector-specific regulations (Australia/NZ)
- **Africa**: Emerging regulatory frameworks, infrastructure challenges

#### Economic Considerations:
- **Developed Markets** (Europe, North America, Oceania): Focus on competition, innovation, talent
- **Emerging Markets** (Parts of Asia, South America, Africa): Focus on infrastructure, political risk, currency

---

## Section 7: Risk Calculation Methodology

### Multivariate Analysis Approach

DecideWright's Quantitative Risk Analysis uses a sophisticated multivariate approach to calculate the 9 risk exposure metrics:

1. **Data Collection**: Survey responses provide quantitative inputs across 16 dimensions
2. **Risk Factor Scoring**: Each factor is converted to a risk score (1-5 or actual data normalized)
3. **Dimension Aggregation**: Risk factors within each dimension are weighted and combined
4. **Domain Analysis**: Dimensions are aggregated at the domain level (Enablers, Execution, Value, Economics)
5. **Cross-Dimensional Correlation**: The model identifies correlations between dimensions that amplify or mitigate risks
6. **Monte Carlo Simulation**: 10,000+ iterations simulate potential outcomes considering:
   - Probability distributions for each risk factor
   - Correlation matrices between factors
   - Uncertainty ranges provided in data inputs
7. **Risk Metric Calculation**: Each of the 9 metrics is calculated based on:
   - Direct impact factors (e.g., Revenue at Risk influenced by Revenue Stability, Customer Concentration)
   - Indirect impact factors (e.g., Technology Reliability affecting Service Availability)
   - Cascading effects (e.g., Reputation Risk affecting Revenue Risk)

### Risk Exposure Metrics Mapping

#### 1. Opex at Risk
**Primary Influences:**
- Process Efficiency (Execution)
- Technology Reliability (Enablers)
- Third-Party Reliability (Enablers)
- People (Talent Retention, Skills Gap)

#### 2. Capex at Risk
**Primary Influences:**
- Technology (Infrastructure needs, Technical Debt)
- Change (Failed initiatives)
- Innovation (R&D investment effectiveness)
- Financials (Funding adequacy)

#### 3. Stratex at Risk
**Primary Influences:**
- Strategic Goals (Achievement rate, Resource allocation)
- Innovation (Investment, Success rate)
- Change (Readiness, Failure rate)
- External Environment (Market changes)

#### 4. Revenue at Risk
**Primary Influences:**
- Annual Results (Revenue stability, Customer concentration)
- Products & Services (Market fit, Quality)
- Brand (Awareness, Reputation)
- Business Model (Resilience, Diversification)
- Reputation (Customer satisfaction)

#### 5. Productivity Time at Risk
**Primary Influences:**
- Processes (Efficiency, Documentation)
- Technology (Downtime, Reliability)
- People (Engagement, Skills gaps)
- Change (Disruption from initiatives)

#### 6. Service Availability at Risk / Product at Risk
**Primary Influences:**
- Technology (Uptime, Cybersecurity)
- Third Parties (Supplier/Service reliability)
- Processes (Quality control)
- Products & Services (Quality, Lifecycle)

#### 7. Reputation at Risk
**Primary Influences:**
- Reputation (Customer satisfaction, Stakeholder perception)
- Brand (Consistency, Reputation management)
- Governance (Compliance, Governance structure)
- Products & Services (Quality)

#### 8. Enterprise Value at Risk
**Primary Influences:**
- ALL DIMENSIONS (comprehensive aggregation)
- Weighted by business model and industry
- Considers interdependencies and cascading effects

---

## Section 8: Output and Reporting

### Survey Completion Outputs

Upon completion, users receive:

1. **Risk Dashboard**: Visual representation of all 9 risk metrics
2. **Domain Heatmap**: Risk levels across the 4 VOC domains
3. **Dimension Analysis**: Detailed breakdown of risk by dimension
4. **Priority Risk Register**: Top 10 risks ranked by exposure and impact
5. **Comparative Benchmarks**: Industry and size-based comparisons (when available)
6. **Recommended Actions**: Prioritized risk mitigation recommendations
7. **Executive Summary**: 2-page PDF suitable for board presentation
8. **Detailed Report**: Comprehensive risk analysis with methodology

### Data Privacy and Security

- All survey data is encrypted at rest and in transit
- No individual responses are shared without explicit consent
- Aggregate benchmarking data is anonymized
- Compliance with GDPR, CCPA, and other data protection regulations

---

## Appendix: Survey Selection Guide

### When to Use Initial Survey - Scale Version
- **Time**: 15-20 minutes
- **Best for**:
  - Quick risk screening
  - Initial assessment before detailed analysis
  - Organizations without detailed metrics available
  - Rapid risk triage
- **Outputs**: Basic risk profile across all 9 metrics

### When to Use Initial Survey - Data Version
- **Time**: 25-35 minutes
- **Best for**:
  - Organizations with some metrics tracked
  - More accurate initial assessment
  - Baseline for future tracking
  - Supporting funding or investor conversations
- **Outputs**: Quantitative risk profile with moderate precision

### When to Use Detailed Survey - Scale Version
- **Time**: 30-40 minutes
- **Best for**:
  - Comprehensive risk assessment when data is limited
  - Annual risk reviews
  - Board-level risk reporting
  - Strategic planning exercises
- **Outputs**: Detailed risk profile across all dimensions and factors

### When to Use Detailed Survey - Data Version
- **Time**: 45-60 minutes
- **Best for**:
  - Organizations with robust metrics and KPIs
  - Highest precision risk assessment
  - Risk-based decision making (M&A, investment, insurance)
  - Regulatory or compliance requirements
  - Enterprise risk management programs
- **Outputs**: Highly precise, data-driven risk analysis suitable for critical decisions

---

**End of Framework Document**

*For questions or support, please contact DecideWright at support@decidewright.com*
