import requests

url = "http://127.0.0.1:8000/posts/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJNYXRuYXphcjA0IiwiZXhwIjoxNzQzNTQyMzE3fQ.Gny5YEmP4LM8if9FBg9BTjhalpJiiRvR0qtqQPx6s-s"
}

# Forma ma'lumotlari va fayllarni birlashtirish uchun 'files' ishlatiladi
multipart_data = [
    ("name", (None, "My Second Post")),
    ("title", (None, "This is a test post")),
    ("text", (None, "This is the content of my second post. welcome!")),
]

# Fayllarni qo'shish
with open("./test_images/test_image1.png", "rb") as f1:
    multipart_data.append(
        ("images", ("test_image1.png", f1.read(), "image/png"))
    )
with open("./test_images/test_image2.png", "rb") as f2:
    multipart_data.append(
        ("images", ("test_image2.png", f2.read(), "image/png"))
    )

# So'rovni yuborish
response = requests.post(url, headers=headers, files=multipart_data)
print(response.status_code)
print(response.json())

"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJNYXRuYXphcjA0IiwiZXhwIjoxNzQzNTAxMjg4fQ.b7DCz2ud4N7gKkVbBrhEKVA40Z7SeQj5BbVNST81MDI"