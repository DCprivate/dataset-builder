# Software/DataHarvester_DDD/services/data_ingestion/docs/SCRAPERS.md

# Data Source Scrapers

## Current Implementations
- YouTube Transcript Scraper

## Planned Legal Data Implementations
### Legal Forums & Q&A
- Avvo Legal Forums
- Justia Forums
- Law Stack Exchange
- Above The Law Comments

### Legal News & Blogs
- Reuters Legal
- Law360
- SCOTUSblog
- ABA Journal
- The Legal Intelligencer
- Above The Law

### Legal Documents & Cases
- PACER (Public Access to Court Electronic Records)
- OpenLegalData.io
- ACLU Cases Database
- EFF Legal Cases

### Future Implementations
- Reddit Scraper
- Twitter Scraper
- Stack Exchange Scraper

## Adding New Scrapers
1. Create new scraper in `application/services/scrapers/{platform}`
2. Implement the base scraper interface
3. Add configuration in `config/scrapers/{platform}.yaml`
4. Add validation rules in `validation/rules/scraper_rules/{platform}_rules.py`

## Special Considerations
### Authentication Requirements
- PACER: Requires account and fees
- Law360: Premium subscription required
- Reuters Legal: Subscription required

### Rate Limiting
- PACER: Strict access limits
- Law360: API rate limits
- Reuters: Request limits

### Data Storage Requirements
- Legal documents: Versioning required
- Case law: Citation tracking
- News articles: Update tracking

### Compliance Requirements
- Terms of Service adherence
- Data retention policies
- Usage rights and licensing
- Privacy considerations

# Scraper Services

## Structure
Each scraper should follow this structure:
scrapers/
├── base/
│   └── base_scraper.py       # Abstract base class for scrapers
├── youtube/                  # Current implementation
├── reddit/                  # Future implementation
│   ├── reddit_scraper.py
│   ├── reddit_api.py
│   └── reddit_models.py
├── twitter/                 # Future implementation
│   ├── twitter_scraper.py
│   ├── twitter_api.py
│   └── twitter_models.py
└── stack_exchange/         # Future implementation
    ├── stack_exchange_scraper.py
    ├── stack_exchange_api.py
    └── stack_exchange_models.py

# Scraper Configurations

## Structure
config/scrapers/
├── youtube.yaml     # Current implementation
├── reddit.yaml     # Future implementation
├── twitter.yaml    # Future implementation
└── stack_exchange.yaml  # Future implementation

Each config should include:
- API credentials (referenced from env)
- Rate limiting settings
- Content filters
- Platform-specific settings

# Scraper Domain Models

## Structure
models/scrapers/
├── base_models.py           # Common base models
├── youtube_models.py        # Current implementation
├── reddit_models.py         # Future implementation
├── twitter_models.py        # Future implementation
└── stack_exchange_models.py # Future implementation

Each platform should define:
- Content models
- User models
- Metadata models
- Platform-specific models

# MongoDB Collections Structure

## Current Collections
- youtube_transcripts
- processed_transcripts

## Planned Collections
- reddit_posts
- reddit_comments
- twitter_tweets
- twitter_threads
- stack_exchange_questions
- stack_exchange_answers

Each collection should have:
- Appropriate indexes
- Data validation rules
- TTL indexes if needed

# Scraper Validation Rules
## Structure

validation/rules/scraper_rules/
├── base_rules.py           # Common validation rules
├── youtube_rules.py        # Current implementation
├── reddit_rules.py         # Future implementation
├── twitter_rules.py        # Future implementation
└── stack_exchange_rules.py # Future implementation

Each platform should define:
- URL validation patterns
- Content validation rules
- Rate limit validation
- API response validation
