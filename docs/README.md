# Architecture & Algorithm Diagrams (`docs/`)

Visual system modeling and step-by-step algorithm flowcharts for the **Browser History & Cache Navigation System**.

---

## Diagram Index (`docs/diagrams/`)

| Diagram | Scope | File |
| :--- | :--- | :--- |
| **System Architecture** | Data flow between CLI Menu, `BrowserHistory`, `CacheStack`, `TwoStackSimulator`, `Page`, and PSAPI/QPC utilities | [`5_System_Architecture.png`](diagrams/5_System_Architecture.png) |
| **UML Class Diagram** | Class members, method signatures, and ownership relationships (`Page`, `DLLNode`, `StackNode`, `BrowserHistory`, `CacheStack`, `TwoStackSimulator`) | [`6_System_Design_UML.png`](diagrams/6_System_Design_UML.png) |
| **DLL Deletion Flowchart** | `O(N)` traversal + `O(1)` relinking covering head, tail, middle, and `current` pointer adjustment | [`1_DLL_Deletion_Algorithm.png`](diagrams/1_DLL_Deletion_Algorithm.png) |
| **Two-Stack Navigation Model** | `backStack` / `forwardStack` push-pop mechanics and forward-stack invalidation on new page visits | [`2_Two-Stack_Navigation.png`](diagrams/2_Two-Stack_Navigation.png) |
| **Bounded Cache Eviction** | Duplicate URL check, bottom-node traversal when `size >= 100`, and LIFO top insertion | [`3_Cache_Limit_Algorithm.png`](diagrams/3_Cache_Limit_Algorithm.png) |
| **QPC Benchmark Harness** | CPU frequency lookup, 1,000-iteration loop timing, and adaptive decimal/scientific formatting | [`4_Benchmark_QPC_Algorithm.png`](diagrams/4_Benchmark_QPC_Algorithm.png) |
