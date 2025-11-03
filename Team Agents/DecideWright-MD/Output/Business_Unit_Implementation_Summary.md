# Business Unit / Subsidiary Analysis Implementation

**Implementation Date:** 2025-10-29
**Framework Extension:** Single-Company → Multi-Business Unit Analysis
**Sheets Added:** 4 new sheets (22 → 27 total)
**Status:** COMPLETE

---

## Executive Summary

The DecideWright Enterprise Architecture framework has been successfully extended from single-company analysis to support **multiple business units** with consolidated enterprise views. This capability enables:

- **BU-Specific Analysis:** Independent risk and performance assessment for each business unit
- **Consolidated Views:** Enterprise-level rollup (CORP) aggregating all BUs
- **Comparative Analysis:** Side-by-side BU comparison to identify best practices and improvement opportunities
- **Flexible Structure:** Support for geographic regions, product lines, or legal entity (subsidiary) structures

The framework maintains full backward compatibility - all existing data has been preserved and defaulted to the consolidated "CORP" view.

---

## What Was Implemented

### 1. BU Configuration Sheet (NEW)

**Purpose:** Master data definition of all business units in the organization

**Structure:**
- BU_Code (e.g., NA, EMEA, APAC, LATAM, CORP)
- BU_Name (full name of business unit)
- BU_Type (Geographic, Product Line, Legal Entity, Consolidated)
- Region (geographic classification)
- Country (if single-country BU)
- Status (Active, Inactive, Planned)
- Consolidation_Method (how BU rolls into CORP)
- Description (purpose and scope of BU)

**Pre-Configured BUs:**
- **CORP** - Corporate / Consolidated (rollup of all BUs)
- **NA** - North America
- **EMEA** - Europe, Middle East & Africa
- **APAC** - Asia Pacific
- **LATAM** - Latin America

**Flexibility:** The sheet includes templates for alternative BU structures:
- Product Line BUs (e.g., Consumer Banking, Commercial Banking, Wealth Management)
- Legal Entity / Subsidiary BUs (e.g., Parent Company, UK Subsidiary, US Subsidiary)

Organizations can customize to match their actual structure by adding/removing BUs in this configuration sheet.

---

### 2. Enhanced Dimension Sheets (12 MODIFIED)

**Sheets Modified:**
1. Brand
2. Culture
3. People
4. Technology
5. Third Parties
6. Processes
7. Change
8. Innovation
9. Product & Services
10. Annual Results
11. Strategic Goals
12. Reputation

**Change Made:**
- **Business_Unit column added as Column A** to all dimension sheets
- All existing data defaulted to **"CORP"** (consolidated view)
- Column formatting: Green header (RGB 70AD47), bold, 11pt font

**How This Works:**
Each row of dimension data can now be tagged with a specific Business Unit. For example:

| Business_Unit | Element_Name | Maturity_Score | ... |
|---------------|--------------|----------------|-----|
| CORP          | Customer Service | 3.5 | ... |
| NA            | Customer Service | 4.0 | ... |
| EMEA          | Customer Service | 3.0 | ... |
| APAC          | Customer Service | 3.2 | ... |

This enables BU-specific data entry while maintaining a consolidated enterprise view.

**Data Entry Approach:**

**Option 1 - Top-Down (Recommended for Initial Setup):**
1. Keep existing CORP data as the enterprise baseline
2. Add BU-specific rows only where there are material differences
3. Use CORP as a default for capabilities that are centralized (e.g., central IT platform)

**Option 2 - Bottom-Up (Recommended for Mature Organizations):**
1. Replace CORP rows with BU-specific rows for each dimension
2. CORP metrics become calculated rollups from BU data
3. Provides most granular analysis but requires more data entry

---

### 3. BU Risk Dashboard (NEW)

**Purpose:** Business Unit-specific view of all 17 risk metrics

**Structure:**
- Business_Unit (filter to specific BU: NA, EMEA, APAC, LATAM, or CORP for consolidated)
- Risk_Metric (17 metrics matching company-level Risk Dashboard)
- Exposure_Amount (calculated from BU dimension data)
- Calculation_Method (how metric is derived)
- Comparison_to_CORP (BU variance from enterprise average)
- BU_Rank (ranking among all BUs for this metric)

**17 Risk Metrics Included:**
1. Opex at Risk
2. Capex at Risk
3. Stratex at Risk
4. Revenue at Risk
5. Productivity Time at Risk
6. Service Availability at Risk
7. Product at Risk
8. Reputation at Risk
9. Enterprise Value at Risk
10. Liquidity Risk
11. Compliance Risk
12. Cyber Risk
13. Third-Party Risk
14. Operational Risk
15. Strategic Risk
16. Financial Risk
17. ESG Risk

**Calculation Methodology:**
For each BU, apply the **same calculation formulas** as the company-level Risk Dashboard (documented in "Risk Calculations" sheet), but **filter input data** to only include dimension rows where Business_Unit = selected BU.

**Example:**
- Company-level "Opex at Risk" = Sum of all Opex exposure across all rows
- NA "Opex at Risk" = Sum of Opex exposure only for rows where Business_Unit = 'NA'
- CORP "Opex at Risk" = Sum across all BUs (or rollup from BU calculations)

**Use Cases:**
- Compare risk exposure across BUs to identify concentration risks
- Identify which BUs are driving enterprise risk
- Tailor risk mitigation strategies to BU-specific risk profiles
- Support BU-level risk appetite and tolerance setting

---

### 4. BU Performance Dashboard (NEW)

**Purpose:** Business Unit-specific view of all 10 performance metrics

**Structure:**
- Business_Unit (NA, EMEA, APAC, LATAM, CORP)
- Performance_Metric (10 metrics matching company-level Performance Dashboard)
- Current_Value (actual performance for the BU)
- Target_Value (BU-specific target)
- Variance (current vs. target)
- Trend (improving, stable, declining)
- BU_Rank (ranking among BUs)
- Calculation_Method

**10 Performance Metrics Included:**
1. **Probability of Execution (PoE)** - likelihood of achieving BU strategic objectives
2. Strategy Alignment Score
3. Process Maturity Index
4. Control Effectiveness Score
5. Risk-Adjusted Performance Score
6. Strategic Initiative Success Rate
7. Objective Achievement Rate
8. Dependency Fulfillment Rate
9. Resource Utilization Efficiency
10. Performance Momentum

**PoE Calculation for Business Units:**

The Probability of Execution for a BU follows the same methodology as enterprise-level PoE, but filtered to BU-specific data:

**Inputs (filtered by BU):**
- Aligned Processes: Only processes tagged to this BU
- Crystallizing Risks: Only risks impacting this BU's objectives
- Control Effectiveness: Only controls implemented within this BU
- Strategic Objectives: Only objectives owned by this BU
- Interdependencies: Consider both intra-BU and inter-BU dependencies

**Key Difference from Enterprise PoE:**
- **Intra-BU Dependencies:** Objectives within the same BU depending on each other
- **Inter-BU Dependencies:** BU objectives depending on other BUs' objectives (e.g., NA sales objectives depend on APAC product development)

Inter-BU dependencies are critical for PoE calculation - a BU's execution probability may be constrained by dependencies on other BUs not on track.

**Use Cases:**
- Identify which BUs are on track vs. off track for strategic delivery
- Compare performance management maturity across BUs
- Allocate resources to BUs with highest performance potential
- Identify best practice BUs for knowledge transfer

---

### 5. BU Comparison Dashboard (NEW)

**Purpose:** Side-by-side comparison of all BUs across risk and performance metrics

**Structure:**

**Comparison Table Format:**
| Metric_Category | Metric_Name | CORP | NA | EMEA | APAC | LATAM | Best_BU | Worst_BU | Range | Avg_Excl_CORP | Notes |
|-----------------|-------------|------|-----|------|------|--------|---------|----------|-------|---------------|-------|
| Risk | Opex at Risk | $50M | $15M | $20M | $10M | $5M | LATAM | EMEA | $15M | $12.5M | EMEA driven by legacy systems |
| Risk | Cyber Risk | High | Med | High | Low | Med | APAC | EMEA | High-Low | Medium | APAC invested in modern security |
| Performance | PoE | 72% | 80% | 65% | 75% | 78% | NA | EMEA | 15% | 74.5% | EMEA facing execution challenges |

**Sections:**
1. **Risk Comparison** (17 metrics)
   - All risk metrics from BU Risk Dashboard
   - Identifies highest and lowest risk exposure by BU
   - Highlights concentration risks

2. **Performance Comparison** (10 metrics)
   - All performance metrics from BU Performance Dashboard
   - Identifies best and worst performing BUs
   - Calculates variance from average

3. **Derived Insights**
   - Risk/Performance Correlation: Do high-risk BUs have lower performance?
   - Best Practice BUs: Which BUs excel across multiple dimensions?
   - Improvement Opportunities: Which BUs need support?
   - Portfolio Balance: Is risk/performance evenly distributed or concentrated?

**Use Cases:**
- **Strategic Planning:** Allocate resources to BUs with highest performance potential and lowest risk
- **Best Practice Sharing:** Identify leading BUs and transfer practices to lagging BUs
- **Risk Management:** Identify BUs requiring additional risk mitigation focus
- **M&A Integration:** Compare acquired subsidiary performance to existing BUs
- **Executive Reporting:** Single-page BU performance and risk summary for Board

---

## How to Use the BU Analysis Capability

### Step 1: Configure Your Business Units

1. Open the **"BU Configuration"** sheet
2. Review the pre-configured BUs (CORP, NA, EMEA, APAC, LATAM)
3. Modify to match your organization's actual structure:
   - **Geographic:** Keep regional structure, adjust regions as needed
   - **Product Line:** Replace with your product/service lines
   - **Legal Entity:** Replace with parent company and subsidiaries
   - **Hybrid:** Combine approaches (e.g., geographic + product matrix)
4. Keep "CORP" as the consolidated view - this is mandatory
5. Update BU_Name, Region, Status, and Description for each BU
6. Add/remove rows as needed to match your BU structure

### Step 2: Populate BU-Specific Dimension Data

**Choose Your Data Entry Approach:**

**Approach A - Incremental (Easiest):**
1. Leave existing CORP data unchanged (your baseline)
2. Add new rows for BU-specific data only where there are differences
3. Example: If NA has different brand maturity than enterprise average, add a row with Business_Unit='NA'

**Approach B - Comprehensive (Most Accurate):**
1. Add rows for each dimension element for each BU
2. Example: Add "Customer Service" rows for NA, EMEA, APAC, LATAM with BU-specific maturity scores
3. CORP becomes a calculated rollup (weighted average or aggregation)

**For Each of the 12 Dimension Sheets:**
1. Brand
2. Culture
3. People
4. Technology
5. Third Parties
6. Processes
7. Change
8. Innovation
9. Product & Services
10. Annual Results
11. Strategic Goals
12. Reputation

**Add/Update Data:**
- Set Business_Unit (Column A) to the appropriate BU code (NA, EMEA, APAC, LATAM)
- Populate dimension-specific data (maturity scores, risk ratings, metrics)
- For centralized capabilities (e.g., enterprise IT platform), keep Business_Unit='CORP'
- For decentralized capabilities (e.g., regional customer service), create BU-specific rows

### Step 3: Calculate BU Risk Metrics

1. Open **"BU Risk Dashboard"** sheet
2. For each BU (NA, EMEA, APAC, LATAM), calculate the 17 risk metrics
3. Use the calculation formulas from **"Risk Calculations"** sheet
4. **KEY:** Filter dimension input data to only rows where Business_Unit = selected BU
5. Populate Exposure_Amount for each metric and BU combination
6. Calculate CORP metrics as rollup/aggregation across all BUs
7. Compare each BU to CORP to identify variances

**Example Calculation:**
```
Metric: Opex at Risk
BU: NA

Step 1: Filter "Processes" sheet to rows where Business_Unit='NA'
Step 2: Apply Opex at Risk calculation to filtered data
Step 3: Result = $15M Opex at Risk for NA
Step 4: Compare to CORP ($50M) → NA represents 30% of enterprise Opex risk
```

### Step 4: Calculate BU Performance Metrics

1. Open **"BU Performance Dashboard"** sheet
2. For each BU, calculate the 10 performance metrics
3. Use calculation formulas from **"Performance Calculations"** sheet
4. Filter dimension data by Business_Unit
5. Pay special attention to **Probability of Execution** calculation:
   - Filter strategic objectives to this BU
   - Filter processes aligned to BU objectives
   - Filter risks crystallizing against BU objectives
   - Filter controls protecting BU objectives
   - **Include inter-BU dependencies** (BU objectives depending on other BUs)

**PoE Calculation Example for NA BU:**
```
1. Strategic Objectives: Filter to objectives owned by NA
2. Aligned Processes: Processes supporting NA objectives
3. Crystallizing Risks: Risks threatening NA objectives
4. Control Effectiveness: Controls implemented in NA
5. Inter-BU Dependencies: NA objectives depending on EMEA product delivery
6. Calculate PoE using standard formula with BU-filtered inputs
```

### Step 5: Perform BU Comparison Analysis

1. Open **"BU Comparison Dashboard"** sheet
2. Populate the comparison table with data from BU Risk and Performance Dashboards
3. For each metric, identify:
   - **Best_BU:** Which BU has best performance or lowest risk
   - **Worst_BU:** Which BU has worst performance or highest risk
   - **Range:** Difference between best and worst
   - **Avg_Excl_CORP:** Average across operating BUs (excluding consolidated CORP)
4. Add qualitative Notes explaining variances (e.g., "EMEA high risk due to legacy systems migration")
5. Derive insights:
   - **Best Practice Transfer:** What can worst BUs learn from best BUs?
   - **Resource Allocation:** Should we invest more in lagging BUs or winning BUs?
   - **Risk Concentration:** Is risk concentrated in one BU or diversified?

### Step 6: Executive Reporting and Decision-Making

**Use BU Analysis For:**

1. **Strategic Planning**
   - Which BUs should receive strategic investment?
   - Which BUs are ready to scale vs. need turnaround?
   - Where should new initiatives be piloted? (start with best-performing BU)

2. **Risk Management**
   - Which BUs represent concentration risks?
   - Where should risk mitigation resources be focused?
   - Are BU risk profiles acceptable given their strategic importance?

3. **Performance Management**
   - Which BUs are on track to deliver objectives (high PoE)?
   - Which BUs need executive intervention or additional resources?
   - How does BU performance trend over time?

4. **Organizational Learning**
   - What best practices from high-performing BUs can be shared?
   - Which BU leadership teams are most effective?
   - Should organizational structure change based on BU performance patterns?

5. **M&A and Corporate Development**
   - How do acquired subsidiaries compare to existing BUs?
   - Which BUs are candidates for divestiture vs. investment?
   - What's the optimal portfolio of BUs for the enterprise?

---

## Technical Architecture

### Data Model

**Hierarchical Structure:**
```
Company (DecideWright)
├── CORP (Consolidated)
│   └── Aggregation of all BUs
├── Business Unit 1 (e.g., NA)
│   ├── Domain 1 (e.g., VALUE)
│   │   ├── Dimension 1 (e.g., Brand)
│   │   │   ├── Element 1
│   │   │   │   └── Sub-Element 1
│   │   │   │       └── Variables (496 total inputs)
│   │   │   └── Element N
│   │   └── Dimension N
│   └── Domain N
├── Business Unit 2 (e.g., EMEA)
└── Business Unit N (e.g., APAC)
```

### Sheet Structure (27 Total)

**Configuration & Master Data (1 sheet):**
1. BU Configuration - Defines all business units

**Risk Analysis (3 sheets):**
1. Risk Dashboard - Company-level risk metrics
2. Risk Calculations - Calculation methodology
3. Risk Assumptions - Assumptions and data sources

**BU Risk Analysis (1 sheet):**
4. BU Risk Dashboard - BU-specific risk metrics

**Performance Analysis (3 sheets):**
5. Performance Dashboard - Company-level performance metrics
6. Performance Calculations - Calculation methodology
7. Performance Assumptions - Assumptions and data sources

**BU Performance Analysis (1 sheet):**
8. BU Performance Dashboard - BU-specific performance metrics

**Comparative Analysis (1 sheet):**
9. BU Comparison Dashboard - Side-by-side BU comparison

**Foundation Sheets (5 sheets):**
10. Input - Base Data
11. Financials
12. Business Model
13. External Environment
14. Governance

**Dimension Sheets (12 sheets) - ALL ENHANCED with Business_Unit column:**
15. Brand
16. Culture
17. People
18. Technology
19. Third Parties
20. Processes
21. Change
22. Innovation
23. Product & Services
24. Annual Results
25. Strategic Goals
26. Reputation

**Future Enhancement Potential:**
27. (Reserved for BU Trend Analysis - tracking BU performance over time)

---

## Calculation Methodology

### Risk Metrics per BU

**General Formula:**
```
BU_Risk_Metric = Apply_Company_Risk_Formula(Filter(Dimension_Data, Business_Unit = 'BU_Code'))
```

**Example - Opex at Risk for EMEA:**
```
1. Company Formula: Opex at Risk = Sum(Process_Opex * Process_Risk_Rating * Process_Impact_Score)
2. Filter: Select only rows from "Processes" sheet where Business_Unit = 'EMEA'
3. Apply Formula: Sum(EMEA_Process_Opex * EMEA_Process_Risk * EMEA_Process_Impact)
4. Result: EMEA Opex at Risk = $20M
```

**Consolidation to CORP:**
```
CORP_Opex_at_Risk = NA_Opex_at_Risk + EMEA_Opex_at_Risk + APAC_Opex_at_Risk + LATAM_Opex_at_Risk
OR
CORP_Opex_at_Risk = Apply_Company_Risk_Formula(All dimension data regardless of BU)
```

*Note: These should produce the same result if data is comprehensive across all BUs.*

### Performance Metrics per BU

**General Formula:**
```
BU_Performance_Metric = Apply_Company_Performance_Formula(Filter(Dimension_Data, Business_Unit = 'BU_Code'))
```

**Example - Probability of Execution for NA:**
```
PoE_NA = f(
  Strategic_Objectives_NA,
  Aligned_Processes_NA,
  Crystallizing_Risks_NA,
  Control_Effectiveness_NA,
  Intra_BU_Dependencies_NA,
  Inter_BU_Dependencies_NA_to_Others
)

Where:
- Strategic_Objectives_NA = Objectives owned by NA BU
- Aligned_Processes_NA = Processes supporting NA objectives
- Crystallizing_Risks_NA = Risks threatening NA objectives
- Control_Effectiveness_NA = Controls implemented in NA
- Intra_BU_Dependencies_NA = NA objectives depending on other NA objectives
- Inter_BU_Dependencies_NA_to_Others = NA objectives depending on EMEA/APAC/LATAM objectives
```

**Inter-BU Dependency Impact:**
If NA has an objective that depends on EMEA delivering a product, NA's PoE is constrained by EMEA's PoE for that dependency:

```
NA_Objective_PoE = f(NA_Internal_Factors) * EMEA_Dependency_PoE

Example:
- NA internal factors suggest 85% PoE
- But NA depends on EMEA product (EMEA PoE = 60%)
- Adjusted NA_Objective_PoE = 85% * 60% = 51%
```

This reflects the reality that BUs are interdependent, and execution in one BU depends on others.

### BU Comparison Metrics

**Best BU Identification:**
```
For Performance Metrics: Best_BU = MAX(NA, EMEA, APAC, LATAM)
For Risk Metrics: Best_BU = MIN(NA, EMEA, APAC, LATAM)
```

**Range Calculation:**
```
Range = MAX(All_BUs) - MIN(All_BUs)
Large range → High variance across BUs
Small range → Consistent performance/risk across BUs
```

**Average Excluding CORP:**
```
Avg = (NA + EMEA + APAC + LATAM) / 4
This represents the "typical" BU performance, excluding consolidated view
```

---

## Key Concepts and Definitions

### Business Unit (BU)
A distinct organizational entity within the enterprise with its own:
- Leadership team and organizational structure
- Strategic objectives and performance targets
- Operational processes and capabilities
- Risk profile and control environment
- Financial results (revenue, costs, investment)

BUs can be structured by:
- **Geography:** Regional business units (NA, EMEA, APAC, LATAM)
- **Product Line:** Business units per product/service category
- **Legal Entity:** Separate legal subsidiaries or entities
- **Function:** Corporate functions as BUs (rare, not recommended)
- **Customer Segment:** BUs organized around customer types (B2B vs. B2C)

### Consolidated View (CORP)
The enterprise-wide aggregated view combining all BUs. Represents:
- Total enterprise risk exposure (sum/rollup of all BU risks)
- Enterprise-level performance (weighted average or aggregation of BU performance)
- Centralized capabilities (e.g., enterprise IT platform, corporate brand)
- Strategic objectives at holding company / parent level

### Intra-BU Dependencies
Dependencies between objectives, processes, or initiatives **within the same BU**.

Example: NA's Q4 revenue objective depends on NA's Q2 product launch completing on time (both within NA).

### Inter-BU Dependencies
Dependencies between objectives, processes, or initiatives **across different BUs**.

Example: NA's revenue objective depends on APAC's product development initiative (cross-BU dependency).

Inter-BU dependencies are critical for PoE calculation because they create execution risk that crosses BU boundaries - even a high-performing BU can be constrained by dependencies on lagging BUs.

### BU Risk Profile
The unique risk exposure and risk management maturity of each BU, considering:
- Operational risks specific to that BU's geography/products/markets
- Strategic risks based on BU strategy and competitive position
- Compliance risks based on BU's regulatory environment
- Financial risks based on BU's financial structure and performance

Different BUs will have different risk profiles based on their context.

### BU Performance Profile
The capability, maturity, and execution track record of each BU across:
- Process maturity and operational excellence
- Control effectiveness and risk management capability
- Strategic delivery (historical objective achievement rate)
- Resource efficiency and productivity

Best-practice BUs have higher performance profiles and can mentor lagging BUs.

---

## Benefits of BU Analysis

### 1. Granular Risk Visibility
- Identify which BUs drive enterprise risk exposure
- Avoid "averaging" that masks concentration risks
- Enable BU-specific risk mitigation strategies
- Support risk-based capital allocation across BUs

### 2. Performance Differentiation
- Recognize high-performing BUs vs. turnaround situations
- Avoid treating all BUs the same when they have different capabilities
- Enable targeted performance improvement programs
- Support accountability with BU-level performance metrics

### 3. Best Practice Sharing
- Identify centers of excellence within the enterprise
- Transfer successful practices from leading to lagging BUs
- Create internal benchmarking to drive continuous improvement
- Build organizational learning mechanisms

### 4. Resource Optimization
- Allocate strategic investment to BUs with highest potential
- Provide turnaround support to struggling BUs
- Optimize corporate overhead allocation based on BU needs
- Balance risk and return across BU portfolio

### 5. Strategic Decision-Making
- Portfolio management: Which BUs to grow, maintain, or divest
- M&A integration: Compare acquired entities to existing BUs
- Organizational design: Should BU structure change based on performance patterns
- Succession planning: Identify BU leadership teams for promotion

### 6. Realistic Execution Planning
- Acknowledge inter-BU dependencies in PoE calculation
- Sequence strategic initiatives based on BU readiness
- Avoid setting enterprise objectives that require BU capabilities not yet in place
- Create cross-BU coordination mechanisms for interdependent objectives

---

## Limitations and Considerations

### 1. Data Entry Effort
**Challenge:** BU-level analysis requires significantly more data entry than company-level analysis.

**Mitigation:**
- Start with Approach A (Incremental) - only add BU data where there are material differences
- Prioritize high-impact dimensions (e.g., Strategic Goals, Annual Results) for BU-specific data
- Use CORP as default for centralized capabilities to reduce duplication

### 2. Aggregation Complexity
**Challenge:** Aggregating BU metrics to CORP requires clear consolidation methodology.

**Considerations:**
- For financial metrics: Sum across BUs (Revenue, Costs, Investment)
- For maturity scores: Weighted average (weight by BU size or strategic importance)
- For risk metrics: May require complex aggregation (not always simple sum due to correlations)
- Document assumptions in BU Comparison Dashboard "Notes" column

### 3. Inter-BU Dependency Tracking
**Challenge:** Inter-BU dependencies are difficult to track and quantify.

**Recommendations:**
- Use Strategic Goals sheet to explicitly document inter-BU dependencies
- Create a dependency matrix (NA objectives → EMEA inputs needed)
- Update dependency status monthly to enable dynamic PoE recalculation
- Establish cross-BU governance for critical dependencies

### 4. Organizational Sensitivity
**Challenge:** BU comparison may create competitive dynamics or sensitivity about "worst BU" labeling.

**Best Practices:**
- Frame as learning opportunity, not punitive ranking
- Recognize context differences (e.g., emerging market APAC vs. mature market NA)
- Use BU comparison for strategic dialogue, not performance appraisal
- Celebrate best practices from all BUs (everyone has something to share)

### 5. Matrix Organizations
**Challenge:** Some organizations have matrix structures (e.g., geographic BUs × product line BUs).

**Current Limitation:** This implementation supports **one-dimensional** BU structure (either geographic OR product line, not both simultaneously).

**Future Enhancement:** Could extend to support matrix by adding "BU_Dimension_1" and "BU_Dimension_2" columns, enabling dual classification. Not implemented in current version.

---

## Future Enhancement Roadmap

### Phase 2: BU Trend Analysis (Planned)
- Track BU risk and performance metrics over time (monthly or quarterly)
- Visualize BU performance trajectories (improving, stable, declining)
- Identify inflection points (e.g., EMEA PoE dropped from 75% to 65% in Q3 - why?)
- Support predictive analytics (which BUs will likely miss targets?)

### Phase 3: BU Portfolio Optimization (Planned)
- Portfolio risk-return optimization across BUs
- Efficient frontier analysis: Which BU portfolio maximizes return for given risk?
- Diversification benefit quantification: Does having multiple BUs reduce enterprise risk?
- Strategic scenario analysis: What if we divest LATAM? Acquire new BU in MENA?

### Phase 4: Matrix BU Support (Future)
- Support dual BU dimensions (e.g., Region × Product Line matrix)
- Enable analysis by either dimension or combination
- Example: "What's the risk profile of Consumer Banking in EMEA?" (intersection of two BU dimensions)

### Phase 5: BU Benchmarking (Future)
- External benchmarking: Compare your BUs to market benchmarks
- Industry-specific BU performance norms
- Peer group comparison (how does our EMEA BU compare to competitors' European operations?)

---

## References and Related Documentation

### Core Framework Documentation:
1. **Risk_Dashboard_Implementation_Summary.md** - Overview of 17 risk metrics (company-level)
2. **Performance_Analysis_Implementation_Summary.md** - Overview of 10 performance metrics (company-level)
3. **Probability_of_Execution_Analysis.md** - Deep dive on PoE concept and methodology
4. **Risk_Documentation_Sheets_Summary.md** - Detailed documentation of risk calculation methodology

### Calculation Methodology:
- **Risk Calculations sheet** (in workbook) - Formulas for all 17 risk metrics
- **Risk Assumptions sheet** (in workbook) - Assumptions and data sources for risk calculations
- **Performance Calculations sheet** (in workbook) - Formulas for all 10 performance metrics
- **Performance Assumptions sheet** (in workbook) - Assumptions and data sources for performance calculations

### BU-Specific Guidance:
- This document serves as primary reference for BU implementation
- Refer to company-level documentation for detailed metric definitions
- Apply company-level formulas to BU-filtered data

---

## Conclusion

The Business Unit / Subsidiary Analysis capability represents a significant enhancement to the DecideWright Enterprise Architecture framework, enabling:

**Multi-Level Analysis:**
- Enterprise (CORP) consolidated view
- Individual BU performance and risk assessment
- Comparative BU analysis for best practice identification

**Strategic Value:**
- More granular risk management (avoid aggregation hiding concentration risks)
- Better resource allocation (invest in BUs with highest potential)
- Organizational learning (transfer best practices from leading BUs)
- Realistic execution planning (acknowledge inter-BU dependencies)

**Backward Compatibility:**
- All existing company-level analysis remains fully functional
- Existing data preserved and defaulted to CORP view
- Organizations can adopt BU analysis incrementally

**Implementation Status:**
- 4 new sheets created (BU Configuration, BU Risk Dashboard, BU Performance Dashboard, BU Comparison Dashboard)
- 12 dimension sheets enhanced with Business_Unit column
- Framework extended from 22 to 27 sheets
- Ready for BU-specific data entry and analysis

The framework now supports organizations ranging from single-company operations (use CORP view only) to complex multi-BU enterprises with diverse geographic, product, or legal entity structures. This flexibility ensures the framework scales with organizational complexity while maintaining analytical rigor.

---

**Implementation Status:** ✓ COMPLETE
**Next Step:** Populate BU-specific data in dimension sheets and calculate BU risk/performance metrics
**Support:** Refer to this document and related framework documentation for guidance
