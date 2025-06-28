# 🌱 SUSTAIN: The Environmentally-Friendly AI 🌱

![Demo Preview](https://img.shields.io/badge/Demo-Interactive-brightgreen) 
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/github/license/djleamen/SUSTAIN)
![Commit Activity](https://img.shields.io/github/commit-activity/w/djleamen/SUSTAIN)
![Last Commit](https://img.shields.io/github/last-commit/djleamen/SUSTAIN)
![Open Issues](https://img.shields.io/github/issues/djleamen/SUSTAIN)
![PRs](https://img.shields.io/github/issues-pr/djleamen/SUSTAIN)
![Contributors](https://img.shields.io/github/contributors/djleamen/SUSTAIN)
![Deployed on Azure](https://img.shields.io/badge/Hosted-Azure-blue)

<picture>
  <source srcset="application/assets/SUSTAINOriginalWhiteTransparentCropped.png" media="(prefers-color-scheme: dark)">
  <img src="application/assets/SUSTAINOriginalBlackTransparentCropped.png" alt="SUSTAIN logo">
</picture>

## Overview
SUSTAIN is an environmentally-friendly, token-optimized AI wrapper designed to reduce compute costs and increase productivity. By filtering out irrelevant words and phrases from prompts, SUSTAIN minimizes the number of tokens sent to and received from the AI, saving energy and boosting performance.

Our mission is to deliver a sustainable, high-efficiency alternative to major large language models (LLMs) while maintaining powerful AI-driven results.🔋

---

## Why SUSTAIN?

### **Environmental Sustainability**
- Traditional AI systems expend significant energy processing large amounts of token data, much of which is redundant or irrelevant (e.g., greetings, fillers, politeness).
- SUSTAIN significantly reduces token usage, minimizing the carbon footprint of AI queries.
- By promoting shorter, optimized inputs and outputs, SUSTAIN contributes to a greener AI ecosystem.

### **Enhanced Productivity**
- Get results faster with condensed, actionable responses.
- Eliminate unnecessary verbose outputs by default, with the option to expand details when needed.
- Powerful, straight-to-the-point professional AI assistant.


---

## Features

### **1. Token Optimization Pipeline**
- Preprocesses user prompts to filter out unnecessary words (e.g., "Hello," "Thank you," etc.) and retain only the core intent.
  - Example Conversion:  
    - **Input:** "Could you kindly explain machine learning? Thank you!" 
    - **Refined input**: "explain machine learning"
- Uses Python's word2number module and intelligently strips detected math from a prompt to calculate locally instead of sending to AI, translating into 100% token savings for all math queries.
  - Example:
    - **Input:** "What's four times three"
    - **Refined input**: 4*3
  
### **2. Short-Form AI Responses**
- Limits responses to concise, actionable outputs using optimized `max_tokens` settings.
- Example Output:
  - **Refined input**: "explain machine learning"
  - **Output:** "Machine learning is a field of AI that trains computers to learn patterns from data."

### **3. Environmentally-Aware Feedback**
- Track token savings and display eco-friendly metrics to users.
- Example:
  - Token savings: 50%
  - You have saved: 0.0023 kWh of power and 0.0009 metric tons of CO₂ emissions

---

## Roadmap
- [x] Provide additional eco-feedback on overall token savings
- [x] Convert to web app and deploy on Azure
- [x] Implement math optimization pipeline
- [x] Implement caching for frequently requested queries to reduce API calls
- [x] Convert to Android, iOS apps
- [ ] Implement dynamic summarization based on context length

---

## Contributing
See our [Contributing](https://github.com/djleamen/SUSTAIN/blob/main/CONTRIBUTING.md) page.

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/djleamen/SUSTAIN)

---

## Contact
For questions or suggestions, feel free to reach out to us:
- **Project Team:**
   - Klein Cafa kleinlester.cafa@ontariotechu.net
   - Tomasz Puzio tomasz.puzio@ontariotechu.net
   - DJ Leamen dj.leamen@ontariotechu.net
   - Juliana Losada Prieto juliana.losadaprieto@ontariotechu.net

---

## Links
[Try it out!](https://sustainai.ca)

[GitHub (Desktop)](https://github.com/djleamen/SUSTAIN)

[GitHub (Web)](https://github.com/Tomasz0720/SUSTAINWebApp)

[GitHub iOS](https://github.com/cafakleinn/SUSTAINForiOS)

[GitHub Android](https://github.com/Tomasz0720/SUSTAINForAndroid)


Let’s build a more sustainable AI future together!
