# LangBridge 🗣️→📝→🌐
### Hindi Speech-to-Text & Translation, Built for the Way India Actually Talks

> Standard ASR models are trained on clean, single-language speech. Real Indian speech constantly switches between Hindi and English mid-sentence — and most models quietly fail at exactly that point. LangBridge measures that failure and fixes it.

---

## The Problem

Ask a voice assistant to transcribe *"mujhe ek meeting schedule karni hai for tomorrow"* and most ASR systems — including strong general-purpose models — stumble. Not because the audio is unclear, but because the sentence isn't monolingual, and monolingual is what these models were trained on.

This isn't an edge case. It's how hundreds of millions of people speak every day. Any product doing voice input, transcription, or translation for Indian users runs into this immediately.

**LangBridge exists to measure that gap precisely, then close it.**

---

## What It Does

```
🎤 Hindi/Hinglish Audio
        │
        ▼
┌───────────────────┐
│  Whisper-small     │   fine-tuned with LoRA on Hindi speech (IndicVoices)
│  (Speech → Text)   │
└───────────────────┘
        │  Hindi transcript
        ▼
┌───────────────────┐
│  IndicTrans2       │   Hindi → English, built for Indian language pairs
│  (Text → Text)     │
└───────────────────┘
        │  English translation
        ▼
┌───────────────────┐
│  Flask REST API    │   POST /transcribe → { "hindi": ..., "english": ... }
└───────────────────┘
        │
        ▼
   📱 Streamlit demo UI
```

Two models, each doing one job, chained into a service you can actually call.

---

## The Finding

Most ASR projects report a single blended accuracy number and stop there. LangBridge deliberately splits evaluation into two slices:

| Test set | Word Error Rate (baseline) | Word Error Rate (fine-tuned) |
|---|---|---|
| Clean Hindi | `[X]%` | `[Y]%` |
| Code-switched Hinglish | `[X]%` | `[Y]%` |

> **The gap between these two rows *is* the point.** A model that looks strong on clean Hindi and quietly falls apart on code-switched speech isn't ready for real Indian users — and you'd never know it from a single aggregate number.

*(Numbers above are placeholders — pending final training run. See [Results](#results) for methodology.)*

---

## Why These Choices

| Component | Choice | Why not the obvious alternative |
|---|---|---|
| ASR base | Whisper-small | Fits free-tier GPU; large/medium variants don't fit a LoRA fine-tune on a T4 |
| Fine-tuning | LoRA / PEFT | Few million trainable params vs. 244M full fine-tune — realistic on limited compute |
| Training data | AI4Bharat IndicVoices | Purpose-built for Indian languages; streams without needing full local download |
| Translation | IndicTrans2 | Trained specifically on Indian language pairs — measurably stronger here than generic multilingual translators |
| Serving | Flask + Docker | Matches production deployment patterns rather than staying in a notebook |

---

## Try It

```bash
# clone and set up
git clone https://github.com/TUZHAR-404/langbridge.git
cd langbridge
docker build -t langbridge .
docker run -p 5000:5000 langbridge
```

```bash
# call the API
curl -X POST http://localhost:5000/transcribe \
  -F "audio=@sample.wav"
```

```json
{
  "hindi": "मुझे कल की मीटिंग शेड्यूल करनी है",
  "english": "I need to schedule tomorrow's meeting"
}
```

Or launch the Streamlit demo for a point-and-click interface:

```bash
streamlit run demo.py
```

---

## Architecture Notes

- Scoped deliberately to **Hindi** for this build. IndicTrans2's existing coverage of ~22 Indian languages means the translation layer generalizes without architectural changes — the ASR fine-tune is the part that would need to be repeated per language.
- LoRA adapters are trained on Hindi audio only; the base Whisper checkpoint is untouched, so the same base model could support additional adapter fine-tunes later without retraining from scratch.

---

## What's Next

- [ ] Expand the code-switched evaluation set beyond the current curated sample
- [ ] Investigate targeted fine-tuning on code-switched data specifically, not just clean Hindi
- [ ] Add streaming/chunked inference for lower end-to-end latency

---

## Credits

Built on [OpenAI Whisper](https://github.com/openai/whisper), [AI4Bharat IndicVoices](https://huggingface.co/datasets/ai4bharat/IndicVoices), and [AI4Bharat IndicTrans2](https://github.com/AI4Bharat/IndicTrans2). This project fine-tunes and integrates these existing models — it doesn't claim to have trained them from scratch.

---

**Author:** Tushar Baghel — [GitHub](https://github.com/TUZHAR-404) · [LinkedIn](https://linkedin.com/in/tushar-baghel05)
