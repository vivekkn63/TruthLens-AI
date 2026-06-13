# API Setup Guide

This guide walks you through setting up the required API keys for TruthLens AI.

## Prerequisites

Before you start, you'll need:
- OpenAI Account (free tier works for testing)
- Tavily Account (free tier available)
- 10-15 minutes for setup

## Step 1: OpenAI API Key

### 1.1 Create OpenAI Account
1. Go to https://platform.openai.com/signup
2. Sign up with email or Google/Microsoft account
3. Verify your email
4. Add payment method (if not already done)

### 1.2 Generate API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it "TruthLens AI" (optional but helpful)
4. Copy the key immediately (you won't see it again!)

### 1.3 Add to .env
```bash
# .env file
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Important**: Keep this key secret! Don't commit it to git.

## Step 2: Tavily API Key

### 2.1 Create Tavily Account
1. Go to https://tavily.com
2. Sign up (free plan available)
3. Verify your email

### 2.2 Get API Key
1. Log in to https://tavily.com
2. Go to your Dashboard
3. Find your API key under "API Keys" section
4. Copy it

### 2.3 Add to .env
```bash
# .env file
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Step 3: Verify Setup

### Test OpenAI Connection
```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test basic request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello!"}]
)
print(response.choices[0].message.content)
```

### Test Tavily Connection
```python
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Test search
response = client.search(query="Python programming")
print(f"Found {len(response['results'])} results")
```

## Pricing Information

### OpenAI
- **Input**: $0.15 per 1M tokens (GPT-4o)
- **Output**: $0.60 per 1M tokens (GPT-4o)
- **Free credits**: $5 available for new accounts (expires after 3 months)

Estimated cost per workflow:
- Research + Writing + Editing = ~2000-3000 tokens
- **Cost estimate**: ~$0.01-0.02 per blog post

### Tavily
- **Free plan**: 100 searches/month
- **Paid**: $20/month for 100,000 searches
- Each topic typically uses 3-4 searches

## Troubleshooting

### "Invalid API Key" Error
- Check key is copied correctly (no extra spaces)
- Ensure OPENAI_API_KEY starts with `sk-`
- Ensure TAVILY_API_KEY starts with `tvly-`
- Check key hasn't been revoked (check API Key management page)

### "Rate Limited" Error
- Wait a few seconds and retry
- Consider upgrading your OpenAI tier
- Reduce number of parallel requests

### "API Key Not Found" Error
- Verify .env file exists in project root
- Check .env file has correct variable names
- Ensure no typos (case-sensitive)
- Run `load_dotenv()` in code

### "No search results" Error
- Check Tavily API key is valid
- Verify search query is not too specific
- Check internet connection
- Try searching for a simpler, well-known topic

## Best Practices

### Security
✅ DO:
- Store keys only in .env file
- Never commit .env to git
- Use .gitignore to prevent accidental commits
- Rotate keys periodically
- Use different keys for development/production

❌ DON'T:
- Put keys directly in code
- Share .env files
- Post keys in forums or documentation
- Use the same key across multiple projects

### Cost Optimization
- Use `gpt-4o-mini` for initial research/drafts
- Use `gpt-4o` only for critical tasks
- Monitor API usage in OpenAI dashboard
- Set rate limits if needed

### Rate Limiting
- TruthLens uses reasonable delays between API calls
- OpenAI free tier: typically fast enough
- For high-volume use, consider upgrading

## Monitoring API Usage

### OpenAI Dashboard
1. Go to https://platform.openai.com/account/usage/overview
2. View daily/monthly costs
3. See breakdown by model and endpoint

### Tavily Dashboard
1. Log in at https://tavily.com
2. View searches used this month
3. Check search history and results

## Next Steps

Once keys are configured:

1. **Test the system**:
   ```bash
   python quick_start.py
   ```

2. **Try a real workflow**:
   ```bash
   python main.py
   ```

3. **Monitor costs**:
   Check API dashboards during first use to understand pricing

## Support

- **OpenAI Issues**: https://platform.openai.com/account/billing/overview
- **Tavily Issues**: https://tavily.com/help
- **TruthLens Issues**: Check README.md for common issues

---

**Happy researching!** 🚀
