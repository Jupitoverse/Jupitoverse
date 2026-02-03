// AI Tools Database - Phase 17: E-commerce, Retail & Supply Chain AI
// 200+ Tools for e-commerce and retail

const AI_TOOLS_PHASE17 = [
    // ==================== E-COMMERCE PLATFORMS ====================
    {name: "Shopify", category: "E-commerce", subcategory: "Platform", desc: "E-commerce platform", url: "shopify.com", pricing: "Paid", rating: 4.6, tags: ["platform", "all-in-one", "popular"], featured: true},
    {name: "WooCommerce", category: "E-commerce", subcategory: "Platform", desc: "WordPress e-commerce", url: "woocommerce.com", pricing: "Free", rating: 4.4, tags: ["wordpress", "open-source", "flexible"]},
    {name: "BigCommerce", category: "E-commerce", subcategory: "Platform", desc: "Enterprise e-commerce", url: "bigcommerce.com", pricing: "Paid", rating: 4.3, tags: ["enterprise", "headless", "scalable"]},
    {name: "Magento (Adobe Commerce)", category: "E-commerce", subcategory: "Enterprise", desc: "Adobe's e-commerce platform", url: "business.adobe.com/products/magento", pricing: "Paid", rating: 4.1, tags: ["enterprise", "adobe", "customizable"]},
    {name: "Squarespace", category: "E-commerce", subcategory: "Website", desc: "Website builder with commerce", url: "squarespace.com", pricing: "Paid", rating: 4.4, tags: ["design", "simple", "beautiful"]},
    {name: "Wix eCommerce", category: "E-commerce", subcategory: "Website", desc: "Wix e-commerce", url: "wix.com/ecommerce", pricing: "Paid", rating: 4.2, tags: ["website", "simple", "drag-drop"]},
    {name: "PrestaShop", category: "E-commerce", subcategory: "Open Source", desc: "Open source e-commerce", url: "prestashop.com", pricing: "Free", rating: 4.1, tags: ["open-source", "europe", "customizable"]},
    {name: "OpenCart", category: "E-commerce", subcategory: "Open Source", desc: "Open source cart", url: "opencart.com", pricing: "Free", rating: 4.0, tags: ["open-source", "simple", "extensions"]},
    {name: "Salesforce Commerce Cloud", category: "E-commerce", subcategory: "Enterprise", desc: "Enterprise commerce platform", url: "salesforce.com/commerce-cloud", pricing: "Paid", rating: 4.2, tags: ["enterprise", "salesforce", "b2b"]},
    {name: "commercetools", category: "E-commerce", subcategory: "Headless", desc: "Headless commerce platform", url: "commercetools.com", pricing: "Paid", rating: 4.4, tags: ["headless", "api-first", "composable"]},
    {name: "Saleor", category: "E-commerce", subcategory: "Headless", desc: "Open source headless commerce", url: "saleor.io", pricing: "Freemium", rating: 4.3, tags: ["headless", "graphql", "open-source"]},
    {name: "Medusa", category: "E-commerce", subcategory: "Headless", desc: "Open source Shopify alternative", url: "medusajs.com", pricing: "Free", rating: 4.3, tags: ["open-source", "headless", "flexible"]},
    {name: "Elastic Path", category: "E-commerce", subcategory: "Headless", desc: "Composable commerce", url: "elasticpath.com", pricing: "Paid", rating: 4.2, tags: ["composable", "enterprise", "api"]},
    {name: "Swell", category: "E-commerce", subcategory: "Headless", desc: "Headless e-commerce", url: "swell.is", pricing: "Paid", rating: 4.2, tags: ["headless", "subscriptions", "api"]},
    {name: "Vendure", category: "E-commerce", subcategory: "Headless", desc: "Headless commerce framework", url: "vendure.io", pricing: "Free", rating: 4.2, tags: ["headless", "graphql", "typescript"]},
    
    // ==================== MARKETPLACES ====================
    {name: "Amazon Seller Central", category: "Marketplace", subcategory: "Amazon", desc: "Sell on Amazon", url: "sellercentral.amazon.com", pricing: "Commission", rating: 4.3, tags: ["amazon", "fba", "global"]},
    {name: "eBay Seller Hub", category: "Marketplace", subcategory: "eBay", desc: "Sell on eBay", url: "ebay.com/sellerhub", pricing: "Commission", rating: 4.1, tags: ["ebay", "auction", "global"]},
    {name: "Etsy", category: "Marketplace", subcategory: "Handmade", desc: "Handmade and vintage marketplace", url: "etsy.com", pricing: "Commission", rating: 4.4, tags: ["handmade", "creative", "niche"]},
    {name: "Walmart Marketplace", category: "Marketplace", subcategory: "Walmart", desc: "Sell on Walmart", url: "marketplace.walmart.com", pricing: "Commission", rating: 4.0, tags: ["walmart", "retail", "large"]},
    {name: "Faire", category: "Marketplace", subcategory: "Wholesale", desc: "Wholesale marketplace", url: "faire.com", pricing: "Commission", rating: 4.3, tags: ["wholesale", "b2b", "indie"]},
    {name: "Alibaba", category: "Marketplace", subcategory: "B2B", desc: "B2B global trade", url: "alibaba.com", pricing: "Commission", rating: 4.1, tags: ["b2b", "wholesale", "china"]},
    {name: "AliExpress", category: "Marketplace", subcategory: "Dropship", desc: "Dropshipping source", url: "aliexpress.com", pricing: "Free", rating: 4.0, tags: ["dropship", "china", "cheap"]},
    {name: "Wish", category: "Marketplace", subcategory: "Discount", desc: "Discount marketplace", url: "wish.com", pricing: "Commission", rating: 3.5, tags: ["discount", "mobile", "global"]},
    {name: "Poshmark", category: "Marketplace", subcategory: "Fashion", desc: "Fashion resale marketplace", url: "poshmark.com", pricing: "Commission", rating: 4.2, tags: ["fashion", "resale", "social"]},
    {name: "Depop", category: "Marketplace", subcategory: "Fashion", desc: "Gen-Z fashion marketplace", url: "depop.com", pricing: "Commission", rating: 4.1, tags: ["fashion", "gen-z", "vintage"]},
    
    // ==================== AI FOR E-COMMERCE ====================
    {name: "Nosto", category: "AI E-commerce", subcategory: "Personalization", desc: "E-commerce personalization", url: "nosto.com", pricing: "Paid", rating: 4.3, tags: ["personalization", "recommendations", "ai"], featured: true},
    {name: "Dynamic Yield", category: "AI E-commerce", subcategory: "Personalization", desc: "Personalization platform", url: "dynamicyield.com", pricing: "Paid", rating: 4.4, tags: ["personalization", "mastercard", "enterprise"]},
    {name: "Algolia", category: "AI E-commerce", subcategory: "Search", desc: "AI-powered search", url: "algolia.com", pricing: "Freemium", rating: 4.6, tags: ["search", "fast", "api"], featured: true},
    {name: "Constructor.io", category: "AI E-commerce", subcategory: "Search", desc: "AI product discovery", url: "constructor.io", pricing: "Paid", rating: 4.4, tags: ["search", "ai", "revenue"]},
    {name: "Bloomreach", category: "AI E-commerce", subcategory: "Discovery", desc: "Commerce experience cloud", url: "bloomreach.com", pricing: "Paid", rating: 4.3, tags: ["discovery", "seo", "cms"]},
    {name: "Klevu", category: "AI E-commerce", subcategory: "Search", desc: "AI search for e-commerce", url: "klevu.com", pricing: "Paid", rating: 4.3, tags: ["search", "nlp", "shopify"]},
    {name: "Vue.ai", category: "AI E-commerce", subcategory: "Styling", desc: "AI for fashion retail", url: "vue.ai", pricing: "Paid", rating: 4.2, tags: ["fashion", "styling", "automation"]},
    {name: "Lily AI", category: "AI E-commerce", subcategory: "Product", desc: "Product attribution AI", url: "lily.ai", pricing: "Paid", rating: 4.2, tags: ["product", "attribution", "fashion"]},
    {name: "Coveo", category: "AI E-commerce", subcategory: "Search", desc: "AI-powered relevance", url: "coveo.com", pricing: "Paid", rating: 4.3, tags: ["search", "enterprise", "relevance"]},
    {name: "Reflektion", category: "AI E-commerce", subcategory: "Personalization", desc: "1:1 personalization", url: "reflektion.com", pricing: "Paid", rating: 4.1, tags: ["personalization", "search", "recs"]},
    {name: "Barilliance", category: "AI E-commerce", subcategory: "Personalization", desc: "E-commerce personalization", url: "barilliance.com", pricing: "Paid", rating: 4.1, tags: ["personalization", "email", "retention"]},
    {name: "Crossing Minds", category: "AI E-commerce", subcategory: "Recommendations", desc: "AI recommendations", url: "crossingminds.com", pricing: "Paid", rating: 4.2, tags: ["recommendations", "ml", "privacy"]},
    {name: "Clerk.io", category: "AI E-commerce", subcategory: "Personalization", desc: "E-commerce personalization", url: "clerk.io", pricing: "Paid", rating: 4.3, tags: ["personalization", "search", "email"]},
    {name: "Visenze", category: "AI E-commerce", subcategory: "Visual", desc: "Visual AI for commerce", url: "visenze.com", pricing: "Paid", rating: 4.2, tags: ["visual-search", "ai", "discovery"]},
    {name: "Syte", category: "AI E-commerce", subcategory: "Visual", desc: "Visual AI platform", url: "syte.ai", pricing: "Paid", rating: 4.2, tags: ["visual", "discovery", "fashion"]},
    
    // ==================== INVENTORY & FULFILLMENT ====================
    {name: "ShipBob", category: "Fulfillment", subcategory: "3PL", desc: "E-commerce fulfillment", url: "shipbob.com", pricing: "Paid", rating: 4.3, tags: ["fulfillment", "3pl", "fast-shipping"], featured: true},
    {name: "ShipStation", category: "Fulfillment", subcategory: "Shipping", desc: "Shipping software", url: "shipstation.com", pricing: "Paid", rating: 4.4, tags: ["shipping", "multi-carrier", "automation"]},
    {name: "Shippo", category: "Fulfillment", subcategory: "Shipping", desc: "Shipping API and platform", url: "goshippo.com", pricing: "Freemium", rating: 4.4, tags: ["shipping", "api", "discounts"]},
    {name: "EasyPost", category: "Fulfillment", subcategory: "API", desc: "Shipping API", url: "easypost.com", pricing: "Pay-per-use", rating: 4.4, tags: ["api", "multi-carrier", "tracking"]},
    {name: "Deliverr", category: "Fulfillment", subcategory: "Fulfillment", desc: "E-commerce fulfillment", url: "deliverr.com", pricing: "Paid", rating: 4.2, tags: ["fulfillment", "2-day", "badges"]},
    {name: "Flexport", category: "Fulfillment", subcategory: "Freight", desc: "Freight forwarding", url: "flexport.com", pricing: "Paid", rating: 4.3, tags: ["freight", "logistics", "global"]},
    {name: "Skubana (Extensiv)", category: "Inventory", subcategory: "OMS", desc: "Order management", url: "extensiv.com", pricing: "Paid", rating: 4.2, tags: ["oms", "inventory", "multichannel"]},
    {name: "TradeGecko (QuickBooks)", category: "Inventory", subcategory: "Inventory", desc: "Inventory management", url: "quickbooks.intuit.com/commerce", pricing: "Paid", rating: 4.2, tags: ["inventory", "wholesale", "intuit"]},
    {name: "Cin7", category: "Inventory", subcategory: "Inventory", desc: "Inventory management", url: "cin7.com", pricing: "Paid", rating: 4.1, tags: ["inventory", "pos", "b2b"]},
    {name: "Ordoro", category: "Inventory", subcategory: "All-in-one", desc: "Inventory and shipping", url: "ordoro.com", pricing: "Paid", rating: 4.3, tags: ["inventory", "shipping", "dropship"]},
    {name: "Fishbowl", category: "Inventory", subcategory: "Warehouse", desc: "Warehouse management", url: "fishbowlinventory.com", pricing: "Paid", rating: 4.1, tags: ["warehouse", "manufacturing", "quickbooks"]},
    {name: "inFlow", category: "Inventory", subcategory: "Simple", desc: "Simple inventory software", url: "inflowinventory.com", pricing: "Paid", rating: 4.3, tags: ["simple", "smb", "affordable"]},
    {name: "Zoho Inventory", category: "Inventory", subcategory: "Zoho", desc: "Zoho inventory management", url: "zoho.com/inventory", pricing: "Freemium", rating: 4.2, tags: ["zoho", "multichannel", "affordable"]},
    {name: "Katana", category: "Inventory", subcategory: "Manufacturing", desc: "Manufacturing ERP", url: "katanamrp.com", pricing: "Paid", rating: 4.4, tags: ["manufacturing", "mrp", "modern"]},
    {name: "NetSuite Inventory", category: "Inventory", subcategory: "Enterprise", desc: "Oracle inventory management", url: "netsuite.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "erp", "oracle"]},
    
    // ==================== PRICING & ANALYTICS ====================
    {name: "Prisync", category: "Pricing", subcategory: "Competitive", desc: "Competitor price tracking", url: "prisync.com", pricing: "Paid", rating: 4.3, tags: ["competitive", "tracking", "automation"]},
    {name: "Intelligence Node", category: "Pricing", subcategory: "AI", desc: "AI pricing optimization", url: "intelligencenode.com", pricing: "Paid", rating: 4.2, tags: ["ai", "competitive", "assortment"]},
    {name: "Competera", category: "Pricing", subcategory: "AI", desc: "AI-driven pricing", url: "competera.net", pricing: "Paid", rating: 4.2, tags: ["ai", "retail", "optimization"]},
    {name: "Pricefx", category: "Pricing", subcategory: "Enterprise", desc: "Cloud pricing software", url: "pricefx.com", pricing: "Paid", rating: 4.3, tags: ["enterprise", "b2b", "cloud"]},
    {name: "Omnia Retail", category: "Pricing", subcategory: "Dynamic", desc: "Dynamic pricing platform", url: "omniaretail.com", pricing: "Paid", rating: 4.2, tags: ["dynamic", "retail", "automation"]},
    {name: "Triple Whale", category: "Analytics", subcategory: "DTC", desc: "DTC analytics", url: "triplewhale.com", pricing: "Paid", rating: 4.4, tags: ["dtc", "attribution", "profit"]},
    {name: "Glew", category: "Analytics", subcategory: "E-commerce", desc: "E-commerce analytics", url: "glew.io", pricing: "Paid", rating: 4.2, tags: ["analytics", "reports", "integrations"]},
    {name: "Metorik", category: "Analytics", subcategory: "WooCommerce", desc: "WooCommerce analytics", url: "metorik.com", pricing: "Paid", rating: 4.4, tags: ["woocommerce", "reports", "email"]},
    {name: "Lifetimely", category: "Analytics", subcategory: "LTV", desc: "Customer LTV analytics", url: "lifetimely.io", pricing: "Paid", rating: 4.3, tags: ["ltv", "cohorts", "shopify"]},
    {name: "Daasity", category: "Analytics", subcategory: "DTC", desc: "DTC data analytics", url: "daasity.com", pricing: "Paid", rating: 4.3, tags: ["dtc", "data", "warehouse"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE17 = AI_TOOLS_PHASE17;
}


