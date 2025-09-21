# ========================================Tutorial==========================================#
#                                                                                                                                                                                                 #
#                                                               Cach cai bot tu A - Z by LongHip12                                                                    #
#                                                               B1: Tai Vscode tai https://code.visualstudio.com                                           #
#                                                               B2: Tai Python tai https://python.org                                                                 #
#                                                               B3: Tai Extension Duoi day:                                                                                 #
#                                                               Python by Microsoft,Jupyter,Path Intellisense,vscodeicon (tuy chon)         #
#                                                               B5: tai package duoi day:                                                                                    #
#                                                               pip install -U discord.py pytz art colorama flask                                                 #
#                                                               Invite: https://pastefy.app/OA5O3MX3                                                           #
#                                                                                                                                                                                             #
# ========================================Code===========================================

import discord
from discord.ext import commands
from discord import app_commands
from art import *
import datetime
import os
import asyncio
import pytz
import json
from colorama import Fore, Style, init
init(autoreset=True)
import itertools
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot đang chạy!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

# Chạy Flask song song
threading.Thread(target=run_web).start()

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
            "• `/time` - Xem giờ hiện tại UTC+7\n"
            "• `/users` - Xem danh sách user được phép\n"
            "• `/help` - Hiển thị trợ giúp này\n"
            "• `/say` - Làm bot nói gì đó"
        ),
        inline=False
    )
    
    # Các lệnh admin
    admin_commands = (
        "• `/ghostping <user_id> [delay] [quantity]` - Ghost ping người dùng\n"
        "• `/dms <user_id> <message>` - Gửi tin nhắn DM đến người dùng\n"
        "• `/spam <message> <quantity> [user_id]` - Spam tin nhắn\n"
        "• `/premium_command` - Xem các lệnh premium (admin only)"
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
    
    # Kiểm tra quyền
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
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
    
    # Kiểm tra quyền
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
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
        
# Spam
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

    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    if interaction.guild and interaction.guild.id == RESTRICTED_GUILD_ID:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Lệnh này không được phép sử dụng trong server này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    if quantity > 1000 or quantity <= 0:
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Số lượng tin nhắn phải từ 1 đến 1000!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    await interaction.response.send_message(
        embed=discord.Embed(
            title="⏳ Đang xử lý...",
            description=f"Đang gửi {quantity} tin nhắn...",
            color=discord.Color.orange()
        ),
        ephemeral=True
    )

    try:
        sent_count = 0
        if user_id:
            try:
                target_user = await bot.fetch_user(int(user_id))
                for _ in range(quantity):
                    await target_user.send(f"{message}")
                    sent_count += 1
                    await asyncio.sleep(0.5)

                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="✅ Hoàn thành",
                        description=f"Đã gửi {sent_count} tin nhắn đến {target_user.mention}",
                        color=discord.Color.green()
                    )
                )

            except Exception as e:
                await interaction.edit_original_response(
                    embed=discord.Embed(
                        title="❌ Lỗi",
                        description=f"Không thể gửi tin nhắn: {e}",
                        color=discord.Color.red()
                    )
                )

        else:
            for _ in range(quantity):
                await interaction.channel.send(f"{message}")
                sent_count += 1
                await asyncio.sleep(0.5)

            await interaction.edit_original_response(
                embed=discord.Embed(
                    title="✅ Hoàn thành",
                    description=f"Đã gửi {sent_count} tin nhắn vào kênh",
                    color=discord.Color.green()
                )
            )

        # 🔥 LOG SAU KHI HOÀN THÀNH
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/spam message:{message} quantity:{quantity} userid:{user_id}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/spam message:{message} quantity:{quantity} userid:{user_id}", guild_name, "Slash Command")

    except Exception as e:
        await interaction.edit_original_response(
            embed=discord.Embed(
                title="❌ Lỗi",
                description=f"Đã xảy ra lỗi: {str(e)}",
                color=discord.Color.red()
            )
        )
        
# LỆNH /SAY - Gửi tin nhắn thay mặt bot
@bot.tree.command(name="say", description="Làm bot gửi tin nhắn")
@app_commands.describe(
    message="Nội dung tin nhắn cần gửi",
    channel="Kênh để gửi tin nhắn (để trống nếu gửi ở kênh hiện tại)"
)
async def say(interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
    """Slash command /say - Gửi tin nhắn thay mặt bot"""
    # Kiểm tra xem user có bị cấm không
    if is_user_banned(interaction.user.id):
        embed = discord.Embed(
            title="❌ Bị cấm",
            description="Bạn đã bị cấm sử dụng bot này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Kiểm tra quyền
    if not is_user_allowed(interaction.user.id):
        embed = discord.Embed(
            title="❌ Lỗi",
            description="Bạn không có quyền sử dụng lệnh này!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Xác định kênh đích
    target_channel = channel or interaction.channel
    
    try:
        # Gửi tin nhắn
        await target_channel.send(message)
        
        # Phản hồi xác nhận
        embed = discord.Embed(
            title="✅ Tin nhắn đã được gửi",
            description=f"Đã gửi tin nhắn đến {target_channel.mention}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # 🔥 LOG SAU KHI HOÀN THÀNH
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/say message:{message}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/say message:{message}", guild_name, "Slash Command")
        
    except discord.Forbidden:
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Bot không có quyền gửi tin nhắn trong {target_channel.mention}!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # 🔥 LOG SAU KHI THẤT BẠI
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/say thất bại (không có quyền) message:{message}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/say thất bại (không có quyền) message:{message}", guild_name, "Slash Command")
        
    except Exception as e:
        embed = discord.Embed(
            title="❌ Lỗi",
            description=f"Đã xảy ra lỗi: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # 🔥 LOG SAU KHI THẤT BẠI
        user = f"{interaction.user.name}#{interaction.user.discriminator}"
        guild_name = interaction.guild.name if interaction.guild else "Direct Message"
        log_command(user, f"/say thất bại (lỗi:{str(e)}) message:{message}", guild_name, "Slash Command")
        await send_dm_notification(user, f"/say thất bại (lỗi:{str(e)}) message:{message}", guild_name, "Slash Command")
        
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
        embed = discord.Emembed(
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
                    "• `ping` - Kiểm tra độ trễ của bot\n"
                    "• `info` - Xem thông tin về bot\n"
                    "• `time` - Xem giờ hiện tại UTC+7\n"
                    "• `users` - Xem danh sách user được phép\n"
                    "• `help` - Hiển thị trợ giúp này"
                ),
                inline=False
            )
            
            # Thêm các lệnh đặc biệt (chỉ cho admin)
            if is_user_allowed(message.author.id):
                embed.add_field(
                    name="⚡ LỆNH ADMIN (Chỉ cho user được phép)",
                    value=(
                        "• `ghostping <user_id> [delay] [quantity]` - Ghost ping người dùng\n"
                        "• `dms <user_id> <message>` - Gửi tin nhắn DM đến người dùng\n"
                        "• `spam <message> <quantity> [user_id]` - Spam tin nhắn\n"
                        "• `premium_command` - Xem các lệnh premium"
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
                    "• Tất cả lệnh đều được ghi log và thông báo qua DM\n"
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
                " [Ronix](https://ronixstudios.com/#/download?platform=macos)\n"
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
