from PIL import Image
import os


image_path = r"C:\Users\ray\OneDrive\Documents\лаб 8.python\image.png"

if not os.path.exists(image_path):
    print("❌ Ошибка: Файл не найден. Проверьте путь к изображению!")
else:
    print("✅ Изображение найдено, открываю...")

    try:
        
        image = Image.open(image_path)
        print("📷 Изображение успешно открыто!")

        
        new_size = (image.width * 2, image.height * 2)
        image_resized = image.resize(new_size)

        
        image_resized.show()
        image_resized.save("image_resized.png")
        print("✅ Изображение увеличено и сохранено как 'image_resized.png'.")

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
