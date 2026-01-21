#!/bin/bash

# Awesome Grok Skills - Comprehensive Test Suite
# This script runs all tests across skills and agents

set -e  # Exit on any error

echo "🚀 Starting Awesome Grok Skills Test Suite"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run a test case
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="${3:-0}"
    
    echo -e "${BLUE}Testing: $test_name${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS: $test_name${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL: $test_name${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo -e "${YELLOW}   Command: $test_command${NC}"
    fi
}

# Function to test file existence
test_file_exists() {
    local file_path="$1"
    local description="$2"
    
    if [ -f "$file_path" ]; then
        echo -e "${GREEN}✅ PASS: $description - $file_path${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL: $description - $file_path${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

# Function to test directory existence
test_dir_exists() {
    local dir_path="$1"
    local description="$2"
    
    if [ -d "$dir_path" ]; then
        echo -e "${GREEN}✅ PASS: $description - $dir_path${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL: $description - $dir_path${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

# Function to test YAML frontmatter
test_yaml_frontmatter() {
    local file="$1"
    local description="$2"
    
    if head -n 20 "$file" | grep -q "^---"; then
        echo -e "${GREEN}✅ PASS: $description has YAML frontmatter${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL: $description missing YAML frontmatter${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

echo -e "\n${YELLOW}🏗️  Testing Project Structure${NC}"

# Test root directories
test_dir_exists "skills" "Skills directory"
test_dir_exists "agents" "Agents directory"
test_dir_exists "templates" "Templates directory"
test_dir_exists "scripts" "Scripts directory"

# Test core files
test_file_exists "README.md" "Main README"
test_file_exists "LICENSE" "License file"
test_file_exists ".gitignore" "Git ignore file"
test_file_exists "CONTRIBUTING.md" "Contributing guide"

echo -e "\n${YELLOW}🎯 Testing Core Skills${NC}"

# Test core skill directories
test_dir_exists "skills/core/tdd" "TDD skill"
test_dir_exists "skills/core/real-time-research" "Real-time research skill"
test_dir_exists "skills/core/physics-simulation" "Physics simulation skill"
test_dir_exists "skills/core/meme-code-hybrids" "Meme-code hybrids skill"
test_dir_exists "skills/core/efficient-code" "Efficient code skill"

# Test core skill files
test_file_exists "skills/core/tdd/GROK.md" "TDD skill file"
test_file_exists "skills/core/real-time-research/GROK.md" "Real-time research skill file"
test_file_exists "skills/core/physics-simulation/GROK.md" "Physics simulation skill file"
test_file_exists "skills/core/meme-code-hybrids/GROK.md" "Meme-code hybrids skill file"
test_file_exists "skills/core/efficient-code/GROK.md" "Efficient code skill file"

echo -e "\n${YELLOW}🌐 Testing Web Development Skills${NC}"

test_dir_exists "skills/web-dev/nextjs-fullstack" "Next.js skill"
test_dir_exists "skills/web-dev/tailwind-shadcn" "Tailwind shadcn skill"
test_dir_exists "skills/web-dev/supabase-auth" "Supabase auth skill"

test_file_exists "skills/web-dev/nextjs-fullstack/GROK.md" "Next.js skill file"
test_file_exists "skills/web-dev/tailwind-shadcn/GROK.md" "Tailwind shadcn skill file"
test_file_exists "skills/web-dev/supabase-auth/GROK.md" "Supabase auth skill file"

echo -e "\n${YELLOW}📱 Testing Mobile Development Skills${NC}"

test_dir_exists "skills/mobile/expo-react-native" "Expo React Native skill"
test_file_exists "skills/mobile/expo-react-native/GROK.md" "Expo React Native skill file"

echo -e "\n${YELLOW}⚙️ Testing Backend Skills${NC}"

test_dir_exists "skills/backend/fastapi-best-practices" "FastAPI skill"
test_file_exists "skills/backend/fastapi-best-practices/GROK.md" "FastAPI skill file"

echo -e "\n${YELLOW}🪙 Testing Crypto/Web3 Skills${NC}"

test_dir_exists "skills/crypto-web3/defi-patterns" "DeFi patterns skill"
test_dir_exists "skills/crypto-web3/nft-marketplace" "NFT marketplace skill"
test_dir_exists "skills/crypto-web3/token-analytics" "Token analytics skill"

test_file_exists "skills/crypto-web3/defi-patterns/GROK.md" "DeFi patterns skill file"
test_file_exists "skills/crypto-web3/nft-marketplace/GROK.md" "NFT marketplace skill file"
test_file_exists "skills/crypto-web3/token-analytics/GROK.md" "Token analytics skill file"

# Test resource files for crypto skills
test_file_exists "skills/crypto-web3/defi-patterns/resources/solidity-templates.md" "Solidity templates resource"
test_file_exists "skills/crypto-web3/nft-marketplace/resources/erc721-standards.md" "ERC721 standards resource"
test_file_exists "skills/crypto-web3/token-analytics/resources/market-data-apis.md" "Market data APIs resource"

echo -e "\n${YELLOW}🤖 Testing Agent Files${NC}"

test_file_exists "agents/full-stack-planner/GROK.md" "Full-stack planner agent"
test_file_exists "agents/code-review-team/GROK.md" "Code review team agent"
test_file_exists "agents/market-research-oracle/GROK.md" "Market research oracle agent"
test_file_exists "agents/physics-simulation-engine/GROK.md" "Physics simulation engine agent"

test_file_exists "agents/full-stack-planner/workflow.yaml" "Full-stack planner workflow"
test_file_exists "agents/code-review-team/review-checklist.md" "Code review checklist"
test_file_exists "agents/market-research-oracle/data-sources.md" "Market research data sources"
test_file_exists "agents/physics-simulation-engine/simulation-templates.md" "Physics simulation templates"

echo -e "\n${YELLOW}🧪 Testing YAML Frontmatter${NC}"

# Test YAML frontmatter in key files
test_yaml_frontmatter "skills/core/tdd/GROK.md" "TDD skill"
test_yaml_frontmatter "skills/core/real-time-research/GROK.md" "Real-time research skill"
test_yaml_frontmatter "skills/web-dev/nextjs-fullstack/GROK.md" "Next.js skill"
test_yaml_frontmatter "agents/full-stack-planner/GROK.md" "Full-stack planner"

echo -e "\n${YELLOW}📜 Testing Template Files${NC}"

test_file_exists "templates/project-GROK.md" "Project template"
test_file_exists "templates/skill-template.md" "Skill template"
test_file_exists "templates/global-skills-install.md" "Global install guide"

echo -e "\n${YELLOW}🔧 Testing Script Files${NC}"

test_file_exists "scripts/setup.sh" "Setup script"
test_file_exists "scripts/validate-skills.sh" "Skills validation script"

echo -e "\n${YELLOW}✍️ Testing Content Quality${NC}"

# Test for required sections in GROK.md files
test_grok_content() {
    local file="$1"
    local skill_name="$2"
    
    if grep -q "## 🎯 Why This Matters for Grok" "$file"; then
        echo -e "${GREEN}✅ PASS: $skill_name has Grok-specific section${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL: $skill_name missing Grok-specific section${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

test_grok_content "skills/core/tdd/GROK.md" "TDD skill"
test_grok_content "skills/core/meme-code-hybrids/GROK.md" "Meme-code hybrids skill"
test_grok_content "agents/market-research-oracle/GROK.md" "Market research oracle"

echo -e "\n${YELLOW}🔍 Testing Code Examples${NC}"

# Test for code examples in key files
test_code_examples() {
    local file="$1"
    local skill_name="$2"
    
    # Check for JavaScript code blocks
    if grep -q "\`\`\`javascript" "$file" || grep -q "\`\`\`python" "$file"; then
        echo -e "${GREEN}✅ PASS: $skill_name contains code examples${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL: $skill_name missing code examples${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

test_code_examples "skills/core/efficient-code/GROK.md" "Efficient code skill"
test_code_examples "skills/crypto-web3/defi-patterns/resources/solidity-templates.md" "DeFi patterns resource"

echo -e "\n${YELLOW}🏗️  Testing YAML Syntax${NC}"

# Test YAML syntax for workflow files
run_test "Full-stack planner YAML syntax" "python -c 'import yaml; yaml.safe_load(open(\"agents/full-stack-planner/workflow.yaml\"))'"

echo -e "\n${YELLOW}📏 Testing File Size Limits${NC}"

# Test for reasonable file sizes (not too large, not too small)
test_file_size() {
    local file="$1"
    local description="$2"
    local min_size=500  # bytes
    local max_size=50000 # bytes
    
    if [ -f "$file" ]; then
        local size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo 0)
        
        if [ "$size" -ge "$min_size" ] && [ "$size" -le "$max_size" ]; then
            echo -e "${GREEN}✅ PASS: $description has reasonable size ($size bytes)${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e "${RED}❌ FAIL: $description size ($size bytes) out of range ($min_size-$max_size)${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
    else
        echo -e "${RED}❌ FAIL: $description - file not found${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

test_file_size "README.md" "README file"
test_file_size "skills/core/tdd/GROK.md" "TDD skill file"

echo -e "\n${YELLOW}🌍 Testing Links and References${NC}"

# Test for broken internal links
test_internal_links() {
    local file="$1"
    local description="$2"
    
    # Extract markdown links and test if they point to existing files
    local broken_links=$(grep -o '\[.*\]([^)]*)' "$file" | grep -v '^http' | grep -v '^#' | sed 's/.*(\(.*\))/\1/' | while read link; do
        if [ ! -f "$link" ] && [ ! -d "$link" ]; then
            echo "$link"
        fi
    done)
    
    if [ -z "$broken_links" ]; then
        echo -e "${GREEN}✅ PASS: $description has no broken internal links${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL: $description has broken links: $broken_links${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

test_internal_links "README.md" "README file"

echo -e "\n${YELLOW}🎭 Testing Grok Personality Elements${NC}"

# Test for Grok personality traits in content
test_grok_personality() {
    local file="$1"
    local description="$2"
    
    # Check for personality indicators
    if grep -qi -E "(meme|physics|real.*time|efficient|maximally)" "$file"; then
        echo -e "${GREEN}✅ PASS: $description reflects Grok personality${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL: $description lacks Grok personality elements${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

test_grok_personality "README.md" "README file"
test_grok_personality "skills/core/meme-code-hybrids/GROK.md" "Meme-code hybrids skill"

echo -e "\n${YELLOW}🚀 Testing Installation Readiness${NC}"

# Test for installation requirements
test_installation_files() {
    # Check if setup script is executable
    if [ -x "scripts/setup.sh" ]; then
        echo -e "${GREEN}✅ PASS: Setup script is executable${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${YELLOW}⚠️  WARN: Setup script is not executable${NC}"
        # Don't count as failure since this might be environment-specific
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    # Check for package.json if Node.js dependencies are expected
    if [ -f "package.json" ]; then
        echo -e "${GREEN}✅ PASS: Package.json exists for Node.js dependencies${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${YELLOW}⚠️  WARN: No package.json found - manual setup may be required${NC}"
        # Don't count as failure since this might be intentional
    fi
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

test_installation_files

echo -e "\n${YELLOW}📊 Test Results Summary${NC}"
echo "=========================================="

echo -e "Total Tests: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"

# Calculate success rate
if [ $TOTAL_TESTS -gt 0 ]; then
    SUCCESS_RATE=$(( (PASSED_TESTS * 100) / TOTAL_TESTS ))
    echo -e "Success Rate: $SUCCESS_RATE%"
    
    if [ $SUCCESS_RATE -ge 90 ]; then
        echo -e "${GREEN}🎉 Excellent! The project is ready for deployment!${NC}"
    elif [ $SUCCESS_RATE -ge 75 ]; then
        echo -e "${YELLOW}👍 Good! Minor fixes needed before deployment.${NC}"
    else
        echo -e "${RED}⚠️  Issues found. Review and fix before deployment.${NC}"
    fi
else
    echo -e "${RED}❌ No tests were executed${NC}"
fi

echo -e "\n${BLUE}Next Steps:${NC}"
echo "1. Fix any failed tests"
echo "2. Review warnings if any"
echo "3. Run 'npm run lint' and 'npm run test' if available"
echo "4. Initialize git repository"
echo "5. Push to GitHub"

exit $FAILED_TESTS