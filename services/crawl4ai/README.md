# Crawl4AI Service

บริการสำหรับทำ Web Scraping และดึงเนื้อหาจากเว็บไซต์เพื่อนำมาวิเคราะห์ต่อโดย AI

## รายละเอียด
- **Image**: `unclecode/crawl4ai:latest`
- **Port**: `8081` (ภายในคอนเทนเนอร์ใช้ `8080`)

## การใช้งาน
Agent สามารถเรียกใช้ Crawl4AI ผ่าน API เพื่อดึงเนื้อหาจาก URL ที่ต้องการ โดยระบบจะทำการแปลงเนื้อหาหน้าเว็บให้เป็นรูปแบบที่ AI เข้าใจง่าย (เช่น Markdown หรือ Cleaned HTML)

## การตั้งค่าใน Docker Compose
```yaml
crawl4ai:
  image: unclecode/crawl4ai:latest
  container_name: crawl4ai
  restart: always
  ports:
    - "8081:8080"
```
