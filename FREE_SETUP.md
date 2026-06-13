# 🆓 FREE Setup Guide - Using Hugging Face Models

## Changes Made

✅ All agents now use **Mistral-7B-Instruct** (completely free, open-source)
✅ Replaced OpenAI (paid) with Hugging Face (free)
✅ Cost: **$0.00** instead of ~$0.02 per blog post
✅ Total monthly cost: **$0.00** (only Tavily for searches)

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Hugging Face Token (2 min)

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Give it a name: `truthlens-ai`
4. **Type**: Read (⚠️ NOT write)
5. Click **"Create token"**
6. Copy the token

### Step 2: Update .env File (1 min)

Edit `.env` file and replace:

```bash
# Change THIS:
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

# To THIS (paste your token):
HUGGINGFACEHUB_API_TOKEN=hf_aBcDeFgHiJkLmNoPqRsTuVwXyZ
```

### Step 3: Get Tavily API Key (1 min)

1. Go to: https://tavily.com
2. Sign up (free)
3. Get API key from dashboard
4. Update .env:

```bash
TAVILY_API_KEY=tvly_aBcDeFgHiJkLmNoPqRsT
```

### Step 4: Install New Dependencies (1 min)

```bash
pip install -r requirements.txt
```

### Step 5: Run It!

```bash
python main.py
```

---

## 📊 Comparison: Free vs Paid

| Factor | Free (Hugging Face) | Paid (OpenAI) |
|--------|-------------------|---------------|
| **Cost** | $0/month | ~$0.40/month (20 blogs) |
| **Speed** | Slower (~5-10 min) | Faster (~2-5 min) |
| **Quality** | Very Good | Excellent |
| **Setup** | 5 min | 5 min |
| **Privacy** | Server-based | Remote API |
| **Rate Limits** | No | Yes (paid tier) |

---

## 🎯 What Model Are We Using?

**Mistral-7B-Instruct**
- ✅ Free and open-source
- ✅ 7 billion parameters (smaller but capable)
- ✅ Excellent instruction-following
- ✅ Works great for research, writing, and editing
- ✅ Available through Hugging Face Inference API (free)

---

## 💡 Performance Notes

### Processing Time

- **Research**: 2-3 minutes
- **Writing**: 3-5 minutes
- **Editing**: 2-3 minutes
- **Total**: ~7-11 minutes per blog post

This is slower than OpenAI but still reasonable for getting free blog posts.

### Quality

Mistral-7B is quite capable:
- ✅ Good at following instructions
- ✅ Decent writing quality
- ✅ Can fact-check and edit
- ✅ Better than many other free models

---

## ⚙️ Alternative Free Models

If Mistral-7B doesn't work well for you, try these:

```python
# Option 1: Llama-2-7B-Chat (Meta's model)
repo_id="meta-llama/Llama-2-7b-chat-hf"

# Option 2: Zephyr-7B-Beta (Optimized for chat)
repo_id="HuggingFaceH4/zephyr-7b-beta"

# Option 3: OpenHermes-2.5 (Very capable)
repo_id="teknium/OpenHermes-2.5-Mistral-7B"
```

**To switch models**: Edit `agents/researcher.py`, `agents/writer.py`, and `agents/editor.py` and change the `repo_id` parameter.

---

## 🔧 Customization

### Adjust Temperature per Model

In `.env`:
```bash
# Lower = more deterministic
TEMPERATURE_RESEARCH=0.1

# Higher = more creative
TEMPERATURE_WRITER=0.9
```

### Switch Back to OpenAI (if needed)

Just revert:
1. `requirements.txt` - Change back to `langchain-openai`
2. Agents - Change imports back to `ChatOpenAI`
3. `.env` - Add `OPENAI_API_KEY`

---

## ⚠️ Limitations of Free Models

1. **Slower Processing**: Takes longer than GPT-4o
2. **Rate Limiting**: Hugging Face free tier has limits
3. **May Need Retry**: Sometimes responses might be incomplete
4. **Quality Variance**: Not always as good as paid models
5. **No Custom Fine-tuning**: Limited to base model

---

## ✅ Troubleshooting

### "Token not found" Error

```
❌ Error: Invalid API token

✓ Solution:
  1. Check token is copied correctly (no spaces)
  2. Verify token on: https://huggingface.co/settings/tokens
  3. Try regenerating token and updating .env
```

### "Rate limited" Error

```
❌ Error: Rate limit exceeded

✓ Solution:
  1. Wait 5-10 minutes before retrying
  2. Hugging Face free tier has limits
  3. Consider upgrading to Pro ($9/month)
```

### Slow Responses

```
⚠️ Model is very slow

✓ Solutions:
  1. This is normal for free models (5-10 min per blog)
  2. Upgrade Hugging Face for faster inference
  3. Try a smaller model (fewer parameters)
```

### Model Not Found

```
❌ Error: Model not found

✓ Solution:
  1. Check model name is correct in agents
  2. Verify model exists at huggingface.co
  3. Make sure token has access
```

---

## 💾 Cost Breakdown (Monthly)

**With Free Hugging Face:**
- LLM: **$0**
- Tavily searches (100/month): **$0** (free tier)
- **Total: $0**

**With OpenAI:**
- GPT-4o (~3000 tokens × 20 blogs): **~$0.40**
- Tavily: **$0**
- **Total: ~$0.40**

---

## 📚 Resources

- **Hugging Face**: https://huggingface.co
- **Mistral-7B**: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1
- **API Docs**: https://huggingface.co/docs/api-inference
- **Models**: https://huggingface.co/models

---

## 🚀 Ready to Go!

1. Get Hugging Face token: https://huggingface.co/settings/tokens
2. Update `.env` with your token
3. Run: `pip install -r requirements.txt`
4. Start: `python main.py`

**Enjoy free AI-powered blogging! ✨**

---

## 🎯 Next Steps

- [ ] Get Hugging Face token
- [ ] Update .env file
- [ ] Run `pip install -r requirements.txt`
- [ ] Test with `python quick_start.py`
- [ ] Run `python main.py` for your first blog
- [ ] Monitor performance and adjust temps if needed

**Questions?** Check DEPLOYMENT.md or CUSTOMIZATION.md in the project root.
