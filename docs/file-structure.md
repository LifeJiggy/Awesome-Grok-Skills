awesome-grok-skills/
├── skills/                     # Core: categorized skill folders (each is portable)
│   ├── core/                   # Foundational / always-useful
│   │   ├── tdd/
│   │   │   ├── GROK.md         # YAML frontmatter + detailed instructions tuned for Grok
│   │   │   ├── resources/      # Optional: example test templates, patterns.md
│   │   │   └── scripts/        # Optional executable helpers (if agent supports)
│   │   ├── real-time-research/
│   │   │   ├── GROK.md         # Leverage Grok's X/web search strength
│   │   │   └── resources/
│   │   │       └── x-api-examples.md
│   │   ├── physics-simulation/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── math-libraries.md
│   │   ├── meme-code-hybrids/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── meme-templates.md
│   │   └── efficient-code/
│   │       ├── GROK.md
│   │       └── resources/
│   │           └── optimization-patterns.md
│   ├── web-dev/
│   │   ├── nextjs-fullstack/
│   │   │   ├── GROK.md
│   │   │   ├── resources/
│   │   │   │   ├── next-config.js
│   │   │   │   └── tailwind-setup.md
│   │   │   └── scripts/
│   │   │       └── setup-next.sh
│   │   ├── tailwind-shadcn/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── component-library.md
│   │   └── supabase-auth/
│   │       ├── GROK.md
│   │       └── resources/
│   │           └── auth-flows.md
│   ├── crypto-web3/
│   │   ├── defi-patterns/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── solidity-templates.md
│   │   ├── nft-marketplace/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── erc721-standards.md
│   │   └── token-analytics/
│   │       ├── GROK.md
│   │       └── resources/
│   │           └── market-data-apis.md
│   ├── mobile/
│   │   ├── expo-react-native/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── navigation-patterns.md
│   │   └── flutter-naija/      # Localized: Paystack, Firebase, slang-friendly prompts
│   │       ├── GROK.md
│   │       └── resources/
│   │           └── african-payment-integrations.md
│   ├── backend/
│   │   ├── fastapi-best-practices/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── api-patterns.md
│   │   ├── rust-cli-patterns/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── cargo-templates.md
│   │   └── graphql-schemas/
│   │       ├── GROK.md
│   │       └── resources/
│   │           └── schema-design.md
│   ├── security/
│   │   ├── vuln-audit-grok/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── security-checklists.md
│   │   └── smart-contract-audit/
│   │       ├── GROK.md
│   │       └── resources/
│   │           └── audit-patterns.md
│   ├── data-science/
│   │   ├── market-analysis/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── trading-algorithms.md
│   │   └── ml-pipelines/
│   │       ├── GROK.md
│   │       └── resources/
│   │           └── model-templates.md
│   ├── indie-hacker/
│   │   ├── micro-saas-spawner/
│   │   │   ├── GROK.md
│   │   │   └── resources/
│   │   │       └── saas-templates.md
│   │   └── product-validation/
│   │       ├── GROK.md
│   │       └── resources/
│   │           └── validation-frameworks.md
│   └── devops/
│       ├── docker-optimization/
│       │   ├── GROK.md
│       │   └── resources/
│       │       └── dockerfile-patterns.md
│       └── ci-cd-pipelines/
│           ├── GROK.md
│           └── resources/
│               └── github-actions-templates.md
├── agents/                     # Multi-step / orchestrator definitions (longer GROK.md or YAML)
│   ├── full-stack-planner/
│   │   ├── GROK.md
│   │   └── workflow.yaml
│   ├── code-review-team/
│   │   ├── GROK.md
│   │   └── review-checklist.md
│   ├── market-research-oracle/
│   │   ├── GROK.md
│   │   └── data-sources.md
│   └── physics-simulation-engine/
│       ├── GROK.md
│       └── simulation-templates.md
├── templates/                  # Ready-to-copy starters
│   ├── project-GROK.md         # Base project memory file
│   ├── skill-template.md       # Template for new skills
│   ├── agent-template.md       # Template for new agents
│   └── global-skills-install.md # How to symlink to ~/.grok/skills/
├── scripts/                    # Utility scripts
│   ├── setup.sh               # Initial project setup
│   ├── validate-skills.sh     # Validate skill format
│   └── sync-docs.sh           # Sync documentation
├── CONTRIBUTING.md             # How to add a skill: format, frontmatter schema, review process
├── .github/
│   ├── workflows/
│   │   ├── lint.yml            # Markdown lint, broken links check
│   │   ├── validate-skills.yml # Validate skill frontmatter
│   │   └── auto-docs.yml       # Auto-generate documentation
│   ├── ISSUE_TEMPLATE/
│   │   ├── skill-request.md
│   │   └── bug-report.md
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── frontmatter-schema.md   # Required/optional YAML keys for GROK.md
│   ├── skill-guidelines.md     # Best practices for writing skills
│   ├── agent-architecture.md   # How agents work
│   └── examples/               # Example implementations
│       ├── simple-skill.md
│       └── complex-agent.md
├── README.md                   # The awesome list itself: table of contents + links to each skill + why Grok-tuned + install guide
├── LICENSE                     # CC0 or MIT (for easy reuse)
├── .gitignore
└── package.json               # Node.js dependencies for scripts/validation