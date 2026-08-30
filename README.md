# Travel Policy Agents

ระบบตอบคำถามนโยบายการเดินทางต่างประเทศด้วย OpenAI Agents SDK บน Python

## Architecture

`question → Travel Policy Retriever → Travel Policy Formatter → answer`

- `Travel Policy Retriever` เรียก RAG tool เพื่อค้นหา section ที่เกี่ยวข้องจาก `knowledge_base.txt` ด้วย embeddings
- `Travel Policy Formatter` ทำให้คำตอบอ่านง่าย โดยห้ามเพิ่มข้อเท็จจริงนอกเหนือจากผลค้นหา
- RAG index อยู่ใน memory: เหมาะกับไฟล์นโยบายขนาดเล็ก และไม่มีบริการฐานข้อมูลเพิ่ม

## Setup

1. ใช้ Python 3.11 ขึ้นไป แล้วสร้าง virtual environment
2. ติดตั้งแพ็กเกจ: `pip install -e ".[dev]"`
3. คัดลอกไฟล์: `cp .env.example .env`
4. กรอก `OPENAI_API_KEY` และปรับ `OPENAI_BASE_URL` หากใช้ OpenAI-compatible endpoint

## Run

```bash
python main.py "เที่ยวบินเกิน 6 ชั่วโมงเลือกชั้นโดยสารอะไรได้บ้าง"
pytest
ruff check .
```

`knowledge_base.txt` คือแหล่งข้อมูลเดียวของคำตอบ โดยแต่ละหัวข้อต้องขึ้นต้นด้วยรูปแบบ `1. ชื่อหัวข้อ`.
