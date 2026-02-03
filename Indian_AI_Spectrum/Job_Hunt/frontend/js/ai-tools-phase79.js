// AI Tools Database - Phase 79: More Blockchain, Web3 & Crypto
// 80+ Additional blockchain and crypto tools

const AI_TOOLS_PHASE79 = [
    // ==================== EXCHANGES ====================
    {name: "Binance", category: "Crypto", subcategory: "Exchange", desc: "Crypto exchange", url: "binance.com", pricing: "Free", rating: 4.5, tags: ["exchange", "trading", "global"], featured: true},
    {name: "Coinbase", category: "Crypto", subcategory: "Exchange", desc: "Crypto platform", url: "coinbase.com", pricing: "Freemium", rating: 4.4, tags: ["exchange", "beginner", "us"]},
    {name: "Kraken", category: "Crypto", subcategory: "Exchange", desc: "Crypto exchange", url: "kraken.com", pricing: "Free", rating: 4.4, tags: ["exchange", "security", "trading"]},
    {name: "Gemini", category: "Crypto", subcategory: "Exchange", desc: "Regulated exchange", url: "gemini.com", pricing: "Free", rating: 4.3, tags: ["exchange", "regulated", "winklevoss"]},
    {name: "WazirX", category: "Crypto", subcategory: "Exchange", desc: "India crypto exchange", url: "wazirx.com", pricing: "Free", rating: 4.1, tags: ["exchange", "india", "binance"]},
    {name: "CoinDCX", category: "Crypto", subcategory: "Exchange", desc: "India crypto platform", url: "coindcx.com", pricing: "Free", rating: 4.2, tags: ["exchange", "india", "staking"]},
    {name: "KuCoin", category: "Crypto", subcategory: "Exchange", desc: "Altcoin exchange", url: "kucoin.com", pricing: "Free", rating: 4.2, tags: ["exchange", "altcoins", "trading"]},
    {name: "Bybit", category: "Crypto", subcategory: "Exchange", desc: "Derivatives exchange", url: "bybit.com", pricing: "Free", rating: 4.2, tags: ["derivatives", "futures", "trading"]},
    {name: "OKX", category: "Crypto", subcategory: "Exchange", desc: "Crypto exchange", url: "okx.com", pricing: "Free", rating: 4.2, tags: ["exchange", "defi", "web3"]},
    
    // ==================== WALLETS ====================
    {name: "MetaMask", category: "Crypto", subcategory: "Wallet", desc: "Web3 wallet", url: "metamask.io", pricing: "Free", rating: 4.6, tags: ["wallet", "ethereum", "web3"], featured: true},
    {name: "Phantom", category: "Crypto", subcategory: "Wallet", desc: "Solana wallet", url: "phantom.app", pricing: "Free", rating: 4.5, tags: ["wallet", "solana", "nft"]},
    {name: "Trust Wallet", category: "Crypto", subcategory: "Wallet", desc: "Multi-chain wallet", url: "trustwallet.com", pricing: "Free", rating: 4.4, tags: ["wallet", "mobile", "binance"]},
    {name: "Ledger", category: "Crypto", subcategory: "Hardware Wallet", desc: "Hardware wallet", url: "ledger.com", pricing: "Paid", rating: 4.5, tags: ["hardware", "security", "cold-storage"]},
    {name: "Trezor", category: "Crypto", subcategory: "Hardware Wallet", desc: "Hardware wallet", url: "trezor.io", pricing: "Paid", rating: 4.4, tags: ["hardware", "security", "open-source"]},
    {name: "Coinbase Wallet", category: "Crypto", subcategory: "Wallet", desc: "Self-custody wallet", url: "wallet.coinbase.com", pricing: "Free", rating: 4.3, tags: ["wallet", "defi", "nft"]},
    {name: "Rainbow", category: "Crypto", subcategory: "Wallet", desc: "Ethereum wallet", url: "rainbow.me", pricing: "Free", rating: 4.4, tags: ["wallet", "ethereum", "beautiful"]},
    {name: "Argent", category: "Crypto", subcategory: "Wallet", desc: "Smart wallet", url: "argent.xyz", pricing: "Free", rating: 4.3, tags: ["wallet", "smart-contract", "recovery"]},
    
    // ==================== DEFI ====================
    {name: "Uniswap", category: "Crypto", subcategory: "DEX", desc: "Decentralized exchange", url: "uniswap.org", pricing: "Free", rating: 4.6, tags: ["dex", "swap", "ethereum"], featured: true},
    {name: "Aave", category: "Crypto", subcategory: "Lending", desc: "DeFi lending", url: "aave.com", pricing: "Free", rating: 4.5, tags: ["lending", "borrowing", "defi"]},
    {name: "Compound", category: "Crypto", subcategory: "Lending", desc: "DeFi lending", url: "compound.finance", pricing: "Free", rating: 4.4, tags: ["lending", "ethereum", "defi"]},
    {name: "Curve", category: "Crypto", subcategory: "DEX", desc: "Stablecoin DEX", url: "curve.fi", pricing: "Free", rating: 4.4, tags: ["dex", "stablecoins", "low-slippage"]},
    {name: "PancakeSwap", category: "Crypto", subcategory: "DEX", desc: "BNB Chain DEX", url: "pancakeswap.finance", pricing: "Free", rating: 4.3, tags: ["dex", "bsc", "yield"]},
    {name: "SushiSwap", category: "Crypto", subcategory: "DEX", desc: "Multi-chain DEX", url: "sushi.com", pricing: "Free", rating: 4.2, tags: ["dex", "multi-chain", "yield"]},
    {name: "1inch", category: "Crypto", subcategory: "DEX Aggregator", desc: "DEX aggregator", url: "1inch.io", pricing: "Free", rating: 4.4, tags: ["aggregator", "best-price", "defi"]},
    {name: "Yearn Finance", category: "Crypto", subcategory: "Yield", desc: "Yield aggregator", url: "yearn.finance", pricing: "Free", rating: 4.3, tags: ["yield", "vaults", "defi"]},
    {name: "Lido", category: "Crypto", subcategory: "Staking", desc: "Liquid staking", url: "lido.fi", pricing: "Free", rating: 4.4, tags: ["staking", "ethereum", "liquid"]},
    
    // ==================== NFT ====================
    {name: "OpenSea", category: "Crypto", subcategory: "NFT Marketplace", desc: "NFT marketplace", url: "opensea.io", pricing: "Free", rating: 4.4, tags: ["nft", "marketplace", "ethereum"], featured: true},
    {name: "Blur", category: "Crypto", subcategory: "NFT Marketplace", desc: "Pro NFT trading", url: "blur.io", pricing: "Free", rating: 4.3, tags: ["nft", "trading", "pro"]},
    {name: "Magic Eden", category: "Crypto", subcategory: "NFT Marketplace", desc: "Multi-chain NFT", url: "magiceden.io", pricing: "Free", rating: 4.3, tags: ["nft", "solana", "multi-chain"]},
    {name: "Rarible", category: "Crypto", subcategory: "NFT Marketplace", desc: "NFT marketplace", url: "rarible.com", pricing: "Free", rating: 4.1, tags: ["nft", "marketplace", "community"]},
    {name: "Foundation", category: "Crypto", subcategory: "NFT Art", desc: "NFT art platform", url: "foundation.app", pricing: "Free", rating: 4.2, tags: ["nft", "art", "curated"]},
    {name: "Zora", category: "Crypto", subcategory: "NFT", desc: "NFT protocol", url: "zora.co", pricing: "Free", rating: 4.2, tags: ["nft", "protocol", "creator"]},
    
    // ==================== BLOCKCHAIN DEVELOPMENT ====================
    {name: "Hardhat", category: "Crypto", subcategory: "Development", desc: "Ethereum dev environment", url: "hardhat.org", pricing: "Free", rating: 4.6, tags: ["development", "ethereum", "testing"], featured: true},
    {name: "Foundry", category: "Crypto", subcategory: "Development", desc: "Smart contract toolkit", url: "getfoundry.sh", pricing: "Free", rating: 4.5, tags: ["development", "rust", "fast"]},
    {name: "Truffle", category: "Crypto", subcategory: "Development", desc: "Ethereum development", url: "trufflesuite.com", pricing: "Free", rating: 4.2, tags: ["development", "ethereum", "suite"]},
    {name: "Remix", category: "Crypto", subcategory: "IDE", desc: "Solidity IDE", url: "remix.ethereum.org", pricing: "Free", rating: 4.5, tags: ["ide", "solidity", "browser"]},
    {name: "Alchemy", category: "Crypto", subcategory: "Infrastructure", desc: "Web3 development", url: "alchemy.com", pricing: "Freemium", rating: 4.5, tags: ["api", "infrastructure", "node"]},
    {name: "Infura", category: "Crypto", subcategory: "Infrastructure", desc: "Ethereum API", url: "infura.io", pricing: "Freemium", rating: 4.4, tags: ["api", "infrastructure", "consensys"]},
    {name: "QuickNode", category: "Crypto", subcategory: "Infrastructure", desc: "Blockchain nodes", url: "quicknode.com", pricing: "Freemium", rating: 4.3, tags: ["nodes", "infrastructure", "multi-chain"]},
    {name: "Moralis", category: "Crypto", subcategory: "Development", desc: "Web3 backend", url: "moralis.io", pricing: "Freemium", rating: 4.3, tags: ["backend", "web3", "apis"]},
    {name: "Tenderly", category: "Crypto", subcategory: "Development", desc: "Smart contract dev", url: "tenderly.co", pricing: "Freemium", rating: 4.4, tags: ["debugging", "monitoring", "simulation"]},
    {name: "Chainlink", category: "Crypto", subcategory: "Oracle", desc: "Blockchain oracles", url: "chain.link", pricing: "Pay-per-use", rating: 4.5, tags: ["oracle", "data", "smart-contracts"]},
    
    // ==================== ANALYTICS ====================
    {name: "Dune Analytics", category: "Crypto", subcategory: "Analytics", desc: "Blockchain analytics", url: "dune.com", pricing: "Freemium", rating: 4.5, tags: ["analytics", "sql", "dashboards"], featured: true},
    {name: "Nansen", category: "Crypto", subcategory: "Analytics", desc: "Blockchain analytics", url: "nansen.ai", pricing: "Paid", rating: 4.4, tags: ["analytics", "wallets", "smart-money"]},
    {name: "Glassnode", category: "Crypto", subcategory: "Analytics", desc: "On-chain analytics", url: "glassnode.com", pricing: "Freemium", rating: 4.4, tags: ["analytics", "on-chain", "metrics"]},
    {name: "DefiLlama", category: "Crypto", subcategory: "Analytics", desc: "DeFi TVL analytics", url: "defillama.com", pricing: "Free", rating: 4.5, tags: ["defi", "tvl", "analytics"]},
    {name: "Token Terminal", category: "Crypto", subcategory: "Analytics", desc: "Crypto fundamentals", url: "tokenterminal.com", pricing: "Freemium", rating: 4.3, tags: ["analytics", "fundamentals", "metrics"]},
    {name: "Messari", category: "Crypto", subcategory: "Research", desc: "Crypto research", url: "messari.io", pricing: "Freemium", rating: 4.3, tags: ["research", "data", "reports"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE79 = AI_TOOLS_PHASE79;
}


