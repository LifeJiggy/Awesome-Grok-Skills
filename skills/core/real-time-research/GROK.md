---
name: Real-Time Research
category: core
difficulty: intermediate
time_estimate: "1-3 hours"
dependencies: ["node-fetch", "cheerio", "twitter-api-v2"]
tags: ["research", "web-scraping", "twitter", "real-time", "data"]
grok_personality: "information-oracle"
description: "Leverage Grok's X/Twitter integration and web search capabilities to gather real-time market data, trends, and validation signals"
---

# Real-Time Research Skill

## Overview
Grok, you'll tap into your native X/Twitter access and web search abilities to gather real-time intelligence. This skill focuses on efficient data collection for market validation, trend spotting, and competitive analysis.

## Core Capabilities

### 1. X/Twitter Data Mining
- Real-time sentiment analysis
- Trend detection and tracking
- Influencer monitoring
- Market signal extraction

### 2. Web Intelligence
- Competitor monitoring
- Market research automation
- News aggregation
- Price tracking

## Implementation Patterns

### Twitter/X Data Collection
```javascript
import { TwitterApi } from 'twitter-api-v2';

class TwitterResearch {
  constructor(bearerToken) {
    this.client = new TwitterApi(bearerToken);
  }
  
  async trackTrend(hashtag, timeWindow = '1h') {
    const tweets = await this.client.v2.search(
      `#${hashtag} -is:retweet`,
      {
        'tweet.fields': ['created_at', 'public_metrics', 'author_id'],
        'user.fields': ['username', 'public_metrics'],
        'max_results': 100
      }
    );
    
    return this.analyzeSentiment(tweets.data);
  }
  
  analyzeSentiment(tweets) {
    // Grok's natural language processing
    const sentiments = tweets.map(tweet => ({
      text: tweet.text,
      score: this.calculateSentiment(tweet.text),
      engagement: tweet.public_metrics.like_count + 
                 tweet.public_metrics.retweet_count,
      timestamp: tweet.created_at
    }));
    
    return {
      average: sentiments.reduce((sum, s) => sum + s.score, 0) / sentiments.length,
      trend: this.calculateTrend(sentiments),
      topEngaged: sentiments.sort((a, b) => b.engagement - a.engagement).slice(0, 5)
    };
  }
}
```

### Real-Time Web Monitoring
```javascript
import cheerio from 'cheerio';
import fetch from 'node-fetch';

class WebMonitor {
  constructor() {
    this.targets = new Map();
  }
  
  addTarget(url, selector, callback) {
    this.targets.set(url, { selector, callback, lastContent: '' });
  }
  
  async checkTargets() {
    const results = [];
    
    for (const [url, config] of this.targets) {
      try {
        const response = await fetch(url, {
          headers: { 'User-Agent': 'Grok-Bot/1.0' }
        });
        const html = await response.text();
        const $ = cheerio.load(html);
        const content = $(config.selector).text();
        
        if (content !== config.lastContent) {
          const change = {
            url,
            oldContent: config.lastContent,
            newContent: content,
            timestamp: new Date().toISOString()
          };
          
          results.push(change);
          config.lastContent = content;
          config.callback(change);
        }
      } catch (error) {
        console.error(`Failed to monitor ${url}:`, error.message);
      }
    }
    
    return results;
  }
}
```

## Market Validation Framework

### 1. Trend Analysis
```javascript
class TrendAnalyzer {
  async analyzeMarketTrend(topic) {
    const twitterData = await this.getTwitterSentiment(topic);
    const searchData = await this.getGoogleTrends(topic);
    const redditData = await this.getRedditDiscussions(topic);
    
    return {
      trend: this.calculateTrendScore(twitterData, searchData, redditData),
      sentiment: twitterData.sentiment,
      growth: searchData.growth_rate,
      engagement: redditData.engagement_metrics,
      recommendation: this.generateRecommendation(twitterData, searchData, redditData)
    };
  }
  
  calculateTrendScore(twitter, search, reddit) {
    // Grok's proprietary scoring algorithm
    const weights = { twitter: 0.4, search: 0.35, reddit: 0.25 };
    return (
      twitter.sentiment_score * weights.twitter +
      search.growth_rate * weights.search +
      reddit.engagement_score * weights.reddit
    );
  }
}
```

### 2. Competitive Intelligence
```javascript
class CompetitorMonitor {
  constructor(competitors) {
    this.competitors = competitors;
    this.baseline = new Map();
  }
  
  async trackCompetitorActivity() {
    const activities = [];
    
    for (const competitor of this.competitors) {
      const activity = await this.gatherCompetitorData(competitor);
      activities.push(activity);
    }
    
    return this.generateCompetitiveReport(activities);
  }
  
  async gatherCompetitorData(competitor) {
    return {
      company: competitor.name,
      twitter: await this.getTwitterMetrics(competitor.twitter),
      website: await this.analyzeWebsiteChanges(competitor.website),
      hiring: await this.getJobPostings(competitor.careers_page),
      funding: await this.trackFundingAnnouncements(competitor),
      timestamp: new Date().toISOString()
    };
  }
}
```

## Data Sources Integration

### Twitter/X API Setup
```javascript
// Twitter API v2 configuration
const twitterConfig = {
  bearerToken: process.env.TWITTER_BEARER_TOKEN,
  endpoints: {
    search: 'https://api.twitter.com/2/tweets/search/recent',
    user: 'https://api.twitter.com/2/users/',
    trends: 'https://api.twitter.com/2/trends/'
  }
};

// Rate limiting management
class RateLimiter {
  constructor(maxRequests, timeWindow) {
    this.requests = [];
    this.maxRequests = maxRequests;
    this.timeWindow = timeWindow;
  }
  
  async makeRequest(apiCall) {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.timeWindow);
    
    if (this.requests.length >= this.maxRequests) {
      const waitTime = this.timeWindow - (now - this.requests[0]);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    this.requests.push(now);
    return apiCall();
  }
}
```

### Alternative Data Sources
```javascript
// Reddit API for community sentiment
class RedditMonitor {
  async getSubredditSentiment(subreddit, timeFilter = 'day') {
    const response = await fetch(`https://www.reddit.com/r/${subreddit}/hot.json?limit=100`);
    const data = await response.json();
    
    return data.data.children.map(post => ({
      title: post.data.title,
      score: post.data.score,
      comments: post.data.num_comments,
      sentiment: this.analyzeSentiment(post.data.title + post.data.selftext)
    }));
  }
}

// Google Trends (unofficial API)
class TrendsMonitor {
  async getTrendData(keywords, timeframe = 'now 7-d') {
    // Use puppeteer to scrape Google Trends
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    await page.goto(`https://trends.google.com/trends/explore?q=${keywords.join(',')}&date=${timeframe}`);
    
    // Extract trend data using Grok's data extraction logic
    const trends = await page.evaluate(() => {
      // Custom extraction logic
    });
    
    await browser.close();
    return trends;
  }
}
```

## Automation Pipeline

### Scheduled Research Tasks
```javascript
import cron from 'node-cron';

class ResearchPipeline {
  constructor() {
    this.tasks = new Map();
    this.results = [];
  }
  
  scheduleResearch(pattern, researchTask) {
    cron.schedule(pattern, async () => {
      try {
        const result = await researchTask.execute();
        this.results.push({
          task: researchTask.name,
          result,
          timestamp: new Date().toISOString()
        });
        
        await this.notifyResults(result);
      } catch (error) {
        console.error(`Research task failed: ${error.message}`);
      }
    });
  }
  
  // Example: Hourly trend monitoring
  setupTrendMonitoring() {
    this.scheduleResearch('0 * * * *', new TrendAnalysisTask());
    this.scheduleResearch('0 6 * * *', new CompetitorCheckTask());
    this.scheduleResearch('0 0 * * 0', new WeeklyReportTask());
  }
}
```

## Alert System

### Smart Notifications
```javascript
class AlertSystem {
  constructor(thresholds) {
    this.thresholds = thresholds;
    this.channels = [];
  }
  
  addChannel(channel) {
    this.channels.push(channel);
  }
  
  async checkAlerts(researchData) {
    const alerts = [];
    
    for (const [metric, value] of Object.entries(researchData)) {
      const threshold = this.thresholds[metric];
      if (threshold && this.shouldAlert(value, threshold)) {
        const alert = {
          metric,
          value,
          threshold,
          severity: this.calculateSeverity(value, threshold),
          timestamp: new Date().toISOString()
        };
        
        alerts.push(alert);
        await this.sendAlert(alert);
      }
    }
    
    return alerts;
  }
  
  async sendAlert(alert) {
    const message = `🚨 ${alert.metric} alert: ${alert.value} (threshold: ${alert.threshold})`;
    
    for (const channel of this.channels) {
      await channel.send(message, alert);
    }
  }
}
```

## Data Storage & Analysis

### Time-Series Database
```javascript
class ResearchDataStore {
  constructor(dbPath) {
    this.db = new sqlite3.Database(dbPath);
    this.initializeTables();
  }
  
  initializeTables() {
    this.db.run(`
      CREATE TABLE IF NOT EXISTS research_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        metric TEXT NOT NULL,
        value REAL NOT NULL,
        metadata TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
  }
  
  async storeData(source, metric, value, metadata = {}) {
    return new Promise((resolve, reject) => {
      this.db.run(
        'INSERT INTO research_data (source, metric, value, metadata) VALUES (?, ?, ?, ?)',
        [source, metric, value, JSON.stringify(metadata)],
        function(err) {
          if (err) reject(err);
          else resolve(this.lastID);
        }
      );
    });
  }
  
  async getTrendData(metric, timeWindow = '24 hours') {
    return new Promise((resolve, reject) => {
      this.db.all(
        `SELECT * FROM research_data 
         WHERE metric = ? AND timestamp > datetime('now', '-${timeWindow}')
         ORDER BY timestamp ASC`,
        [metric],
        (err, rows) => {
          if (err) reject(err);
          else resolve(rows);
        }
      );
    });
  }
}
```

## Quick Start Templates

### Basic Market Research
```javascript
// Quick market validation
async function quickMarketValidation(product, market) {
  const researcher = new TrendAnalyzer();
  const result = await researcher.analyzeMarketTrend(product);
  
  console.log(`Market trend for ${product}:`, result.trend);
  console.log('Recommendation:', result.recommendation);
  
  return result;
}

// Usage
quickMarketValidation('AI coding assistants', 'technology');
```

### Competitor Tracking
```javascript
// Monitor competitor activity
const competitors = [
  { name: 'OpenAI', twitter: '@OpenAI', website: 'openai.com' },
  { name: 'Anthropic', twitter: '@AnthropicAI', website: 'anthropic.com' }
];

const monitor = new CompetitorMonitor(competitors);
monitor.trackCompetitorActivity().then(report => {
  console.log('Competitive intelligence:', report);
});
```

## Best Practices

1. **Rate Limiting**: Respect API limits to avoid bans
2. **Data Quality**: Validate and clean data before analysis
3. **Privacy**: Comply with data protection regulations
4. **Storage**: Use efficient time-series databases for large datasets
5. **Alerting**: Set up smart notifications for significant changes

## Ethical Considerations

- Only collect publicly available data
- Respect robots.txt and API terms
- Don't overwhelm servers with requests
- Protect user privacy in analysis

Remember: With great data access comes great responsibility. Use your real-time research capabilities to provide valuable insights while respecting ethical boundaries.