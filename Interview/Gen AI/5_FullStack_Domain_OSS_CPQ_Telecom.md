# 5. Full-Stack & Domain (Java, Angular, JS, OSS/BSS, CPQ, Telecom) – Interview Guide

Skills covered: Java, Angular, JavaScript, OSS/BSS, CPQ, Telecom

---

## 📋 Quick Reference

| Area | Key Points |
|------|------------|
| Java | OOP, JVM, collections, streams, Spring (if used) |
| Angular | Components, services, RxJS, routing, HTTP client |
| JavaScript | ES6+, async/await, DOM, fetch, modules |
| OSS/BSS | Operations/Business Support; provisioning, billing, CRM |
| CPQ | Configure, Price, Quote; product config, pricing, quotes |
| Telecom | Networks, services, SR/ticketing, fulfillment, assurance |

---

## 🔑 Core Concepts

### 1. Java (Backend / Integration Context)

- OOP: Encapsulation, inheritance, polymorphism, abstraction; interfaces and abstract classes.
- JVM: Bytecode, GC, multi-threading; Java runs on JVM (portable).
- Collections: List, Set, Map; ArrayList, HashMap; streams for functional-style ops.
- Relevance: Backend services, integrations, OSS/BSS/CPQ systems often use Java.

### 2. Angular

- Components: Template + class + metadata; @Component decorator; input/output; lifecycle hooks.
- Services: Injectable singletons for logic and HTTP; dependency injection.
- RxJS: Observables for async data; subscribe, map, filter; HttpClient returns Observable.
- Routing: RouterModule, routes, routerLink, router-outlet; lazy loading for modules.

### 3. JavaScript

- ES6+: let/const, arrow functions, template literals, destructuring, spread, classes, modules (import/export).
- Async: Promises, async/await; fetch for HTTP.
- DOM: querySelector, addEventListener, createElement; or use a framework (Angular, React).

### 4. OSS (Operations Support Systems)

- Purpose: Network and service operations: provisioning, inventory, fault/performance management, activation.
- Examples: Order management, network inventory, activation, trouble ticketing, monitoring.
- Link to Gen AI: RAG over OSS docs/tickets; chatbots for provisioning status, workarounds.

### 5. BSS (Business Support Systems)

- Purpose: Customer-facing business processes: CRM, billing, orders, products, revenue.
- Examples: Billing, CRM, order capture, product catalog, revenue management.
- Link to Gen AI: CPQ, quote generation, FAQ bots, billing inquiry handling.

### 6. CPQ (Configure, Price, Quote)

- Configure: Product configuration (rules, constraints, options).
- Price: Pricing rules, discounts, contracts.
- Quote: Generate and manage quotes/proposals.
- Link to Gen AI: Guided configuration, natural-language quote requests, document generation.

### 7. Telecom Domain

- Concepts: Networks (core, access, transport), services (voice, data, IoT), fulfillment (activate), assurance (monitor, fix), inventory, SR/ticketing.
- Relevance: OSS/BSS/CPQ sit in telecom IT; Gen AI can support deflections, workarounds, and knowledge search (e.g. SR Analyzer, Orionverse).

---

## 💡 Top 15 Interview Q&A – Full-Stack & Domain

Q1: What is the difference between let, const, and var in JavaScript?
> "let and const are block-scoped; var is function-scoped. const is for constants (reference fixed; object contents can change). let for reassignable variables. Prefer const by default, let when reassignment is needed."

Q2: What is an Observable (RxJS) and how does it differ from a Promise?
> "Observable represents a stream of values over time; you subscribe to get values. Promise is single value, eager. Observables are cancellable, composable (operators), and can emit multiple values. Angular HttpClient uses Observables."

Q3: How does Angular dependency injection work?
> "Services (and other injectables) are registered in providers (root, module, or component). When a component asks for a service in the constructor, the injector provides the instance. Enables testing and loose coupling."

Q4: What is the difference between Java and Python in the context of backend?
> "Java: static typing, JVM, strong in enterprise and OSS/BSS. Python: dynamic, concise; strong in data/ML and rapid prototyping. I use Python for Gen AI/RAG and Flask; Java where existing systems or performance requirements dictate it."

Q5: What is OSS and BSS?
> "OSS is operations support: provisioning, inventory, fault/performance management, activation. BSS is business support: CRM, billing, orders, products. Together they support telecom service delivery and revenue."

Q6: What is CPQ?
> "Configure, Price, Quote: software for product configuration (rules and constraints), pricing (rules, discounts), and quote/proposal generation. Used in sales and telecom product offerings."

Q7: How does Gen AI apply to telecom/OSS/BSS?
> "RAG over knowledge bases and tickets for deflections and workarounds; chatbots for status and FAQ; summarization of SRs; CPQ assistance (natural-language config or quote requests). I’ve built RAG for SR analysis and workaround suggestion."

Q8: What is an Angular component and what does it contain?
> "A component has a template (HTML), a class (logic and state), and metadata (@Component: selector, templateUrl, styleUrls). It can have inputs/outputs and lifecycle hooks (ngOnInit, etc.)."

Q9: What is the Angular HTTP client and how do you use it?
> "HttpClient from @angular/common/http: get, post, put, delete return Observables. I subscribe in the component or use async pipe. I handle errors with catchError and use interceptors for auth or logging."

Q10: What is REST and how does it differ from SOAP?
> "REST is resource-based over HTTP: URLs for resources, methods (GET/POST/PUT/DELETE), stateless, often JSON. SOAP is XML-based, WSDL, more formal. REST is common for modern APIs and front–back communication."

Q11: What is the role of OSS in telecom?
> "OSS supports network and service operations: order fulfillment, inventory, activation, fault and performance management. It ensures services are provisioned and maintained; integrates with BSS for orders and billing."

Q12: How would you integrate a Gen AI (e.g. RAG) service with an existing Angular front-end?
> "Expose a REST API from the backend (e.g. Flask) that the Angular app calls via HttpClient. Backend runs RAG/LLM and returns structured JSON. Front-end displays results and handles loading/error states. Auth via same session or token as rest of app."

Q13: What is the difference between synchronous and asynchronous in JavaScript?
> "Synchronous runs in order and blocks. Asynchronous (callbacks, Promises, async/await) allows other code to run while waiting for I/O. I use async/await for HTTP and file ops to keep code readable."

Q14: What is dependency injection and why is it useful?
> "DI provides dependencies (e.g. services) to a class from outside rather than the class creating them. Benefits: testability (mock dependencies), loose coupling, single place to configure implementations. Angular and Spring use DI."

Q15: How do your full-stack and telecom skills support a Gen AI role?
> "I can build end-to-end: front-end (Angular/JS) for chat or search, backend (Flask/Python) for RAG/LLM, and integrate with OSS/BSS/CPQ APIs. Domain knowledge in telecom and OSS/BSS helps me design RAG content, workarounds, and use cases that fit real operations and support flows."

---

## 📊 Key Talking Points

- Full-stack: Angular components and services, JS/ES6+, HTTP client; backend (Flask/Java) APIs; integration of Gen AI via REST.
- OSS/BSS: OSS for operations and network; BSS for business and billing; both feed and benefit from Gen AI (deflection, workarounds, CPQ).
- CPQ: Configure–Price–Quote; natural-language and RAG can support configuration and quote generation.
- Telecom: Fulfillment, assurance, SR/ticketing; Gen AI for knowledge retrieval and support (e.g. Orionverse, SR Analyzer).

---

## 📁 See Also

- [1_Core_GenAI_RAG_LLM.md](1_Core_GenAI_RAG_LLM.md) – RAG/LLM  
- [3_Backend_DevOps_Cloud.md](3_Backend_DevOps_Cloud.md) – Flask, APIs  
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index  
- Project Details: Orionverse, SR Analyzer – concrete examples of Gen AI in support/telecom context  
