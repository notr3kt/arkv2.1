#!/usr/bin/env python3
"""
Quick test script to verify API keys are configured correctly.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 S1NGULARITY API Key Configuration Check\n")
print("=" * 60)

# Check OpenAI
openai_key = os.getenv("OPENAI_API_KEY", "")
if openai_key and openai_key.startswith("sk-"):
    print("✅ OpenAI API Key: Configured")
    print(f"   Key prefix: {openai_key[:20]}...")
else:
    print("❌ OpenAI API Key: Missing or invalid")

# Check Anthropic
anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
if anthropic_key and anthropic_key.startswith("sk-ant-"):
    print("✅ Anthropic API Key: Configured")
    print(f"   Key prefix: {anthropic_key[:20]}...")
else:
    print("⚠️  Anthropic API Key: Not configured (optional)")

# Check Tavily
tavily_key = os.getenv("TAVILY_API_KEY", "")
if tavily_key and tavily_key.startswith("tvly-"):
    print("✅ Tavily API Key: Configured")
    print(f"   Key prefix: {tavily_key[:20]}...")
else:
    print("❌ Tavily API Key: Missing or invalid")

# Check JobDiva
jobdiva_client = os.getenv("JOBDIVA_CLIENT_ID", "")
if jobdiva_client and jobdiva_client != "your_client_id_here":
    print("✅ JobDiva API: Configured")
else:
    print("⚠️  JobDiva API: Not configured (placeholder values)")

# Check LLM Provider
llm_provider = os.getenv("LLM_PROVIDER", "anthropic")
print(f"\n📊 Default LLM Provider: {llm_provider}")

print("\n" + "=" * 60)

# Test OpenAI connection
print("\n🧪 Testing OpenAI Connection...")
try:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)

    # Quick test with minimal tokens
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use mini for cost efficiency
        messages=[{"role": "user", "content": "Say 'OK' if you can read this"}],
        max_tokens=10
    )
    print(f"✅ OpenAI Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ OpenAI Error: {str(e)[:100]}")

# Test Tavily connection
print("\n🧪 Testing Tavily Connection...")
try:
    from tavily import TavilyClient
    tavily = TavilyClient(api_key=tavily_key)

    # Quick search test
    result = tavily.search("test", max_results=1)
    print(f"✅ Tavily Response: Found {len(result.get('results', []))} result(s)")
except Exception as e:
    print(f"❌ Tavily Error: {str(e)[:100]}")

print("\n" + "=" * 60)
print("\n✨ Configuration check complete!")
print("\nNext steps:")
print("1. If JobDiva not configured: Add your JobDiva credentials to .env")
print("2. Run: ./start.sh (to start full stack)")
print("3. Or run: uvicorn main:app --reload (to start just the backend)")
