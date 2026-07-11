# Data Sources for Market Research

## Real-Time Data Sources

### X/Twitter API
- **Endpoint**: `https://api.twitter.com/2/tweets/search/recent`
- **Rate Limit**: 450 requests/15-min window (Essential tier)
- **Use Cases**: Trend detection, sentiment analysis, viral content identification
- **Query Examples**:
  - `"(web3 OR crypto) -is:retweet lang:en`
  - `"next.js" OR "react" OR "node.js" -is:retweet`

### Xquik Read-Only API

- **Endpoint**: `https://xquik.com/api/v1`
- **Authentication**: `X-API-Key` header
- **Use Cases**: Structured post search, public profile research, and trend comparison
- **Agent Access**: Remote MCP server at `https://xquik.com/mcp`

Keep collection read-only by default. Require explicit approval before enabling
writes, persistent monitors, webhooks, or private account access.

```bash
export XQUIK_API_KEY="your-api-key"

# Search recent public posts
curl 'https://xquik.com/api/v1/x/tweets/search?q=open%20source%20agents&limit=20' \
  -H "X-API-Key: ${XQUIK_API_KEY}"

# Fetch a public profile
export X_USERNAME="github"
curl "https://xquik.com/api/v1/x/users/${X_USERNAME}" \
  -H "X-API-Key: ${XQUIK_API_KEY}"

# Compare worldwide trends
curl 'https://xquik.com/api/v1/trends?woeid=1&count=10' \
  -H "X-API-Key: ${XQUIK_API_KEY}"
```

See the [Xquik MCP overview](https://docs.xquik.com/mcp/overview) for
agent-native setup and tool discovery.

### Reddit API
- **Endpoint**: `https://www.reddit.com/r/{subreddit}/hot.json`
- **Rate Limit**: 60 requests/minute
- **Key Subreddits**: r/programming, r/webdev, r/reactjs, r/node, r/cryptocurrency
- **Use Cases**: Technical discussions, community sentiment, problem identification

### GitHub API
- **Endpoint**: `https://api.github.com/search/repositories`
- **Rate Limit**: 10 requests/minute (unauthenticated)
- **Metrics**: Stars, forks, issues, commits, contributors
- **Use Cases**: Technology adoption trends, project health assessment

## Market Intelligence Platforms

### Google Trends
- **Endpoint**: `https://trends.google.com/trends/api/`
- **Indicators**: Interest over time, regional interest, related queries
- **Use Cases**: Technology adoption forecasting, market demand validation

### Product Hunt
- **API**: Limited public API, consider web scraping
- **Metrics**: Upvotes, comments, launch success
- **Use Cases**: Product validation, feature gap analysis

### Crunchbase
- **Endpoint**: `https://api.crunchbase.com/v4/entities/organizations`
- **Indicators**: Funding rounds, company growth, market size
- **Use Cases**: Market size estimation, competitive landscape

## Technical Trend Detection

### Stack Overflow Developer Survey
- **Frequency**: Annual
- **Data**: Technology usage, developer preferences, salary trends
- **Use Cases**: Technology selection validation

### NPM Download Statistics
- **Endpoint**: `https://api.npmjs.org/downloads`
- **Metrics**: Weekly/monthly downloads, growth rate
- **Use Cases**: Package popularity, ecosystem health

### GitHub Language Statistics
- **Endpoint**: `https://api.github.com/languages`
- **Indicators**: Language usage trends, project distribution
- **Use Cases**: Technology trend forecasting

## AI-Powered Analysis Tools

### Sentiment Analysis

```javascript
const sentimentProviders = {
  twitter: 'natural-language-understanding',
  reddit: 'perspective-api',
  news: 'azure-text-analytics'
};
```

### Topic Modeling

```python
# Using GPT-based topic extraction
def extract_topics(text_corpus):
    topics = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "Extract key technology topics from this text corpus"
        }, {
            "role": "user",
            "content": text_corpus
        }]
    )
    return topics.choices[0].message.content
```

## Validation Metrics

### Market Demand Indicators
- **Search Volume**: Google Trends, Keyword Planner
- **Social Mentions**: Twitter mentions, Reddit discussions
- **Project Activity**: GitHub stars, npm downloads
- **Job Postings**: Indeed, LinkedIn job trends
- **Developer Questions**: Stack Overflow activity

### Technical Validation
- **Code Quality**: Lighthouse scores, bundle size
- **Performance**: Core Web Vitals, load times
- **Community Health**: Issue resolution time, contributor activity
- **Documentation**: README completeness, API docs quality

## Data Collection Scripts

### Twitter Trend Collector

```javascript
async function collectTweets(query, maxResults = 100) {
  const response = await fetch(
    `https://api.twitter.com/2/tweets/search/recent?query=${encodeURIComponent(query)}&max_results=${maxResults}`,
    {
      headers: {
        'Authorization': `Bearer ${process.env.TWITTER_BEARER_TOKEN}`
      }
    }
  );

  const data = await response.json();
  return analyzeSentiment(data.data);
}
```

### Reddit Sentiment Monitor

```python
import praw

def monitor_reddit_sentiment(subreddits, keywords, timeframe='week'):
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent='market-research-oracle'
    )

    sentiment_data = {}

    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).top(time_filter=timeframe):
            if any(keyword in submission.title.lower() for keyword in keywords):
                sentiment = analyze_sentiment(
                    submission.title + " " + submission.selftext
                )
                sentiment_data[submission.id] = {
                    'title': submission.title,
                    'sentiment': sentiment,
                    'upvotes': submission.score,
                    'comments': submission.num_comments
                }

    return sentiment_data
```

### GitHub Growth Tracker

```javascript
async function trackRepositoryGrowth(repoNames, period = '30d') {
  const growthData = {};

  for (const repo of repoNames) {
    const [owner, name] = repo.split('/');

    // Get current stats
    const currentStats = await fetch(
      `https://api.github.com/repos/${owner}/${name}`
    ).then(res => res.json());

    // Get historical data
    const history = await fetch(
      `https://api.github.com/repos/${owner}/${name}/stats/commit_activity`
    ).then(res => res.json());

    growthData[repo] = {
      stars: currentStats.stargazers_count,
      forks: currentStats.forks_count,
      growth_rate: calculateGrowthRate(history, period),
      health_score: calculateHealthScore(currentStats, history)
    };
  }

  return growthData;
}
```

## Reporting Framework

### Market Validation Score

```javascript
function calculateValidationScore(metrics) {
  const weights = {
    search_trend: 0.2,
    social_mention: 0.15,
    github_growth: 0.25,
    npm_downloads: 0.2,
    developer_interest: 0.1,
    market_size: 0.1
  };

  return Object.entries(weights).reduce((score, [metric, weight]) => {
    return score + (metrics[metric] * weight);
  }, 0);
}
```

### Trend Prediction Model

```python
def predict_trend_direction(historical_data, confidence_threshold=0.7):
    # Analyze multiple indicators
    indicators = {
        'growth_rate': calculate_growth_rate(historical_data),
        'volatility': calculate_volatility(historical_data),
        'correlation': calculate_correlation_with_similar_tech(historical_data)
    }

    # Machine learning model for prediction
    prediction = ml_model.predict(indicators)
    confidence = ml_model.predict_proba(indicators).max()

    if confidence >= confidence_threshold:
        return {
            'direction': prediction,
            'confidence': confidence,
            'key_factors': identify_driving_factors(indicators)
        }
    else:
        return {
            'direction': 'uncertain',
            'confidence': confidence,
            'recommendation': 'collect_more_data'
        }
```

## Data Pipeline Architecture

### Real-time Processing

```
Data Sources -> Kafka -> Spark Processing -> ML Models -> Dashboard
     |             |           |            |           |
   Twitter    Reddit    GitHub     Sentiment   Metrics API
    API         API        API      Analysis
```

### Batch Processing (Daily)

```
Historical Data -> Data Lake -> Analytics -> Reports -> Stakeholders
```

## Alert System

### Market Opportunity Alerts

```javascript
const alertConditions = {
  viral_trend: (data) => data.mentions_24h > data.average_mentions * 3,
  technology_shift: (data) => data.technology_growth > 50,
  community_spike: (data) => data.new_contributors > 10,
  funding_activity: (data) => data.recent_funding > 1000000
};

function checkMarketAlerts(marketData) {
  const alerts = [];

  for (const [condition, check] of Object.entries(alertConditions)) {
    if (check(marketData)) {
      alerts.push({
        type: condition,
        severity: 'high',
        data: marketData,
        timestamp: new Date().toISOString()
      });
    }
  }

  return alerts;
}
```

---

## Appendix: API Authentication Reference

### OAuth 2.0 Setup for Twitter

```python
import tweepy

def setup_twitter_api():
    auth = tweepy.OAuthHandler(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET')
    )
    auth.set_access_token(
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_SECRET')
    )
    return tweepy.API(auth, wait_on_rate_limit=True)
```

### GitHub Personal Access Token

```bash
# Create token with 'repo' and 'read:org' scopes
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Verify authentication
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### Reddit Script App Credentials

```python
import praw

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='market-research-oracle/1.0'
)
```

## Competitive Intelligence Data

### Patent Database Queries

```python
def search_patents(keywords, assignee=None, date_range=None):
    """Search USPTO for patent filings."""
    query = " OR ".join(keywords)
    if assignee:
        query += f' AND AN/"{assignee}"'
    if date_range:
        query += f' AND APD:[{date_range[0]} TO {date_range[1]}]'

    results = uspto_search(query)
    return {
        'total': len(results),
        'recent': [r for r in results if r.filing_date > datetime.now() - timedelta(days=365)],
        'technology_clusters': cluster_patents(results)
    }
```

### Job Posting Analysis

```python
def analyze_job_postings(company, platform='linkedin'):
    """Analyze job postings for technology signals."""
    postings = scrape_job_postings(company, platform)

    tech_signals = {
        'technologies': extract_technologies(postings),
        'team_growth': len(postings),
        'new_initiatives': identify_new_initiatives(postings),
        'salary_ranges': extract_salary_data(postings)
    }

    return tech_signals
```

### Funding Round Tracking

```python
def track_funding_rounds(industry, min_amount=1000000):
    """Track recent funding rounds in an industry."""
    rounds = crunchbase_search(industry, min_amount=min_amount)

    return {
        'total_raised': sum(r.amount for r in rounds),
        'avg_round_size': np.mean([r.amount for r in rounds]),
        'top_deals': sorted(rounds, key=lambda x: x.amount, reverse=True)[:10],
        'investor_activity': aggregate_investors(rounds)
    }
```

## Data Quality Validation

### Source Reliability Scoring

| Source | Reliability | Update Frequency | Cost |
|--------|------------|-----------------|------|
| Twitter API | High | Real-time | Free tier available |
| Reddit API | High | Near real-time | Free |
| GitHub API | High | Real-time | Free |
| Google Trends | Medium | Daily | Free |
| Crunchbase | High | Weekly | Paid |
| Product Hunt | Medium | Daily | Free |
| Stack Overflow | High | Annual survey | Free |
| NPM Registry | High | Real-time | Free |

### Data Freshness Requirements

```yaml
freshness_requirements:
  social_media: "last 24 hours"
  github_activity: "last 7 days"
  npm_downloads: "last 30 days"
  market_trends: "last 90 days"
  funding_data: "last 30 days"
  job_postings: "last 14 days"
```

### Anomaly Detection Rules

```python
def detect_anomalies(data_series, threshold=2.0):
    mean = np.mean(data_series)
    std = np.std(data_series)
    anomalies = [x for x in data_series if abs(x - mean) > threshold * std]
    return anomalies
```

---

*Remember: The best market research combines real-time data with historical context. Always validate across multiple sources before making strategic decisions.*
