import random
import os

def generate_data(size):
    real_sites = [
        ("https://www.google.com", "Google - Tim kiem"),
        ("https://www.youtube.com", "YouTube - Xem video"),
        ("https://www.facebook.com", "Facebook - Mang xa hoi"),
        ("https://www.vnexpress.net", "VnExpress - Bao tieng Viet"),
        ("https://www.github.com", "GitHub - Luu tru ma nguon"),
        ("https://www.stackoverflow.com", "Stack Overflow - Hoi dap code"),
        ("https://www.wikipedia.org", "Wikipedia - Bach khoa toan thu"),
        ("https://www.netflix.com", "Netflix - Xem phim truc tuyen"),
        ("https://www.shopee.vn", "Shopee - Mua sam online"),
        ("https://www.tiktok.com", "TikTok - Video ngan")
    ]
    
    filename = f'data_{size}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(1, size + 1):
            base_url, base_title = random.choice(real_sites)
            
            # Add some variations to make them look like real browsing history
            if i % 3 == 0:
                url = f"{base_url}/search?q=tu+khoa+{i}"
                title = f"{base_title} (Tim kiem)"
            elif i % 5 == 0:
                url = f"{base_url}/user/profile_{i}"
                title = f"{base_title} - Ho so"
            elif i % 7 == 0:
                url = f"{base_url}/watch?v=videoID_{i}"
                title = f"{base_title} - Video"
            else:
                url = f"{base_url}/page/{i}"
                title = f"{base_title} - Trang"
                
            f.write(f"{url},{title}\n")
    print(f"Dataset {filename} with {size} rows generated successfully.")

if __name__ == '__main__':
    # Generate datasets of evenly spaced sizes for a perfect linear chart
    sizes = [10, 100, 1000, 5000, 10000]
    for size in sizes:
        generate_data(size)
    
    print("All datasets generated successfully!")
