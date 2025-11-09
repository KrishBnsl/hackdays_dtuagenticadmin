# 🎨 UI Features Overview

## Main Interface

### Header Section
```
┌─────────────────────────────────────────────────────────────┐
│                  📝 Exam Grading System                      │
│         Upload your exam answer sheet PDF to get             │
│                   automated grading                          │
└─────────────────────────────────────────────────────────────┘
```

### Sidebar (Left Panel)
```
┌─────────────────────────┐
│ ℹ️ About                │
│ - Automated grading     │
│ - Question-wise eval    │
│ - Detailed feedback     │
│ - Consistent results    │
│                         │
│ 📋 Instructions         │
│ 1. Upload PDF           │
│ 2. Click 'Grade Exam'   │
│ 3. Wait for processing  │
│ 4. View results         │
└─────────────────────────┘
```

### Upload Section
```
┌─────────────────────────────────────────────────────────────┐
│  📁 Drag and drop PDF here or click to browse               │
│                                                              │
│  ✓ File uploaded: Physics_Exam_Student1.pdf                 │
│                                                              │
│  [🚀 Grade Exam]                                            │
└─────────────────────────────────────────────────────────────┘
```

### Processing View
```
┌─────────────────────────────────────────────────────────────┐
│  Processing...                                               │
│  ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 45%        │
│  Grading Section B - Short Answer Questions...              │
└─────────────────────────────────────────────────────────────┘
```

## Results Dashboard

### Summary Cards (Top Row)
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total Score  │ Percentage   │    Grade     │  Questions   │
│   85.5/100   │   85.50%     │      A       │   Graded: 25 │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

### Visual Chart
```
📈 Question-wise Scores

Percentage
100% ┤     █
 90% ┤ █   █ █
 80% ┤ █ █ █ █   █
 70% ┤ █ █ █ █ █ █
 60% ┤ █ █ █ █ █ █ █
 50% ┤ █ █ █ █ █ █ █
     └─────────────────
      Q1 Q2 Q3 Q4 Q5 Q6 Q7
```

### Score Table (Expandable)
```
┌─────────────────────────────────────────────────────────────┐
│ 📋 View Detailed Score Table                          [▼]   │
├──────────┬──────────┬──────────┬────────────────────────────┤
│ Question │ Obtained │  Total   │      Percentage            │
├──────────┼──────────┼──────────┼────────────────────────────┤
│   Q1     │   4.0    │   4.0    │       100.0%               │
│   Q2     │   3.5    │   4.0    │        87.5%               │
│   Q3     │   2.0    │   3.0    │        66.7%               │
│   Q4     │   5.0    │   5.0    │       100.0%               │
└──────────┴──────────┴──────────┴────────────────────────────┘
```

### Detailed Evaluation (Expandable Sections)
```
┌─────────────────────────────────────────────────────────────┐
│ 📝 Detailed Evaluation                                       │
├─────────────────────────────────────────────────────────────┤
│ 📂 Section A - Multiple Choice Questions            [▼]     │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ Question 1: 4.0/4.0                                   │   │
│ │ ────────────────────────────────────────────────────  │   │
│ │ Student's Answer:                                     │   │
│ │ Selected option (C) - Newton's Second Law             │   │
│ │                                                       │   │
│ │ Expected Answer (from Marking Scheme):                │   │
│ │ Option (C) is correct                                 │   │
│ │                                                       │   │
│ │ Evaluation:                                           │   │
│ │ ✓ Correct: Answer matches marking scheme             │   │
│ │ ✗ Missing/Incorrect: None                            │   │
│ │                                                       │   │
│ │ Marks Breakdown:                                      │   │
│ │ Full marks awarded for correct answer                │   │
│ └───────────────────────────────────────────────────────┘   │
│                                                              │
│ 📂 Section B - Short Answer Questions               [▶]     │
│ 📂 Section C - Long Answer Questions                [▶]     │
│ 📂 Section D - Numerical Problems                   [▶]     │
└─────────────────────────────────────────────────────────────┘
```

### Download Section
```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  [📥 Download Full Report]                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Color Scheme

### Grade Colors
- **A+/A**: Green background (#d4edda) - Excellent
- **B+/B**: Blue background (#d1ecf1) - Good
- **C**: Yellow background (#fff3cd) - Average
- **D**: Light red background (#f8d7da) - Below Average
- **F**: Red background (#f5c6cb) - Fail

### UI Elements
- **Primary Blue**: #1f77b4 (Headers)
- **Secondary Blue**: #3498db (Borders, accents)
- **Dark Text**: #2c3e50 (Section headers)
- **Light Background**: #f8f9fa (Cards)
- **Gray Text**: #7f8c8d (Footer)

## Interactive Elements

### Buttons
- **Primary Button**: Blue with white text
- **Hover Effect**: Slightly darker shade
- **Disabled State**: Gray with reduced opacity

### Expandable Sections
- **Collapsed**: Shows arrow (▶) and section name
- **Expanded**: Shows arrow (▼) and full content
- **Click anywhere** on header to toggle

### Progress Bar
- **Animated**: Smooth progression
- **Color**: Blue gradient
- **Status Text**: Updates with current action

### File Upload
- **Drag & Drop**: Highlighted border on hover
- **Click to Browse**: Opens file picker
- **Success State**: Green checkmark with filename

## Responsive Design

### Desktop (Wide Screen)
- 4-column summary cards
- Full-width charts
- Side-by-side layouts

### Tablet (Medium Screen)
- 2-column summary cards
- Adjusted chart width
- Stacked layouts

### Mobile (Small Screen)
- Single column layout
- Vertical cards
- Scrollable content

## Accessibility Features

- **High Contrast**: Clear text on backgrounds
- **Large Fonts**: Readable sizes (1.5rem headers)
- **Color + Icons**: Not relying on color alone
- **Keyboard Navigation**: Tab through elements
- **Screen Reader Friendly**: Semantic HTML

## User Experience Flow

1. **Landing** → Clean interface with clear CTA
2. **Upload** → Immediate feedback on file selection
3. **Processing** → Real-time progress updates
4. **Results** → Organized, scannable information
5. **Export** → One-click download

## Performance Indicators

- **Loading Spinner**: During API calls
- **Progress Bar**: Shows completion percentage
- **Status Messages**: Describes current action
- **Success Animation**: Balloons on completion
- **Error Messages**: Clear, actionable feedback

---

**Design Philosophy**: Clean, professional, and user-friendly interface that makes exam grading efficient and transparent.
