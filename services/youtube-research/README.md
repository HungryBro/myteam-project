# YouTube Research Service

บริการสำหรับดึงข้อมูลและวิเคราะห์วิดีโอจาก YouTube เพื่อหาความรู้และสัญญาณการเทรด (Trading Signals) โดยใช้ AI ในการสรุปเนื้อหา

## ฟีเจอร์หลัก
- ดึงรายการวิดีโอล่าสุดจากช่องที่กำหนด (7 ช่องหลัก)
- ดึง Transcript (คำบรรยาย) ของวิดีโอโดยอัตโนมัติ
- สรุปเนื้อหาด้วย OpenRouter AI (GPT-4o-mini)
- บันทึกผลลัพธ์ลงใน KM Vault ในรูปแบบ JSON

## การติดตั้ง
1. ติดตั้ง Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. ตั้งค่า Environment Variables ในไฟล์ `.env`:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   VAULT_PATH=../../km-vault/research/youtube-summaries/
   ```

## การใช้งาน
รันสคริปต์หลักเพื่อเริ่มการวิเคราะห์:
```bash
python youtube_service.py
```

## โครงสร้างไฟล์
- `youtube_service.py`: สคริปต์หลักในการทำงาน
- `config.json`: รายชื่อช่อง YouTube ที่ติดตาม
- `RULES.md`: กฎและเกณฑ์ในการวิเคราะห์ข้อมูล
- `requirements.txt`: รายการไลบรารีที่จำเป็น
