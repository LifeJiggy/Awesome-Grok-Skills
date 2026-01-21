# Market Data APIs

## 📊 Real-Time Price Data

### CoinGecko API
```javascript
class CoinGeckoAPI {
    constructor() {
        this.baseURL = 'https://api.coingecko.com/api/v3';
    }
    
    async getPrice(coinId, vsCurrency = 'usd') {
        const response = await fetch(
            `${this.baseURL}/simple/price?ids=${coinId}&vs_currencies=${vsCurrency}&include_24hr_change=true`
        );
        return response.json();
    }
    
    async getMarketChart(coinId, vsCurrency = 'usd', days = '7') {
        const response = await fetch(
            `${this.baseURL}/coins/${coinId}/market_chart?vs_currency=${vsCurrency}&days=${days}`
        );
        return response.json();
    }
    
    async getTopCoins(limit = 100, vsCurrency = 'usd') {
        const response = await fetch(
            `${this.baseURL}/coins/markets?vs_currency=${vsCurrency}&order=market_cap_desc&per_page=${limit}&page=1`
        );
        return response.json();
    }
    
    async searchCoins(query) {
        const response = await fetch(`${this.baseURL}/search?query=${query}`);
        return response.json();
    }
}

// Usage
const coinGecko = new CoinGeckoAPI();
const bitcoinPrice = await coinGecko.getPrice('bitcoin');
console.log(bitcoinPrice.bitcoin.usd); // Current price
console.log(bitcoinPrice.bitcoin.usd_24h_change); // 24h change
```

### CoinMarketCap API
```javascript
class CoinMarketCapAPI {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseURL = 'https://pro-api.coinmarketcap.com/v1';
    }
    
    async getQuotes(symbols, convert = 'USD') {
        const response = await fetch(
            `${this.baseURL}/cryptocurrency/quotes/latest?symbol=${symbols.join(',')}&convert=${convert}`,
            {
                headers: {
                    'X-CMC_PRO_API_KEY': this.apiKey
                }
            }
        );
        return response.json();
    }
    
    async getListings(limit = 100, convert = 'USD') {
        const response = await fetch(
            `${this.baseURL}/cryptocurrency/listings/latest?limit=${limit}&convert=${convert}`,
            {
                headers: {
                    'X-CMC_PRO_API_KEY': this.apiKey
                }
            }
        );
        return response.json();
    }
    
    async getGlobalMetrics(convert = 'USD') {
        const response = await fetch(
            `${this.baseURL}/global-metrics/quotes/latest?convert=${convert}`,
            {
                headers: {
                    'X-CMC_PRO_API_KEY': this.apiKey
                }
            }
        );
        return response.json();
    }
}
```

## 🔍 On-Chain Data Analysis

### Ethereum Block Explorer (Etherscan)
```javascript
class EtherscanAPI {
    constructor(apiKey, network = 'mainnet') {
        this.apiKey = apiKey;
        this.network = network;
        this.baseURL = `https://api${network === 'mainnet' ? '' : `-${network}`}.etherscan.io/api`;
    }
    
    async getTransactions(address, startblock = 0, endblock = 99999999) {
        const params = new URLSearchParams({
            module: 'account',
            action: 'txlist',
            address: address,
            startblock: startblock,
            endblock: endblock,
            sort: 'desc',
            apikey: this.apiKey
        });
        
        const response = await fetch(`${this.baseURL}?${params}`);
        return response.json();
    }
    
    async getTokenTransfers(contractAddress, startblock = 0, endblock = 99999999) {
        const params = new URLSearchParams({
            module: 'account',
            action: 'tokentx',
            contractaddress: contractAddress,
            startblock: startblock,
            endblock: endblock,
            sort: 'desc',
            apikey: this.apiKey
        });
        
        const response = await fetch(`${this.baseURL}?${params}`);
        return response.json();
    }
    
    async getContractABI(contractAddress) {
        const params = new URLSearchParams({
            module: 'contract',
            action: 'getsourcecode',
            address: contractAddress,
            apikey: this.apiKey
        });
        
        const response = await fetch(`${this.baseURL}?${params}`);
        return response.json();
    }
    
    async getGasPrice() {
        const params = new URLSearchParams({
            module: 'proxy',
            action: 'eth_gasPrice',
            apikey: this.apiKey
        });
        
        const response = await fetch(`${this.baseURL}?${params}`);
        return response.json();
    }
}
```

### Dune Analytics API
```javascript
class DuneAnalytics {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseURL = 'https://api.dune.com/api/v1';
    }
    
    async executeQuery(queryId, parameters = {}) {
        const response = await fetch(`${this.baseURL}/query/${queryId}/execute`, {
            method: 'POST',
            headers: {
                'X-Dune-Api-Key': this.apiKey,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ parameters })
        });
        
        const result = await response.json();
        return result.execution_id;
    }
    
    async getQueryResults(queryId, executionId = null) {
        const url = executionId 
            ? `${this.baseURL}/execution/${executionId}/results`
            : `${this.baseURL}/query/${queryId}/results`;
            
        const response = await fetch(url, {
            headers: {
                'X-Dune-Api-Key': this.apiKey
            }
        });
        
        return response.json();
    }
    
    async getLatestResults(queryId) {
        const executionId = await this.executeQuery(queryId);
        
        // Poll for results
        while (true) {
            const results = await this.getQueryResults(queryId, executionId);
            
            if (results.state === 'QUERY_STATE_COMPLETED') {
                return results.result.data;
            } else if (results.state === 'QUERY_STATE_FAILED') {
                throw new Error('Query failed');
            }
            
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
}

// Example: Get DEX trading volume
const dune = new DuneAnalytics(process.env.DUNE_API_KEY);
const dexVolume = await dune.getLatestResults('187967'); // Popular DEX volume query
```

## 📈 DeFi Protocol Data

### Uniswap V3 Data
```javascript
class UniswapV3Data {
    constructor(subgraphURL) {
        this.subgraphURL = subgraphURL || 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3';
    }
    
    async queryPool(address) {
        const query = `
            query GetPool($address: ID!) {
                pool(id: $address) {
                    id
                    token0 { symbol, decimals }
                    token1 { symbol, decimals }
                    feeTier
                    liquidity
                    sqrtPrice
                    tick
                    volumeUSD
                    volumeToken0
                    volumeToken1
                    totalValueLockedUSD
                }
            }
        `;
        
        const response = await fetch(this.subgraphURL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query,
                variables: { address: address.toLowerCase() }
            })
        });
        
        return response.json();
    }
    
    async getTopPools(orderBy = 'totalValueLockedUSD', orderDirection = 'desc') {
        const query = `
            query GetTopPools {
                pools(
                    first: 100,
                    orderBy: ${orderBy},
                    orderDirection: ${orderDirection},
                    where: { liquidity_gt: 0 }
                ) {
                    id
                    token0 { symbol, id }
                    token1 { symbol, id }
                    feeTier
                    totalValueLockedUSD
                    volumeUSD
                }
            }
        `;
        
        const response = await fetch(this.subgraphURL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        
        return response.json();
    }
}
```

### Aave Lending Data
```javascript
class AaveData {
    constructor(subgraphURL) {
        this.subgraphURL = subgraphURL || 'https://api.thegraph.com/subgraphs/name/aave/protocol-v2-ethereum';
    }
    
    async getReserveData() {
        const query = `
            query GetReserves {
                reserves(first: 100, orderBy: totalLiquidityUSD, orderDirection: desc) {
                    id
                    name
                    symbol
                    decimals
                    liquidityRate
                    stableBorrowRate
                    variableBorrowRate
                    totalLiquidityUSD
                    totalDebtUSD
                    utilizationRate
                    price {
                        id
                        priceInEth
                    }
                }
            }
        `;
        
        const response = await fetch(this.subgraphURL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        
        return response.json();
    }
    
    async getUserDeposits(userAddress) {
        const query = `
            query GetUserDeposits($user: ID!) {
                user(id: $user) {
                    id
                    reserves {
                        id
                        symbol
                        currentATokenBalance
                        currentUnderlyingBalanceUSD
                    }
                }
            }
        `;
        
        const response = await fetch(this.subgraphURL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query,
                variables: { user: userAddress.toLowerCase() }
            })
        });
        
        return response.json();
    }
}
```

## 📊 Sentiment Analysis

### Twitter Sentiment Analysis
```javascript
class TwitterSentiment {
    constructor(bearerToken) {
        this.bearerToken = bearerToken;
        this.baseURL = 'https://api.twitter.com/2';
    }
    
    async searchTweets(query, maxResults = 100) {
        const response = await fetch(
            `${this.baseURL}/tweets/search/recent?query=${encodeURIComponent(query)}&max_results=${maxResults}&tweet.fields=public_metrics,created_at`,
            {
                headers: {
                    'Authorization': `Bearer ${this.bearerToken}`
                }
            }
        );
        
        return response.json();
    }
    
    async getSentiment(text) {
        // Using a simple sentiment analysis approach
        const positiveWords = ['bullish', 'moon', 'pump', 'buy', 'hodl', 'diamond hands'];
        const negativeWords = ['bearish', 'dump', 'sell', 'crash', 'fud', 'paper hands'];
        
        const words = text.toLowerCase().split(/\s+/);
        let score = 0;
        
        words.forEach(word => {
            if (positiveWords.includes(word)) score += 1;
            if (negativeWords.includes(word)) score -= 1;
        });
        
        return {
            score,
            sentiment: score > 0 ? 'positive' : score < 0 ? 'negative' : 'neutral'
        };
    }
    
    async analyzeCryptoSentiment(coinSymbol) {
        const tweets = await this.searchTweets(`${coinSymbol} -is:retweet lang:en`);
        
        const sentiments = tweets.data?.map(async tweet => {
            const sentiment = await this.getSentiment(tweet.text);
            return {
                text: tweet.text,
                sentiment: sentiment.sentiment,
                score: sentiment.score,
                metrics: tweet.public_metrics
            };
        }) || [];
        
        const results = await Promise.all(sentiments);
        
        const totalSentiments = results.reduce(
            (acc, result) => ({
                positive: acc.positive + (result.sentiment === 'positive' ? 1 : 0),
                negative: acc.negative + (result.sentiment === 'negative' ? 1 : 0),
                neutral: acc.neutral + (result.sentiment === 'neutral' ? 1 : 0),
                totalScore: acc.totalScore + result.score,
                totalTweets: acc.totalTweets + 1
            }),
            { positive: 0, negative: 0, neutral: 0, totalScore: 0, totalTweets: 0 }
        );
        
        return {
            symbol: coinSymbol,
            ...totalSentiments,
            averageScore: totalSentiments.totalScore / totalSentiments.totalTweets,
            timestamp: new Date().toISOString()
        };
    }
}
```

## 📱 Real-Time Data Streaming

### WebSocket Price Updates
```javascript
class CryptoWebSocket {
    constructor() {
        this.subscriptions = new Map();
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }
    
    connectBinance() {
        this.wsBinance = new WebSocket('wss://stream.binance.com:9443/ws');
        
        this.wsBinance.onopen = () => {
            console.log('Connected to Binance WebSocket');
            this.reconnectAttempts = 0;
        };
        
        this.wsBinance.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.s && data.c) { // Trade data
                this.handlePriceUpdate({
                    symbol: data.s,
                    price: parseFloat(data.c),
                    change: parseFloat(data.P),
                    volume: parseFloat(data.v)
                });
            }
        };
        
        this.wsBinance.onerror = (error) => {
            console.error('Binance WebSocket error:', error);
        };
        
        this.wsBinance.onclose = () => {
            console.log('Binance WebSocket closed');
            this.reconnectBinance();
        };
    }
    
    subscribeToSymbol(symbol, callback) {
        if (!this.wsBinance || this.wsBinance.readyState !== WebSocket.OPEN) {
            this.connectBinance();
        }
        
        this.subscriptions.set(symbol.toLowerCase(), callback);
        
        const subscribeMessage = {
            method: 'SUBSCRIBE',
            params: [`${symbol.toLowerCase()}@ticker`],
            id: Date.now()
        };
        
        this.wsBinance.send(JSON.stringify(subscribeMessage));
    }
    
    handlePriceUpdate(data) {
        const callback = this.subscriptions.get(data.symbol.toLowerCase());
        if (callback) {
            callback(data);
        }
    }
    
    reconnectBinance() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            setTimeout(() => {
                console.log(`Reconnecting to Binance (attempt ${this.reconnectAttempts})`);
                this.connectBinance();
            }, 1000 * this.reconnectAttempts);
        }
    }
}

// Usage
const cryptoWS = new CryptoWebSocket();
cryptoWS.subscribeToSymbol('BTCUSDT', (data) => {
    console.log(`BTC Price: $${data.price} (${data.change}%)`);
});
```

## 📊 Data Aggregation

### Multi-Source Data Aggregator
```javascript
class MarketDataAggregator {
    constructor(config) {
        this.sources = {
            coingecko: new CoinGeckoAPI(),
            binance: new BinanceAPI(),
            etherscan: new EtherscanAPI(config.etherscanKey),
            dune: new DuneAnalytics(config.duneKey),
            twitter: new TwitterSentiment(config.twitterBearerToken)
        };
    }
    
    async getComprehensiveData(coinId, contractAddress = null) {
        try {
            const [priceData, onChainData, sentimentData] = await Promise.allSettled([
                this.sources.coingecko.getPrice(coinId),
                contractAddress ? this.getOnChainMetrics(contractAddress) : null,
                this.sources.twitter.analyzeCryptoSentiment(coinId.toUpperCase())
            ]);
            
            return {
                price: priceData.status === 'fulfilled' ? priceData.value : null,
                onChain: onChainData?.value || null,
                sentiment: sentimentData.status === 'fulfilled' ? sentimentData.value : null,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            console.error('Error aggregating data:', error);
            throw error;
        }
    }
    
    async getOnChainMetrics(contractAddress) {
        const [transactions, tokenHolders] = await Promise.all([
            this.sources.etherscan.getTokenTransfers(contractAddress),
            this.getTokenHolderCount(contractAddress)
        ]);
        
        return {
            totalTransactions: transactions.result.length,
            uniqueHolders: tokenHolders,
            transferVolume: this.calculateTransferVolume(transactions.result)
        };
    }
    
    calculateTransferVolume(transactions) {
        return transactions.reduce((total, tx) => {
            const value = parseFloat(tx.value) / Math.pow(10, tx.tokenDecimal);
            return total + value;
        }, 0);
    }
    
    async generateMarketReport(coinId, contractAddress = null) {
        const data = await this.getComprehensiveData(coinId, contractAddress);
        
        const report = {
            timestamp: data.timestamp,
            asset: coinId,
            market: {
                currentPrice: data.price?.[coinId]?.usd,
                priceChange24h: data.price?.[coinId]?.usd_24h_change,
                marketCap: await this.getMarketCap(coinId)
            },
            onChain: data.onChain,
            sentiment: {
                score: data.sentiment?.averageScore,
                sentiment: data.sentiment?.averageScore > 0 ? 'positive' : 
                         data.sentiment?.averageScore < 0 ? 'negative' : 'neutral',
                tweetCount: data.sentiment?.totalTweets
            },
            analysis: this.generateAnalysis(data)
        };
        
        return report;
    }
    
    generateAnalysis(data) {
        const priceUp = data.price?.[data.price ? Object.keys(data.price)[0] : '']?.usd_24h_change > 0;
        const sentimentPositive = data.sentiment?.averageScore > 0;
        const volumeHigh = data.onChain?.totalTransactions > 100;
        
        let analysis = [];
        
        if (priceUp && sentimentPositive) {
            analysis.push("Strong bullish sentiment with price momentum");
        } else if (!priceUp && sentimentPositive) {
            analysis.push("Positive sentiment despite price decline - potential buying opportunity");
        } else if (priceUp && !sentimentPositive) {
            analysis.push("Price rally with negative sentiment - watch for reversal");
        } else {
            analysis.push("Bearish indicators align - exercise caution");
        }
        
        if (volumeHigh) {
            analysis.push("High on-chain activity indicates strong market participation");
        }
        
        return analysis;
    }
}
```

---

*Remember: Always implement proper error handling, rate limiting, and data validation when working with external APIs. Consider using caching for frequently requested data to reduce API costs.* 📊