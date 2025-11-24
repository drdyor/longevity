"""
Generate realistic demo data from r/longevity for testing the pipeline.
This allows testing without Reddit API credentials.
"""
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Realistic r/longevity posts based on actual community patterns
DEMO_POSTS = [
    {
        "title": "6mg rapamycin weekly - my 1 year update",
        "selftext": "Started taking 6mg rapamycin weekly about a year ago. Noticed improvements in recovery time from workouts, better skin quality, and consistent energy levels. Blood work shows slightly improved lipid panel. No major side effects except some minor mouth sores in the first month. Planning to continue.",
        "score": 342,
        "num_comments": 89
    },
    {
        "title": "NAD+ precursors: NMN vs NR - what does the science actually say?",
        "selftext": "Been researching NAD+ boosters and the evidence seems mixed. Most studies are in mice, and the human trials show modest increases in NAD+ levels but unclear functional benefits. NMN seems to have better bioavailability than NR, but both are expensive. What are people's experiences?",
        "score": 278,
        "num_comments": 156
    },
    {
        "title": "Metformin for longevity - TAME trial update?",
        "selftext": "Has anyone heard updates on the TAME (Targeting Aging with Metformin) trial? I've been taking 500mg twice daily for 6 months (off-label for longevity). Feel good but hard to know if it's placebo. Interested in hearing others' experiences.",
        "score": 215,
        "num_comments": 67
    },
    {
        "title": "GLP-1 agonists (semaglutide) for healthspan extension",
        "selftext": "Recent studies show GLP-1 agonists like semaglutide (Ozempic/Wegovy) may have benefits beyond weight loss - reduced inflammation, improved cardiovascular outcomes, potential neuroprotective effects. Anyone taking these for longevity purposes (not just weight loss)?",
        "score": 567,
        "num_comments": 234
    },
    {
        "title": "Time-restricted eating: 16:8 vs OMAD for autophagy",
        "selftext": "Been experimenting with different fasting protocols. Started with 16:8 intermittent fasting, now doing one meal a day (OMAD). Feel amazing - mental clarity, stable energy, lost 15 lbs. Question: does the autophagy benefit plateau after 16 hours or continue to increase with longer fasts?",
        "score": 189,
        "num_comments": 92
    },
    {
        "title": "Senolytics update: Dasatinib + Quercetin protocol",
        "selftext": "Just completed my first senolytic treatment cycle (100mg dasatinib + 1000mg quercetin for 2 days). No major side effects. Too early to tell on benefits. Following the Mayo Clinic protocol. Anyone else trying this?",
        "score": 445,
        "num_comments": 178
    },
    {
        "title": "Resveratrol - overhyped or underrated?",
        "selftext": "The SIRT1 activator that was supposed to mimic caloric restriction. Initial studies were exciting but later research questioned the mechanism. Bioavailability is reportedly poor. Is anyone still taking this? What dosage?",
        "score": 156,
        "num_comments": 98
    },
    {
        "title": "Heavy resistance training 3x/week - best longevity exercise?",
        "selftext": "Recent research suggests resistance training may be more important than cardio for healthspan. Benefits: maintains muscle mass (critical as we age), bone density, metabolic health, functional strength. Doing 3x/week full body workouts. Game changer.",
        "score": 298,
        "num_comments": 112
    },
    {
        "title": "Spermidine from wheat germ - autophagy inducer",
        "selftext": "Taking 10mg spermidine daily (from wheat germ extract). Research shows it induces autophagy similar to fasting, may improve cardiovascular health and cognitive function. Relatively cheap supplement with promising animal data. Human trials are limited though.",
        "score": 123,
        "num_comments": 45
    },
    {
        "title": "Cold exposure protocol - 3 min cold showers daily",
        "selftext": "Been doing 3-minute cold showers every morning for 6 months. Benefits: improved mood/alertness, better cold tolerance, possibly increased brown fat activation. Some studies show immune system benefits. It's free and relatively easy to implement!",
        "score": 167,
        "num_comments": 73
    },
    {
        "title": "Alpha-ketoglutarate (AKG) - underrated longevity supplement?",
        "selftext": "New study showed AKG reduced biological age by 8 years in humans. It's a TCA cycle intermediate that declines with age. Taking 1g twice daily. Anyone else experimenting with this?",
        "score": 234,
        "num_comments": 87
    },
    {
        "title": "Berberine as a metformin alternative",
        "selftext": "For those who can't get metformin prescribed, berberine might be an alternative. Similar mechanism (AMPK activation), improves glucose metabolism and insulin sensitivity. Taking 500mg 3x daily with meals. Cheaper and no prescription needed.",
        "score": 189,
        "num_comments": 65
    },
    {
        "title": "Nicotinamide riboside (NR) - 8 month results",
        "selftext": "Been taking 300mg NR daily for 8 months. Initial boost in energy has leveled off but sustained improvements in recovery and sleep quality. Blood NAD+ levels increased by ~40% according to lab tests. Expensive but seems worth it for me.",
        "score": 145,
        "num_comments": 56
    },
    {
        "title": "Rapamycin dosing: weekly vs biweekly for longevity",
        "selftext": "Seeing different protocols: some take 5-6mg weekly, others do 10-12mg biweekly. What does the research suggest is optimal for healthspan benefits while minimizing immunosuppression? Current protocol is 6mg every 10 days.",
        "score": 267,
        "num_comments": 134
    },
    {
        "title": "Glycine supplementation for sleep and longevity",
        "selftext": "Taking 3g glycine before bed has dramatically improved my sleep quality. Research also shows glycine may extend lifespan (rodent data) and improve metabolic health. Super cheap supplement, highly recommend trying.",
        "score": 198,
        "num_comments": 71
    },
    {
        "title": "Acarbose for longevity - anyone taking this?",
        "selftext": "Acarbose is an alpha-glucosidase inhibitor that slows carb absorption. Extended lifespan in male mice in ITP study. Thinking of adding to my stack. Side effects seem to be mainly GI (gas, bloating). Anyone have experience?",
        "score": 134,
        "num_comments": 48
    },
    {
        "title": "VO2 max training - the single best longevity metric?",
        "selftext": "Attia and others argue VO2 max is the strongest predictor of all-cause mortality. Been doing HIIT 2x/week and zone 2 cardio 3x/week to improve it. Went from 42 to 51 ml/kg/min in 6 months. Highly recommend testing yours.",
        "score": 312,
        "num_comments": 145
    },
    {
        "title": "Lithium microdosing for neuroprotection",
        "selftext": "Low-dose lithium (5-10mg elemental) may have neuroprotective benefits and potentially extend lifespan. Much lower than psychiatric doses. Some evidence for reduced dementia risk in areas with higher lithium in water supply. Starting 5mg daily.",
        "score": 176,
        "num_comments": 82
    },
    {
        "title": "Sulforaphane from broccoli sprouts - Nrf2 activator",
        "selftext": "Growing my own broccoli sprouts for sulforaphane. Activates Nrf2 pathway for antioxidant defense. Way cheaper than supplements and fresher. Simple to grow at home. One tablespoon of sprouts daily gives therapeutic dose.",
        "score": 221,
        "num_comments": 94
    },
    {
        "title": "Fisetin as a senolytic - Mayo Clinic dosing protocol",
        "selftext": "Planning to try fisetin (1000-1500mg/day for 2 consecutive days, once per month) as a senolytic. Cheaper than dasatinib/quercetin combo. Animal studies promising. Human data lacking. Worth a shot?",
        "score": 187,
        "num_comments": 73
    }
]

def generate_demo_data():
    """Generate realistic demo dataset."""
    print("=" * 60)
    print("Generating Demo Data (No Reddit API Needed)")
    print("=" * 60)
    
    # Generate data with realistic timestamps
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    posts = []
    for i, post_data in enumerate(DEMO_POSTS):
        # Random date within last year
        days_ago = random.randint(0, 365)
        created_date = end_date - timedelta(days=days_ago)
        
        posts.append({
            "id": f"demo_{i+1:03d}",
            "title": post_data["title"],
            "selftext": post_data["selftext"],
            "url": f"https://reddit.com/r/longevity/comments/demo_{i+1:03d}/",
            "score": post_data["score"] + random.randint(-20, 50),
            "num_comments": post_data["num_comments"] + random.randint(-10, 30),
            "created_utc": created_date.isoformat(),
            "author": f"longevity_user_{random.randint(1, 100)}"
        })
    
    # Save to CSV
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(output_dir, f"posts_{timestamp}.csv")
    
    df = pd.DataFrame(posts)
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Generated {len(df)} demo posts")
    print(f"✓ Saved to: {output_file}")
    print(f"  Date range: {df['created_utc'].min()} to {df['created_utc'].max()}")
    print(f"  Total score: {df['score'].sum():,}")
    print(f"  Total comments: {df['num_comments'].sum():,}")
    print(f"\n  Topics covered:")
    print(f"  - Rapamycin, NAD+, Metformin, GLP-1 agonists")
    print(f"  - Fasting, Exercise, Senolytics, Cold exposure")
    print(f"  - And more...")
    print(f"\n✅ Ready for claim extraction!")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(generate_demo_data())
