# DecideWright QRA Platform - Product Requirements Document

**Version:** 1.0
**Date:** October 27, 2025
**Status:** Ready for Implementation
**Optimized for:** Claude Code

---

## Executive Summary

DecideWright QRA Platform is a comprehensive web application that enables businesses to conduct quantitative risk assessments using the Value Orchestration Canvas (VOC) framework. The platform provides both qualitative (scale-based) and quantitative (data-driven) risk analysis modes, delivering real-time risk exposure metrics through interactive dashboards powered by Monte Carlo simulation and multivariate analysis.

### Key Objectives

1. **Enable Rapid Risk Assessment**: Users can complete initial or detailed surveys in 15-90 minutes
2. **Provide Actionable Insights**: Real-time dashboards show 9 risk exposure metrics across 16 VOC dimensions
3. **Support Multiple Assessment Modes**: Qualitative (1-5 scales) and Quantitative (actual data)
4. **Scale Globally**: Region-specific analysis for up to 6 geographic regions
5. **Drive Risk Mitigation**: Prioritized recommendations based on quantified risk exposure

---

## 1. Technology Stack

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript 5+
- **UI Components**: Shadcn/ui (Radix UI + Tailwind CSS)
- **Styling**: Tailwind CSS 3+
- **State Management**: React Context + Zustand
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts / D3.js for risk visualizations
- **Real-time**: Azure SignalR Service for dashboard updates

### Backend
- **API**: Next.js API Routes (App Router)
- **Validation**: Zod schemas
- **Authentication**: NextAuth.js with Azure AD B2C
- **Risk Engine**: Python FastAPI microservice (for Monte Carlo simulation)

### Database
- **Primary**: Azure Cosmos DB (multi-model)
  - Survey responses (document DB)
  - User profiles and organizations
  - Risk calculation results
- **Cache**: Redis (Azure Cache for Redis)
- **Time Series**: Azure Data Explorer (for historical risk trends)

### AI/ML Services
- **Risk Analysis Engine**: Python + NumPy + SciPy (Monte Carlo simulation)
- **Recommendations**: Azure OpenAI Service (GPT-4)
- **Data Validation**: Custom ML models for data quality scoring

### Infrastructure
- **Hosting**: Azure App Service / Azure Static Web Apps
- **Functions**: Azure Functions (Python) for risk calculations
- **CDN**: Azure Front Door
- **Monitoring**: Azure Application Insights
- **Secrets**: Azure Key Vault

---

## 2. User Experience (UX) Pattern

### Design System: Claude Desktop / Studio55IQ Pattern

#### 2.1 Layout Structure

```
┌─────────────────────────────────────────────────────┐
│  [Icon Nav]  [Sidebar]        [Main Content]        │
│     64px       280px              Flexible           │
│  ┌────────┐ ┌──────────┐  ┌─────────────────────┐  │
│  │        │ │          │  │                     │  │
│  │  Logo  │ │ Primary  │  │   Survey /          │  │
│  │        │ │ Menu     │  │   Dashboard         │  │
│  ├────────┤ ├──────────┤  │   Content           │  │
│  │   Q    │ │ Initial  │  │                     │  │
│  │   [●]  │ │ Detail   │  │                     │  │
│  │        │ │ Dashboard│  │                     │  │
│  ├────────┤ ├──────────┤  │                     │  │
│  │   Qt   │ │          │  │                     │  │
│  │   [ ]  │ │          │  │                     │  │
│  │        │ │          │  │                     │  │
│  ├────────┤ └──────────┘  │                     │  │
│  │   ⚙   │               │                     │  │
│  └────────┘               └─────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

#### 2.2 Navigation Components

**Icon Navigation Bar (64px)**
- Fixed left sidebar
- Vertical icon buttons
- Active state highlighting
- Icons:
  - Logo/Home (top)
  - Q (Qualitative Risk Analysis)
  - Qt (Quantitative Risk Analysis)
  - Spacer
  - Settings (bottom)
  - User Profile (bottom)

**Expandable Sidebar (280px)**
- Slides in/out on icon click
- Nested menu structure
- Smooth transitions
- Menu items:
  - **Qualitative Risk Analysis**
    - → Initial Survey (48 questions)
    - → Detailed Survey (48 questions × regions)
    - → Dashboard
  - **Quantitative Risk Analysis**
    - → Initial Survey (48 data points)
    - → Detailed Survey (48 data points × regions)
    - → Dashboard

**Main Content Area**
- Full height, responsive width
- Smooth page transitions
- Progress indicators for surveys
- Auto-save functionality

#### 2.3 Color Palette

```css
:root {
  /* Primary Colors */
  --color-primary: #F5F5F0;        /* Background */
  --color-secondary: #EAEAE0;      /* Secondary BG */
  --color-accent: #6B7280;         /* Accent/Active */
  --color-dark: #2c2c2c;           /* Text */

  /* Risk Colors */
  --risk-very-low: #10b981;        /* Green */
  --risk-low: #84cc16;             /* Light Green */
  --risk-medium: #fbbf24;          /* Yellow */
  --risk-high: #f97316;            /* Orange */
  --risk-very-high: #ef4444;       /* Red */

  /* Chart Colors */
  --chart-opex: #3b82f6;
  --chart-capex: #8b5cf6;
  --chart-stratex: #ec4899;
  --chart-revenue: #f59e0b;
  --chart-productivity: #10b981;
  --chart-availability: #06b6d4;
  --chart-reputation: #f43f5e;
  --chart-enterprise: #6366f1;
}
```

---

## 3. Information Architecture

### 3.1 Application Flow

```
Landing Page
    │
    ├─> Authentication (Azure AD B2C / Demo Mode)
    │
    └─> Main Application
         │
         ├─> Qualitative Risk Analysis
         │    ├─> Initial Survey (Scale 1-5)
         │    │    └─> Survey Flow → Auto-save → Submit → Results
         │    ├─> Detailed Survey (Scale 1-5, Region-specific)
         │    │    └─> Region Selection → Survey Flow → Submit → Results
         │    └─> Dashboard
         │         └─> View past assessments, compare results
         │
         └─> Quantitative Risk Analysis
              ├─> Initial Survey (Real Data)
              │    └─> Survey Flow → Data Validation → Submit → Results
              ├─> Detailed Survey (Real Data, Region-specific)
              │    └─> Region Selection → Survey Flow → Validation → Results
              └─> Dashboard
                   └─> View assessments, trends, export data
```

### 3.2 URL Structure

```
/                                    # Landing page
/auth/signin                         # Sign in
/auth/signup                         # Sign up
/dashboard                           # Main dashboard (overview)

/qualitative/initial                 # Qualitative Initial Survey
/qualitative/detailed               # Qualitative Detailed Survey
/qualitative/dashboard              # Qualitative Results Dashboard

/quantitative/initial               # Quantitative Initial Survey
/quantitative/detailed              # Quantitative Detailed Survey
/quantitative/dashboard             # Quantitative Results Dashboard

/assessments/:id                    # Individual assessment view
/assessments/:id/results            # Assessment results & recommendations
/assessments/:id/export             # Export assessment data

/organization/settings              # Organization settings
/organization/users                 # User management
/organization/billing               # Billing & subscription

/profile                            # User profile
/settings                           # User settings
```

---

## 4. Core Features & User Stories

### 4.1 User Registration & Authentication

**As a** business user,
**I want to** register my company and create an account,
**So that** I can conduct risk assessments for my organization.

**Acceptance Criteria:**
- ✅ Registration form captures: Business Name, Size (FTEs), Annual Revenue, Industry, HQ Country
- ✅ Email verification required
- ✅ Azure AD B2C integration for enterprise SSO
- ✅ Demo mode available for evaluation (no registration required)
- ✅ Role-based access: Admin, Analyst, Viewer

**Technical Implementation:**
- NextAuth.js with Azure AD B2C provider
- Cosmos DB document for organization profile
- Session management with JWT tokens
- Email service: Azure Communication Services

---

### 4.2 Survey Selection & Configuration

**As a** risk analyst,
**I want to** choose between qualitative and quantitative assessment modes,
**So that** I can select the approach that best fits my data availability.

**Acceptance Criteria:**
- ✅ Clear explanation of qualitative vs quantitative modes
- ✅ Initial vs Detailed survey comparison (time estimates, question counts)
- ✅ Business model selection from 10 options
- ✅ Geographic region selection (multi-select from 6 regions)
- ✅ IT infrastructure profile selection
- ✅ Save configuration as draft

**Technical Implementation:**
- React Hook Form for survey configuration
- Zod schema validation
- Local storage for draft persistence
- API: `POST /api/assessments/create`

---

### 4.3 Qualitative Initial Survey (Scale 1-5)

**As a** business user without detailed metrics,
**I want to** complete a quick scale-based risk assessment,
**So that** I can get a baseline risk profile in 15-20 minutes.

**Acceptance Criteria:**
- ✅ 48 questions (3 per dimension) with 1-5 scale
- ✅ Progress indicator showing completion percentage
- ✅ Auto-save every 30 seconds
- ✅ Ability to skip questions and return later
- ✅ Question help tooltips with examples
- ✅ Mobile-responsive design
- ✅ Keyboard navigation support
- ✅ Domain/dimension grouping with visual separators

**UI Components:**
```tsx
// Survey Question Component
interface SurveyQuestionProps {
  questionId: string;
  questionText: string;
  dimension: string;
  domain: string;
  helpText?: string;
  value: number | null;
  onChange: (value: number) => void;
}

// Rating Scale Component (1-5)
<RatingScale
  min={1}
  max={5}
  labels={["Very Low Risk", "Low Risk", "Medium Risk", "High Risk", "Very High Risk"]}
  value={value}
  onChange={onChange}
  colors={riskColors}
/>
```

**Technical Implementation:**
- Component: `components/survey/QualitativeSurvey.tsx`
- State management: Zustand store for survey responses
- API: `POST /api/assessments/{id}/responses`
- Auto-save: Debounced API calls every 30s
- Validation: All 48 questions must be answered before submission

---

### 4.4 Quantitative Initial Survey (Real Data)

**As a** business user with access to metrics,
**I want to** provide actual quantitative data for risk assessment,
**So that** I can get precise risk calculations based on real numbers.

**Acceptance Criteria:**
- ✅ 48 data input fields with appropriate units (%, $, count, hours, etc.)
- ✅ Data validation (range checks, format validation)
- ✅ Fallback scale option if data not available
- ✅ Data quality indicators
- ✅ High-priority field highlighting
- ✅ Estimation guidance and industry benchmarks
- ✅ CSV import for bulk data entry
- ✅ Real-time data validation feedback

**UI Components:**
```tsx
// Data Input Component
interface DataInputProps {
  fieldId: string;
  label: string;
  unit: "percentage" | "currency" | "count" | "hours" | "months" | "years";
  value: number | null;
  onChange: (value: number) => void;
  validationRules: ValidationSchema;
  fallbackScale?: boolean;
  benchmark?: number;
  helpText?: string;
}

// Example Usage
<DataInput
  fieldId="FIN-001"
  label="Revenue at Risk (% of annual revenue)"
  unit="percentage"
  value={revenueAtRisk}
  onChange={setRevenueAtRisk}
  validationRules={{ min: 0, max: 100 }}
  benchmark={15.2}
  fallbackScale={true}
/>
```

**Technical Implementation:**
- Component: `components/survey/QuantitativeSurvey.tsx`
- Validation: Zod schemas with custom rules per data type
- API: `POST /api/assessments/{id}/data`
- CSV Import: `components/survey/CSVImport.tsx`
- Data quality scoring: ML model via Azure Function

---

### 4.5 Detailed Survey (Region-Specific)

**As a** multi-national business user,
**I want to** provide region-specific risk data,
**So that** I can understand risk exposure across different geographies.

**Acceptance Criteria:**
- ✅ All 48 questions repeated for each selected region
- ✅ Region selector with visual map
- ✅ Progress tracking per region
- ✅ Compare regions side-by-side
- ✅ Region-specific help text and benchmarks
- ✅ Bulk copy from one region to another
- ✅ Variance highlighting across regions

**UI Design:**
```
┌─────────────────────────────────────────────┐
│  Regions: [●] Europe  [●] N. America  [ ] Asia  │
│  Progress: Europe 45/48 | N. America 32/48    │
├─────────────────────────────────────────────┤
│                                             │
│  Current Region: Europe          [Change]  │
│                                             │
│  FIN-001: Liquidity Risk                   │
│  ─────────────────────────────────────     │
│  Rating: [1] [2] [●3] [4] [5]             │
│                                             │
│  📊 Compare with N. America: ●4 (+1 risk)  │
│                                             │
└─────────────────────────────────────────────┘
```

**Technical Implementation:**
- Component: `components/survey/RegionalSurvey.tsx`
- State: Nested structure `{ [region]: { [questionId]: value } }`
- API: `POST /api/assessments/{id}/regional-data`
- Region comparison: Client-side calculation with visual diff

---

### 4.6 Risk Dashboard (Real-time Results)

**As a** business decision-maker,
**I want to** see real-time risk metrics as I complete the survey,
**So that** I can immediately understand my organization's risk exposure.

**Acceptance Criteria:**
- ✅ Real-time calculation as survey progresses (minimum 25% complete)
- ✅ 9 risk exposure metrics displayed with currency values
- ✅ Risk heatmap across 16 VOC dimensions
- ✅ Domain-level risk aggregation (4 domains)
- ✅ Regional risk comparison (for detailed surveys)
- ✅ Trend analysis (comparison with previous assessments)
- ✅ Monte Carlo distribution visualization
- ✅ Scenario analysis (best case, worst case, most likely)
- ✅ Export to PDF, Excel, PowerPoint

**Dashboard Sections:**

1. **Executive Summary Card**
   - Total Enterprise Value at Risk: $X.XM (XX%)
   - Risk Level: [High/Medium/Low]
   - Top 3 Risk Areas
   - Completion Date
   - Assessment Mode (Qualitative/Quantitative)

2. **Risk Exposure Metrics (9 KPIs)**
   ```
   ┌──────────────────────────────────────────┐
   │  Opex at Risk        $XXX,XXX  ████░░  │
   │  Capex at Risk       $XXX,XXX  ███░░░  │
   │  Stratex at Risk     $XXX,XXX  █████░  │
   │  Revenue at Risk     $XXX,XXX  ██████  │
   │  Productivity Days   XX,XXX    ███░░░  │
   │  Service Avail. %    XX.X%     ████░░  │
   │  Reputation Score    X.X/10    ██░░░░  │
   │  Enterprise Value    $X.XM     █████░  │
   └──────────────────────────────────────────┘
   ```

3. **VOC Dimension Heatmap (4x4 Grid)**
   ```
   ┌────────────────────────────────────────┐
   │         ECONOMICS    │    ENABLERS     │
   │  Financials    [██]  │ Brand      [███]│
   │  Bus. Model    [███] │ Culture    [██] │
   │  External      [████]│ People     [███]│
   │  Governance    [██]  │ Technology [███]│
   │                      │ 3rd Party  [██] │
   ├──────────────────────┼─────────────────┤
   │      EXECUTION       │     VALUE       │
   │  Innovation    [███] │ Results    [██] │
   │  Change        [████]│ Strategy   [███]│
   │  Processes     [██]  │ Reputation [███]│
   │  Products      [███] │                 │
   └────────────────────────────────────────┘
   ```

4. **Monte Carlo Distribution Chart**
   - Probability distribution of Enterprise Value at Risk
   - 95% confidence interval
   - P50 (median), P75, P90, P95 values

5. **Regional Comparison (Detailed Surveys Only)**
   - Side-by-side bar charts for each region
   - Variance analysis
   - Hotspot identification

6. **Recommendations (AI-Generated)**
   - Top 5 risk mitigation priorities
   - Estimated impact of mitigation
   - Resource requirements
   - Implementation timeline

**Technical Implementation:**

**Frontend:**
```tsx
// components/dashboard/RiskDashboard.tsx
import { useAssessmentResults } from '@/hooks/useAssessmentResults'
import { RiskMetricsPanel } from './RiskMetricsPanel'
import { VOCHeatmap } from './VOCHeatmap'
import { MonteCarloChart } from './MonteCarloChart'
import { RegionalComparison } from './RegionalComparison'
import { RecommendationsPanel } from './RecommendationsPanel'

export function RiskDashboard({ assessmentId }: { assessmentId: string }) {
  const { data, isLoading, error } = useAssessmentResults(assessmentId)

  return (
    <div className="dashboard-grid">
      <ExecutiveSummary data={data.summary} />
      <RiskMetricsPanel metrics={data.riskMetrics} />
      <VOCHeatmap dimensions={data.dimensions} />
      <MonteCarloChart distribution={data.monteCarloResults} />
      {data.isRegional && <RegionalComparison regions={data.regionalData} />}
      <RecommendationsPanel recommendations={data.recommendations} />
    </div>
  )
}
```

**Backend API:**
```typescript
// app/api/assessments/[id]/results/route.ts
export async function GET(req: Request, { params }: { params: { id: string } }) {
  const assessmentId = params.id

  // 1. Fetch assessment responses from Cosmos DB
  const assessment = await cosmosDB.getAssessment(assessmentId)

  // 2. Call Python Risk Engine for calculations
  const riskResults = await riskEngine.calculate({
    responses: assessment.responses,
    mode: assessment.mode, // 'qualitative' | 'quantitative'
    regions: assessment.regions,
    organizationProfile: assessment.organization
  })

  // 3. Generate AI recommendations
  const recommendations = await openAI.generateRecommendations({
    riskResults,
    topRisks: riskResults.topRisks
  })

  // 4. Return comprehensive results
  return Response.json({
    summary: riskResults.summary,
    riskMetrics: riskResults.metrics,
    dimensions: riskResults.dimensionScores,
    monteCarloResults: riskResults.monteCarlo,
    regionalData: riskResults.regional,
    recommendations,
    calculatedAt: new Date().toISOString()
  })
}
```

**Risk Engine (Python FastAPI):**
```python
# risk_engine/calculator.py
import numpy as np
from scipy import stats
from typing import Dict, List

class RiskCalculator:
    def __init__(self, responses: Dict, mode: str):
        self.responses = responses
        self.mode = mode

    def calculate_metrics(self) -> Dict:
        """
        Main calculation method using Monte Carlo simulation
        """
        # 1. Convert responses to risk scores (normalized 0-1)
        risk_scores = self.normalize_responses()

        # 2. Apply VOC dimension weights
        weighted_scores = self.apply_weights(risk_scores)

        # 3. Run Monte Carlo simulation (10,000 iterations)
        mc_results = self.monte_carlo_simulation(weighted_scores)

        # 4. Calculate 9 risk exposure metrics
        risk_metrics = self.calculate_risk_exposures(mc_results)

        return {
            'metrics': risk_metrics,
            'dimensions': weighted_scores,
            'monteCarlo': mc_results,
            'summary': self.generate_summary(risk_metrics)
        }

    def monte_carlo_simulation(self, scores: Dict, iterations: int = 10000) -> Dict:
        """
        Monte Carlo simulation for probabilistic risk assessment
        """
        results = []

        for _ in range(iterations):
            # Add randomness based on uncertainty in responses
            simulated_scores = self.add_uncertainty(scores)

            # Calculate enterprise value at risk for this iteration
            ev_risk = self.calculate_ev_risk(simulated_scores)
            results.append(ev_risk)

        results = np.array(results)

        return {
            'mean': np.mean(results),
            'median': np.median(results),
            'p75': np.percentile(results, 75),
            'p90': np.percentile(results, 90),
            'p95': np.percentile(results, 95),
            'std': np.std(results),
            'distribution': results.tolist()
        }
```

---

### 4.7 Assessment History & Comparison

**As a** risk analyst,
**I want to** view historical assessments and track risk trends over time,
**So that** I can measure the effectiveness of risk mitigation efforts.

**Acceptance Criteria:**
- ✅ List all past assessments with metadata
- ✅ Compare up to 3 assessments side-by-side
- ✅ Trend charts showing risk metric changes over time
- ✅ Filter by date range, assessment type, region
- ✅ Tag assessments with custom labels
- ✅ Archive old assessments
- ✅ Export comparison reports

**Technical Implementation:**
- API: `GET /api/assessments?filter=...&sort=...`
- Component: `components/assessments/AssessmentHistory.tsx`
- Comparison: Client-side diff calculation
- Charts: Recharts for time-series visualization

---

### 4.8 Export & Reporting

**As a** business executive,
**I want to** export risk assessment results in multiple formats,
**So that** I can share insights with stakeholders and board members.

**Acceptance Criteria:**
- ✅ Export to PDF (executive summary + detailed report)
- ✅ Export to Excel (raw data + charts)
- ✅ Export to PowerPoint (presentation deck)
- ✅ Customizable report templates
- ✅ Scheduled automated reports (email delivery)
- ✅ API access for data integration

**Export Formats:**

1. **PDF Report Structure:**
   - Cover page with company logo
   - Executive summary (1 page)
   - Risk metrics dashboard (1 page)
   - VOC dimension breakdown (2 pages)
   - Regional comparison (if applicable, 1-2 pages)
   - Recommendations (2-3 pages)
   - Appendix: Survey responses (optional)

2. **Excel Workbook:**
   - Sheet 1: Executive Summary
   - Sheet 2: Risk Metrics
   - Sheet 3: Dimension Scores
   - Sheet 4: Regional Data (if applicable)
   - Sheet 5: Raw Survey Responses
   - Sheet 6: Monte Carlo Results
   - Sheet 7: Recommendations

3. **PowerPoint Deck:**
   - Slide 1: Title & Executive Summary
   - Slide 2: Risk Metrics Overview
   - Slide 3: VOC Heatmap
   - Slide 4: Top 5 Risk Areas
   - Slide 5: Regional Comparison (if applicable)
   - Slide 6: Recommendations & Action Plan

**Technical Implementation:**
- PDF: Puppeteer for server-side rendering
- Excel: ExcelJS library
- PowerPoint: PptxGenJS library
- API: `POST /api/assessments/{id}/export`
- Queue: Azure Service Bus for async generation
- Storage: Azure Blob Storage for generated files

---

## 5. Data Models

### 5.1 Organization Schema

```typescript
interface Organization {
  id: string
  name: string
  size: 'micro' | 'small' | 'medium' | 'large' | 'enterprise'
  employeeCount: number
  annualRevenue: number
  currency: string
  industry: string // GICS classification
  headquartersCountry: string
  headquartersRegion: Region
  operationalRegions: Region[]
  itInfrastructure: 'cloud' | 'on-premises' | 'hybrid'
  businessModel: BusinessModel
  createdAt: string
  updatedAt: string
  subscription: {
    plan: 'free' | 'pro' | 'enterprise'
    status: 'active' | 'trial' | 'expired'
    assessmentsPerMonth: number
    usersLimit: number
  }
}

type Region = 'Europe' | 'North America' | 'South America' | 'Asia' | 'Oceania' | 'Africa'

type BusinessModel =
  | 'Transaction/Sales'
  | 'Fee-for-Service'
  | 'Subscription/Recurring'
  | 'B2B/Wholesale'
  | 'Manufacturing/Production'
  | 'Platform/Marketplace'
  | 'Advertising'
  | 'Franchise'
  | 'Freemium'
  | 'Licensing/IP'
```

### 5.2 Assessment Schema

```typescript
interface Assessment {
  id: string
  organizationId: string
  name: string
  description?: string
  mode: 'qualitative' | 'quantitative'
  type: 'initial' | 'detailed'
  status: 'draft' | 'in-progress' | 'completed' | 'archived'
  selectedRegions: Region[]
  createdBy: string
  createdAt: string
  updatedAt: string
  completedAt?: string

  // Survey responses
  responses: QualitativeResponses | QuantitativeResponses

  // Calculated results
  results?: AssessmentResults

  // Metadata
  completionPercentage: number
  estimatedTimeRemaining: number // minutes
  tags: string[]
}

interface QualitativeResponses {
  [questionId: string]: {
    value: 1 | 2 | 3 | 4 | 5
    answeredAt: string
    region?: Region
  }
}

interface QuantitativeResponses {
  [questionId: string]: {
    value: number
    unit: DataUnit
    dataQualityScore: number // 0-100
    answeredAt: string
    region?: Region
    usedFallbackScale?: boolean
  }
}

type DataUnit = 'percentage' | 'currency' | 'count' | 'hours' | 'months' | 'years' | 'ratio'
```

### 5.3 Risk Results Schema

```typescript
interface AssessmentResults {
  assessmentId: string
  calculatedAt: string
  calculationMode: 'qualitative' | 'quantitative'

  // Executive Summary
  summary: {
    enterpriseValueAtRisk: {
      amount: number
      percentage: number
      currency: string
    }
    overallRiskLevel: 'very-low' | 'low' | 'medium' | 'high' | 'very-high'
    topRisks: Array<{
      dimension: string
      score: number
      impact: string
    }>
    completionDate: string
  }

  // 9 Risk Exposure Metrics
  riskMetrics: {
    opexAtRisk: RiskMetric
    capexAtRisk: RiskMetric
    stratexAtRisk: RiskMetric
    revenueAtRisk: RiskMetric
    productivityTimeAtRisk: RiskMetric
    serviceAvailabilityAtRisk: RiskMetric
    reputationAtRisk: RiskMetric
    enterpriseValueAtRisk: RiskMetric
  }

  // Dimension Scores (16 VOC dimensions)
  dimensions: {
    [dimensionId: string]: DimensionScore
  }

  // Domain Aggregations (4 domains)
  domains: {
    economics: DomainScore
    enablers: DomainScore
    execution: DomainScore
    value: DomainScore
  }

  // Monte Carlo Simulation Results
  monteCarlo: MonteCarloResults

  // Regional Data (for detailed assessments)
  regional?: {
    [region: string]: RegionalResults
  }

  // AI-Generated Recommendations
  recommendations: Recommendation[]
}

interface RiskMetric {
  value: number
  unit: string
  riskLevel: 'very-low' | 'low' | 'medium' | 'high' | 'very-high'
  percentile: number // 0-100, compared to industry benchmark
  trend?: 'improving' | 'stable' | 'worsening' // vs previous assessment
  contributors: Array<{
    dimension: string
    contribution: number // percentage
  }>
}

interface DimensionScore {
  id: string
  name: string
  domain: string
  score: number // 0-100
  riskLevel: 'very-low' | 'low' | 'medium' | 'high' | 'very-high'
  factors: Array<{
    factorId: string
    factorName: string
    score: number
  }>
}

interface DomainScore {
  name: string
  score: number
  riskLevel: 'very-low' | 'low' | 'medium' | 'high' | 'very-high'
  dimensions: string[] // dimension IDs
}

interface MonteCarloResults {
  iterations: number
  mean: number
  median: number
  p75: number
  p90: number
  p95: number
  standardDeviation: number
  distribution: number[] // histogram data
  confidenceInterval95: [number, number]
}

interface RegionalResults {
  region: Region
  summary: {
    enterpriseValueAtRisk: number
    overallRiskLevel: string
  }
  riskMetrics: { [metric: string]: number }
  dimensions: { [dimension: string]: number }
}

interface Recommendation {
  id: string
  priority: 1 | 2 | 3 | 4 | 5
  category: 'process' | 'technology' | 'people' | 'governance'
  title: string
  description: string
  impactedRisks: string[] // risk metric IDs
  estimatedImpact: {
    riskReduction: number // percentage
    costToImplement: number
    timeToImplement: string // e.g., "3-6 months"
  }
  actionItems: string[]
  generatedBy: 'ai' | 'manual'
}
```

---

## 6. API Specifications

### 6.1 Authentication APIs

```typescript
// POST /api/auth/register
interface RegisterRequest {
  email: string
  password: string
  organization: {
    name: string
    size: OrganizationSize
    industry: string
  }
}

// POST /api/auth/signin
interface SignInRequest {
  email: string
  password: string
}

// GET /api/auth/session
interface SessionResponse {
  user: {
    id: string
    email: string
    name: string
    role: 'admin' | 'analyst' | 'viewer'
  }
  organization: Organization
}
```

### 6.2 Assessment APIs

```typescript
// POST /api/assessments
interface CreateAssessmentRequest {
  name: string
  mode: 'qualitative' | 'quantitative'
  type: 'initial' | 'detailed'
  selectedRegions: Region[]
  description?: string
}

interface CreateAssessmentResponse {
  assessmentId: string
  status: 'draft'
  createdAt: string
}

// GET /api/assessments
interface ListAssessmentsQuery {
  status?: 'draft' | 'in-progress' | 'completed' | 'archived'
  mode?: 'qualitative' | 'quantitative'
  dateFrom?: string
  dateTo?: string
  limit?: number
  offset?: number
}

// GET /api/assessments/:id
interface GetAssessmentResponse extends Assessment {}

// PATCH /api/assessments/:id
interface UpdateAssessmentRequest {
  name?: string
  description?: string
  tags?: string[]
  status?: AssessmentStatus
}

// POST /api/assessments/:id/responses
interface SaveResponsesRequest {
  responses: {
    [questionId: string]: {
      value: number
      region?: Region
    }
  }
}

// POST /api/assessments/:id/submit
interface SubmitAssessmentResponse {
  status: 'completed'
  resultsAvailable: boolean
  calculationJobId: string
}

// GET /api/assessments/:id/results
interface GetResultsResponse extends AssessmentResults {}

// POST /api/assessments/:id/export
interface ExportRequest {
  format: 'pdf' | 'excel' | 'powerpoint'
  sections: string[] // which sections to include
  includeRawData: boolean
}

interface ExportResponse {
  jobId: string
  status: 'queued' | 'processing' | 'completed' | 'failed'
  downloadUrl?: string // available when status = 'completed'
  expiresAt?: string
}
```

### 6.3 Risk Calculation APIs (Python FastAPI)

```python
# POST /calculate
class CalculateRiskRequest(BaseModel):
    assessment_id: str
    responses: Dict[str, Any]
    mode: str  # 'qualitative' | 'quantitative'
    type: str  # 'initial' | 'detailed'
    organization: Dict[str, Any]
    regions: List[str]

class CalculateRiskResponse(BaseModel):
    job_id: str
    status: str
    results: Optional[Dict[str, Any]]

# GET /calculate/{job_id}/status
class CalculationStatusResponse(BaseModel):
    job_id: str
    status: str  # 'queued' | 'processing' | 'completed' | 'failed'
    progress: int  # 0-100
    results: Optional[Dict[str, Any]]
    error: Optional[str]
```

---

## 7. Real-time Features

### 7.1 Auto-save & Sync

**Requirements:**
- Auto-save survey responses every 30 seconds
- Sync across multiple devices/tabs
- Conflict resolution for concurrent edits
- Offline support with local storage
- Visual indicator for save status

**Technical Implementation:**

```typescript
// hooks/useAutoSave.ts
import { useEffect, useRef } from 'react'
import { useDebouncedCallback } from 'use-debounce'

export function useAutoSave(
  data: any,
  saveFunction: (data: any) => Promise<void>,
  delay: number = 30000 // 30 seconds
) {
  const savedData = useRef(data)

  const debouncedSave = useDebouncedCallback(async (currentData) => {
    if (JSON.stringify(currentData) !== JSON.stringify(savedData.current)) {
      await saveFunction(currentData)
      savedData.current = currentData
    }
  }, delay)

  useEffect(() => {
    debouncedSave(data)
  }, [data, debouncedSave])
}

// Usage in Survey Component
const { responses, updateResponse } = useSurveyState(assessmentId)

useAutoSave(responses, async (data) => {
  await fetch(`/api/assessments/${assessmentId}/responses`, {
    method: 'POST',
    body: JSON.stringify(data)
  })
})
```

### 7.2 Real-time Dashboard Updates

**Requirements:**
- Dashboard updates in real-time as survey responses are submitted
- Multiple users can view the same assessment dashboard simultaneously
- Live progress tracking
- WebSocket/SignalR connection for push updates

**Technical Implementation:**

```typescript
// lib/signalr-client.ts
import { HubConnectionBuilder, HubConnection } from '@microsoft/signalr'

export class RiskDashboardHub {
  private connection: HubConnection

  constructor(assessmentId: string) {
    this.connection = new HubConnectionBuilder()
      .withUrl(`${process.env.NEXT_PUBLIC_SIGNALR_URL}/riskhub`)
      .withAutomaticReconnect()
      .build()
  }

  async start() {
    await this.connection.start()
    await this.connection.invoke('JoinAssessment', this.assessmentId)
  }

  onResultsUpdated(callback: (results: AssessmentResults) => void) {
    this.connection.on('ResultsUpdated', callback)
  }

  onProgressUpdated(callback: (progress: number) => void) {
    this.connection.on('ProgressUpdated', callback)
  }
}

// Usage in Dashboard Component
const hub = useSignalRHub(assessmentId)

useEffect(() => {
  hub.onResultsUpdated((results) => {
    setDashboardData(results)
  })

  hub.onProgressUpdated((progress) => {
    setCompletionProgress(progress)
  })
}, [hub])
```

---

## 8. Security & Compliance

### 8.1 Security Requirements

**Authentication & Authorization:**
- ✅ Multi-factor authentication (MFA) required for admin users
- ✅ Role-based access control (RBAC): Admin, Analyst, Viewer
- ✅ Session timeout after 30 minutes of inactivity
- ✅ Azure AD B2C integration for enterprise SSO
- ✅ API key authentication for programmatic access

**Data Security:**
- ✅ Encryption at rest (Azure Cosmos DB built-in encryption)
- ✅ Encryption in transit (TLS 1.3)
- ✅ Row-level security for multi-tenant data
- ✅ Secrets management via Azure Key Vault
- ✅ Regular security audits and penetration testing

**Input Validation:**
- ✅ Zod schema validation for all API inputs
- ✅ XSS prevention via React's built-in escaping
- ✅ SQL injection prevention (using parameterized queries)
- ✅ CSRF protection via NextAuth.js
- ✅ Rate limiting (100 requests/minute per user)

**Compliance:**
- ✅ GDPR compliance (data export, right to deletion)
- ✅ SOC 2 Type II certification (planned)
- ✅ ISO 27001 compliance (planned)
- ✅ Audit logging for all sensitive operations
- ✅ Data residency options (EU, US, Asia regions)

### 8.2 Privacy & Data Handling

**Personal Data:**
- User email, name, role
- Organization name, size, industry
- Survey responses (may contain business-sensitive information)

**Data Retention:**
- Active assessments: Retained indefinitely
- Archived assessments: Retained for 7 years
- Deleted assessments: Soft delete for 30 days, then permanent deletion
- User data: Deleted within 30 days of account closure

**Data Sharing:**
- No data shared with third parties without explicit consent
- Anonymized aggregate data may be used for benchmarking (opt-in)
- Export functionality allows users to extract all their data

---

## 9. Performance Requirements

### 9.1 Response Times

| Operation | Target | Maximum |
|-----------|--------|---------|
| Page load (initial) | < 2s | < 4s |
| Survey question navigation | < 200ms | < 500ms |
| Auto-save response | < 1s | < 2s |
| Dashboard load | < 3s | < 6s |
| Risk calculation (Initial) | < 10s | < 20s |
| Risk calculation (Detailed) | < 30s | < 60s |
| Export generation (PDF) | < 10s | < 30s |
| Export generation (Excel/PPT) | < 20s | < 60s |

### 9.2 Scalability Targets

**Concurrent Users:**
- 1,000 concurrent users (Year 1)
- 10,000 concurrent users (Year 2)
- 100,000 concurrent users (Year 3)

**Database:**
- 100,000 organizations
- 1,000,000 assessments
- 100,000,000 survey responses

**Storage:**
- 1 TB for assessment data
- 10 TB for generated reports

### 9.3 Availability

**Uptime Target:** 99.9% (8.77 hours downtime/year)

**Disaster Recovery:**
- RPO (Recovery Point Objective): 1 hour
- RTO (Recovery Time Objective): 4 hours
- Geo-redundant backups across 2 Azure regions

---

## 10. Implementation Roadmap

### Phase 1: MVP (Weeks 1-6)

**Week 1-2: Foundation**
- ✅ Project setup (Next.js 14 + TypeScript + Shadcn/ui)
- ✅ Authentication (NextAuth.js + Azure AD B2C)
- ✅ Database schema (Cosmos DB)
- ✅ Navigation shell (icon nav + sidebar)
- ✅ Organization registration flow

**Week 3-4: Survey Engine**
- ✅ Qualitative Initial Survey (48 questions)
- ✅ Question components (rating scale, progress bar)
- ✅ Auto-save functionality
- ✅ Survey validation
- ✅ Assessment creation & management APIs

**Week 5-6: Risk Calculation & Dashboard**
- ✅ Python Risk Engine (Monte Carlo simulation)
- ✅ Risk metrics calculation (9 metrics)
- ✅ Basic dashboard (executive summary + metrics)
- ✅ VOC heatmap visualization
- ✅ Export to PDF

**Deliverable:** Functional qualitative risk assessment with basic dashboard

---

### Phase 2: Quantitative Mode (Weeks 7-10)

**Week 7-8: Quantitative Survey**
- ✅ Data input components (with units)
- ✅ Data validation (Zod schemas)
- ✅ Fallback scale option
- ✅ CSV import functionality
- ✅ Data quality scoring

**Week 9-10: Enhanced Analytics**
- ✅ Monte Carlo distribution visualization
- ✅ Scenario analysis (best/worst/likely)
- ✅ AI-generated recommendations (Azure OpenAI)
- ✅ Trend analysis (compare assessments)
- ✅ Export to Excel & PowerPoint

**Deliverable:** Full quantitative assessment mode with advanced analytics

---

### Phase 3: Regional & Collaboration (Weeks 11-14)

**Week 11-12: Regional Assessments**
- ✅ Detailed survey (region-specific responses)
- ✅ Region selector & progress tracking
- ✅ Regional comparison dashboard
- ✅ Variance analysis & hotspot identification
- ✅ Bulk copy across regions

**Week 13-14: Collaboration Features**
- ✅ Multi-user collaboration (invite team members)
- ✅ Role-based permissions (Admin/Analyst/Viewer)
- ✅ Comments & annotations on survey responses
- ✅ Approval workflows
- ✅ Activity log & audit trail

**Deliverable:** Regional risk analysis with team collaboration

---

### Phase 4: Enterprise Features (Weeks 15-18)

**Week 15-16: Advanced Reporting**
- ✅ Custom report templates
- ✅ Scheduled automated reports
- ✅ Dashboard embedding (iframe)
- ✅ API access for data integration
- ✅ Webhooks for assessment events

**Week 17-18: Administration & Billing**
- ✅ Organization settings & user management
- ✅ Subscription management (Stripe integration)
- ✅ Usage analytics & billing dashboard
- ✅ White-label options
- ✅ SSO configuration (SAML 2.0)

**Deliverable:** Enterprise-ready platform with billing & admin features

---

### Phase 5: Optimization & Launch (Weeks 19-20)

**Week 19: Performance & Security**
- ✅ Performance optimization (caching, CDN)
- ✅ Security audit & penetration testing
- ✅ Load testing (10,000 concurrent users)
- ✅ Compliance documentation (GDPR, SOC 2)
- ✅ Accessibility audit (WCAG 2.1 AA)

**Week 20: Launch Preparation**
- ✅ User documentation & help center
- ✅ Video tutorials & onboarding flows
- ✅ Marketing website integration
- ✅ Beta user feedback incorporation
- ✅ Production deployment

**Deliverable:** Production-ready platform ready for public launch

---

## 11. Success Metrics

### 11.1 Product Metrics

**Usage Metrics:**
- Monthly Active Users (MAU)
- Weekly Active Users (WAU)
- Daily Active Users (DAU)
- Assessments created per month
- Assessment completion rate
- Average time to complete (Initial vs Detailed)

**Engagement Metrics:**
- User retention (30-day, 90-day)
- Feature adoption rate (Qualitative vs Quantitative)
- Dashboard views per assessment
- Export downloads per assessment
- Return user rate (multiple assessments)

**Business Metrics:**
- Free-to-paid conversion rate
- Monthly Recurring Revenue (MRR)
- Customer Lifetime Value (LTV)
- Customer Acquisition Cost (CAC)
- Net Promoter Score (NPS)

### 11.2 Technical Metrics

**Performance:**
- Page load time (p50, p90, p95)
- API response time (p50, p90, p95)
- Time to Interactive (TTI)
- First Contentful Paint (FCP)
- Cumulative Layout Shift (CLS)

**Reliability:**
- Uptime percentage
- Mean Time Between Failures (MTBF)
- Mean Time To Recovery (MTTR)
- Error rate (4xx, 5xx responses)
- Failed transaction rate

**Quality:**
- Test coverage (>80% target)
- Production bugs per release
- Customer-reported issues per month
- Time to fix critical bugs

---

## 12. Non-Functional Requirements

### 12.1 Accessibility

**WCAG 2.1 Level AA Compliance:**
- ✅ Keyboard navigation support
- ✅ Screen reader compatibility
- ✅ Sufficient color contrast (4.5:1 for text)
- ✅ Focus indicators
- ✅ Alt text for images
- ✅ ARIA labels for interactive elements
- ✅ Responsive text sizing

### 12.2 Internationalization

**Language Support (Phase 2+):**
- English (default)
- Spanish
- French
- German
- Portuguese (Brazilian)

**Localization:**
- Currency formatting
- Date/time formatting
- Number formatting
- Right-to-left (RTL) support (future)

### 12.3 Browser Support

**Desktop:**
- Chrome 90+ (primary)
- Firefox 88+
- Safari 14+
- Edge 90+

**Mobile:**
- iOS Safari 14+
- Chrome Mobile 90+
- Samsung Internet 14+

**Note:** Internet Explorer not supported

### 12.4 Device Support

**Responsive Breakpoints:**
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px - 1439px
- Large Desktop: 1440px+

**Optimal Experience:**
- Desktop: 1920×1080 or higher
- Tablet: 1024×768 landscape
- Mobile: Survey simplified, dashboard view-only

---

## 13. Risk Mitigation (Product Development)

### 13.1 Technical Risks

**Risk:** Python Risk Engine performance bottleneck
**Mitigation:**
- Implement caching for common calculation patterns
- Use Azure Functions with auto-scaling
- Pre-calculate results for partial survey completion
- Queue system for long-running calculations

**Risk:** Database costs for large-scale deployment
**Mitigation:**
- Implement intelligent data archival
- Use Azure Cosmos DB's serverless pricing for development
- Optimize queries and indexes
- Consider read replicas for reporting

**Risk:** Real-time sync conflicts in multi-user scenarios
**Mitigation:**
- Implement operational transformation for conflict resolution
- Lock mechanism for concurrent edits
- Clear visual indicators for conflicts
- Auto-merge with user review

### 13.2 User Experience Risks

**Risk:** Survey abandonment due to length
**Mitigation:**
- Progress indicator with time estimates
- Save & continue later functionality
- Auto-save every 30 seconds
- Reminder emails for incomplete assessments
- Gamification elements (progress badges)

**Risk:** Complex dashboard overwhelming users
**Mitigation:**
- Progressive disclosure of information
- Guided tours for first-time users
- Collapsible sections with smart defaults
- Customizable dashboard layout
- Export to familiar formats (Excel, PDF)

### 13.3 Business Risks

**Risk:** Low user adoption of quantitative mode (data availability issues)
**Mitigation:**
- Industry benchmark data to fill gaps
- Estimation guidance and calculators
- Hybrid mode (mix of scale and data)
- Partner integrations for automated data pull

**Risk:** Difficulty explaining risk calculation methodology
**Mitigation:**
- Transparent methodology documentation
- White papers on Monte Carlo approach
- Academic partnerships for credibility
- Case studies with real results
- Certification program for users

---

## 14. Future Enhancements (Post-MVP)

### 14.1 Advanced Analytics

**Predictive Risk Modeling:**
- Machine learning models to predict future risk trends
- Early warning system for emerging risks
- Automated anomaly detection

**Industry Benchmarking:**
- Compare risk profile against industry peers
- Percentile rankings by company size, region, industry
- Best practice recommendations from high-performers

**Scenario Planning:**
- "What-if" analysis tools
- Stress testing (recession, cyber attack, regulatory change)
- Risk mitigation ROI calculator

### 14.2 Integration Ecosystem

**Data Integrations:**
- ERP systems (SAP, Oracle, Microsoft Dynamics)
- Financial systems (QuickBooks, Xero, NetSuite)
- HR systems (Workday, BambooHR, ADP)
- Project management (Jira, Monday.com, Asana)
- GRC platforms (ServiceNow, MetricStream)

**Workflow Integrations:**
- Slack/Teams notifications for risk alerts
- Email automation for stakeholder reports
- Calendar integration for review schedules
- CRM integration (Salesforce, HubSpot)

### 14.3 Mobile Applications

**Native Mobile Apps:**
- iOS app (SwiftUI)
- Android app (Kotlin)
- Offline-first architecture
- Push notifications for risk alerts
- Mobile-optimized survey experience

### 14.4 AI-Powered Features

**Intelligent Survey Assistant:**
- Auto-fill suggestions based on organization profile
- Smart question routing (skip irrelevant questions)
- Natural language query interface
- Voice input for survey responses

**Risk Intelligence Agent:**
- Proactive risk monitoring
- Automated risk mitigation tracking
- Natural language recommendations
- Conversational dashboard exploration

---

## 15. Success Criteria for MVP Launch

**Must Have (P0):**
- ✅ Complete Qualitative Initial Survey (48 questions)
- ✅ Risk calculation engine with Monte Carlo simulation
- ✅ Dashboard with 9 risk metrics
- ✅ VOC heatmap (16 dimensions)
- ✅ User authentication & organization management
- ✅ PDF export functionality
- ✅ Mobile-responsive design
- ✅ <3s dashboard load time
- ✅ 99% uptime in production

**Should Have (P1):**
- ✅ Quantitative survey mode
- ✅ Excel & PowerPoint export
- ✅ Assessment history & comparison
- ✅ AI-generated recommendations
- ✅ Multi-user organization support
- ✅ Auto-save functionality

**Nice to Have (P2):**
- ✅ Detailed regional surveys
- ✅ Real-time dashboard updates (SignalR)
- ✅ CSV import for data
- ✅ Custom report templates
- ✅ API access

**Launch Metrics Targets:**
- 100 beta users complete at least one assessment
- Average NPS score >50
- <5% survey abandonment rate
- >80% of users understand dashboard metrics
- >90% of users find recommendations actionable

---

## 16. Appendix

### 16.1 Survey Question Mapping

See files:
- `Initial_Survey_Scale_Version_v2.csv`
- `Initial_Survey_Data_Version_v2.csv`
- `Detailed_Survey_Scale_Version_v2.csv`
- `Detailed_Survey_Data_Version_v2.csv`

### 16.2 Risk Calculation Formulas

**Monte Carlo Simulation Approach:**

```python
def calculate_enterprise_value_at_risk(responses, org_profile, iterations=10000):
    """
    Calculate Enterprise Value at Risk using Monte Carlo simulation

    Inputs:
    - responses: Dict of survey responses (48 questions)
    - org_profile: Organization profile (revenue, size, etc.)
    - iterations: Number of Monte Carlo iterations

    Output:
    - EV at Risk distribution (mean, median, percentiles)
    """

    # 1. Normalize responses to 0-1 risk scores
    risk_scores = normalize_responses(responses)

    # 2. Apply VOC dimension weights
    dimension_weights = {
        'Financials': 0.15,
        'Business Model': 0.12,
        'External Environment': 0.10,
        'Governance': 0.08,
        'Brand': 0.08,
        'Culture': 0.07,
        'People': 0.07,
        'Technology': 0.08,
        'Third Parties': 0.05,
        'Innovation': 0.05,
        'Change': 0.04,
        'Processes': 0.04,
        'Products & Services': 0.07,
        'Annual Results': 0.10,
        'Strategic Goals': 0.05,
        'Reputation': 0.05
    }

    # 3. Calculate weighted dimension scores
    weighted_scores = apply_weights(risk_scores, dimension_weights)

    # 4. Run Monte Carlo simulation
    ev_risks = []
    for i in range(iterations):
        # Add stochastic variation based on data quality
        simulated_scores = add_uncertainty(weighted_scores)

        # Calculate EV at Risk for this iteration
        ev_risk = calculate_ev_for_iteration(
            simulated_scores,
            org_profile['annualRevenue'],
            org_profile['employeeCount']
        )
        ev_risks.append(ev_risk)

    # 5. Analyze distribution
    return {
        'mean': np.mean(ev_risks),
        'median': np.median(ev_risks),
        'p75': np.percentile(ev_risks, 75),
        'p90': np.percentile(ev_risks, 90),
        'p95': np.percentile(ev_risks, 95),
        'std': np.std(ev_risks),
        'distribution': ev_risks
    }
```

**Risk Metric Mappings:**

Each of the 9 risk metrics is influenced by specific VOC dimensions:

```python
RISK_METRIC_MAPPINGS = {
    'opex_at_risk': [
        ('Financials', 0.25),
        ('Technology', 0.20),
        ('Third Parties', 0.15),
        ('Processes', 0.15),
        ('People', 0.15),
        ('Governance', 0.10)
    ],
    'capex_at_risk': [
        ('Financials', 0.30),
        ('Technology', 0.25),
        ('Change', 0.20),
        ('Innovation', 0.15),
        ('Governance', 0.10)
    ],
    'stratex_at_risk': [
        ('Strategic Goals', 0.30),
        ('Innovation', 0.25),
        ('Change', 0.20),
        ('Culture', 0.15),
        ('External Environment', 0.10)
    ],
    'revenue_at_risk': [
        ('Annual Results', 0.25),
        ('Business Model', 0.20),
        ('Products & Services', 0.15),
        ('Brand', 0.15),
        ('Reputation', 0.15),
        ('External Environment', 0.10)
    ],
    # ... additional mappings
}
```

### 16.3 Technology Vendor List

**Core Infrastructure:**
- Microsoft Azure (Cloud platform)
- Vercel (Frontend hosting - alternative)
- Cloudflare (CDN & security)

**Development Tools:**
- Next.js 14 (Framework)
- TypeScript (Language)
- Shadcn/ui (UI components)
- Tailwind CSS (Styling)
- Recharts (Charts)
- React Hook Form (Forms)
- Zod (Validation)

**Backend Services:**
- Azure Cosmos DB (Database)
- Azure Functions (Serverless compute)
- Azure Cache for Redis (Caching)
- Azure SignalR Service (Real-time)
- Azure Blob Storage (File storage)
- Azure Service Bus (Message queue)

**AI/ML:**
- Azure OpenAI Service (GPT-4)
- Python + NumPy + SciPy (Monte Carlo)

**Monitoring & Analytics:**
- Azure Application Insights (APM)
- Azure Monitor (Infrastructure)
- Sentry (Error tracking)
- Google Analytics (Web analytics)

**Development:**
- GitHub (Code repository)
- GitHub Actions (CI/CD)
- Jest (Testing)
- Playwright (E2E testing)
- Storybook (Component library)

---

## 17. Glossary

**Assessment:** A single risk analysis session (one survey completion)

**Domain:** Top-level grouping in VOC framework (Economics, Enablers, Execution, Value)

**Dimension:** One of 16 risk categories within VOC framework

**Enterprise Value at Risk (EV at Risk):** Total estimated impact on firm value from identified risks

**Monte Carlo Simulation:** Statistical technique using repeated random sampling to estimate probability distributions

**Qualitative Assessment:** Risk analysis using subjective 1-5 scales

**Quantitative Assessment:** Risk analysis using objective numerical data

**Region:** One of 6 geographic areas (Europe, North America, South America, Asia, Oceania, Africa)

**Risk Factor:** Individual question/metric within a dimension (3 factors per dimension in Initial, 4 in Detailed)

**Risk Metric:** One of 9 calculated risk exposure values (Opex, Capex, Stratex, Revenue, Productivity, Service Availability, Reputation, Enterprise Value)

**Value Orchestration Canvas (VOC):** Framework with 16 dimensions across 4 domains for holistic business analysis

---

## 18. Contact & Support

**Product Owner:** [Name]
**Technical Lead:** [Name]
**Project Manager:** [Name]

**For Claude Code Implementation:**
- All code should follow Next.js 14 App Router patterns
- Use TypeScript strict mode
- Follow Shadcn/ui design system
- Implement comprehensive error handling
- Include unit tests for all business logic
- Document API endpoints with OpenAPI/Swagger
- Use environment variables for all configuration
- Follow Azure Well-Architected Framework principles

---

**Document Version:** 1.0
**Last Updated:** October 27, 2025
**Next Review:** November 10, 2025

**Approved by:** [Stakeholder Name]
**Status:** Ready for Development Sprint Planning
