from faker import Faker
import random
import pandas as pd
from datetime import datetime,timedelta
from unidecode  import unidecode 
from pathlib import Path


faker = Faker()

roles = ['user','admin','manager']
statuses = ['active','inactive','pending']
name_domain = '@example.com'

# 🔧 Tìm thư mục gốc dự án (dựa vào file requirements.txt)
def get_project_folder():
    current_path = Path(__file__).resolve()
    while current_path != current_path.root:
        if (current_path / 'requirements.txt').exists():
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError("Không tìm thấy 'requirements.txt' trong các thư mục cha.")

# 🎲 Fake danh sách người dùng
def generate_user(number):
    user_lists = []
    try:
        for i in range(1,number):
            name = faker.name()
            name_email = name.replace(" ","_").lower()
            email = name_email + name_domain
            user_lists.append({
                'user_id' : f'U{i:03d}',
                'full name': name,
                'email': email,
                'address':  faker.address(),
                'role' : random.choice(roles),
                'birthday': faker.date_of_birth(),
                'status':random.choice(statuses),
                'phone_number' : faker.phone_number(),
                'password': faker.password(),
                'created_date' : faker.date_this_decade(),
                'expirated_date' : faker.date_this_year()
            })
        return user_lists
    except Exception as e:
        print(f"[❌] Lỗi khi tạo user: {e}")
        return []

def save_userlist(filename:str,list_users: list[dict]):
    try:
        current_path = get_project_folder()
        save_location = current_path / 'data' /filename
        save_location.mkdir(exist_ok=True)
        df= pd.DataFrame(list_users)
        df.to_csv(f'{save_location}.csv', index=False,encoding='utf-8')
        df.to_excel(f'{save_location}.xlsx',index=False)
        print(f"[✅] Đã lưu file CSV & Excel tại folder {save_location}")
    except Exception as e:
        print(f"[❌] Lỗi khi lưu file: {e}")



if __name__ == "__main__":
    users = generate_user(1000)
    if users:
        save_userlist("list_users", users)

# df = pd.DataFrame(user_lists)
# df.to_csv()
