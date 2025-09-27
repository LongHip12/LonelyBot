# ========================================Tutorial==========================================#
#                                                                                                                                                                                                 #
#                                                               Cach cai bot tu A - Z by LongHip12                                                                    #
#                                                               B1: Tai Vscode tai https://code.visualstudio.com                                           #
#                                                               B2: Tai Python tai https://python.org                                                                 #
#                                                               B3: Tai Extension Duoi day:                                                                                 #
#                                                               Python by Microsoft,Jupyter,Path Intellisense,vscodeicon (tuy chon)         #
#                                                               B5: tai package duoi day:                                                                                    #
#                                                               pip install -U discord.py pytz art colorama                                                      #
#                                                               Invite: https://pastefy.app/OA5O3MX3                                                           #
#                                                                                                                                                                                             #
# ========================================Code===========================================

import os
import json
import asyncio
import random
import datetime
import itertools
from pathlib import Path
import discord
from discord import FFmpegPCMAudio, app_commands
from discord.ext import commands, tasks
import yt_dlp as youtube_dl
import pytz
from colorama import Fore, Style, init
init(autoreset=True)

# Màu rainbow chroma
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

ascii_art = r"""
 _                          _          ____          _
| |      ___   _ __    ___ | | _   _  | __ )   ___  | |_
| |     / _ \ | '_ \  / _ \| || | | | |  _ \  / _ \ | __|
| |___ | (_) || | | ||  __/| || |_| | | |_) || (_) || |_
|_____| \___/ |_| |_| \___||_| \__, | |____/  \___/  \__|
                               |___/
"""

def print_chroma(text):
    cycle_colors = itertools.cycle(colors)
    result = ""
    for char in text:
        if char.strip():  # có ký tự
            result += next(cycle_colors) + char + Style.RESET_ALL
        else:  # giữ khoảng trắng
            result += char
    print(result)

print_chroma(ascii_art)
print(Fore.GREEN + "=" * 67)

# Thư mục dữ liệu (relative tới file main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # thư mục chứa main.py
DATA_DIR = os.path.join(BASE_DIR, "Bot_Data")

# Tên file
WHITELIST_FILE = os.path.join(DATA_DIR, "whitelist_users.json")
BANNED_FILE    = os.path.join(DATA_DIR, "blacklist_users.json")
DATA_FILE = Path(os.path.join(DATA_DIR, "data.json"))
LEVEL_FILE = Path(os.path.join(DATA_DIR, "levels.json"))
REACTION_FILE = Path(os.path.join(DATA_DIR, "reaction_roles.json"))
SHOP_FILE = Path(os.path.join(DATA_DIR, "shop.json"))
DAILY_FILE = Path(os.path.join(DATA_DIR, "daily_login.json"))
WORK_FILE = Path(os.path.join(DATA_DIR, "work.json"))
TAIXIU_HISTORY_FILE = Path(os.path.join(DATA_DIR, "taixiu_history.json"))

# Biến toàn cục
ALLOWED_USERS = {}
BANNED_USERS = {}

# Tạo folder nếu chưa tồn tại
os.makedirs(DATA_DIR, exist_ok=True)

# Nếu file chưa có, khởi tạo file rỗng
for p in (WHITELIST_FILE, BANNED_FILE):
    if not os.path.exists(p):
        try:
            with open(p, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[ERROR] Không thể tạo file {p}: {e}")
# Hàm load/save cho whitelist
def save_whitelist():
    try:
        with open(WHITELIST_FILE, "w", encoding="utf-8") as f:
            # lưu key dưới dạng string để JSON hợp lệ
            json.dump({str(k): v for k, v in ALLOWED_USERS.items()}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[ERROR] Không thể lưu {WHITELIST_FILE}: {e}")

def load_whitelist():
    global ALLOWED_USERS
    try:
        with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # chuyển key về int nếu có thể
        ALLOWED_USERS = {}
        for k, v in data.items():
            try:
                ALLOWED_USERS[int(k)] = v
            except Exception:
                ALLOWED_USERS[k] = v
    except Exception as e:
        print(f"[ERROR] Không thể đọc {WHITELIST_FILE}: {e}")
        ALLOWED_USERS = {}

# Hàm load/save cho blacklist
def save_banned_users():
    try:
        with open(BANNED_FILE, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in BANNED_USERS.items()}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[ERROR] Không thể lưu {BANNED_FILE}: {e}")

def load_banned_users():
    global BANNED_USERS
    try:
        with open(BANNED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        BANNED_USERS = {}
        for k, v in data.items():
            try:
                BANNED_USERS[int(k)] = v
            except Exception:
                BANNED_USERS[k] = v
    except Exception as e:
        print(f"[ERROR] Không thể đọc {BANNED_FILE}: {e}")
        BANNED_USERS = {}
        
def load_json(file_path):
    try:
        if file_path.exists():
            return json.loads(file_path.read_text(encoding='utf-8'))
        return {}
    except (json.JSONDecodeError, Exception):
        return {}

def save_json(data, file_path):
    try:
        file_path.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding='utf-8')
    except Exception as e:
        print(f"Lỗi khi lưu file {file_path}: {e}")

# Tạo file shop mẫu nếu chưa có
if not SHOP_FILE.exists():
    default_shop = {
        "vip": {"price": 10000, "role_id": 1420718498530721864, "name": "VIP Role", "description": "Receive the VIP Rank on the Lonely Hub Script, Lonely Hub Forums, and Lonely Hub Discord."},
        "vipplus": {"price": 50000, "role_id": 1420718386786340977, "name": "Vip+ Role", "description": "Receive the VIP+ Rank on the Lonely Hub Script, Lonely Hub Forums, and Lonely Hub Discord."},
        "vipplusplus": {"price": 70000, "role_id": 1421143311900479588, "name": "Vip++ Role", "description": "Receive the VIP+ Rank on the Lonely Hub Script, Lonely Hub Forums, and Lonely Hub Discord."},                                                         
        "mvp": {"price": 100000, "role_id": 1421143426795307018, "name": "MVP Role", "description": "Receive the MVP Rank on the Lonely Hub Script, Lonely Hub Forums, and Lonely Hub Discord."},
        "mvpplus": {"price": 150000, "role_id": 1421143520034426971, "name": "MVP+ Role", "description": "Receive the MVP+ Rank on the Lonely Hub Script, Lonely Hub Forums, and Lonely Hub Discord."},
        "mvpplusplus": {"price": 300000, "role_id": 1421143612543991900, "name": "MVP++ Role", "description": "Receive the MVP++ Rank on the Lonely Hub Script, Lonely Hub Forums, and Lonely Hub Discord."},
        "managerbot": {"price": 999999999999, "role_id": 1410600949646364702, "name": "Manager Role", "description": "Receive the Manager Rank on the Lonely Hub Script, Lonely Hub Forums, and Lonely Hub Discord."}
    }
    save_json(default_shop, SHOP_FILE)

credits = load_json(DATA_FILE)
levels = load_json(LEVEL_FILE)
reaction_roles = load_json(REACTION_FILE)
shop_data = load_json(SHOP_FILE)
daily_data = load_json(DAILY_FILE)
work_data = load_json(WORK_FILE)
taixiu_history = load_json(TAIXIU_HISTORY_FILE)

# ====== ECONOMY FUNCTIONS ======
def get_balance(user_id):
    return credits.get(str(user_id), 0)

def add_balance(user_id, amount):
    credits[str(user_id)] = get_balance(user_id) + amount
    save_json(credits, DATA_FILE)

def remove_balance(user_id, amount):
    if get_balance(user_id) >= amount:
        credits[str(user_id)] -= amount
        save_json(credits, DATA_FILE)
        return True
    return False
    
def can_daily(user_id):
    """Kiểm tra user có thể nhận daily không"""
    user_id = str(user_id)
    if user_id not in daily_data:
        return True
    
    last_daily = datetime.datetime.fromisoformat(daily_data[user_id]["last_claimed"])
    now = datetime.datetime.now()
    return (now - last_daily).days >= 1

def can_work(user_id):
    """Kiểm tra user có thể work không"""
    user_id = str(user_id)
    if user_id not in work_data:
        return True, 0
    
    last_work_date = datetime.datetime.fromisoformat(work_data[user_id]["last_date"]).date()
    today = datetime.datetime.now().date()
    
    # Nếu khác ngày thì reset
    if last_work_date != today:
        work_data[user_id]["count"] = 0
        work_data[user_id]["last_date"] = today.isoformat()
        save_json(work_data, WORK_FILE)
        return True, 0
    
    return work_data[user_id]["count"] < 5, work_data[user_id]["count"]

def add_balance(user_id, amount):
    user_id = str(user_id)
    credits[user_id] = get_balance(user_id) + amount
    save_json(credits, DATA_FILE)
    return credits[user_id]  # 🔥 Trả về số dư mới
    
def remove_balance(user_id, amount):
    user_id = str(user_id)
    if get_balance(user_id) >= amount:
        credits[user_id] -= amount
        save_json(credits, DATA_FILE)
        return credits[user_id]  # 🔥 Trả về số dư sau khi trừ
    return None
    
def simple_embed(title: str, description: str, color: discord.Color = discord.Color.blue()):
    """
    Hàm tạo embed đơn giản để dùng lại nhiều lần
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed
    
def update_daily(user_id):
    """Cập nhật thời gian daily"""
    user_id = str(user_id)
    now = datetime.datetime.now()
    daily_data[user_id] = {
        "last_claimed": now.isoformat(),
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M:%S")
    }
    save_json(daily_data, DAILY_FILE)

def update_work(user_id):
    """Cập nhật số lần work"""
    user_id = str(user_id)
    today = datetime.datetime.now().date()
    
    if user_id not in work_data:
        work_data[user_id] = {"count": 0, "last_date": today.isoformat()}
    
    # Nếu khác ngày thì reset
    if datetime.datetime.fromisoformat(work_data[user_id]["last_date"]).date() != today:
        work_data[user_id]["count"] = 0
        work_data[user_id]["last_date"] = today.isoformat()
    
    work_data[user_id]["count"] += 1
    work_data[user_id]["last_work"] = datetime.datetime.now().isoformat()
    work_data[user_id]["date"] = datetime.datetime.now().strftime("%d/%m/%Y")
    work_data[user_id]["time"] = datetime.datetime.now().strftime("%H:%M:%S")
    save_json(work_data, WORK_FILE)
        
# Cấu hình bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=['!', '?', '.', '/'], intents=intents)

# URLs
ICON_URL = "https://i.imgur.com/TWW22k4.jpeg"
FOOTER_ICON_URL = "https://i.imgur.com/TWW22k4.jpeg"
BANNER_URL = ""

# Thiết lập múi giờ UTC+7
UTC7 = pytz.timezone('Asia/Bangkok')  # Bangkok là UTC+7

# GUILD ID bị cấm sử dụng spam và ghostping
RESTRICTED_GUILD_ID = 1409783780217983029

def is_user_allowed(user_id):
    """Kiểm tra xem user có được phép sử dụng lệnh đặc biệt không"""
    return user_id in ALLOWED_USERS

def is_user_banned(user_id):
    """Kiểm tra xem user có bị cấm sử dụng bot không"""
    return user_id in BANNED_USERS

def get_banned_users_table():
    """Hiển thị danh sách user bị ban (mobile-friendly)"""
    if not BANNED_USERS:
        return (
            "```\n📋 Danh sách người dùng bị cấm:\n"
            "--------------------------------\n"
            "Không có người dùng nào bị cấm\n"
            "--------------------------------\n```"
        )
    
    table = "```\n📋 Danh sách người dùng bị cấm:\n"
    table += "-" * 23 + "\n"
    for user_id, ban_info in BANNED_USERS.items():
        # Phòng khi ban_info không đủ key
        reason = ban_info.get("reason", "Không rõ")
        banned_by = ban_info.get("banned_by", "Không rõ")
        banned_at = ban_info.get("banned_at", "Không rõ")

        table += f"👤 User ID : {user_id}\n"
        table += f"📝 Lý do   : {reason}\n"
        table += f"🛡️ Bởi    : {banned_by}\n"
        table += f"⏰ Thời gian: {banned_at}\n"
        table += "-" * 23 + "\n"
    table += f"Tổng số: {len(BANNED_USERS)} user bị cấm\n```"
    return table

def get_allowed_users_table():
    """Đọc trực tiếp từ whitelist.json và trả về bảng user (mobile-friendly)."""
    if not os.path.exists(WHITELIST_FILE):
        return "⚠️ Hiện chưa có user nào trong whitelist."

    try:
        with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return f"⚠️ Lỗi khi đọc whitelist.json: {e}"

    if not data:
        return "⚠️ Hiện chưa có user nào trong whitelist."

    table = "```\nDanh sách user whitelist:\n"
    table += "-" * 31 + "\n"
    for user_id, user_name in data.items():
        table += f"Tên: {user_name}\n"
        table += f"ID : {user_id}\n"
        table += "-" * 31 + "\n"
    table += f"Tổng số: {len(data)} user được cấp quyền admin\n```"
    return table

def setup_logging():
    """Tạo thư mục logs nếu chưa tồn tại"""
    if not os.path.exists('Logs'):
        os.makedirs('Logs')

def add_taixiu_history(user_id, dice, total, result, win, amount):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    status = "win" if win else "lose"
    dice_str = f"{dice[0]},{dice[1]},{dice[2]}={total},{result.capitalize()}"

    record = {
        "time": now,
        "result": f"{status},{dice_str}",
        "amount": amount
    }

    user_id = str(user_id)
    if user_id not in taixiu_history:
        taixiu_history[user_id] = []
    taixiu_history[user_id].insert(0, record)
    taixiu_history[user_id] = taixiu_history[user_id][:5]
    save_json(taixiu_history, TAIXIU_HISTORY_FILE)
    
def get_utc7_time():
    """Lấy thời gian hiện tại theo UTC+7"""
    now = datetime.datetime.now(UTC7)
    return now
    
# Thêm vào đầu file (sau setup_logging / get_utc7_time)
def log(message: str):
    """Hàm log đơn giản — in console và ghi file hàng ngày."""
    now = get_utc7_time()
    timestamp = now.strftime("[%H:%M:%S | %d/%m/%Y]")
    log_message = f"{timestamp} {message}"
    try:
        print(log_message)
        log_filename = now.strftime("Logs/command_log_%d-%m-%Y.txt")
        with open(log_filename, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    except Exception as e:
        # Không ném lỗi từ hàm log để tránh phá flow chính
        print(f"[LOG ERROR] {e}")

def log_command(user, command_name, guild_name, command_type="Text Command"):
    """Ghi log vào file và console"""
    # Lấy thời gian hiện tại theo UTC+7
    now = get_utc7_time()
    timestamp = now.strftime("[%H:%M:%S | %d/%m/%Y]")
    
    # Format log message
    log_message = f"{timestamp} {user}: {command_name} ({guild_name}) [{command_type}]"
    
    # Ghi vào console
    print(log_message)
    
    # Ghi vào file (theo ngày)
    log_filename = now.strftime("Logs/command_log_%d-%m-%Y.txt")
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(log_message + '\n')
    
    return log_message

async def send_dm_notification(user, command_name, guild_name, command_type):
    """Gửi thông báo đến DM dạng Embed cho tất cả user được phép"""
    current_time = get_utc7_time()
    time_str = current_time.strftime("%H:%M:%S %d/%m/%Y")
    
    for user_id in ALLOWED_USERS.keys():
        try:
            user_obj = await bot.fetch_user(user_id)
            
            embed = discord.Embed(
                title="Lonely Hub Notification",
                color=discord.Color.blue(),
                timestamp=current_time
            )
            
            # Set author với icon
            embed.set_author(
                name="Lonely Hub Command Log",
                icon_url=ICON_URL
            )
            
            # Thêm các field theo format yêu cầu
            embed.add_field(
                name="[🤖] Command:",
                value=f"```{command_name}```",
                inline=False
            )
            
            embed.add_field(
                name="[👤] User:",
                value=f"```{user}```",
                inline=True
            )
            
            embed.add_field(
                name="[🏠] Server:",
                value=f"```{guild_name}```",
                inline=True
            )
            
            embed.add_field(
                name="[📝] Type:",
                value=f"```{command_type}```",
                inline=True
            )
            
            embed.add_field(
                name="[🕐] Command Run Time:",
                value=f"```{time_str} (UTC+7)```",
                inline=False
            )
            
            # Set footer với icon
            embed.set_footer(
                text=f"Lonely Hub | {time_str}",
                icon_url=FOOTER_ICON_URL
            )
            
            # Set thumbnail
            embed.set_thumbnail(url=ICON_URL)
            
            await user_obj.send(embed=embed)
            
        except Exception as e:
            print(f"Không thể gửi DM cho user {user_id}: {e}")

@bot.event
async def on_ready():
    # Load dữ liệu whitelist và blacklist từ file
    load_whitelist()
    load_banned_users()
    
    # In ra trạng thái bot
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} {Fore.GREEN}{bot.user}{Style.RESET_ALL} đã kết nối thành công!")
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Múi giờ: {Fore.YELLOW}UTC+7{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Đã load {Fore.BLUE}{len(ALLOWED_USERS)}{Style.RESET_ALL} user whitelist")
    print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Đã load {Fore.RED}{len(BANNED_USERS)}{Style.RESET_ALL} user bị cấm")
    
    try:
        synced = await bot.tree.sync()
        print(f"{Fore.CYAN}[Info]{Style.RESET_ALL} Đã đồng bộ {Fore.YELLOW}{len(synced)}{Style.RESET_ALL} slash command(s)")
        print("=" * 31 + "Console" + "=" * 29)
    except Exception as e:
        print(f"{Fore.RED}[Error]Lỗi đồng bộ slash commands: {Fore.YELLOW}{e}{Style.RESET_ALL}")
    
# ==================== CÁC LỆNH MỚI: BAN/UNBAN/WHITELIST ====================

# Slash Command - Bancmd: Cấm người dùng sử dụng bot
@bot.tree.command(name="bancmd", description="Cấm người dùng sử dụng bot")
@app_commands.describe(user_id="ID của người dùng cần cấm", reason="Lý do cấm")
async def bancmd(interaction: discord.Interaction, user_id: str, reason: str):
    if not is_user_allowed(interaction.user.id):
        await interaction.response.send_message(
            embed=discord.Embed(title="❌ Lỗi", description="Bạn không có quyền!", color=discord.Color.red()),
            ephemeral=True
        )
        return

    try:
        target_user_id = int(user_id)
        if target_user_id == interaction.user.id:
            await interaction.response.send_message(
                embed=discord.Embed(title="❌ Lỗi", description="Không thể tự cấm chính mình!", color=discord.Color.red()),
                ephemeral=True
            )
            return

        if target_user_id in ALLOWED_USERS:
            await interaction.response.send_message(
                embed=discord.Embed(title="❌ Lỗi", description="Không thể cấm admin khác!", color=discord.Color.red()),
                ephemeral=True
            )
            return

        if is_user_banned(target_user_id):
            await interaction.response.send_message(
                embed=discord.Embed(title="❌ Lỗi", description="User đã bị cấm trước đó!", color=discord.Color.red()),
                ephemeral=True
            )
            return

        # thêm vào danh sách cấm
        current_time = get_utc7_time().strftime("%H:%M:%S %d/%m/%Y")
        BANNED_USERS[target_user_id] = {
            "reason": reason,
            "banned_by": f"{interaction.user}",
            "banned_at": current_time
        }
        save_banned_users()  # 🔥 Lưu lại

        # trả lời ngay
        await interaction.response.send_message(
            embed=discord.Embed(
                title="✅ Đã cấm",
                description=f"Đã cấm user `{user_id}`.\n**Lý do:** {reason}",
                color=discord.Color.green()
            ),
            ephemeral=True
        )

        # log + dm sau khi đã trả lời
        user = f"{interaction.user}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/bancmd userid:{user_id} reason:{reason}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/bancmd userid:{user_id} reason:{reason}", guild_name, "Slash Command")

    except ValueError:
        await interaction.response.send_message(
            embed=discord.Embed(title="❌ Lỗi", description="User ID không hợp lệ!", color=discord.Color.red()),
            ephemeral=True
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Lỗi không xác định",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

@bot.tree.command(name="taixiu", description="Chơi Tài Xỉu")
@app_commands.describe(select="Chọn Tài hoặc Xỉu", amount="Số coin bạn muốn cược")
@app_commands.choices(select=[
    app_commands.Choice(name="Tài", value="tai"),
    app_commands.Choice(name="Xỉu", value="xiu")
])
async def taixiu(interaction: discord.Interaction, select: app_commands.Choice[str], amount: int):
    # Kiểm tra bị cấm
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    user_id = str(interaction.user.id)
    bal = get_balance(user_id)
    if bal < amount:
        await interaction.response.send_message(
            embed=simple_embed("❌ Không đủ coin", f"Bạn chỉ có {bal} coin", discord.Color.red()),
            ephemeral=True
        )
        return
        
    # Tung xúc xắc
    dice = [random.randint(1, 6) for _ in range(3)]
    total = sum(dice)
    result = "tai" if 11 <= total <= 17 else "xiu"

    # ✅ Xử lý kết quả
    win = (select.value == result)
    if win:
        add_balance(user_id, amount)
        outcome_text = f"🎉 Bạn thắng {amount} coin!"
        color = discord.Color.green()
    else:
        remove_balance(user_id, amount)
        outcome_text = f"💀 Bạn thua {amount} coin!"
        color = discord.Color.red()

    # 🔥 Lưu lịch sử
    add_taixiu_history(
        interaction.user.id,
        dice, total, result,
        win, amount
    )

    # Embed kết quả
    new_bal = get_balance(user_id)
    e = discord.Embed(title="🎲 Kết Quả Tài Xỉu", color=color)
    e.add_field(name="Xúc xắc", value=f"🎲 {dice[0]} • 🎲 {dice[1]} • 🎲 {dice[2]}", inline=False)
    e.add_field(name="Tổng", value=f"{total} → {result.upper()}", inline=False)
    e.add_field(name="Kết quả", value=outcome_text, inline=False)
    e.set_footer(text=f"Số dư: {new_bal} coin")
    e.set_author(name=str(interaction.user), icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=e)
    
    # LOG command
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/taixiu {select.value} {amount}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/taixiu {select.value} {amount}", guild_name, "Slash Command")
    
@bot.tree.command(name="lichsutaixiu", description="Xem 5 trận gần nhất của bạn trong Tài Xỉu")
async def lichsutaixiu(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    if user_id not in taixiu_history or len(taixiu_history[user_id]) == 0:
        await interaction.response.send_message(
            embed=simple_embed("📜 Lịch Sử Tài Xỉu", "Bạn chưa chơi ván nào!", discord.Color.orange()),
            ephemeral=True
        )
        return

    embed = discord.Embed(title="📜 Lịch Sử Tài Xỉu (5 trận gần nhất)", color=discord.Color.blue())

    for rec in taixiu_history[user_id]:
        time = rec["time"]
        status, dice_str = rec["result"].split(",", 1)
        amount = rec["amount"]

        # Tách tiếp dice
        dice_part = dice_str.split("=")[0]     # "1,3,2"
        total_part = dice_str.split("=")[1]    # "6,Xiu"
        total, result = total_part.split(",")

        # Chuyển tiếng Việt
        vn_status = "Thắng" if status == "win" else "Thua"
        vn_result = "Tài" if result.lower() == "tai" else "Xỉu"

        embed.add_field(
            name=f"⏰ {time}",
            value=f"{vn_status} {amount} coin\n🎲 {dice_part} = {total} → {vn_result}",
            inline=False
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)
    
@bot.tree.command(name="addcoin", description="(Admin) Thêm coin cho user")
async def addcoin(interaction: discord.Interaction, user_id: str, amount: int):
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # LOG command
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/addcoin {user_id} {amount}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/addcoin {user_id} {amount}", guild_name, "Slash Command")
    
    new_bal = add_balance(user_id, amount)
    await interaction.response.send_message(embed=simple_embed("✅ Đã Thêm Coin", f"Cộng {amount} coin cho {user_id}\n💰 Số dư: {new_bal}", discord.Color.green()))

@bot.tree.command(name="removecoin", description="(Admin) Trừ coin của user")
async def removecoin(interaction: discord.Interaction, user_id: str, amount: int):
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    new_bal = remove_balance(user_id, amount)
    await interaction.response.send_message(embed=simple_embed("⚠️ Đã Trừ Coin", f"Trừ {amount} coin của {user_id}\n💰 Số dư: {new_bal}", discord.Color.orange()))

    # LOG command
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/removecoin {user_id} {amount}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/removecoin {user_id} {amount}", guild_name, "Slash Command")
    
@bot.tree.command(name="setcoin", description="(Admin) Set coin cho user")
async def setcoin(interaction: discord.Interaction, user_id: str, amount: int):
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    set_balance(user_id, amount)
    await interaction.response.send_message(embed=simple_embed("🔧 Đặt Coin", f"Số dư của {user_id} = {amount} coin", discord.Color.blue()))
    
    # LOG command
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/setcoin {user_id} {amount}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/setcoin {user_id} {amount}", guild_name, "Slash Command")
    
# Slash Command - Unbancmd: Gỡ cấm người dùng
@bot.tree.command(name="unbancmd", description="Gỡ cấm người dùng sử dụng bot")
@app_commands.describe(
    user_id="ID của người dùng cần gỡ cấm",
    reason="Lý do gỡ cấm"
)
async def unbancmd(interaction: discord.Interaction, user_id: str, reason: str):
    """Slash command gỡ cấm người dùng sử dụng bot"""
    # Kiểm tra quyền admin
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    try:
        # Chuyển đổi user_id sang integer
        target_user_id = int(user_id)
        
        # Kiểm tra xem user có bị cấm không
        if not is_user_banned(target_user_id):
            embed = discord.Embed(
                title="❌ Lỗi",
                description="Người dùng này không bị cấm!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Xóa khỏi danh sách cấm + lưu file JSON
        del BANNED_USERS[target_user_id]
        save_banned_users()  # 🔥 thêm dòng này để persist sau restart
        
        # Thông báo thành công (⚡ trả lời trước)
        embed = discord.Embed(
            title="✅ Đã gỡ cấm người dùng",
            description=f"Đã gỡ cấm người dùng với ID {user_id}.\n**Lý do:** {reason}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Sau khi trả lời xong mới log + gửi DM
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/unbancmd userid:{user_id} reason:{reason}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/unbancmd userid:{user_id} reason:{reason}", guild_name, "Slash Command")
        
    except ValueError:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="User ID không hợp lệ! Vui lòng nhập ID đúng định dạng số.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Lỗi không xác định",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
# Slash Command - Bancmdlist: Hiển thị danh sách người dùng bị cấm
@bot.tree.command(name="bancmdlist", description="Hiển thị danh sách người dùng bị cấm sử dụng bot")
async def bancmdlist(interaction: discord.Interaction):
    """Slash command hiển thị danh sách người dùng bị cấm"""
    # Kiểm tra quyền admin
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    current_time = get_utc7_time()
    
    embed = discord.Embed(
        title="🔨 Danh sách người dùng bị cấm",
        description=get_banned_users_table(),
        color=discord.Color.orange(),
        timestamp=current_time
    )
    
    embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
    embed.set_footer(text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}", icon_url=FOOTER_ICON_URL)
    embed.set_thumbnail(url=ICON_URL)
    
    # ⚡ Phản hồi trước
    await interaction.response.send_message(embed=embed, ephemeral=True)

    # 📌 Log + gửi DM sau khi đã phản hồi
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/bancmdlist", guild_name, "Slash Command")
    await send_dm_notification(user, "/bancmdlist", guild_name, "Slash Command")
    
# Slash Command - Addwhitelist: Thêm người dùng vào whitelist
@bot.tree.command(name="addwhitelist", description="Thêm người dùng vào danh sách được phép sử dụng bot")
@app_commands.describe(
    user_id="ID của người dùng cần thêm",
    display_name="Tên hiển thị của người dùng"
)
async def addwhitelist(interaction: discord.Interaction, user_id: str, display_name: str):
    """Slash command thêm người dùng vào whitelist"""
    # Kiểm tra quyền admin
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    try:
        # Chuyển đổi user_id sang integer
        target_user_id = int(user_id)
        
        # Kiểm tra xem user đã có trong whitelist chưa
        if target_user_id in ALLOWED_USERS:
            embed = discord.Embed(
                title="❌ Lỗi",
                description="Người dùng này đã có trong whitelist!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # ✅ Thêm vào whitelist và lưu JSON
        ALLOWED_USERS[target_user_id] = display_name
        save_whitelist()  # 🔥 lưu lại ngay vào whitelist.json
        
        # ⚡ Phản hồi thành công trước
        embed = discord.Embed(
            title="✅ Đã thêm vào whitelist",
            description=f"Đã thêm người dùng {display_name} (ID: {user_id}) vào whitelist.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # 📌 Sau khi phản hồi mới log + DM
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/addwhitelist userid:{user_id} name:{display_name}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/addwhitelist userid:{user_id} name:{display_name}", guild_name, "Slash Command")
        
    except ValueError:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="User ID không hợp lệ! Vui lòng nhập ID đúng định dạng số.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Lỗi không xác định",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
@bot.event
async def on_message(message):
    if message.author.bot or not message.guild: 
        return await bot.process_commands(message)
    
    user_id = str(message.author.id)
    current_data = levels.get(user_id, {"xp": 0, "level": 1})
    xp = current_data["xp"] + random.randint(5, 15)
    level = current_data["level"]
    
    if xp >= level * 100:
        xp -= level * 100
        level += 1
        embed = discord.Embed(
            title="🎉 Level Up!",
            description=f"{message.author.mention} đã lên level {level}!",
            color=discord.Color.gold()
        )
        await message.channel.send(embed=embed)
    
    levels[user_id] = {"xp": xp, "level": level}
    save_json(levels, LEVEL_FILE)
    await bot.process_commands(message)

# ====== ECONOMY COMMANDS ======
@bot.command()
async def balance(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    balance_amount = get_balance(ctx.author.id)
    embed = discord.Embed(title="💳 Số dư", description=f"{ctx.author.mention}, bạn có **{balance_amount}** credits.", color=discord.Color.green())
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!balance", guild_name, "Text Command")
    await send_dm_notification(user, "!balance", guild_name, "Text Command")

@bot.tree.command(name="balance", description="Xem số dư credits của bạn")
async def balance_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    balance_amount = get_balance(interaction.user.id)
    embed = discord.Embed(title="💳 Số dư", description=f"{interaction.user.mention}, bạn có **{balance_amount}** credits.", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/balance", guild_name, "Slash Command")
    await send_dm_notification(user, "/balance", guild_name, "Slash Command")

@bot.command()
async def daily(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if not can_daily(ctx.author.id):
        user_id = str(ctx.author.id)
        last_claim = datetime.datetime.fromisoformat(daily_data[user_id]["last_claimed"])
        next_claim = last_claim + datetime.timedelta(days=1)
        wait_time = next_claim - datetime.datetime.now()
        hours = int(wait_time.total_seconds() // 3600)
        minutes = int((wait_time.total_seconds() % 3600) // 60)
        
        embed = discord.Embed(
            title="❌ Đã nhận daily hôm nay",
            description=f"Bạn có thể nhận lại sau {hours} giờ {minutes} phút\n⏰ Lần cuối: {daily_data[user_id]['time']} {daily_data[user_id]['date']}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    add_balance(ctx.author.id, 100)
    update_daily(ctx.author.id)
    
    embed = discord.Embed(
        title="🎁 Daily Reward",
        description=f"{ctx.author.mention} nhận **100 credits**\n⏰ Thời gian: {datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')}",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!daily", guild_name, "Text Command")
    await send_dm_notification(user, "!daily", guild_name, "Text Command")

@bot.tree.command(name="daily", description="Nhận 100 credits mỗi ngày")
async def daily_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if not can_daily(interaction.user.id):
        user_id = str(interaction.user.id)
        last_claim = datetime.datetime.fromisoformat(daily_data[user_id]["last_claimed"])
        next_claim = last_claim + datetime.timedelta(days=1)
        wait_time = next_claim - datetime.datetime.now()
        hours = int(wait_time.total_seconds() // 3600)
        minutes = int((wait_time.total_seconds() % 3600) // 60)
        
        embed = discord.Embed(
            title="❌ Đã nhận daily hôm nay",
            description=f"Bạn có thể nhận lại sau {hours} giờ {minutes} phút\n⏰ Lần cuối: {daily_data[user_id]['time']} {daily_data[user_id]['date']}",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    add_balance(interaction.user.id, 100)
    update_daily(interaction.user.id)
    
    embed = discord.Embed(
        title="🎁 Daily Reward",
        description=f"{interaction.user.mention} nhận **100 credits**\n⏰ Thời gian: {datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')}",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/daily", guild_name, "Slash Command")
    await send_dm_notification(user, "/daily", guild_name, "Slash Command")
    
@bot.command()
async def work(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    can_work_result, work_count = can_work(ctx.author.id)
    if not can_work_result:
        embed = discord.Embed(
            title="❌ Đã đạt giới hạn",
            description=f"Bạn đã work {work_count}/5 lần hôm nay!\n⏰ Chờ đến ngày mai để reset.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra cooldown 90 giây
    user_id = str(ctx.author.id)
    if user_id in work_data and "last_work" in work_data[user_id]:
        last_work = datetime.datetime.fromisoformat(work_data[user_id]["last_work"])
        cooldown = datetime.timedelta(seconds=90)
        if datetime.datetime.now() - last_work < cooldown:
            wait_seconds = int((cooldown - (datetime.datetime.now() - last_work)).total_seconds())
            embed = discord.Embed(
                title="⏳ Đang chờ cooldown",
                description=f"Vui lòng chờ {wait_seconds} giây nữa!",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return
    
    earn = random.randint(50, 200)
    add_balance(ctx.author.id, earn)
    update_work(ctx.author.id)
    
    embed = discord.Embed(
        title="💼 Làm việc",
        description=f"{ctx.author.mention} làm việc kiếm được **{earn}** credits\n📊 Lần work: {work_count + 1}/5\n⏰ Thời gian: {datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!work", guild_name, "Text Command")
    await send_dm_notification(user, "!work", guild_name, "Text Command")

@bot.tree.command(name="work", description="Làm việc để kiếm credits")
async def work_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    can_work_result, work_count = can_work(interaction.user.id)
    if not can_work_result:
        embed = discord.Embed(
            title="❌ Đã đạt giới hạn",
            description=f"Bạn đã work {work_count}/5 lần hôm nay!\n⏰ Chờ đến ngày mai để reset.",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Kiểm tra cooldown 90 giây
    user_id = str(interaction.user.id)
    if user_id in work_data and "last_work" in work_data[user_id]:
        last_work = datetime.datetime.fromisoformat(work_data[user_id]["last_work"])
        cooldown = datetime.timedelta(seconds=90)
        if datetime.datetime.now() - last_work < cooldown:
            wait_seconds = int((cooldown - (datetime.datetime.now() - last_work)).total_seconds())
            embed = discord.Embed(
                title="⏳ Đang chờ cooldown",
                description=f"Vui lòng chờ {wait_seconds} giây nữa!",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    
    earn = random.randint(50, 200)
    add_balance(interaction.user.id, earn)
    update_work(interaction.user.id)
    
    embed = discord.Embed(
        title="💼 Làm việc",
        description=f"{interaction.user.mention} đã làm việc và kiếm được **{earn}** credits\n📊 Lần work: {work_count + 1}/5\n⏰ Thời gian: {datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')}",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/work", guild_name, "Slash Command")
    await send_dm_notification(user, "/work", guild_name, "Slash Command")
    
@bot.command()
async def gamble(ctx, amount: int):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if amount <= 0:
        embed = discord.Embed(title="❌ Lỗi", description="Số credits phải lớn hơn 0!", color=discord.Color.red())
        return await ctx.send(embed=embed)
    
    if get_balance(ctx.author.id) < amount:
        embed = discord.Embed(title="❌ Lỗi", description="Không đủ credits!", color=discord.Color.red())
        return await ctx.send(embed=embed)
    
    if random.random() < 0.5:
        remove_balance(ctx.author.id, amount)
        embed = discord.Embed(title="💥 Thua", description=f"Thua **{amount}** credits!", color=discord.Color.red())
    else:
        add_balance(ctx.author.id, amount)
        embed = discord.Embed(title="🎉 Thắng", description=f"Thắng **{amount}** credits!", color=discord.Color.green())
    
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, f"!gamble {amount}", guild_name, "Text Command")
    await send_dm_notification(user, f"!gamble {amount}", guild_name, "Text Command")

@bot.tree.command(name="gamble", description="Cược credits (tỉ lệ thắng 50%)")
async def gamble_slash(interaction: discord.Interaction, amount: int):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if amount <= 0:
        embed = discord.Embed(title="❌ Lỗi", description="Số credits phải lớn hơn 0!", color=discord.Color.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    if get_balance(interaction.user.id) < amount:
        embed = discord.Embed(title="❌ Lỗi", description="Không đủ credits!", color=discord.Color.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    if random.random() < 0.5:
        remove_balance(interaction.user.id, amount)
        embed = discord.Embed(title="💥 Thua", description=f"Thua **{amount}** credits!", color=discord.Color.red())
    else:
        add_balance(interaction.user.id, amount)
        embed = discord.Embed(title="🎉 Thắng", description=f"Thắng **{amount}** credits!", color=discord.Color.green())
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/gamble {amount}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/gamble {amount}", guild_name, "Slash Command")

@bot.command()
async def guess(ctx, number: int):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if number < 1 or number > 10:
        embed = discord.Embed(title="❌ Lỗi", description="Chọn số từ 1 đến 10!", color=discord.Color.red())
        return await ctx.send(embed=embed)
    
    win = random.randint(1, 10)
    if number == win:
        add_balance(ctx.author.id, 200)
        embed = discord.Embed(title="🎯 Đúng!", description=f"Số đúng là {win}! Bạn nhận **200 credits**.", color=discord.Color.green())
    else:
        embed = discord.Embed(title="❌ Sai!", description=f"Số đúng là {win}. Thử lại nhé!", color=discord.Color.red())
    
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, f"!guess {number}", guild_name, "Text Command")
    await send_dm_notification(user, f"!guess {number}", guild_name, "Text Command")

@bot.tree.command(name="guess", description="Đoán số từ 1-10 để nhận 200 credits")
async def guess_slash(interaction: discord.Interaction, number: int):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if number < 1 or number > 10:
        embed = discord.Embed(title="❌ Lỗi", description="Chọn số từ 1 đến 10!", color=discord.Color.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    win = random.randint(1, 10)
    if number == win:
        add_balance(interaction.user.id, 200)
        embed = discord.Embed(title="🎯 Đúng!", description=f"Số đúng là {win}! Bạn nhận **200 credits**.", color=discord.Color.green())
    else:
        embed = discord.Embed(title="❌ Sai!", description=f"Số đúng là {win}. Thử lại nhé!", color=discord.Color.red())
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/guess {number}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/guess {number}", guild_name, "Slash Command")

@bot.command()
async def slot(ctx, amount: int):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if amount <= 0:
        embed = discord.Embed(title="❌ Lỗi", description="Số credits phải lớn hơn 0!", color=discord.Color.red())
        return await ctx.send(embed=embed)
    
    if get_balance(ctx.author.id) < amount:
        embed = discord.Embed(title="❌ Lỗi", description="Không đủ credits!", color=discord.Color.red())
        return await ctx.send(embed=embed)
    
    symbols = ["🍒", "🍋", "🍉", "⭐", "💎"]
    result = [random.choice(symbols) for _ in range(3)]
    
    embed = discord.Embed(title="🎰 Slot Machine", description=" | ".join(result), color=discord.Color.purple())
    
    if len(set(result)) == 1:
        add_balance(ctx.author.id, amount * 5)
        embed.add_field(name="🎰 JACKPOT!", value=f"Bạn nhận **{amount * 5}** credits!", inline=False)
    elif len(set(result)) == 2:
        add_balance(ctx.author.id, amount * 2)
        embed.add_field(name="🎰 Trúng nhỏ!", value=f"Bạn nhận **{amount * 2}** credits!", inline=False)
    else:
        remove_balance(ctx.author.id, amount)
        embed.add_field(name="🎰 Thua!", value=f"Mất **{amount}** credits!", inline=False)
    
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, f"!slot {amount}", guild_name, "Text Command")
    await send_dm_notification(user, f"!slot {amount}", guild_name, "Text Command")

@bot.tree.command(name="slot", description="Chơi slot machine với credits")
async def slot_slash(interaction: discord.Interaction, amount: int):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if amount <= 0:
        embed = discord.Embed(title="❌ Lỗi", description="Số credits phải lớn hơn 0!", color=discord.Color.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    if get_balance(interaction.user.id) < amount:
        embed = discord.Embed(title="❌ Lỗi", description="Không đủ credits!", color=discord.Color.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    symbols = ["🍒", "🍋", "🍉", "⭐", "💎"]
    result = [random.choice(symbols) for _ in range(3)]
    
    embed = discord.Embed(title="🎰 Slot Machine", description=" | ".join(result), color=discord.Color.purple())
    
    if len(set(result)) == 1:
        add_balance(interaction.user.id, amount * 5)
        embed.add_field(name="🎰 JACKPOT!", value=f"Bạn nhận **{amount * 5}** credits!", inline=False)
    elif len(set(result)) == 2:
        add_balance(interaction.user.id, amount * 2)
        embed.add_field(name="🎰 Trúng nhỏ!", value=f"Bạn nhận **{amount * 2}** credits!", inline=False)
    else:
        remove_balance(interaction.user.id, amount)
        embed.add_field(name="🎰 Thua!", value=f"Mất **{amount}** credits!", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/slot {amount}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/slot {amount}", guild_name, "Slash Command")

# ====== SHOP SYSTEM ======
@bot.command()
async def shop(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(title="🏪 Cửa Hàng", color=discord.Color.blue())
    
    for role_id, item in shop_data.items():
        embed.add_field(
            name=f"🛒 {item['name']} - {item['price']} credits",
            value=f"{item['description']}",
            inline=False
        )
    
    embed.set_footer(text="Sử dụng /buy để mua items")
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!shop", guild_name, "Text Command")
    await send_dm_notification(user, "!shop", guild_name, "Text Command")

@bot.tree.command(name="shop", description="Xem cửa hàng")
async def shop_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="🏪 Cửa Hàng", color=discord.Color.blue())
    
    for role_id, item in shop_data.items():
        embed.add_field(
            name=f"🛒 {item['name']} - {item['price']} credits",
            value=f"{item['description']}",
            inline=False
        )
    
    embed.set_footer(text="Sử dụng /buy để mua items")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/shop", guild_name, "Slash Command")
    await send_dm_notification(user, "/shop", guild_name, "Slash Command")

@bot.tree.command(name="buy", description="Mua item từ cửa hàng")
@app_commands.choices(item=[
    app_commands.Choice(name="VIP Role - 10000 credits", value="vip"),
    app_commands.Choice(name="Vip+ Role - 50000 credits", value="vipplus"),
    app_commands.Choice(name="Vip++ Role - 70000 credits", value="vipplusplus"),
    app_commands.Choice(name="MVP Role - 100000 credits", value="mvp"),
    app_commands.Choice(name="MVP+ Role - 150000 credits", value="mvpplus"),
    app_commands.Choice(name="MVP++ Role - 300000 credits", value="mvpplusplus"),
    app_commands.Choice(name="Manager Role - 999999999999 credits", value="managerbot")
])
async def buy_slash(interaction: discord.Interaction, item: app_commands.Choice[str]):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    item_data = shop_data.get(item.value)
    if not item_data:
        embed = discord.Embed(title="❌ Lỗi", description="Item không tồn tại!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    price = item_data['price']
    role_id = item_data['role_id']
    
    if get_balance(interaction.user.id) < price:
        embed = discord.Embed(title="❌ Không đủ credits", description=f"Bạn cần {price} credits để mua {item_data['name']}!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    role = interaction.guild.get_role(role_id)
    if not role:
        embed = discord.Embed(title="❌ Lỗi", description="Role không tồn tại trong server!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if role in interaction.user.roles:
        embed = discord.Embed(title="❌ Đã có role", description=f"Bạn đã có role {item_data['name']} rồi!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if remove_balance(interaction.user.id, price):
        await interaction.user.add_roles(role)
        embed = discord.Embed(title="✅ Mua thành công", description=f"Đã mua {item_data['name']} với {price} credits!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Không thể thực hiện giao dịch!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/buy {item.value}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/buy {item.value}", guild_name, "Slash Command")

# ====== LEVEL COMMANDS ======
@bot.command()
async def rank(ctx, member: discord.Member = None):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    member = member or ctx.author
    user_data = levels.get(str(member.id), {"xp": 0, "level": 1})
    
    embed = discord.Embed(title="🏆 Rank", color=discord.Color.purple())
    embed.add_field(name="👤 User", value=member.mention, inline=True)
    embed.add_field(name="📊 Level", value=user_data['level'], inline=True)
    embed.add_field(name="⭐ XP", value=user_data['xp'], inline=True)
    
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, f"!rank {member.name}", guild_name, "Text Command")
    await send_dm_notification(user, f"!rank {member.name}", guild_name, "Text Command")

@bot.tree.command(name="rank", description="Xem level và XP của bạn hoặc thành viên khác")
async def rank_slash(interaction: discord.Interaction, member: discord.Member = None):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    member = member or interaction.user
    user_data = levels.get(str(member.id), {"xp": 0, "level": 1})
    
    embed = discord.Embed(title="🏆 Rank", color=discord.Color.purple())
    embed.add_field(name="👤 User", value=member.mention, inline=True)
    embed.add_field(name="📊 Level", value=user_data['level'], inline=True)
    embed.add_field(name="⭐ XP", value=user_data['xp'], inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/rank", guild_name, "Slash Command")
    await send_dm_notification(user, "/rank", guild_name, "Slash Command")

@bot.command()
async def leaderboard(ctx, type: str = "credits"):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if type == "credits":
        top = sorted(credits.items(), key=lambda x: x[1], reverse=True)[:10]
        embed = discord.Embed(title="🏅 Top 10 Credits", color=discord.Color.gold())
        for i, (uid, amt) in enumerate(top, 1):
            user = ctx.guild.get_member(int(uid))
            name = user.display_name if user else f"User {uid}"
            embed.add_field(name=f"{i}. {name}", value=f"{amt} credits", inline=False)
    elif type == "level":
        top = sorted(levels.items(), key=lambda x: x[1].get("level", 1), reverse=True)[:10]
        embed = discord.Embed(title="🏅 Top 10 Levels", color=discord.Color.gold())
        for i, (uid, info) in enumerate(top, 1):
            user = ctx.guild.get_member(int(uid))
            name = user.display_name if user else f"User {uid}"
            embed.add_field(name=f"{i}. {name}", value=f"Level {info.get('level', 1)}", inline=False)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Loại leaderboard không hợp lệ! Dùng 'credits' hoặc 'level'", color=discord.Color.red())
    
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, f"!leaderboard {type}", guild_name, "Text Command")
    await send_dm_notification(user, f"!leaderboard {type}", guild_name, "Text Command")

@bot.tree.command(name="leaderboard", description="Xem bảng xếp hạng credits hoặc level")
@app_commands.describe(type="Chọn loại bảng xếp hạng")
@app_commands.choices(type=[
    app_commands.Choice(name="Credits", value="credits"),
    app_commands.Choice(name="Level", value="level")
])
async def leaderboard_slash(interaction: discord.Interaction, type: app_commands.Choice[str]):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Dùng value từ dropdown
    type = type.value  

    if type == "credits":
        top = sorted(credits.items(), key=lambda x: x[1], reverse=True)[:10]
        embed = discord.Embed(title="🏅 Top 10 Credits", color=discord.Color.gold())
        for i, (uid, amt) in enumerate(top, 1):
            try:
                user = await bot.fetch_user(int(uid))
                name = user.name
            except:
                name = f"User {uid}"
            embed.add_field(name=f"{i}. {name}", value=f"{amt} credits", inline=False)

    elif type == "level":
        top = sorted(levels.items(), key=lambda x: x[1].get("level", 1), reverse=True)[:10]
        embed = discord.Embed(title="🏅 Top 10 Levels", color=discord.Color.gold())
        for i, (uid, info) in enumerate(top, 1):
            try:
                user = await bot.fetch_user(int(uid))
                name = user.name
            except:
                name = f"User {uid}"
            embed.add_field(name=f"{i}. {name}", value=f"Level {info.get('level', 1)}", inline=False)

    else:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Loại leaderboard không hợp lệ!",
            color=discord.Color.red()
        )

    await interaction.response.send_message(embed=embed, ephemeral=False)

    # Log
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/leaderboard {type}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/leaderboard {type}", guild_name, "Slash Command")
    
# ====== UTILITY COMMANDS ======
@bot.command()
async def serverinfo(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    guild = ctx.guild
    embed = discord.Embed(title=f"🏠 Thông tin server: {guild.name}", color=0x00ff00)
    embed.add_field(name="👥 Thành viên", value=guild.member_count, inline=True)
    embed.add_field(name="👑 Chủ server", value=guild.owner.mention, inline=True)
    embed.add_field(name="📅 Tạo ngày", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!serverinfo", guild_name, "Text Command")
    await send_dm_notification(user, "!serverinfo", guild_name, "Text Command")

@bot.tree.command(name="serverinfo", description="Xem thông tin server")
async def serverinfo_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    guild = interaction.guild
    embed = discord.Embed(title=f"🏠 Thông tin server: {guild.name}", color=0x00ff00)
    embed.add_field(name="👥 Thành viên", value=guild.member_count, inline=True)
    embed.add_field(name="👑 Chủ server", value=guild.owner.mention, inline=True)
    embed.add_field(name="📅 Tạo ngày", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/serverinfo", guild_name, "Slash Command")
    await send_dm_notification(user, "/serverinfo", guild_name, "Slash Command")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 Thông tin user: {member.name}", color=0x00ff00)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📅 Tạo tài khoản", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="📅 Tham gia server", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, f"!userinfo {member.name}", guild_name, "Text Command")
    await send_dm_notification(user, f"!userinfo {member.name}", guild_name, "Text Command")

@bot.tree.command(name="userinfo", description="Xem thông tin user")
async def userinfo_slash(interaction: discord.Interaction, member: discord.Member = None):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    member = member or interaction.user
    embed = discord.Embed(title=f"👤 Thông tin user: {member.name}", color=0x00ff00)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📅 Tạo tài khoản", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="📅 Tham gia server", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/userinfo", guild_name, "Slash Command")
    await send_dm_notification(user, "/userinfo", guild_name, "Slash Command")

@bot.command()
async def premium(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(title="💎 Premium", description=f"{ctx.author.mention}, bạn đang dùng bản Free.", color=0xffd700)
    embed.add_field(name="Tính năng Premium", value="• Không giới hạn music\n• Priority support\n• Custom commands", inline=False)
    await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!premium", guild_name, "Text Command")
    await send_dm_notification(user, "!premium", guild_name, "Text Command")

@bot.tree.command(name="premium", description="Thông tin về gói Premium")
async def premium_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed = discord.Embed(title="💎 Premium", description=f"{interaction.user.mention}, bạn đang dùng bản Free.", color=0xffd700)
    embed.add_field(name="Tính năng Premium", value="• Không giới hạn music\n• Priority support\n• Custom commands", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/premium", guild_name, "Slash Command")
    await send_dm_notification(user, "/premium", guild_name, "Slash Command")

# ====== MUSIC SYSTEM ======
ytdl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_opts), data=data)

@bot.command()
async def join(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        embed = discord.Embed(title="✅ Đã kết nối", description=f"Đã kết nối đến {ctx.author.voice.channel.name}", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Bạn chưa vào voice channel.", color=discord.Color.red())
        await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!join", guild_name, "Text Command")
    await send_dm_notification(user, "!join", guild_name, "Text Command")

@bot.tree.command(name="join", description="Bot tham gia voice channel của bạn")
async def join_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if interaction.user.voice:
        await interaction.user.voice.channel.connect()
        embed = discord.Embed(title="✅ Đã kết nối", description=f"Đã kết nối đến {interaction.user.voice.channel.name}", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Bạn chưa vào voice channel.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/join", guild_name, "Slash Command")
    await send_dm_notification(user, "/join", guild_name, "Slash Command")

@bot.command()
async def leave(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        embed = discord.Embed(title="✅ Đã rời khỏi", description="Đã rời khỏi voice channel.", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Bot không ở trong voice channel.", color=discord.Color.red())
        await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!leave", guild_name, "Text Command")
    await send_dm_notification(user, "!leave", guild_name, "Text Command")

@bot.tree.command(name="leave", description="Bot rời khỏi voice channel")
async def leave_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        embed = discord.Embed(title="✅ Đã rời khỏi", description="Đã rời khỏi voice channel.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Bot không ở trong voice channel.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/leave", guild_name, "Slash Command")
    await send_dm_notification(user, "/leave", guild_name, "Slash Command")

@bot.command()
async def play(ctx, *, query: str):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            embed = discord.Embed(title="❌ Lỗi", description="Bạn chưa vào voice channel.", color=discord.Color.red())
            return await ctx.send(embed=embed)
    
    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
            ctx.voice_client.stop()
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            embed = discord.Embed(title="🎵 Đang phát", description=f"**{player.title}**", color=discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Lỗi", description=f"Lỗi khi phát nhạc: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, f"!play {query}", guild_name, "Text Command")
    await send_dm_notification(user, f"!play {query}", guild_name, "Text Command")

@bot.tree.command(name="play", description="Phát nhạc từ YouTube")
async def play_slash(interaction: discord.Interaction, query: str):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if not interaction.guild.voice_client:
        if interaction.user.voice:
            await interaction.user.voice.channel.connect()
        else:
            embed = discord.Embed(title="❌ Lỗi", description="Bạn chưa vào voice channel.", color=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    await interaction.response.defer()
    try:
        player = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
        interaction.guild.voice_client.stop()
        interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        embed = discord.Embed(title="🎵 Đang phát", description=f"**{player.title}**", color=discord.Color.green())
        await interaction.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Lỗi", description=f"Lỗi khi phát nhạc: {e}", color=discord.Color.red())
        await interaction.followup.send(embed=embed)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, f"/play {query}", guild_name, "Slash Command")
    await send_dm_notification(user, f"/play {query}", guild_name, "Slash Command")

@bot.command()
async def stop(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if ctx.voice_client:
        ctx.voice_client.stop()
        embed = discord.Embed(title="⏹️ Đã dừng", description="Đã dừng phát nhạc.", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Bot không đang phát nhạc.", color=discord.Color.red())
        await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!stop", guild_name, "Text Command")
    await send_dm_notification(user, "!stop", guild_name, "Text Command")

@bot.tree.command(name="stop", description="Dừng phát nhạc")
async def stop_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if interaction.guild.voice_client:
        interaction.guild.voice_client.stop()
        embed = discord.Embed(title="⏹️ Đã dừng", description="Đã dừng phát nhạc.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Bot không đang phát nhạc.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/stop", guild_name, "Slash Command")
    await send_dm_notification(user, "/stop", guild_name, "Slash Command")

@bot.command()
async def pause(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        embed = discord.Embed(title="⏸️ Đã tạm dừng", description="Đã tạm dừng phát nhạc.", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Không có nhạc đang phát.", color=discord.Color.red())
        await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!pause", guild_name, "Text Command")
    await send_dm_notification(user, "!pause", guild_name, "Text Command")

@bot.tree.command(name="pause", description="Tạm dừng nhạc")
async def pause_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.pause()
        embed = discord.Embed(title="⏸️ Đã tạm dừng", description="Đã tạm dừng phát nhạc.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Không có nhạc đang phát.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/pause", guild_name, "Slash Command")
    await send_dm_notification(user, "/pause", guild_name, "Slash Command")

@bot.command()
async def resume(ctx):
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        embed = discord.Embed(title="▶️ Đã tiếp tục", description="Đã tiếp tục phát nhạc.", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Nhạc không đang tạm dừng.", color=discord.Color.red())
        await ctx.send(embed=embed)
    
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_command(user, "!resume", guild_name, "Text Command")
    await send_dm_notification(user, "!resume", guild_name, "Text Command")

@bot.tree.command(name="resume", description="Tiếp tục phát nhạc")
async def resume_slash(interaction: discord.Interaction):
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(title="❌ Bị cấm", description="Bạn đã bị cấm sử dụng bot này!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
        interaction.guild.voice_client.resume()
        embed = discord.Embed(title="▶️ Đã tiếp tục", description="Đã tiếp tục phát nhạc.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="❌ Lỗi", description="Nhạc không đang tạm dừng.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/resume", guild_name, "Slash Command")
    await send_dm_notification(user, "/resume", guild_name, "Slash Command")

# Slash Command - Removewhitelist: Xóa người dùng khỏi whitelist
@bot.tree.command(name="removewhitelist", description="Xóa người dùng khỏi danh sách được phép sử dụng bot")
@app_commands.describe(
    user_id="ID của người dùng cần xóa"
)
async def removewhitelist(interaction: discord.Interaction, user_id: str):
    """Slash command xóa người dùng khỏi whitelist"""
    # Kiểm tra quyền admin
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    try:
        # Chuyển đổi user_id sang integer
        target_user_id = int(user_id)
        
        # Kiểm tra xem user có trong whitelist không
        if target_user_id not in ALLOWED_USERS:
            embed = discord.Embed(
                title="❌ Lỗi",
                description="Người dùng này không có trong whitelist!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Xóa khỏi whitelist + lưu lại JSON
        removed_user = ALLOWED_USERS.pop(target_user_id)
        save_whitelist()  # 🔥 lưu whitelist.json ngay sau khi xoá
        
        # ⚡ Trả lời thành công trước
        embed = discord.Embed(
            title="✅ Đã xóa khỏi whitelist",
            description=f"Đã xóa người dùng {removed_user} (ID: {user_id}) khỏi whitelist.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        # 📌 Sau khi phản hồi, mới log + DM
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/removewhitelist userid:{user_id}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/removewhitelist userid:{user_id}", guild_name, "Slash Command")
        
    except ValueError:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="User ID không hợp lệ! Vui lòng nhập ID đúng định dạng số.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Lỗi không xác định",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        
# Slash Command - Premium Commands (Admin only)
@bot.tree.command(name="premium_command", description="Hiển thị các lệnh premium chỉ dành cho admin")
async def premium_command(interaction: discord.Interaction):
    """Slash command hiển thị các lệnh premium"""
    # Kiểm tra quyền
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    current_time = get_utc7_time()
    embed = discord.Embed(
        title="Premium Commands",
        description="List of available premium command",
        color=0x00ffaa,
        timestamp=current_time
    )
    embed.set_author(name="Lonely Hub Bot", icon_url=ICON_URL)

    embed.add_field(
        name="**?nukeall**",
        value="Nuke the server with ping everyone\n\n**Requirements:** Bot must have permission to create, delete channels, rename servers and ping everyone",
        inline=False
    )
    embed.add_field(
        name="**?raidall**",
        value="Raid all channel with ping everyone and message.\n\n**Requirements:** Bot must have permission to ping everyone.",
        inline=False
    )
    embed.add_field(name="**?spampingall**", value="Spam ping everyone all channels", inline=False)
    embed.add_field(
        name="**?banalluser**",
        value="Ban all user with ultra-speed\n\n**Requirements:** The bot needs to have the highest role in the server.",
        inline=False
    )
    embed.add_field(
        name="**?purge [quantity]**",
        value="Xóa số lượng tin nhắn được chỉ định\n\n**Requirements:** Bot must have permission to manage messages.",
        inline=False
    )
    embed.add_field(
        name="**?purgeallwebhook**",
        value="Xóa tất cả webhook trong server\n\n**Requirements:** Bot must have permission to manage webhooks.",
        inline=False
    )

    embed.set_footer(text="Lonely Hub Bot", icon_url=FOOTER_ICON_URL)
    embed.set_thumbnail(url=ICON_URL)

    # ⚡ trả lời ngay trước (ephemeral để chỉ người gọi thấy)
    await interaction.response.send_message(embed=embed, ephemeral=True)

    # 📌 log + gửi DM chạy sau khi đã phản hồi
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/premium_command", guild_name, "Slash Command")
    await send_dm_notification(user, "/premium_command", guild_name, "Slash Command")
# Slash Command - Help
@bot.tree.command(name="help", description="Hiển thị tất cả lệnh có sẵn trong bot")
async def help_command(interaction: discord.Interaction):
    """Slash command hiển thị trợ giúp"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    current_time = get_utc7_time()
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"

    embed = discord.Embed(
        title="🤖 Lonely Hub - Hệ Thống Lệnh",
        description="Xin chào! Đây là danh sách đầy đủ các lệnh có trong bot.\n\n**📊 Thông tin bot:**\n• Prefix: `!`, `?`, `.`, `/`\n• Múi giờ: `UTC+7`\n• Phiên bản: `1.0.0`",
        color=0x00ffaa,
        timestamp=current_time
    )
    
    # Thêm các lệnh cơ bản
    embed.add_field(
        name="🔧 LỆNH CƠ BẢN",
        value=(
            "• `/ping` - Kiểm tra độ trễ của bot\n"
            "• `/info` - Xem thông tin về bot\n"
            "• `/whitelist` - Xem danh sách user được phép\n"
            "• `/help` - Hiển thị trợ giúp này\n"
            "• `/say` - Làm bot nói gì đó"
            "• `/sayv2` - Làm bot nói gì đó (No Need Invite)"
            "• `/ghostping <user_id> [delay] [quantity]` - Ghost ping người dùng\n"
            "• `/ghostpingv2 <user_id> [delay] [quantity]` - Ghost ping người dùng (No Need Invite)\n"
            "• `/dms <user_id> <message>` - Gửi tin nhắn DM đến người dùng\n"
            "• `/spam <message> <quantity> [user_id]` - Spam tin nhắn\n"
            "• `/spamv2 <message> <quantity> [user_id]` - Spam tin nhắn (No Need Invite)\n"            
            "• `/invite` - Invite Bot To The Server"
        ),
        inline=False
    )
    
    # Các lệnh admin
    admin_commands = (
        "• `/premium_command` - Xem các lệnh premium (admin only)"
        "• `/bancmd <user_id> <reason>` - Cấm user dùng lệnh"
        "• `/unbancmd <user_id> <reason>` - Gỡ cấm user dùng lệnh"
        "• `/bancmdlist` - Xem các users bị cấm dùng lệnh"
        "• `/addwhitelist <user_id> <name>` - Add Whitelist Cho Users"
        "• `/removewhitelist <user_id> <name>` - Xoá whitelist của users"
    ) 
    
    if is_user_allowed(interaction.user.id):
        embed.add_field(
            name="⚡ LỆNH ADMIN (Chỉ cho user được phép)",
            value=admin_commands,
            inline=False
        )
    else:
        embed.add_field(
            name="🔒 LỆNH ADMIN",
            value="*Bạn không có quyền sử dụng các lệnh admin*",
            inline=False
        )
    
    # Auto response
    embed.add_field(
        name="🤖 TỰ ĐỘNG PHẢN HỒI",
        value=(
            "Bot sẽ tự động phản hồi khi nhận diện các từ khóa:\n"
            "• `client`, `executor`, `executors` - Hiển thị danh sách client\n"
            "• `luật` - Hướng dẫn xem luật\n"
            "• `máy ảo`, `cách nhận máy ảo` - Hướng dẫn nhận máy ảo"
        ),
        inline=False
    )
    
    # Notes
    embed.add_field(
        name="📝 GHI CHÚ",
        value=(
            "• Các lệnh admin chỉ dành cho user được cấp quyền\n"
            "• Tất cả lệnh đều được kiểm soát, ghi log và thông báo qua DM Owner\n"
            "• Thời gian hiển thị là UTC+7 (Việt Nam)"
        ),
        inline=False
    )
    
    # Set author, thumbnail, footer
    embed.set_author(name="Lonely Hub Help System", icon_url=ICON_URL)
    embed.set_thumbnail(url=ICON_URL)
    embed.set_footer(
        text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')} | Yêu cầu bởi {user}",
        icon_url=FOOTER_ICON_URL
    )
    embed.set_image(url=BANNER_URL)
    
    # ⚡ Phản hồi trước
    await interaction.response.send_message(embed=embed, ephemeral=True)

    # 📌 Sau khi trả lời thì log + DM
    log_command(user, "/help", guild_name, "Slash Command")
    await send_dm_notification(user, "/help", guild_name, "Slash Command")
    
# Slash Command - Ping
@bot.tree.command(name="ping", description="Kiểm tra độ trễ của bot")
async def ping(interaction: discord.Interaction):
    """Slash command ping"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    latency = round(bot.latency * 1000)
    current_time = get_utc7_time()
    
    # ⚡ Phản hồi trước
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Độ trễ: **{latency}ms**\n⏰ Thời gian: **{current_time.strftime('%H:%M:%S %d/%m/%Y')}** (UTC+7)",
        color=discord.Color.green(),
        timestamp=current_time
    )
    embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
    embed.set_footer(text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}", icon_url=FOOTER_ICON_URL)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

    # 📌 Sau khi phản hồi, mới log + DM
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/ping", guild_name, "Slash Command")
    await send_dm_notification(user, "/ping", guild_name, "Slash Command")
    
# Lenh Info
@bot.tree.command(name="info", description="Xem thông tin về bot")
async def info(interaction: discord.Interaction):
    """Slash command info"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    current_time = get_utc7_time()
    
    # ⚡ Phản hồi trước
    embed = discord.Embed(
        title="🤖 Bot Information",
        description="Bot logging system với UTC+7",
        color=discord.Color.blue(),
        timestamp=current_time
    )
    embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
    embed.add_field(name="🕐 Múi giờ", value="UTC+7", inline=True)
    embed.add_field(name="📊 Số server", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="⚡ Độ trễ", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="📝 Logging", value="Text commands & Slash commands", inline=False)
    embed.add_field(name="📨 DM Notification", value=f"Gửi đến {len(ALLOWED_USERS)} user", inline=True)
    embed.add_field(name="👥 User được phép spam", value=str(len(ALLOWED_USERS)), inline=True)
    embed.set_footer(text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}", icon_url=FOOTER_ICON_URL)
    embed.set_thumbnail(url=ICON_URL)
    
    await interaction.response.send_message(embed=embed)

    # 📌 Sau khi phản hồi, mới log + DM
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/info", guild_name, "Slash Command")
    await send_dm_notification(user, "/info", guild_name, "Slash Command")
    
# Slash Command - Whitelist: Hiển thị danh sách user được phép
@bot.tree.command(name="whitelist", description="Xem danh sách user whitelist")
async def whitelist(interaction: discord.Interaction):
    """Slash command hiển thị danh sách user whitelist"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # LOG TRƯỚC KHI PHẢN HỒI
    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    guild_name = interaction.guild.name if interaction.guild else "Direct Message"
    log_command(user, "/whitelist", guild_name, "Slash Command")

    # Gửi DM thông báo với Embed
    await send_dm_notification(user, "/whitelist", guild_name, "Slash Command")

    current_time = get_utc7_time()

    # 🔥 Đọc trực tiếp whitelist từ JSON
    try:
        with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        data = {}
        print(f"[ERROR] Không thể đọc {WHITELIST_FILE}: {e}")

    if not data:
        desc = "⚠️ Hiện chưa có user nào trong whitelist."
    else:
        desc = "```\nDanh sách user whitelist:\n"
        desc += "-" * 21 + "\n"
        for uid, name in data.items():
            desc += f"Tên: {name}\n"
            desc += f"ID : {uid}\n"
            desc += "-" * 21 + "\n"
        desc += f"Tổng số: {len(data)} user được phép sử dụng lệnh premium\n```"

    embed = discord.Embed(
        title="👥 Danh sách User Whitelist",
        description=desc,
        color=discord.Color.purple(),
        timestamp=current_time
    )
    embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
    embed.set_footer(
        text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}",
        icon_url=FOOTER_ICON_URL
    )
    embed.set_thumbnail(url=ICON_URL)

    await interaction.response.send_message(embed=embed, ephemeral=True)
    
# Slash Command - Ghostping
@bot.tree.command(name="ghostping", description="Ghost ping người dùng")
@app_commands.describe(
    user_id="ID của người dùng cần ghost ping",
    delay="Thời gian delay giữa các lần ping (giây), tối thiểu 0.1",
    quantity="Số lượng ping, mặc định là 5, tối đa 50"
)
async def ghostping(interaction: discord.Interaction, user_id: str, delay: float = 0.5, quantity: int = 5):
    """Slash command ghost ping"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Kiểm tra nếu đang ở guild bị cấm
    if interaction.guild and interaction.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Phản hồi trước để tránh lỗi Unknown interaction
    await interaction.response.send_message(
        embed=discord.Embed(
            title="⏳ Đang xử lý...",
            description=f"Đang chuẩn bị ghost ping {quantity} lần với delay {delay}s...",
            color=discord.Color.orange()
        ),
        ephemeral=True
    )
    
    try:
        target_user_id = int(user_id)
        target_user = await bot.fetch_user(target_user_id)
        
        sent_count = 0
        for i in range(quantity):
            try:
                ping_message = await interaction.channel.send(f"{target_user.mention}")
                await asyncio.sleep(0.3)
                await ping_message.delete()
                sent_count += 1
                
                if i < quantity - 1:
                    await asyncio.sleep(delay)
                    
            except discord.Forbidden:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="❌ Lỗi",
                        description="Bot không có quyền xóa tin nhắn!",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
                return
            except Exception as e:
                print(f"[ERROR] Lỗi khi ghost ping: {e}")
        
        # Thông báo thành công
        await interaction.followup.send(
            embed=discord.Embed(
                title="✅ Hoàn thành",
                description=f"Đã thực hiện {sent_count}/{quantity} lần ghost ping đến {target_user.mention}",
                color=discord.Color.green()
            ),
            ephemeral=True
        )
        
        # 🔥 LOG SAU KHI HOÀN THÀNH
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/ghostping userid:{user_id} delay:{delay} quantity:{quantity}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/ghostping userid:{user_id} delay:{delay} quantity:{quantity}", guild_name, "Slash Command")
        
    except ValueError:
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Lỗi",
                description="User ID không hợp lệ!",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
    except discord.NotFound:
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Lỗi",
                description="Không tìm thấy user!",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Lỗi",
                description=f"Đã xảy ra lỗi: {str(e)}",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
       
@bot.tree.command(name="ghostpingv2", description="Ghost ping người dùng (ko cần invite)")
@app_commands.describe(
    user_id="ID của người dùng cần ghost ping",
    delay="Thời gian delay giữa các lần ping (giây), tối thiểu 0.1",
    quantity="Số lượng ping, mặc định là 5, tối đa 50"
)
async def ghostpingv2(interaction: discord.Interaction, user_id: str, delay: float = 0.5, quantity: int = 5):
    """Slash command ghost ping"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Kiểm tra nếu đang ở guild bị cấm
    if interaction.guild and interaction.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Defer để dùng followup.send
    await interaction.response.defer(ephemeral=True)
    
    try:
        target_user_id = int(user_id)
        target_user = await bot.fetch_user(target_user_id)
        
        sent_count = 0
        for i in range(quantity):
            try:
                # Gửi ping bằng followup.send
                ping_message = await interaction.followup.send(f"{target_user.mention}")
                await asyncio.sleep(0.3)
                
                # Xóa tin nhắn ping
                await ping_message.delete()
                sent_count += 1
                
                if i < quantity - 1:
                    await asyncio.sleep(delay)
                    
            except discord.Forbidden:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="❌ Lỗi",
                        description="Bot không có quyền xóa tin nhắn!",
                        color=discord.Color.red()
                    ),
                    ephemeral=True
                )
                return
            except Exception as e:
                print(f"[ERROR] Lỗi khi ghost ping: {e}")
        
        # Thông báo thành công
        await interaction.followup.send(
            embed=discord.Embed(
                title="✅ Hoàn thành",
                description=f"Đã thực hiện {sent_count}/{quantity} lần ghost ping đến {target_user.mention}",
                color=discord.Color.green()
            ),
            ephemeral=True
        )
        
        # 🔥 LOG SAU KHI HOÀN THÀNH
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/ghostpingv2 userid:{user_id} delay:{delay} quantity:{quantity}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/ghostpingv2 userid:{user_id} delay:{delay} quantity:{quantity}", guild_name, "Slash Command")
        
    except ValueError:
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Lỗi",
                description="User ID không hợp lệ!",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
    except discord.NotFound:
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Lỗi",
                description="Không tìm thấy user!",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Lỗi",
                description=f"Đã xảy ra lỗi: {str(e)}",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        
# Slash Command - DMS
@bot.tree.command(name="dms", description="Gửi tin nhắn DM đến người dùng")
@app_commands.describe(
    user_id="ID của người dùng cần gửi tin nhắn",
    message="Nội dung tin nhắn cần gửi"
)
async def dms(interaction: discord.Interaction, user_id: str, message: str):
    """Slash command gửi DM"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    try:
        target_user_id = int(user_id)
        target_user = await bot.fetch_user(target_user_id)

        try:
            await target_user.send(f"{message}")
            embed = discord.Embed(
                title="✅ Đã gửi tin nhắn",
                description=f"Đã gửi tin nhắn đến {target_user.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except discord.Forbidden:
            error_embed = discord.Embed(
                title="❌ Không thể gửi tin nhắn",
                description=f"Không thể gửi tin nhắn đến {target_user.mention}\n\n**Lý do:** User đã chặn DM hoặc bot không có quyền gửi tin nhắn",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

        # 🔥 LOG SAU KHI THỰC HIỆN
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/dms userid:{user_id} message:{message}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/dms userid:{user_id} message:{message}", guild_name, "Slash Command")

    except ValueError:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="User ID không hợp lệ! Vui lòng nhập ID đúng định dạng số.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    except discord.NotFound:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Không tìm thấy người dùng với ID này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Lỗi không xác định",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

# Spam V1
@bot.tree.command(name="spam", description="spam tin nhắn ở kênh (hoặc dms)")
@app_commands.describe(
    message="Nội dung tin nhắn cần gửi",
    quantity="Số lượng tin nhắn (tối đa 1000)",
    user_id="ID của người dùng cần gửi (để trống nếu gửi ở channel hiện tại)"
)
async def spam(interaction: discord.Interaction, message: str, quantity: int, user_id: str = None):
    """Slash command spam"""
    
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    # Kiểm tra guild bị hạn chế
    if interaction.guild and interaction.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # FIX: Xử lý user_id rỗng
    if user_id is not None and user_id.strip() == "":
        user_id = None
    
    # Kiểm tra giới hạn số lượng
    if quantity > 1000:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Số lượng tin nhắn tối đa là 1000!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if quantity <= 0:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Số lượng tin nhắn phải lớn hơn 0!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Phản hồi ban đầu
    embed = discord.Embed(
        title="⏳ Đang xử lý...",
        description=f"Đang gửi {quantity} tin nhắn...",
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

    try:
        sent_count = 0
        
        # Nếu có user_id, gửi tin nhắn cho user
        if user_id:
            try:
                target_user = await bot.fetch_user(int(user_id))
                for i in range(quantity):
                    try:
                        await target_user.send(f"{message}")
                        sent_count += 1
                    except Exception as e:
                        print(f"Lỗi gửi tin nhắn cho user: {e}")
                
                # LOG SAU KHI HOÀN THÀNH - GIỮ NGUYÊN NỘI DUNG NHƯ CŨ
                user = f"{interaction.user.name}#{interaction.user.discriminator}"
                guild_name = interaction.guild.name if interaction.guild else "Direct Message"
                
                # FIX: Chỉ lấy thông tin target_user.name an toàn, không dùng mention trong log
                target_display = f"userid:{user_id}"
                
                # Ghi log command - GIỮ NGUYÊN FORMAT
                log_content = f"/spam message:{message} quantity:{quantity}"
                log_message = log_command(user, log_content, guild_name, "Slash Command")
                await send_dm_notification(user, log_content, guild_name, "Slash Command")
                
                # Thông báo thành công - ở đây vẫn dùng mention vì là embed cho user
                embed = discord.Embed(
                    title="✅ Hoàn thành",
                    description=f"Đã gửi {sent_count}/{quantity} tin nhắn đến {target_user.mention}",
                    color=discord.Color.green()
                )
                await interaction.edit_original_response(embed=embed)
                
            except ValueError:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="User ID không hợp lệ!",
                    color=discord.Color.red()
                )
                await interaction.edit_original_response(embed=embed)
            except discord.NotFound:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Không tìm thấy user!",
                    color=discord.Color.red()
                )
                await interaction.edit_original_response(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Không thể gửi tin nhắn cho user này!",
                    color=discord.Color.red()
                )
                await interaction.edit_original_response(embed=embed)
        
        # Nếu không có user_id, gửi ở channel hiện tại
        else:
            for i in range(quantity):
                try:
                    await interaction.channel.send(f"{message}")
                    sent_count += 1
                    await asyncio.sleep(0.5)  # Delay 0.5 giây giữa các tin nhắn
                except Exception as e:
                    print(f"Lỗi gửi tin nhắn: {e}")
            
            # LOG SAU KHI HOÀN THÀNH - GIỮ NGUYÊN NỘI DUNG NHƯ CŨ
            user = f"{interaction.user.name}#{interaction.user.discriminator}"
            guild_name = interaction.guild.name if interaction.guild else "Direct Message"
            
            # Ghi log command - GIỮ NGUYÊN FORMAT
            log_content = f"/spam message:{message} quantity:{quantity} (sent: {sent_count}/{quantity})"
            log_message = log_command(user, log_content, guild_name, "Slash Command")
            await send_dm_notification(user, log_content, guild_name, "Slash Command")
            
            # Thông báo thành công
            embed = discord.Embed(
                title="✅ Hoàn thành",
                description=f"Đã gửi {sent_count}/{quantity} tin nhắn trong channel này",
                color=discord.Color.green()
            )
            await interaction.edit_original_response(embed=embed)
    
    except Exception as e:
        # LOG LỖI - GIỮ NGUYÊN NỘI DUNG NHƯ CŨ
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        
        # FIX: Xử lý target_display an toàn cho log lỗi
        target_display = f"userid:{user_id}" if user_id else ""
        log_content = f"/spam message:{message} quantity:{quantity} {target_display} (ERROR: {str(e)})"
        
        log_message = log_command(user, log_content, guild_name, "Slash Command")
        await send_dm_notification(user, log_content, guild_name, "Slash Command")
        
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.edit_original_response(embed=embed)
        
# Spam
class SpamButton(discord.ui.View):
    def __init__(self, message, user_id=None):
        super().__init__()
        self.message = message
        self.user_id = user_id

    @discord.ui.button(label="Spam", style=discord.ButtonStyle.red, emoji="💥")
    async def spam_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Defer để có thể dùng followup.send
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Spam qua DM nếu có user_id
            if self.user_id:
                try:
                    target_user_id = int(self.user_id)
                    target_user = await bot.fetch_user(target_user_id)
                    
                    # Spam 5 tin nhắn qua DM
                    for _ in range(5):
                        await target_user.send(f"{self.message}")
                    
                    # Thông báo thành công
                    await interaction.followup.send(
                        f"✅ Đã spam 5 tin nhắn đến {target_user.mention}",
                        ephemeral=True
                    )
                    
                except Exception as e:
                    await interaction.followup.send(
                        f"❌ Lỗi khi spam DM: {str(e)}",
                        ephemeral=True
                    )
                    return
            
            # Spam trong channel hiện tại bằng followup.send
            else:
                # Spam 5 tin nhắn trong channel
                for _ in range(5):
                    await interaction.followup.send(f"{self.message}")
                
                # Thông báo thành công
                await interaction.followup.send(
                    "✅ Đã spam 5 tin nhắn vào kênh",
                    ephemeral=True
                )

            # Log hành động
            user = f"{interaction.user.name}#{interaction.user.discriminator}"
            guild_name = interaction.guild.name if interaction.guild else "Direct Message"
            log_command(user, f"/spamv2 message:{self.message} userid:{self.user_id}", guild_name, "Slash Command")
            await send_dm_notification(user, f"/spamv2 message:{self.message} userid:{self.user_id}", guild_name, "Slash Command")

        except Exception as e:
            await interaction.followup.send(
                f"❌ Lỗi khi spam: {str(e)}",
                ephemeral=True
            )

@bot.tree.command(name="spamv2", description="Spam tin nhắn ở kênh (hoặc DMs,ko cần invite)")
@app_commands.describe(
    message="Nội dung tin nhắn cần gửi",
    user_id="ID của người dùng cần gửi (để trống nếu gửi ở channel hiện tại)"
)
async def spamv2(interaction: discord.Interaction, message: str, user_id: str = None):
    """Slash command spam - Với nút Spam cố định 5 tin nhắn"""
    # Kiểm tra user banned
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    # Kiểm tra guild bị hạn chế
    if interaction.guild and interaction.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Tạo view với nút Spam
    view = SpamButton(message, user_id)
    
    # Embed thông báo (bỏ field "Đích đến")
    embed = discord.Embed(
        title="💥 SPAM TEXT",
        description=f"**Nội dung:** {message}",
        color=discord.Color.red()
    )
    embed.add_field(name="📊 Số lượng", value="5 tin nhắn", inline=True)
    embed.add_field(name="👤 Người yêu cầu", value=interaction.user.mention, inline=True)
    
    await interaction.response.send_message(
        embed=embed,
        view=view,
        ephemeral=True
    )
    
# LỆNH /say
@bot.tree.command(name="say", description="Làm bot gửi tin nhắn")
@app_commands.describe(
    message="Nội dung tin nhắn cần gửi",
    channel="Kênh để gửi tin nhắn (để trống nếu gửi ở kênh hiện tại)"
)
async def say(interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
    """Slash command /say - Gửi tin nhắn thay mặt bot"""
    
    # Kiểm tra user bị cấm
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    # Xác định kênh đích
    target_channel = channel or interaction.channel

    try:
        # Phản hồi trước (defer để có thời gian xử lý)
        await interaction.response.defer(ephemeral=True)
        
        # Gửi tin nhắn
        await target_channel.send(message)
        
        # LOG SAU KHI PHẢN HỒI  
        user = f"{interaction.user.name}#{interaction.user.discriminator}"  
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"  
        log_message = log_command(user, f"/say message:{message}", guild_name, "Slash Command")  
        
        # Gửi DM thông báo với Embed  
        await send_dm_notification(user, f"/say message:{message}", guild_name, "Slash Command")  
        
        # Gửi embed xác nhận
        embed = discord.Embed(  
            title="✅ Tin nhắn đã được gửi",  
            description=f"Đã gửi tin nhắn đến {target_channel.mention}",  
            color=discord.Color.green()  
        )  
        await interaction.followup.send(embed=embed, ephemeral=True)
        
    except discord.Forbidden:  
        embed = discord.Embed(  
            title="❌ Lỗi",  
            description=f"Bot không có quyền gửi tin nhắn trong {target_channel.mention}!",  
            color=discord.Color.red()  
        )  
        await interaction.followup.send(embed=embed, ephemeral=True)
    except Exception as e:  
        embed = discord.Embed(  
            title="❌ Lỗi",  
            description=f"Đã xảy ra lỗi: {str(e)}",  
            color=discord.Color.red()  
        )  
        await interaction.followup.send(embed=embed, ephemeral=True)

#Say V2
@bot.tree.command(name="sayv2", description="Làm bot gửi tin nhắn vào channel hiện tại (Ko cần invite)")
@app_commands.describe(
    message="Nội dung tin nhắn cần gửi"
)
async def sayv2(interaction: discord.Interaction, message: str):
    """Slash command /say - Gửi 1 tin nhắn (dùng followup.send)"""
    
    # Kiểm tra user bị cấm
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    try:
        # Gửi tin nhắn ngay lập tức bằng followup.send (KHÔNG defer)
        await interaction.response.send_message(
            "🔄 Đang gửi tin nhắn...", 
            ephemeral=True
        )
        
        # Gửi tin nhắn thật bằng followup.send (không ephemeral)
        await interaction.followup.send(message)

        # Log hành động
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/sayv2 message:{message}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/sayv2 message:{message}", guild_name, "Slash Command")

    except Exception as e:
        await interaction.followup.send(
            f"❌ Lỗi khi gửi tin nhắn: {str(e)}",
            ephemeral=True
        )
        
@bot.tree.command(name="invite", description="Lấy link mời bot vào server")
async def invite(interaction: discord.Interaction):
    try:
        # Kiểm tra user bị cấm
        if is_user_banned(interaction.user.id):
            embed = discord.Embed(
                title="❌ Bị cấm",
                description="Bạn đã bị cấm sử dụng bot này!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # Log hành động bị cấm
            user = f"{interaction.user.name}#{interaction.user.discriminator}"
            guild_name = interaction.guild.name if interaction.guild else "Direct Message"
            log_message = log_command(user, "/invite", guild_name, "BLOCKED - Banned User")
            return

        await interaction.response.defer(ephemeral=True)

        # Tạo embed
        embed = discord.Embed(
            title="🎉 Mời bot vào server của bạn!",
            description="Nhấn vào link bên dưới để thêm bot vào server",
            color=0x00ff00
        )
        
        # Tạo invite link với các quyền cơ bản
        invite_url = discord.utils.oauth_url(
            bot.user.id,
            permissions=discord.Permissions(
                send_messages=True,
                read_messages=True,
                embed_links=True,
                attach_files=True,
                read_message_history=True,
                use_application_commands=True
            )
        )
        
        embed.add_field(
            name="🔗 Link mời",
            value=f"[Invite Link(User Install)]({invite_url})\n[Invite Bot To Server](https://discord.com/oauth2/authorize?client_id=1410958593041104957&permissions=8&integration_type=0&scope=bot+applications.commands)",
            inline=False
        )
        
        embed.add_field(
            name="📋 Quyền được cấp",
            value="• Admintranistor\n• Slash commands",
            inline=False
        )
        
        if bot.user.avatar:
            embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text="Cảm ơn bạn đã sử dụng bot!")
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # LOG SAU KHI PHẢN HỒI THÀNH CÔNG
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_message = log_command(user, "/invite", guild_name, "Slash Command")

    except discord.Forbidden:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bot không có quyền gửi tin nhắn!",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Log lỗi Forbidden
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_message = log_command(user, "/invite", guild_name, "ERROR - Forbidden")
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Log lỗi tổng quát
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_message = log_command(user, f"/invite - ERROR: {str(e)}", guild_name, "ERROR - Exception")
                                                                    
# ==================== CÁC LỆNH MỚI TÍCH HỢP ====================

# Lệnh ?nukeall - Nuke server (tích hợp từ nuke.py)
@bot.command()
async def nukeall(ctx):
    """Raid server"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra quyền
    if not is_user_allowed(ctx.author.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra nếu đang ở guild bị cấm
    if ctx.guild and ctx.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # LOG TRƯỚC KHI XỬ LÝ
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_message = log_command(user, "?nukeall", guild_name, "Text Command")
    
    # Gửi DM thông báo với Embed
    await send_dm_notification(user, "?nukeall", guild_name, "Text Command")
    
    try:
        if not ctx.guild.me.guild_permissions.administrator:
            await ctx.send("Bot Has Missing Administrator Role")
            log("Bot Has Missing Administrator Role")
            return
        
        try:
            await ctx.message.delete()
            log("Deleted Command Succesfully!")
        except:
            log("Can't Delete Command")
        
        log("Starting Raid Server...")
        status_msg = await ctx.send("Starting raid...")
        await asyncio.sleep(1)
        await status_msg.delete()
        
        await raid_server(ctx.guild)
        
    except Exception as e:
        log(f"Error In Nuke Command: {e}")

async def raid_server(guild):
    """Function To Raid"""
    try:
        log(f"Starting Raid: {guild.name}")
        
        try:
            await guild.edit(name="Raidded By Lonely Hub")
            log("Rename Server Succesfuly!")
        except Exception as e:
            log(f"Error When Rename Server: {e}")
        
        log("Deleting Channel...")
        channel_count = 0
        for channel in list(guild.channels):
            try:
                await channel.delete()
                channel_count += 1
            except Exception as e:
                log(f"Error When Delete Channel: {channel.name}: {e}")
        log(f"Deleted {channel_count} Channel Succesfuly")
        
        log("Creating Channel and send messages...")
        message_content = """@everyone
# Your Server Got Raided By Lonely Hub
# Join Server And Dms Owner To Invite Bot
# Invite: https://discord.gg/2anc7nHw6b"""
        
        msg_count = 0
        channel_create_tasks = []
        
        for i in range(100):
            channel_create_tasks.append(guild.create_text_channel(f"⊹‧₊˚꒰💀꒱・ʀᴀɪᴅᴅᴇᴅ ʙʏ ʟᴏɴᴇʟʏ ʜᴜʙ"))
        
        new_channels = await asyncio.gather(*channel_create_tasks, return_exceptions=True)
        
        successful_channels = []
        for i, channel in enumerate(new_channels):
            if isinstance(channel, discord.TextChannel):
                successful_channels.append(channel)
                log(f"Channel Created {i+1}")
            else:
                log(f"Error When Create Channel {i+1}: {channel}")
        
        log(f"Created {len(successful_channels)} channel Succesfuly")
        
        message_tasks = []
        for channel in successful_channels:
            for i in range(50):
                message_tasks.append(channel.send(message_content))
        
        message_results = await asyncio.gather(*message_tasks, return_exceptions=True)
        
        for result in message_results:
            if not isinstance(result, Exception):
                msg_count += 1
        
        log(f"Succesfully Send {msg_count} Messages")
        log("Raid Completed!")
        
    except Exception as e:
        log(f"Raid Error:: {e}")

# Lệnh ?raidall - Spam tất cả kênh với tin nhắn
@bot.command()
async def raidall(ctx):
    """Spam tất cả kênh với tin nhắn"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra quyền
    if not is_user_allowed(ctx.author.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra nếu đang ở guild bị cấm
    if ctx.guild and ctx.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # LOG TRƯỚC KHI XỬ LÝ
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_message = log_command(user, "?raidall", guild_name, "Text Command")
    
    # Gửi DM thông báo với Embed
    await send_dm_notification(user, "?raidall", guild_name, "Text Command")
    
    try:
        message_content = """# Your Server Got Raided By Lonely Hub
# Join Server And Dms Owner To Invite Bot
# Invite: https://discord.gg/2anc7nHw6b"""
        
        msg_count = 0
        status_msg = await ctx.send("Starting raid all channels...")
        
        # Gửi tin nhắn đến tất cả các kênh
        for channel in ctx.guild.text_channels:
            try:
                if channel.permissions_for(ctx.guild.me).send_messages:
                    await channel.send(message_content)
                    msg_count += 1
                    await asyncio.sleep(0)  # Không delay
            except Exception as e:
                print(f"Lỗi gửi tin nhắn đến {channel.name}: {e}")
        
        await status_msg.delete()
        
        # Thông báo thành công
        embed = discord.Embed(
            title="✅ Hoàn thành",
            description=f"Đã gửi {msg_count} tin nhắn đến tất cả kênh",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# Lệnh ?spampingall - Spam ping everyone tất cả kênh
@bot.command()
async def spampingall(ctx):
    """Spam ping everyone tất cả kênh"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra quyền
    if not is_user_allowed(ctx.author.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra nếu đang ở guild bị cấm
    if ctx.guild and ctx.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # LOG TRƯỚC KHI XỬ LÝ
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_message = log_command(user, "?spampingall", guild_name, "Text Command")
    
    # Gửi DM thông báo với Embed
    await send_dm_notification(user, "?spampingall", guild_name, "Text Command")
    
    try:
        message_content = "@everyone"
        
        msg_count = 0
        status_msg = await ctx.send("Starting spam ping all channels...")
        
        # Gửi tin nhắn đến tất cả các kênh
        for channel in ctx.guild.text_channels:
            try:
                if channel.permissions_for(ctx.guild.me).send_messages and channel.permissions_for(ctx.guild.me).mention_everyone:
                    await channel.send(message_content)
                    msg_count += 1
                    await asyncio.sleep(0)  # Không delay
            except Exception as e:
                print(f"Lỗi gửi tin nhắn đến {channel.name}: {e}")
        
        await status_msg.delete()
        
        # Thông báo thành công
        embed = discord.Embed(
            title="✅ Hoàn thành",
            description=f"Đã gửi {msg_count} tin nhắn ping đến tất cả kênh",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# Lệnh ?banalluser - Ban tất cả user trong server
@bot.command()
async def banalluser(ctx):
    """Ban tất cả user trong server"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra quyền
    if not is_user_allowed(ctx.author.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra nếu đang ở guild bị cấm
    if ctx.guild and ctx.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # LOG TRƯỚC KHI XỬ LÝ
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_message = log_command(user, "?banalluser", guild_name, "Text Command")
    
    # Gửi DM thông báo với Embed
    await send_dm_notification(user, "?banalluser", guild_name, "Text Command")
    
    try:
        if not ctx.guild.me.guild_permissions.ban_members:
            embed = discord.Embed(
                title="❌ Lỗi",
                description="Bot không có quyền ban members!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        status_msg = await ctx.send("Starting ban all users...")
        banned_count = 0
        
        # Ban tất cả user
        for member in ctx.guild.members:
            try:
                if member != ctx.guild.me and member != ctx.author:
                    await member.ban(reason="Raided by Lonely Hub")
                    banned_count += 1
                    await asyncio.sleep(0)  # Không delay
            except Exception as e:
                print(f"Lỗi ban user {member.name}: {e}")
        
        await status_msg.delete()
        
        # Thông báo thành công
        embed = discord.Embed(
            title="✅ Hoàn thành",
            description=f"Đã ban {banned_count} user",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# Lệnh ?purge - Xóa tin nhắn
@bot.command()
async def purge(ctx, quantity: int):
    """Xóa số lượng tin nhắn được chỉ định"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra quyền
    if not is_user_allowed(ctx.author.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra nếu đang ở guild bị cấm
    if ctx.guild and ctx.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # LOG TRƯỚC KHI XỬ LÝ
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_message = log_command(user, f"?purge {quantity}", guild_name, "Text Command")
    
    # Gửi DM thông báo với Embed
    await send_dm_notification(user, f"?purge {quantity}", guild_name, "Text Command")
    
    try:
        if not ctx.guild.me.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ Lỗi",
                description="Bot không có quyền quản lý tin nhắn!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if quantity <= 0:
            embed = discord.Embed(
                title="❌ Lỗi",
                description="Số lượng tin nhắn phải lớn hơn 0!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Xóa tin nhắn
        deleted = await ctx.channel.purge(limit=quantity + 1)  # +1 để xóa cả tin nhắn lệnh
        
        # Thông báo thành công
        embed = discord.Embed(
            title="✅ Hoàn thành",
            description=f"Đã xóa {len(deleted) - 1} tin nhắn",
            color=discord.Color.green()
        )
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await msg.delete()
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# Lệnh ?purgeallwebhook - Xóa tất cả webhook
@bot.command()
async def purgeallwebhook(ctx):
    """Xóa tất cả webhook trong server"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(ctx.author.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra quyền
    if not is_user_allowed(ctx.author.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Kiểm tra nếu đang ở guild bị cấm
    if ctx.guild and ctx.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # LOG TRƯỚC KHI XỬ LÝ
    user = f"{ctx.author.name}#{ctx.author.discriminator}"
    guild_name = ctx.guild.name if ctx.guild else "Direct Message"
    log_message = log_command(user, "?purgeallwebhook", guild_name, "Text Command")
    
    # Gửi DM thông báo với Embed
    await send_dm_notification(user, "?purgeallwebhook", guild_name, "Text Command")
    
    try:
        if not ctx.guild.me.guild_permissions.manage_webhooks:
            embed = discord.Embed(
                title="❌ Lỗi",
                description="Bot không có quyền quản lý webhooks!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        status_msg = await ctx.send("Deleting all webhooks...")
        deleted_count = 0
        
        # Xóa tất cả webhook
        for channel in ctx.guild.text_channels:
            try:
                webhooks = await channel.webhooks()
                for webhook in webhooks:
                    await webhook.delete()
                    deleted_count += 1
            except Exception as e:
                print(f"Lỗi xóa webhook trong {channel.name}: {e}")
        
        await status_msg.delete()
        
        # Thông báo thành công
        embed = discord.Embed(
            title="✅ Hoàn thành",
            description=f"Đã xóa {deleted_count} webhook",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

# ==================== TEXT COMMAND HANDLER ====================

@bot.event
async def on_message(message):
    # Bỏ qua tin nhắn từ bot
    if message.author == bot.user:
        return
    
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(message.author.id):
        # Chỉ phản hồi nếu là lệnh
        if message.content.startswith(('!', '?', '.')):
            embed = discord.Embed(
                title="❌ Bị cấm",
                description="Bạn đã bị cấm sử dụng bot này!",
                color=discord.Color.red()
            )
            await message.reply(embed=embed, mention_author=False)
        return
    
    # Xử lý các lệnh text command
    if message.content.startswith(('!', '?', '.')):
        # Tách lệnh và tham số
        content = message.content[1:]  # Bỏ ký tự prefix đầu tiên
        parts = content.split()
        command = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        
        # LOG TRƯỚC KHI XỬ LÝ
        user = f"{message.author.name}#{message.author.discriminator}"
        guild_name = message.guild.name if message.guild else "Direct Message"
        log_message = log_command(user, message.content, guild_name, "Text Command")
        
        # Gửi DM thông báo với Embed
        await send_dm_notification(user, message.content, guild_name, "Text Command")
        
        # Xử lý các lệnh text command
        if command == "ping":
            latency = round(bot.latency * 1000)
            current_time = get_utc7_time()
            
            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"Độ trễ: **{latency}ms**\n⏰ Thời gian: **{current_time.strftime('%H:%M:%S %d/%m/%Y')}** (UTC+7)",
                color=discord.Color.green(),
                timestamp=current_time
            )
            embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
            embed.set_footer(text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}", icon_url=FOOTER_ICON_URL)
            
            await message.reply(embed=embed, mention_author=False)
        
        elif command == "help":
            current_time = get_utc7_time()
            
            embed = discord.Embed(
                title="🤖 Lonely Hub - Hệ Thống Lệnh",
                description="Xin chào! Đây là danh sách đầy đủ các lệnh có trong bot.\n\n**📊 Thông tin bot:**\n• Prefix: `!`, `?`, `.`, `/`\n• Múi giờ: `UTC+7`\n• Phiên bản: `1.0.0`",
                color=0x00ffaa,
                timestamp=current_time
            )
            
            # Thêm các lệnh thông thường
            embed.add_field(
                name="🔧 LỆNH CƠ BẢN",
                value=(
                    "• `/ping` - Kiểm tra độ trễ của bot\n"
                    "• `/info` - Xem thông tin về bot\n"
                    "• `/whitelist` - Xem danh sách user được phép\n"
                    "• `/help` - Hiển thị trợ giúp này\n"
                    "• `/say` - Làm bot nói gì đó\n"
                    "• `/sayv2` - Làm bot nói gì đó (No Need Invite)\n"
                    "• `/ghostping <user_id> [delay] [quantity]` - Ghost ping người dùng\n"
                    "• `/ghostpingv2 <user_id> [delay] [quantity]` - Ghost ping người dùng (No Need Invite)\n"
                    "• `/dms <user_id> <message>` - Gửi tin nhắn DM đến người dùng\n"
                    "• `/spam <message> <quantity> [user_id]` - Spam tin nhắn\n"
                    "• `/spamv2 <message> <quantity> [user_id]` - Spam tin nhắn (No Need Invite)\n"            
                    "• `/invite` - Invite Bot To The Server"
                ),
                inline=False
            )
            
            # Thêm các lệnh đặc biệt (chỉ cho admin)
            if is_user_allowed(message.author.id):
                embed.add_field(
                    name="⚡ LỆNH ADMIN (Chỉ cho user được phép)",
                    value=(
                        "• `/premium_command` - Xem các lệnh premium (admin only)\n"
                        "• `/bancmd <user_id> <reason>` - Cấm user dùng lệnh\n"
                        "• `/unbancmd <user_id> <reason>` - Gỡ cấm user dùng lệnh\n"
                        "• `/bancmdlist` - Xem các users bị cấm dùng lệnh\n"
                        "• `/addwhitelist <user_id> <name>` - Add Whitelist Cho Users\n"
                        "• `/removewhitelist <user_id> <name>` - Xoá whitelist của users"
                    ),
                    inline=False
                )
            else:
                embed.add_field(
                    name="🔒 LỆNH ADMIN",
                    value="*Bạn không có quyền sử dụng các lệnh admin*",
                    inline=False
                )
            
            # Thêm thông tin về auto response
            embed.add_field(
                name="🤖 TỰ ĐỘNG PHẢN HỒI",
                value=(
                    "Bot sẽ tự động phản hồi khi nhận diện các từ khóa:\n"
                    "• `client`, `executor`, `executors` - Hiển thị danh sách client\n"
                    "• `luật` - Hướng dẫn xem luật\n"
                    "• `máy ảo`, `cách nhận máy ảo` - Hướng dẫn nhận máy ảo"
                ),
                inline=False
            )
            
            # Thêm thông tin footer
            embed.add_field(
                name="📝 GHI CHÚ",
                value=(
                    "• Các lệnh admin chỉ dành cho user được cấp quyền\n"
                    "• Tất cả lệnh đều được kiểm soát, ghi log và thông báo qua DM Owner\n"
                    "• Thời gian hiển thị là UTC+7 (Việt Nam)"
                ),
                inline=False
            )
            
            # Set author, thumbnail, footer
            embed.set_author(name="Lonely Hub Help System", icon_url=ICON_URL)
            embed.set_thumbnail(url=ICON_URL)
            embed.set_footer(
                text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')} | Yêu cầu bởi {user}",
                icon_url=FOOTER_ICON_URL
            )
            
            await message.reply(embed=embed, mention_author=False)
        
        elif command == "info":
            current_time = get_utc7_time()
            
            embed = discord.Embed(
                title="🤖 Bot Information",
                description="Bot logging system với UTC+7",
                color=discord.Color.blue(),
                timestamp=current_time
            )
            
            embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
            embed.add_field(name="🕐 Múi giờ", value="UTC+7", inline=True)
            embed.add_field(name="📊 Số server", value=str(len(bot.guilds)), inline=True)
            embed.add_field(name="⚡ Độ trễ", value=f"{round(bot.latency * 1000)}ms", inline=True)
            embed.add_field(name="📝 Logging", value="Text commands & Slash commands", inline=False)
            embed.add_field(name="📨 DM Notification", value=f"Gửi đến {len(ALLOWED_USERS)} user", inline=True)
            embed.add_field(name="👥 User được phép spam", value=str(len(ALLOWED_USERS)), inline=True)
            embed.set_footer(text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}", icon_url=FOOTER_ICON_URL)
            embed.set_thumbnail(url=ICON_URL)
            
            await message.reply(embed=embed, mention_author=False)
        
        elif command == "time":
            current_time = get_utc7_time()
            
            embed = discord.Embed(
                title="🕐 Thời gian hiện tại",
                description=f"**UTC+7 (Việt Nam)**\n```{current_time.strftime('%H:%M:%S %d/%m/%Y')}```",
                color=discord.Color.gold(),
                timestamp=current_time
            )
            
            embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
            embed.set_footer(text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}", icon_url=FOOTER_ICON_URL)
            embed.set_thumbnail(url=ICON_URL)
            
            await message.reply(embed=embed, mention_author=False)
        
        elif command == "users":
            current_time = get_utc7_time()
            
            embed = discord.Embed(
                title="👥 Danh sách User được phép",
                description=get_allowed_users_table(),
                color=discord.Color.purple(),
                timestamp=current_time
            )
            
            embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
            embed.set_footer(text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}", icon_url=FOOTER_ICON_URL)
            embed.set_thumbnail(url=ICON_URL)
            
            await message.reply(embed=embed, mention_author=False)
        
        elif command == "premium_command":
            # Kiểm tra quyền
            if not is_user_allowed(message.author.id):
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bạn không có quyền sử dụng lệnh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
                
            current_time = get_utc7_time()
            
            embed = discord.Embed(
                title="Premium Commands",
                description="List of available premium command",
                color=0x00ffaa,
                timestamp=current_time
            )
            
            # Set author với icon
            embed.set_author(
                name="Lonely Hub Bot",
                icon_url=ICON_URL
            )
            
            # Thêm các lệnh premium
            embed.add_field(
                name="**?nukeall**",
                value=(
                    "Nuke the server with ping everyone\n\n"
                    "**Requirements:** Bot must have permission to create, delete channels, rename servers and ping everyone"
                ),
                inline=False
            )
            
            embed.add_field(
                name="**?raidall**",
                value=(
                    "Raid all channel with ping everyone and message.\n\n"
                    "**Requirements:** Bot must have permission to ping everyone."
                ),
                inline=False
            )
            
            embed.add_field(
                name="**?spampingall**",
                value="Spam ping everyone all channels",
                inline=False
            )
            
            embed.add_field(
                name="**?banalluser**",
                value=(
                    "Ban all user with ultra-speed\n\n"
                    "**Requirements:** The bot needs to have the highest role in the server."
                ),
                inline=False
            )
            
            embed.add_field(
                name="**?purge [quantity]**",
                value=(
                    "Xóa số lượng tin nhắn được chỉ định\n\n"
                    "**Requirements:** Bot must have permission to manage messages."
                ),
                inline=False
            )
            
            embed.add_field(
                name="**?purgeallwebhook**",
                value=(
                    "Xóa tất cả webhook trong server\n\n"
                    "**Requirements:** Bot must have permission to manage webhooks."
                ),
                inline=False
            )
            
            # Set footer với icon
            embed.set_footer(
                text="Lonely Hub Bot",
                icon_url=FOOTER_ICON_URL
            )
            
            # Set thumbnail
            embed.set_thumbnail(url=ICON_URL)
            
            await message.reply(embed=embed, mention_author=False)
        
        elif command == "ghostping":
            # Kiểm tra quyền
            if not is_user_allowed(message.author.id):
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bạn không có quyền sử dụng lệnh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra nếu đang ở guild bị cấm
            if message.guild and message.guild.id == RESTRICTED_GUILD_ID:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Lệnh này không được phép sử dụng trong server này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra tham số
            if len(args) < 1:
                embed = discord.Embed(
                    title="❌ Thiếu tham số",
                    description="Cú pháp: `!ghostping <user_id> [delay] [quantity]`",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            user_id = args[0]
            delay = 0.5
            quantity = 5
            
            # Xử lý tham số tùy chọn
            if len(args) >= 2:
                try:
                    delay = float(args[1])
                except ValueError:
                    embed = discord.Embed(
                        title="❌ Lỗi",
                        description="Delay phải là số!",
                        color=discord.Color.red()
                    )
                    await message.reply(embed=embed, mention_author=False)
                    return
            
            if len(args) >= 3:
                try:
                    quantity = int(args[2])
                except ValueError:
                    embed = discord.Embed(
                        title="❌ Lỗi",
                        description="Quantity phải là số nguyên!",
                        color=discord.Color.red()
                    )
                    await message.reply(embed=embed, mention_author=False)
                    return
            
            # Kiểm tra giới hạn delay
            if delay < 0.1:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Delay tối thiểu là 0.1 giây!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra giới hạn số lượng
            if quantity > 50:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Số lượng ping tối đa là 50!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            if quantity <= 0:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Số lượng ping phải lớn hơn 0!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Phản hồi ban đầu
            embed = discord.Embed(
                title="⏳ Đang xử lý...",
                description=f"Đang chuẩn bị ghost ping {quantity} lần với delay {delay}s...",
                color=discord.Color.orange()
            )
            processing_msg = await message.reply(embed=embed, mention_author=False)
            
            try:
                # Chuyển đổi user_id sang integer
                target_user_id = int(user_id)
                
                # Lấy thông tin user
                target_user = await bot.fetch_user(target_user_id)
                
                # Thực hiện ghost ping
                sent_count = 0
                for i in range(quantity):
                    try:
                        # Gửi tin nhắn ping
                        ping_message = await message.channel.send(f"{target_user.mention}")
                        await asyncio.sleep(0.5)  # Đợi 0.5 giây
                        
                        # Xóa tin nhắn
                        await ping_message.delete()
                        sent_count += 1
                        
                        # Đợi delay (trừ đi 0.5 giây đã đợi)
                        remaining_delay = max(0, delay - 0.5)
                        if i < quantity - 1 and remaining_delay > 0:  # Không đợi sau lần ping cuối
                            await asyncio.sleep(remaining_delay)
                            
                    except discord.Forbidden:
                        embed = discord.Embed(
                            title="❌ Lỗi",
                            description="Bot không có quyền xóa tin nhắn!",
                            color=discord.Color.red()
                        )
                        await processing_msg.edit(embed=embed)
                        return
                    except Exception as e:
                        print(f"Lỗi khi ghost ping: {e}")
                
                # Thông báo thành công
                embed = discord.Embed(
                    title="✅ Hoàn thành",
                    description=f"Đã thực hiện {sent_count}/{quantity} lần ghost ping đến {target_user.mention}",
                    color=discord.Color.green()
                )
                await processing_msg.edit(embed=embed)
                
            except ValueError:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="User ID không hợp lệ!",
                    color=discord.Color.red()
                )
                await processing_msg.edit(embed=embed)
            except discord.NotFound:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Không tìm thấy user!",
                    color=discord.Color.red()
                )
                await processing_msg.edit(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description=f"Đã xảy ra lỗi: {str(e)}",
                    color=discord.Color.red()
                )
                await processing_msg.edit(embed=embed)
        
        elif command == "dms":
            # Kiểm tra quyền
            if not is_user_allowed(message.author.id):
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bạn không có quyền sử dụng lệnh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra tham số
            if len(args) < 2:
                embed = discord.Embed(
                    title="❌ Thiếu tham số",
                    description="Cú pháp: `!dms <user_id> <message>`",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            user_id = args[0]
            dm_message = " ".join(args[1:])
            
            try:
                # Chuyển đổi user_id sang integer
                target_user_id = int(user_id)
                
                # Lấy thông tin user
                target_user = await bot.fetch_user(target_user_id)
                
                # Thử gửi tin nhắn
                try:
                    await target_user.send(f"{dm_message}")
                    
                    # Thông báo thành công
                    embed = discord.Embed(
                        title="✅ Đã gửi tin nhắn",
                        description=f"Đã gửi tin nhắn đến {target_user.mention}",
                        color=discord.Color.green()
                        )
                    await message.reply(embed=embed, mention_author=False)
                    
                except discord.Forbidden:
                    # Nếu không gửi được, gửi thông báo lỗi cho người dùng
                    error_embed = discord.Embed(
                        title="❌ Không thể gửi tin nhắn",
                        description=f"Không thể gửi tin nhắn đến {target_user.mention}\n\n**Lý do:** User đã chặn DM hoặc bot không có quyền gửi tin nhắn",
                        color=discord.Color.red()
                    )
                    await message.reply(embed=error_embed, mention_author=False)
                    
                except Exception as e:
                    # Xử lý các lỗi khác
                    error_embed = discord.Embed(
                        title="❌ Lỗi khi gửi tin nhắn",
                        description=f"Đã xảy ra lỗi: {str(e)}",
                        color=discord.Color.red()
                    )
                    await message.reply(embed=error_embed, mention_author=False)
                    
            except ValueError:
                # User ID không hợp lệ
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="User ID không hợp lệ! Vui lòng nhập ID đúng định dạng số.",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                
            except discord.NotFound:
                # Không tìm thấy user
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Không tìm thấy người dùng với ID này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                
            except Exception as e:
                # Lỗi khác
                error_embed = discord.Embed(
                    title="❌ Lỗi không xác định",
                    description=f"Đã xảy ra lỗi: {str(e)}",
                    color=discord.Color.red()
                )
                await message.reply(embed=error_embed, mention_author=False)
        
        elif command == "spam":
            # Kiểm tra quyền sử dụng lệnh
            if not is_user_allowed(message.author.id):
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bạn không có quyền sử dụng lệnh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra nếu đang ở guild bị cấm
            if message.guild and message.guild.id == RESTRICTED_GUILD_ID:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Lệnh này không được phép sử dụng trong server này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra tham số
            if len(args) < 2:
                embed = discord.Embed(
                    title="❌ Thiếu tham số",
                    description="Cú pháp: `!spam <message> <quantity> [user_id]`",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            spam_message = args[0]
            
            try:
                quantity = int(args[1])
            except ValueError:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Quantity phải là số nguyên!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            user_id = args[2] if len(args) >= 3 else None
            
            # Kiểm tra giới hạn số lượng
            if quantity > 1000:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Số lượng tin nhắn tối đa là 1000!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            if quantity <= 0:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Số lượng tin nhắn phải lớn hơn 0!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Phản hồi ban đầu
            embed = discord.Embed(
                title="⏳ Đang xử lý...",
                description=f"Đang gửi {quantity} tin nhắn...",
                color=discord.Color.orange()
            )
            processing_msg = await message.reply(embed=embed, mention_author=False)
            
            try:
                sent_count = 0
                
                # Nếu có user_id, gửi tin nhắn cho user
                if user_id:
                    try:
                        target_user = await bot.fetch_user(int(user_id))
                        for i in range(quantity):
                            try:
                                await target_user.send(f"{spam_message}")
                                sent_count += 1
                                await asyncio.sleep(0.5)  # Delay 0.5 giây giữa các tin nhắn
                            except Exception as e:
                                print(f"Lỗi gửi tin nhắn cho user: {e}")
                        
                        # Thông báo thành công
                        embed = discord.Embed(
                            title="✅ Hoàn thành",
                            description=f"Đã gửi {quantity} tin nhắn đến {target_user.mention}",
                            color=discord.Color.green()
                        )
                        await processing_msg.edit(embed=embed)
                        
                    except ValueError:
                        embed = discord.Embed(
                            title="❌ Lỗi",
                            description="User ID không hợp lệ!",
                            color=discord.Color.red()
                        )
                        await processing_msg.edit(embed=embed)
                    except discord.NotFound:
                        embed = discord.Embed(
                            title="❌ Lỗi",
                            description="Không tìm thấy user!",
                            color=discord.Color.red()
                        )
                        await processing_msg.edit(embed=embed)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            title="❌ Lỗi",
                            description="Không thể gửi tin nhắn cho user này!",
                            color=discord.Color.red()
                        )
                        await processing_msg.edit(embed=embed)
                
                # Nếu không có user_id, gửi ở channel hiện tại
                else:
                    for i in range(quantity):
                        try:
                            await message.channel.send(f"{spam_message}")
                            sent_count += 1
                            await asyncio.sleep(0.5)  # Delay 0.5 giây giữa các tin nhắn
                        except Exception as e:
                            print(f"Lỗi gửi tin nhắn: {e}")
                    
                    # Thông báo thành công
                    embed = discord.Embed(
                        title="✅ Hoàn thành",
                        description=f"Đã gửi {quantity} tin nhắn vào kênh",
                        color=discord.Color.green()
                    )
                    await processing_msg.edit(embed=embed)
                    
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description=f"Đã xảy ra lỗi: {str(e)}",
                    color=discord.Color.red()
                )
                await processing_msg.edit(embed=embed)
        
        elif command == "say":
            # Kiểm tra quyền
            if not is_user_allowed(message.author.id):
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bạn không có quyền sử dụng lệnh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra tham số
            if len(args) < 1:
                embed = discord.Embed(
                    title="❌ Thiếu tham số",
                    description="Cú pháp: `!say <message>`",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            say_message = " ".join(args)
            
            try:
                # Gửi tin nhắn
                await message.channel.send(say_message)
                
                # Xóa tin nhắn lệnh của user
                try:
                    await message.delete()
                except:
                    pass  # Không xóa được cũng không sao
                
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bot không có quyền gửi tin nhắn trong kênh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description=f"Đã xảy ra lỗi: {str(e)}",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)

        # Xử lý lệnh ?bancmd
        elif command == "bancmd":
            # Kiểm tra quyền admin
            if not is_user_allowed(message.author.id):
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bạn không có quyền sử dụng lệnh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra tham số
            if len(args) < 2:
                embed = discord.Embed(
                    title="❌ Thiếu tham số",
                    description="Cú pháp: `!bancmd <user_id> <reason>`",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            user_id = args[0]
            reason = " ".join(args[1:])
            
            try:
                # Chuyển đổi user_id sang integer
                target_user_id = int(user_id)
                
                # Kiểm tra xem có tự cấm chính mình không
                if target_user_id == message.author.id:
                    embed = discord.Embed(
                        title="❌ Lỗi",
                        description="Bạn không thể tự cấm chính mình!",
                        color=discord.Color.red()
                    )
                    await message.reply(embed=embed, mention_author=False)
                    return
                
                # Kiểm tra xem có cấm admin khác không
                if target_user_id in ALLOWED_USERS:
                    embed = discord.Embed(
                        title="❌ Lỗi",
                        description="Bạn không thể cấm một admin khác!",
                        color=discord.Color.red()
                    )
                    await message.reply(embed=embed, mention_author=False)
                    return
                
                # Kiểm tra xem user đã bị cấm chưa
                if is_user_banned(target_user_id):
                    embed = discord.Embed(
                        title="❌ Lỗi",
                        description="Người dùng này đã bị cấm trước đó!",
                        color=discord.Color.red()
                    )
                    await message.reply(embed=embed, mention_author=False)
                    return
                
                # Lấy thời gian hiện tại
                current_time = get_utc7_time()
                time_str = current_time.strftime("%H:%M:%S %d/%m/%Y")
                
                # Thêm vào danh sách cấm
                BANNED_USERS[target_user_id] = {
                    "reason": reason,
                    "banned_by": f"{message.author.name}#{message.author.discriminator}",
                    "banned_at": time_str
                }
                
                # LOG
                user = f"{message.author.name}#{message.author.discriminator}"
                guild_name = message.guild.name if message.guild else "Direct Message"
                log_message = log_command(user, f"?bancmd userid:{user_id} reason:{reason}", guild_name, "Text Command")
                
                # Gửi DM thông báo với Embed
                await send_dm_notification(user, f"?bancmd userid:{user_id} reason:{reason}", guild_name, "Text Command")
                
                # Thông báo thành công
                embed = discord.Embed(
                    title="✅ Đã cấm người dùng",
                    description=f"Đã cấm người dùng với ID {user_id} sử dụng bot.\n**Lý do:** {reason}",
                    color=discord.Color.green()
                )
                await message.reply(embed=embed, mention_author=False)
                
            except ValueError:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="User ID không hợp lệ! Vui lòng nhập ID đúng định dạng số.",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Lỗi không xác định",
                    description=f"Đã xảy ra lỗi: {str(e)}",
                    color=discord.Color.red()
                )
                await message.reply(embed=error_embed, mention_author=False)

        # Xử lý lệnh ?unbancmd
        elif command == "unbancmd":
            # Kiểm tra quyền admin
            if not is_user_allowed(message.author.id):
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bạn không có quyền sử dụng lệnh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # Kiểm tra tham số
            if len(args) < 2:
                embed = discord.Embed(
                    title="❌ Thiếu tham số",
                    description="Cú pháp: `!unbancmd <user_id> <reason>`",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            user_id = args[0]
            reason = " ".join(args[1:])
            
            try:
                # Chuyển đổi user_id sang integer
                target_user_id = int(user_id)
                
                # Kiểm tra xem user có bị cấm không
                if not is_user_banned(target_user_id):
                    embed = discord.Embed(
                        title="❌ Lỗi",
                        description="Người dùng này không bị cấm!",
                        color=discord.Color.red()
                    )
                    await message.reply(embed=embed, mention_author=False)
                    return
                
                # Xóa khỏi danh sách cấm
                del BANNED_USERS[target_user_id]
                
                # LOG
                user = f"{message.author.name}#{message.author.discriminator}"
                guild_name = message.guild.name if message.guild else "Direct Message"
                log_message = log_command(user, f"?unbancmd userid:{user_id} reason:{reason}", guild_name, "Text Command")
                
                # Gửi DM thông báo với Embed
                await send_dm_notification(user, f"?unbancmd userid:{user_id} reason:{reason}", guild_name, "Text Command")
                
                # Thông báo thành công
                embed = discord.Embed(
                    title="✅ Đã gỡ cấm người dùng",
                    description=f"Đã gỡ cấm người dùng với ID {user_id}.\n**Lý do:** {reason}",
                    color=discord.Color.green()
                )
                await message.reply(embed=embed, mention_author=False)
                
            except ValueError:
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="User ID không hợp lệ! Vui lòng nhập ID đúng định dạng số.",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Lỗi không xác định",
                    description=f"Đã xảy ra lỗi: {str(e)}",
                    color=discord.Color.red()
                )
                await message.reply(embed=error_embed, mention_author=False)

        # Xử lý lệnh ?bancmdlist
        elif command == "bancmdlist":
            # Kiểm tra quyền admin
            if not is_user_allowed(message.author.id):
                embed = discord.Embed(
                    title="❌ Lỗi",
                    description="Bạn không có quyền sử dụng lệnh này!",
                    color=discord.Color.red()
                )
                await message.reply(embed=embed, mention_author=False)
                return
            
            # LOG
            user = f"{message.author.name}#{message.author.discriminator}"
            guild_name = message.guild.name if message.guild else "Direct Message"
            log_message = log_command(user, "?bancmdlist", guild_name, "Text Command")
            
            # Gửi DM thông báo với Embed
            await send_dm_notification(user, "?bancmdlist", guild_name, "Text Command")
            
            current_time = get_utc7_time()
            
            embed = discord.Embed(
                title="🔨 Danh sách người dùng bị cấm",
                description=get_banned_users_table(),
                color=discord.Color.orange(),
                timestamp=current_time
            )
            
            embed.set_author(name="Lonely Hub", icon_url=ICON_URL)
            embed.set_footer(text=f"Lonely Hub | {current_time.strftime('%H:%M:%S %d/%m/%Y')}", icon_url=FOOTER_ICON_URL)
            embed.set_thumbnail(url=ICON_URL)
            
            await message.reply(embed=embed, mention_author=False)
        
        else:
            # Lệnh không xác định
            embed = discord.Embed(
                title="❌ Lệnh không tồn tại",
                description="Sử dụng `!help` để xem danh sách lệnh",
                color=discord.Color.red()
            )
            await message.reply(embed=embed, mention_author=False)
    
    # Xử lý auto response
    elif any(keyword in message.content.lower() for keyword in ["client", "executor", "executors"]):
        embed = discord.Embed(
            title="🤖 Danh sách Client",
            description=(
                "> # Android\n"
                "• [Delta X](https://deltaexploits.gg/delta-executor-android)\n"
                "• [Code X](https://codex.lol/android)\n"
                "• [Arceus X Global](https://spdmteam.com/index?os=android)\n"
                "• [Arceus X VNG](https://spdmteam.com/index?os=android_vng)\n"
                "• [Krnl](https://krnl.cat/downloads)\n"
                "• [Ronix VNG](https://ronixstudios.com/#/download?platform=vietnam)\n"
                "• [Ronix](https://ronixstudios.com/#/download?platform=android)\n"
                "> # IOS\n"
                "• [Delta X](https://deltaexploits.gg/delta-executor-ios)\n"
                "• [Krnl](https://krnl.cat/downloads)\n"
                "• [Arceus X](https://spdmteam.com/index?os=ios)\n"
                "• [Code X](https://codex.lol/ios)\n"
                "> # Mac OS\n"
                "• [Ronix](https://ronixstudios.com/#/download?platform=macos)\n"
                "> # Windows\n"
                "• [Volcano](https://volcano.wtf)\n"
                "• [Velocity](https://discord.gg/velocityide)\n"
                "• [Swift](https://getswift.vip)\n"
                "Các client vng như delta thì sẽ cập nhật sau tại kênh client nhé!"
            ),
            color=discord.Color.blue()
        )
        await message.reply(embed=embed, mention_author=False)
    
    elif "luật" in message.content.lower():
        embed = discord.Embed(
            title="⚖️ Luật Server",
            description=(
                "**Để xem luật server, vui lòng:**\n"
                "1. Vào kênh <#1409785046075965460>\n"
                "2. Đọc kỹ các điều khoản và quy định\n"
                "3. Tuân thủ luật để tránh bị ban\n\n"
                "**📌 Lưu ý quan trọng:**\n"
                "• Không spam, flood chat\n"
                "• Không gây war, toxic\n"
                "• Tôn trọng lẫn nhau và admin"
                "• Không quảng cáo shop,server khác khi chưa được phép"
            ),
            color=discord.Color.gold()
        )
        await message.reply(embed=embed, mention_author=False)
    
    elif any(keyword in message.content.lower() for keyword in ["máy ảo", "cách nhận máy ảo"]):
        embed = discord.Embed(
            title="🖥️ Nhận Máy Ảo",
            description=(
                "**Để nhận máy ảo, vui lòng:**\n"
                "1. Vào kênh <#1409792064438403154>\n"
                "Có 2 bot để bạn nhận máy ảo là hanami và king\n\n"
                "Hanami thì bạn nhập lệnh `/gethcoin` vượt link nhận coin rồi thì nhập lệnh "
                "`/getredfinger` hoặc máy ảo mà bạn muốn nhận\n\n"
                "King thì bạn nhập `/nhiemvu` hoặc `!nv` vượt link nhận điểm r nhận máy ảo thôi "
                "bạn có thể nhập `/account` để xem King còn lại bao nhiêu máy ảo\n"
                "3. Enjoy:)\n\n"
                "**📋 Yêu cầu:**\n"
                "• Không lạm dụng bot\n"
                "• Đã đọc và đồng ý với luật server\n"
                "• Chỉ dùng bot tại kênh bot\n\n"
            ),
            color=discord.Color.green()
        )
        await message.reply(embed=embed, mention_author=False)
    
    # Tiếp tục xử lý các lệnh khác
    await bot.process_commands(message)

# Chạy bot (THÊM TOKEN CỦA BẠN VÀO ĐÂY)
if __name__ == "__main__":
    # Lấy token từ biến môi trường
    token = os.getenv("DISCORD_BOT_TOKEN")  # nếu không có, sẽ yêu cầu input

    if not token:
        token = input(Fore.CYAN + "[Info]" + Fore.WHITE + " Vui lòng nhập token bot Discord: " + Style.RESET_ALL).strip()

    try:
        print(Fore.CYAN + "[Info]" + Fore.WHITE + " Đang khởi động bot..." + Style.RESET_ALL)
        bot.run(token)
    except Exception as e:
        print(Fore.RED + f"[Error] Lỗi khi khởi động bot: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "[Debug] Vui lòng kiểm tra lại token và thử lại." + Style.RESET_ALL)