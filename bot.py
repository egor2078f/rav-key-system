import telebot
from telebot import types
import random
import string
import json
import os
from datetime import datetime, timedelta

# ТВОЙ ТОКЕН БОТА (УЖЕ ВСТАВЛЕН!)
TOKEN = "7905298437:AAHCk2FQbFIgDd0NldpnSC_M8fFRogOSUI4"
bot = telebot.TeleBot(TOKEN)

# ТВОЙ ADMIN ID (УЖЕ ВСТАВЛЕН!)
ADMIN_ID = 7405747844

# Database files
USERS_DB = "users_db.json"
KEYS_DB = "keys_db.json"

def init_db():
    if not os.path.exists(USERS_DB):
        with open(USERS_DB, 'w', encoding='utf-8') as f:
            json.dump({}, f)
    
    if not os.path.exists(KEYS_DB):
        with open(KEYS_DB, 'w', encoding='utf-8') as f:
            json.dump({}, f)

def load_users():
    try:
        with open(USERS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_DB, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_keys():
    try:
        with open(KEYS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_keys(keys):
    with open(KEYS_DB, 'w', encoding='utf-8') as f:
        json.dump(keys, f, ensure_ascii=False, indent=2)

def generate_key_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(4))

def generate_key(days=1):
    code = generate_key_code()
    return f"RAV-{days}DAY-{code}"

def can_get_key(user_id):
    users = load_users()
    user_id_str = str(user_id)
    
    if user_id_str not in users:
        return True
    
    last_key_time = users[user_id_str].get('last_key_time')
    if not last_key_time:
        return True
    
    last_time = datetime.fromisoformat(last_key_time)
    time_passed = datetime.now() - last_time
    
    return time_passed.total_seconds() >= 86400

def get_time_until_next_key(user_id):
    users = load_users()
    user_id_str = str(user_id)
    
    if user_id_str not in users or not users[user_id_str].get('last_key_time'):
        return None
    
    last_time = datetime.fromisoformat(users[user_id_str]['last_key_time'])
    next_time = last_time + timedelta(days=1)
    time_left = next_time - datetime.now()
    
    if time_left.total_seconds() <= 0:
        return None
    
    hours = int(time_left.total_seconds() // 3600)
    minutes = int((time_left.total_seconds() % 3600) // 60)
    
    return f"{hours}h {minutes}m"

def create_main_menu(is_admin=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🔑 Get Key")
    btn2 = types.KeyboardButton("👤 Profile")
    
    markup.add(btn1, btn2)
    
    if is_admin:
        btn_admin = types.KeyboardButton("👑 Admin Panel")
        markup.add(btn_admin)
    
    return markup

def create_admin_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("👥 Users", callback_data="admin_users")
    btn2 = types.InlineKeyboardButton("🔑 Keys", callback_data="admin_keys")
    btn3 = types.InlineKeyboardButton("📊 Stats", callback_data="admin_stats")
    btn4 = types.InlineKeyboardButton("🗑️ Clear DB", callback_data="admin_clear")
    btn5 = types.InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
    btn6 = types.InlineKeyboardButton("« Back", callback_data="admin_back")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    markup.add(btn6)
    
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    users = load_users()
    
    if user_id not in users:
        users[user_id] = {
            'username': message.from_user.username or 'Unknown',
            'first_name': message.from_user.first_name or 'User',
            'registered': datetime.now().isoformat(),
            'last_key_time': None,
            'keys_received': 0,
            'current_key': None
        }
        save_users(users)
    
    is_admin = message.from_user.id == ADMIN_ID
    
    text = f"✨ Welcome to RAV Key Generator, {message.from_user.first_name}!\n\n"
    text += "🔑 You can get 1 key every 24 hours.\n"
    text += "📱 Use the menu below to get started."
    
    bot.send_message(
        message.chat.id,
        text,
        reply_markup=create_main_menu(is_admin)
    )

@bot.message_handler(func=lambda message: '🔑' in message.text)
def get_key(message):
    user_id = str(message.from_user.id)
    users = load_users()
    
    if user_id not in users:
        bot.send_message(message.chat.id, "❌ Error! Use /start to register.")
        return
    
    if not can_get_key(int(user_id)):
        time_left = get_time_until_next_key(int(user_id))
        text = f"⏱️ You already got a key today!\n\n"
        text += f"⏰ Next key available in: {time_left}\n\n"
        text += f"🔑 Your current key:\n<code>{users[user_id].get('current_key', 'None')}</code>\n\n"
        text += f"💡 Tap on the key to copy it!"
        bot.send_message(message.chat.id, text, parse_mode='HTML')
        return
    
    # Generate key
    key = generate_key(1)
    
    # Save key
    keys = load_keys()
    keys[key] = {
        'user_id': user_id,
        'username': users[user_id]['username'],
        'generated': datetime.now().isoformat(),
        'expires': (datetime.now() + timedelta(days=1)).isoformat(),
        'used': False
    }
    save_keys(keys)
    
    # Update user
    users[user_id]['last_key_time'] = datetime.now().isoformat()
    users[user_id]['keys_received'] = users[user_id].get('keys_received', 0) + 1
    users[user_id]['current_key'] = key
    save_users(users)
    
    text = f"✅ Your key has been generated!\n\n"
    text += f"🔑 Key: <code>{key}</code>\n\n"
    text += f"⏰ Valid for: 1 day\n"
    text += f"⏱️ Next key in: 24 hours\n\n"
    text += f"💡 Copy the key and paste it in Roblox!\n"
    text += f"📱 Tap on the key to copy it."
    
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda message: '👤' in message.text)
def profile(message):
    user_id = str(message.from_user.id)
    users = load_users()
    
    if user_id not in users:
        bot.send_message(message.chat.id, "❌ Use /start first.")
        return
    
    user = users[user_id]
    
    time_left = get_time_until_next_key(int(user_id))
    next_key_text = time_left if time_left else "Available now ✅"
    
    current_key = user.get('current_key', 'None')
    
    text = f"<b>👤 Your Profile</b>\n\n"
    text += f"<b>📋 User Information:</b>\n"
    text += f"👤 Name: {user['first_name']}\n"
    text += f"📱 Username: @{user['username']}\n"
    text += f"🆔 ID: <code>{user_id}</code>\n\n"
    text += f"<b>🔑 Current Key:</b>\n"
    text += f"<code>{current_key}</code>\n\n"
    text += f"<b>📊 Statistics:</b>\n"
    text += f"🔑 Keys received: {user['keys_received']}\n"
    text += f"📅 Registered: {user['registered'][:10]}\n"
    text += f"⏰ Next key: {next_key_text}"
    
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(func=lambda message: '👑' in message.text)
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Access denied!")
        return
    
    users = load_users()
    keys = load_keys()
    
    text = f"<b>👑 Admin Panel</b>\n\n"
    text += f"<b>📊 Statistics:</b>\n"
    text += f"👥 Total users: {len(users)}\n"
    text += f"🔑 Total keys: {len(keys)}\n"
    text += f"✅ Active keys: {sum(1 for k in keys.values() if not k['used'])}\n\n"
    text += f"📱 Select an action:"
    
    bot.send_message(
        message.chat.id,
        text,
        parse_mode='HTML',
        reply_markup=create_admin_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.from_user.id != ADMIN_ID and call.data.startswith('admin_'):
        bot.answer_callback_query(call.id, "❌ Access denied!", show_alert=True)
        return
    
    if call.data == 'admin_users':
        users = load_users()
        
        text = f"<b>👥 Users ({len(users)})</b>\n\n"
        
        for i, (uid, data) in enumerate(list(users.items())[:15], 1):
            text += f"{i}. {data['first_name']} (@{data['username']})\n"
            text += f"   🆔 ID: <code>{uid}</code>\n"
            text += f"   🔑 Keys: {data['keys_received']}\n\n"
        
        if len(users) > 15:
            text += f"... and {len(users) - 15} more users"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=create_admin_menu()
        )
    
    elif call.data == 'admin_keys':
        keys = load_keys()
        
        text = f"<b>🔑 Keys ({len(keys)})</b>\n\n"
        text += f"✅ Active: {sum(1 for k in keys.values() if not k['used'])}\n\n"
        
        for i, (key, data) in enumerate(sorted(keys.items(), 
                                               key=lambda x: x[1]['generated'], 
                                               reverse=True)[:10], 1):
            status = "✅" if not data['used'] else "❌"
            text += f"{i}. <code>{key}</code> {status}\n"
            text += f"   👤 User: {data['user_id']}\n"
            text += f"   📅 Date: {data['generated'][:16]}\n\n"
        
        if len(keys) > 10:
            text += f"... and {len(keys) - 10} more keys"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=create_admin_menu()
        )
    
    elif call.data == 'admin_stats':
        users = load_users()
        keys = load_keys()
        
        today_keys = sum(1 for k in keys.values() 
                        if datetime.fromisoformat(k['generated']).date() == datetime.now().date())
        
        active_users = sum(1 for u in users.values() 
                          if u.get('last_key_time') and 
                          (datetime.now() - datetime.fromisoformat(u['last_key_time'])).days < 7)
        
        text = f"<b>📊 Statistics</b>\n\n"
        text += f"<b>👥 Users:</b>\n"
        text += f"Total: {len(users)}\n"
        text += f"Active (7d): {active_users}\n\n"
        text += f"<b>🔑 Keys:</b>\n"
        text += f"Total: {len(keys)}\n"
        text += f"Today: {today_keys}\n"
        text += f"Active: {sum(1 for k in keys.values() if not k['used'])}\n"
        text += f"Used: {sum(1 for k in keys.values() if k['used'])}\n\n"
        text += f"<b>💻 System:</b>\n"
        text += f"Status: Working ✅\n"
        text += f"Database: Loaded ✅"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=create_admin_menu()
        )
    
    elif call.data == 'admin_clear':
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Yes", callback_data="admin_clear_confirm"),
            types.InlineKeyboardButton("❌ Cancel", callback_data="admin_stats")
        )
        
        bot.edit_message_text(
            "⚠️ <b>WARNING!</b>\n\n"
            "Are you sure you want to clear the database?\n"
            "This action cannot be undone!",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=markup
        )
    
    elif call.data == 'admin_clear_confirm':
        save_users({})
        save_keys({})
        
        bot.answer_callback_query(call.id, "✅ Database cleared!", show_alert=True)
        
        bot.edit_message_text(
            "✅ Database successfully cleared!\n\n"
            "All users and keys have been removed.",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='HTML',
            reply_markup=create_admin_menu()
        )
    
    elif call.data == 'admin_broadcast':
        msg = bot.edit_message_text(
            "📢 Send a message to broadcast to all users:",
            call.message.chat.id,
            call.message.message_id
        )
        bot.register_next_step_handler(msg, broadcast_message)
    
    elif call.data == 'admin_back':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            "Main menu",
            reply_markup=create_main_menu(True)
        )

def broadcast_message(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    users = load_users()
    text = message.text
    
    success = 0
    failed = 0
    
    status_msg = bot.send_message(
        message.chat.id,
        f"📢 Broadcasting...\n\n👥 Users: {len(users)}"
    )
    
    for user_id in users.keys():
        try:
            bot.send_message(
                int(user_id),
                f"📢 <b>ADMIN ANNOUNCEMENT</b>\n\n{text}",
                parse_mode='HTML'
            )
            success += 1
        except:
            failed += 1
    
    bot.edit_message_text(
        f"✅ Broadcast completed!\n\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}",
        message.chat.id,
        status_msg.message_id
    )

# Инициализация
init_db()

if __name__ == '__main__':
    print("=" * 50)
    print("🔥 RAV Key Generator Bot")
    print("=" * 50)
    print("📱 Status: Running...")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print(f"🤖 Bot Token: {TOKEN[:20]}...")
    print("=" * 50)
    bot.polling(none_stop=True)
