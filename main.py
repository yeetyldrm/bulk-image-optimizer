import os
import argparse
from PIL import Image

def optimize_images(input_dir, output_dir, max_width=1920, quality=80):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    processed_count = 0

    print(f"[*] Optimizasyon baslatiliyor... Hedef klasor: {output_dir}")

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(input_dir, filename)
            try:
                with Image.open(file_path) as img:
                    if img.width > max_width:
                        ratio = max_width / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                    new_filename = os.path.splitext(filename)[0] + ".webp"
                    output_path = os.path.join(output_dir, new_filename)

                    img.save(output_path, 'webp', optimize=True, quality=quality)
                    print(f"[+] Basarili: {filename} -> {new_filename}")
                    processed_count += 1
            except Exception as e:
                print(f"[-] Hata: {filename} islenemedi. Detay: {e}")

    print(f"[*] Islem tamamlandi! Toplam {processed_count} gorsel optimize edildi.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acik Kaynak Toplu Gorsel Optimize Edici")
    parser.add_argument("-i", "--input", default="input_images", help="Girdi klasoru")
    parser.add_argument("-o", "--output", default="output_images", help="Cikti klasoru")
    parser.add_argument("-w", "--width", type=int, default=1920, help="Maksimum genislik")
    parser.add_argument("-q", "--quality", type=int, default=80, help="Gorsel kalitesi (1-100)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        os.makedirs(args.input)
        print(f"[!] '{args.input}' klasoru olusturuldu. Lutfen icine gorselleri ekleyip tekrar calistirin.")
    else:
        optimize_images(args.input, args.output, args.width, args.quality)