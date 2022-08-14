from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty, MessageTooLong, UserNotParticipant,ChatAdminRequired, ChannelInvalid, MediaEmpty

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, ChatPrivileges
from pyrogram import Client, filters, idle, enums

from pyromod import listen

import asyncio, sqlite3, random, jdatetime, aiocron, os, re, time

jdatetime.set_locale('fa_IR')

#Writed By Ahura - @Ahur4

#---------------------------------------------------+
API_ID = 1308503 #                                 |
API_HASH = '2a0ecd8f8118fa7569d8b008d4056c3a' #     |
#---------------------------------------------------+

app = Client(
    name="Mersad_Self",
    api_id = API_ID,
    api_hash = API_HASH
)

db = sqlite3.connect('database.sqlite')
cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS mute(
    status INT(10)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS muted(
    user_id BIGINT,
    time INT(10),
    start INT(50),
    end INT(50)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS names(
    name TEXT
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS bios(
    bio TEXT
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS enemy(
    user_id BIGINT
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS statusname(
    status INT(5)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS statusbio(
    status INT(5)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS fonttype(
    status INT(5)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS statusbold(
    status INT(5)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS statusitalic(
    status INT(5)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS statusunderline(
    status INT(5)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS statusstrik(
    status INT(5)
)
''')
cur.execute('''CREATE TABLE IF NOT EXISTS statusmention(
    status INT(5)
)
''')

cur.execute('SELECT * FROM mute')
if cur.fetchall() == []:
    cur.execute('INSERT INTO mute(status) VALUES(0)')

cur.execute('SELECT * FROM statusname')
if cur.fetchall() == []:
    cur.execute('INSERT INTO statusname(status) VALUES(0)')

cur.execute('SELECT * FROM statusbio')
if cur.fetchall() == []:
    cur.execute('INSERT INTO statusbio(status) VALUES(0)')

cur.execute('SELECT * FROM fonttype')
if cur.fetchall() == []:
    cur.execute('INSERT INTO fonttype(status) VALUES(1)')

cur.execute('SELECT * FROM statusbold')
if cur.fetchall() == []:
    cur.execute('INSERT INTO statusbold(status) VALUES(0)')

cur.execute('SELECT * FROM statusitalic')
if cur.fetchall() == []:
    cur.execute('INSERT INTO statusitalic(status) VALUES(0)')

cur.execute('SELECT * FROM statusunderline')
if cur.fetchall() == []:
    cur.execute('INSERT INTO statusunderline(status) VALUES(0)')

cur.execute('SELECT * FROM statusstrik')
if cur.fetchall() == []:
    cur.execute('INSERT INTO statusstrik(status) VALUES(0)')

cur.execute('SELECT * FROM statusmention')
if cur.fetchall() == []:
    cur.execute('INSERT INTO statusmention(status) VALUES(0)')

db.commit()

app.start()

def readenemy():
    cur.execute('SELECT * FROM enemy')
    x = cur.fetchall()
    if x == []: return []
    else:
        ahura = []
        for i in x:
            ahura.append(i[0])
        return ahura

def readmute():
    cur.execute('SELECT * FROM muted')
    x = cur.fetchall()
    if x == []: return []
    else:
        ahura = []
        for i in x:
            ahura.append(i[0])
        return ahura

@app.on_message(filters.me & ~filters.reply & (filters.regex(r'^(میوت پیوی)') | filters.regex(r'^([Mm][Uu][Tt][Ee] [Pp][Vv])')))
async def inlinemute(c:Client, m:Message):
    text = m.text
    fuck = text.split()
    check_index_2 = False
    if len(fuck) == 4: check_index_2 = True
    else: pass
    pattern = re.search(r'^([Mm][Uu][Tt][Ee] [Pp][Vv])', text).strip()
    text = text.replace('میوت پیوی','')
    try:
        text = text.replace(pattern[0],'').strip()
    except:
        pass
    if check_index_2 == True:
        text = fuck[2]
        start = time.time()
        end = start + float(int(fuck[3]) * 60)
    try: ee = start; bb = end
    except: start = time.time(); end = time.time() + 1234678852.214563
    try: text = int(text)
    except: pass
    try: req = await app.get_chat(text)
    except: return await m.edit('__**❃ کاربر یافت نشد !**__')
    cur.execute(f'SELECT * FROM muted WHERE user_id = {req.id}')
    if cur.fetchall() == []: pass
    else: return await m.edit(f'__**❃ کاربر {req.first_name} از قبل در لیست میوت وجود دارد !**__')
    query = 'INSERT INTO muted(user_id, time, start, end) VALUES(?,?,?,?)'
    x = 100000000000 if check_index_2 == False else (int(fuck[3]) * 60)
    try:
        cur.execute(query,(req.id, x, start, end))
    except sqlite3.OperationalError as e:
        os.system('sudo fuser -k database.sqlite')
        cur.execute(query,(req.id, x, start, end))
    db.commit()
    x = await m.edit(f'__❃ کاربر {req.first_name} به مدت {fuck[3]} دقیقه سکوت شد !__') if check_index_2 == True else await m.edit(f'کاربر {req.first_name} با موفقیت سکوت شد !')

@app.on_message(filters.me & ~filters.reply & (filters.regex(r'^(حذف میوت)') | filters.regex(r'^([Uu][Nn][Mm][Uu][Tt][Ee] [Pp][Vv])')))
async def inlineunmute(c:Client, m:Message):
    text = m.text
    pattern = re.search(r'^([[Uu][Nn][Mm][Uu][Tt][Ee][Pp][Vv])', text)
    text = text.replace('حذف میوت','').strip()
    try:
        text  = text.replace(pattern[0],'').strip()
    except:
        pass
    try: text = int(text)
    except: pass
    try: req = await app.get_chat(text)
    except: return await m.edit('__**❃ کاربر مورد نظر یافت نشد !**__')
    cur.execute(f'SELECT * FROM muted WHERE user_id = {req.id}')
    if cur.fetchall() == []:
        return await m.edit(f'__**❃ کاربر {req.first_name} در لیست میوت یافت نشد !**__')
    else:
        cur.execute(f'DELETE FROM muted WHERE user_id = {req.id}')
        db.commit()
        return await m.edit(f'__**❃ کاربر {req.first_name} از لیست میوت حذف شد !**__')

@app.on_message(filters.me & filters.reply & (filters.regex(r'^(میوت پیوی)') | filters.regex(r'^([Mm][Uu][Tt][Ee] [Pp][Vv])')))
async def replymute(c:Client, m:Message):
    text = m.text
    user_id = m.reply_to_message.from_user.id
    fuck = text.split()
    check_arg = False
    try:
        mameh = fuck[2]
        check_arg = True
    except: pass
    if check_arg == True:
        if len(fuck) >= 4: return await m.edit('این دستور فقط یک مقدار میگیرد !\n`سکوت پیوی (آیدی عددی)`')
        start = time.time()
        end = start + float(int(fuck[2]) * 60)
        tim = int(fuck[2]) * 60
    else: start = time.time(); end = start + 123456789.25468; tim = 10000000000

    cur.execute(f'SELECT * FROM muted WHERE user_id = {user_id}')
    ahura = cur.fetchall()
    if ahura == []: pass
    else: return await m.edit(f'__**❃ کاربر {m.reply_to_message.from_user.first_name} از قبل در لیست میوت وجود دارد !**__')
    
    query = 'INSERT INTO muted(user_id, time, start, end) VALUES(?,?,?,?)'
    try: cur.execute(query, (user_id, tim, start, end))
    except:
        os.system('fuser -k database.sqlite')
        cur.execute(query, (user_id, tim, start, end))
    db.commit()
    x = await m.edit(f'__**❃ کاربر {m.reply_to_message.from_user.first_name} به مدت {fuck[2]} دقیقه به لیست میوت اضافه شد !**__') if check_arg == True else await m.edit(f'__**❃ کاربر {m.reply_to_message.from_user.first_name} به لیست میوت اضافه شد !**__')

@app.on_message(filters.me & filters.reply & (filters.regex(r'^(حذف میوت)') | filters.regex(r'^([Uu][Nn][Mm][Uu][Tt][Ee] [Pp][Vv])')))
async def replyunmute(c:Client, m:Message):
    user_id = m.reply_to_message.from_user.id
    first_name = m.reply_to_message.from_user.first_name
    cur.execute(f'SELECT * FROM muted WHERE user_id = {user_id}')
    if cur.fetchall() != []:
        cur.execute(f'DELETE FROM Muted WHERE user_id = {user_id}')
        db.commit()
        return await m.edit(f'__**❃ کاربر {first_name} از لیست میوت حذف شد !**__')
    else: return await m.edit(f'__**❃ کاربر {first_name} در لیست میوت یافت نشد !**__')

@app.on_message(filters.me & (filters.regex(r'^(لیست میوت)$') | filters.regex(r'^([Mm][Uu][Tt][Ee][Ll][Ii][Ss][Tt])$')))
async def listmute(c:Client, m:Message):
    cur.execute('SELECT * FROM muted')
    x = cur.fetchall()
    if x == []: return await m.edit('__**❃ لیست میوت خالی میباشد !**__')
    char = ''
    for i in x:
        try:
            req = await c.get_chat(int(i[0]))
            char += f'-> [{req.first_name}](tg://openmessage?user_id={req.id}) : {req.id}\n'
            await asyncio.sleep(0.3)
        except: pass
    return await m.edit(char)

@app.on_message(filters.me & ~filters.reply & (filters.regex(r'^(افزودن بیو)') | filters.regex(r'^([Nn][Ee][Ww][Bb][Ii][Oo])')))
async def inlinebiography(c:Client, m:Message):
    text = m.text
    pattern = re.search(r'^([Nn][Ee][Ww][Bb][Ii][Oo])',text)
    text = text.replace('افزودن بیو','')
    try: text = text.replace(pattern[0],'')
    except: pass
    if 'time' not in text: return await m.edit('__**❃ لطفا محل قرار گیری زمان را در بیوی خود با قرار دادن عبارت `time` مشخص کنید !**__')
    counter = 0
    for i in text:
        counter += 1
    if counter >= 66: return await m.edit('__**❃ طول پیام بیشتر از 70 کاراکتر میباشد !**__')
    cur.execute(f'SELECT * FROM bios WHERE bio = "{text}"')
    if cur.fetchall() == []:
        query = 'INSERT INTO bios(bio) VALUES(?)'
        try: cur.execute(query, (text,))
        except:
            os.system('sudo fuser -k database.sqlite')
            cur.execute(query, (text,))
        db.commit()
        return await m.edit('__**❃ متن مورد نظر به لیست بیو اضافه شد !**__')
    else: return await m.edit('__**❃ این متن از قبل در لیست بیو وجود داشت !**__')

@app.on_message(filters.me & ~filters.reply & (filters.regex(r'^(افزودن نام)') | filters.regex(r'^([Nn][Ee][Ww][Nn][Aa][Mm][Ee])')))
async def inlinename(c:Client, m:Message):
    text = m.text
    pattern = re.search(r'^([Nn][Ee][Ww][Nn][Aa][Mm][Ee])',text)
    text = text.replace('افزودن نام','')
    try: text = text.replace(pattern[0],'')
    except: pass
    if 'time' not in text: return await m.edit('__**❃ لطفا محل قرار گیری زمان را در نام خود با قرار دادن عبارت `time` مشخص کنید !**__')
    cur.execute(f'SELECT * FROM names WHERE name = "{text}"')
    if cur.fetchall() == []:
        query = 'INSERT INTO names(name) VALUES(?)'
        try: cur.execute(query, (text,))
        except:
            os.system('sudo fuser -k database.sqlite')
            cur.execute(query, (text,))
        db.commit()
        return await m.edit('__**❃ متن مورد نظر به لیست نام اضافه شد !**__')
    else: return await m.edit('__**❃ این متن از قبل در لیست نام وجود داشت !**__')

@app.on_message(filters.me & filters.reply & (filters.regex(r'^(افزودن بیو)$') | filters.regex(r'^([Nn][Ee][Ww][Bb][Ii][Oo]$)')))
async def replybiography(c:Client, m:Message):
    text = m.reply_to_message.text
    counter = 0
    for i in text:
        counter += 1
    if counter >= 66: return await m.edit('__**❃ طول پیام بیشتر از 70 کاراکتر میباشد !**__')
    if 'time' not in text: return await m.edit('__**❃ در پیام مورد نظر محلی برای تعیین ساعت مقرر نشده بود !**__')
    cur.execute(f'SELECT * FROM bios WHERE bio = "{text}"')
    if cur.fetchall() == []:
        query = 'INSERT INTO bios(bio) VALUES(?)'
        try: cur.execute(query, (text,))
        except sqlite3.OperationalError:
            os.system('fuser -k database.sqlite')
            cur.execute(query, (text,))
        db.commit()
        return await m.edit('__**❃ متن مورد نظر برای بیوگرافی تنظیم شد !**__')
    else: return await m.edit('__**❃ متن مورد نظر از قبل در لیست بیوگرافی بود !**__')

@app.on_message(filters.me & filters.reply & (filters.regex(r'^(افزودن نام)$') | filters.regex(r'^([Nn][Ee][Ww][Nn][Aa][Mm][Ee]$)')))
async def replyname(c:Client, m:Message):
    text = m.reply_to_message.text
    if 'time' not in text: return await m.edit('__**❃ در پیام مورد نظر محلی برای تعیین ساعت مقرر نشده بود !**__')
    cur.execute(f'SELECT * FROM names WHERE name = "{text}"')
    if cur.fetchall() == []:
        query = 'INSERT INTO names(name) VALUES(?)'
        try: cur.execute(query, (text,))
        except sqlite3.OperationalError:
            os.system('fuser -k database.sqlite')
            cur.execute(query, (text,))
        db.commit()
        return await m.edit('__**❃ متن مورد نظر برای نام تنظیم شد !**__')
    else: return await m.edit('__**❃ متن مورد نظر از قبل در لیست نام بود !**__')

@app.on_message(filters.me & (filters.regex(r'^(لیست نام)$') | filters.regex(r'^([Nn][Aa][Mm][Ee][Ss]$)')))
async def nameslist(c:Client, m:Message):
    char = ''
    cur.execute('SELECT * FROM names')
    x = cur.fetchall()
    if x == []: return await m.edit('__**❃ لیست نام خالی میباشد !**__')
    else:
        counter = 0
        for i in x:
            counter += 1
            char += f'{counter} -> {i[0]}\n'
        return await m.edit(char)

@app.on_message(filters.me & (filters.regex(r'^(لیست بیو)$') | filters.regex(r'^([Bb][Ii][Oo][Ss]$)')))
async def bioslist(c:Client, m:Message):
    char = ''
    cur.execute('SELECT * FROM bios')
    x = cur.fetchall()
    if x == []: return await m.edit('__**❃ لیست بیو خالی میباشد !**__')
    else:
        counter = 0
        for i in x:
            counter += 1
            char += f'{counter} -> {i[0]}\n'
        return await m.edit(char)

@app.on_message(filters.me & filters.private & filters.reply & filters.regex(r'([جون | نت خره | صبر | چیه])'))
async def timepic(c:Client, m:Message):
    if m.reply_to_message.photo:
        photo = await m.reply_to_message.download()
        try:
            await c.send_photo('me',photo,f'__**❃ اینم عکسی که {m.reply_to_message.from_user.first_name} برات فرستاده بود !**__')
        except:
            await c.send_message('me',f'__**❃ مشکلی در دانلود عکس {m.reply_to_message.from_user.first_name} پیش آمد !**__')
    elif m.reply_to_message.video:
        video = await m.reply_to_message.download()
        try:
            await c.send_video('me',video,f'__**❃ اینم ویدیویی که {m.reply_to_message.from_user.first_name} برات فرستاده بود !**__')
        except:
            await c.send_message('me',f'__**❃ مشکلی در دانلود ویدیو {m.reply_to_message.from_user.first_name} پیش آمد !**__')
    else:
        m.continue_propagation()

@app.on_message(filters.me & ~filters.reply & (filters.regex(r'^(حذف بیو)') | filters.regex(r'^([Dd][Ee][Ll][Bb][Ii][Oo])')))
async def inlinedelbio(c:Client, m:Message):
    text = m.text
    pattern = re.search(r'^([Dd][Ee][Ll][Bb][Ii][Oo])',text)
    try:
        text = text.replace('حذف بیو','')
        text = text.replace(pattern[0],'')
    except:
        pass
    cur.execute(f'SELECT * FROM bios WHERE bio = "{text}"')
    if cur.fetchall() != []:
        cur.execute(f'DELETE FROM bios WHERE bio = "{text}"')
        db.commit()
        return await m.edit('__**❃ بیو مورد نظر از لیست بیو ها حذف شد !**__')
    else:
        return await m.edit('__**❃ بیو مورد نظر در لیست بیو ها یافت نشد !**__')

@app.on_message(filters.me & filters.reply & (filters.regex(r'^(حذف بیو)$') | filters.regex(r'^([Dd][Ee][Ll][Bb][Ii][Oo])$')))
async def replydelbio(c:Client, m:Message):
    text = m.reply_to_message.text
    cur.execute(f'SELECT * FROM bios WHERE bio = "{text}"')
    if cur.fetchall() == []:
        return await m.edit('__**❃ بیو مورد نظر در لیست بیو ها موجود نیست !**__')
    else:
        cur.execute('DELETE FROM bios WHERE bio = "{text}"')
        db.commit()
        return await m.edit('__**❃ عبارت مورد نظر با موفقیت از لیست بیو ها حذف شد !**__')

@app.on_message(filters.me & ~filters.reply & (filters.regex(r'^(حذف نام)') | filters.regex(r'^([Dd][Ee][Ll][Nn][Aa][Mm][Ee])')))
async def inlinedelname(c:Client, m:Message):
    text = m.text
    pattern = re.search(r'^([Dd][Ee][Ll][Nn][Aa][Mm][Ee])',text)
    try:
        text = text.replace('حذف نام','')
        text = text.replace(pattern[0],'')
    except:
        pass
    cur.execute(f'SELECT * FROM names WHERE name = "{text}"')
    if cur.fetchall() != []:
        cur.execute(f'DELETE FROM names WHERE name = "{text}"')
        db.commit()
        return await m.edit('__**❃ نام مورد نظر از لیست نام ها حذف شد !**__')
    else:
        return await m.edit('__**❃ نام مورد نظر در لیست نام ها یافت نشد !**__')

@app.on_message(filters.me & filters.reply & (filters.regex(r'^(حذف نام)$') | filters.regex(r'^([Dd][Ee][Ll][Nn][Aa][Mm][Ee])$')))
async def replydelname(c:Client, m:Message):
    text = m.reply_to_message.text
    cur.execute(f'SELECT * FROM names WHERE name = "{text}"')
    if cur.fetchall() == []:
        return await m.edit('__**❃ نام مورد نظر در لیست نام موجود ندارد !**__')
    else:
        cur.execute(f'DELETE FROM names WHERE name = "{text}"')
        db.commit()
        return await m.edit('__**❃ عبارت مورد نظر از لیست نام حذف شد !**__')

@app.on_message(filters.me & ~filters.reply & (filters.regex(r'^(افزودن دشمن)') | filters.regex(r'^([Ss][Ee][Tt][Ee][Nn][Ee][Mm][Yy])')))
async def inlineaddenemy(c:Client, m:Message):
    text = m.text
    fuck = text.split()
    
    pattern = re.search(r'^([Ss][Ee][Tt][Ee][Nn][Ee][Mm][Yy])', text)
    text = text.replace('افزودن دشمن','').strip()
    try:
        text = text.replace(pattern[0],'').strip()
    except:
        pass
    try: text = int(text)
    except: pass
    try: req = await app.get_chat(text)
    except: return await m.edit('__**❃ کاربر وجود ندارد یا اینکه ایدی عددی یا یوزر نیم اشتباه است !**__')
    cur.execute(f'SELECT * FROM enemy WHERE user_id = {req.id}')
    if cur.fetchall() == []: pass
    else: return await m.edit(f'__**❃ کاربر {req.first_name} از قبل در لیست دشمنان وجود داشت !**__')
    query = 'INSERT INTO enemy(user_id) VALUES(?)'
    try:
        cur.execute(query,(req.id,))
    except sqlite3.OperationalError as e:
        os.system('sudo fuser -k database.sqlite')
        cur.execute(query,(req.id,))
    db.commit()
    return await m.edit(f'__**❃ کاربر {req.first_name} به لیست دشمنان اضافه شد !**__')

@app.on_message(filters.me & filters.reply & (filters.regex(r'^(افزودن دشمن)') | filters.regex(r'^([Ss][Ee][Tt][Ee][Nn][Ee][Mm][Yy])')))
async def replyaddenemy(c:Client, m:Message):
    text = m.reply_to_message.text
    
    cur.execute(f'SELECT * FROM enemy WHERE user_id = {m.reply_to_message.from_user.id}')
    if cur.fetchall() == []:
        query = 'INSERT INTO enemy(user_id) VALUES(?)'
        try:
            cur.execute(query, (m.reply_to_message.from_user.id,))
        except sqlite3.OperationalError:
            os.system('fuser -k database.sqlite')
            cur.execute(query, (m.reply_to_message.from_user.id,))
        db.commit()
        return await m.edit(f'__**❃ کاربر {m.reply_to_message.from_user.first_name} به لیست دشمنان افزوده شد !**__')
    else:
        return await m.edit('__**❃ کاربر مورد نظر از قبل در لیست دشمنان بود !**__')

@app.on_message(filters.me & ~filters.reply & (filters.regex(r'^(حذف دشمن)') | filters.regex(r'^([Dd][Ee][Ll][Ee][Nn][Ee][Mm][Yy])')))
async def inlinedelenemy(c:Client, m:Message):
    text = m.text
    pattern = re.search(r'^([Dd][Ee][Ll][Ee][Nn][Ee][Mm][Yy])', text)
    text = text.replace('حذف دشمن','').strip()
    try:
        text  = text.replace(pattern[0],'').strip()
    except:
        pass
    try: text = int(text)
    except: pass
    try: req = await app.get_chat(text)
    except: return await m.edit('__**❃ کاربر مورد نظر یافت نشد !**__')
    cur.execute(f'SELECT * FROM enemy WHERE user_id = {req.id}')
    if cur.fetchall() == []:
        return await m.edit(f'__**❃ کاربر {req.first_name} در لیست دشمنان یافت نشد !**__')
    else:
        cur.execute(f'DELETE FROM enemy WHERE user_id = {req.id}')
        db.commit()
        return await m.edit(f'__**❃ کاربر {req.first_name} از لیست دشمنان حذف شد !**__')

@app.on_message(filters.me & filters.reply & (filters.regex(r'^(حذف دشمن)$') | filters.regex(r'^([Dd][Ee][Ll][Ee][Nn][Ee][Mm][Yy])$')))
async def replydelenemy(c:Client, m:Message):
    user_id = m.reply_to_message.from_user.id
    first_name = m.reply_to_message.from_user.first_name
    cur.execute(f'SELECT * FROM enemy WHERE user_id = {user_id}')
    if cur.fetchall() == []:
        return await m.edit('__**❃ کاربر مورد نظر در لیست دشمنان یافت نشد !**__')
    else:
        cur.execute(f'DELETE FROM enemy WHERE user_id = {user_id}')
        db.commit()
        return await m.edit(f'__**❃ کاربر {first_name} از لیست دشمنان حذف شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(لیست دشمنان)$') | filters.regex(r'^([Ee][Nn][Ee][Mm][Yy][Ll][Ii][Ss][Tt]$)')))
async def enemieslist(c:Client, m:Message):
    char = ''
    cur.execute('SELECT * FROM enemy')
    x = cur.fetchall()
    if x == []:
        return await m.edit('__**❃ لیست دشمنان خالی میباشد !**__')
    else:
        counter = 0
        for i in x:
            counter += 1
            char += f'{counter} -> [Click !](tg://openmessage?user_id={i[0]}) -> `{i[0]}`\n'
        return await m.edit(char)

@app.on_message(filters.me & (filters.regex(r'^(فلود)') | filters.regex(r'^([Ff][Ll][Oo][Oo][Dd])')))
async def flood(c:Client, m:Message):
    textt = m.text
    pattern = re.search(r'^([Ff][Ll][Oo][Oo][Dd])',textt)
    try:
        textt = textt.replace('فلود','')
        textt = textt.replace(pattern[0],'')
    except: pass
    if '-' not in textt: return await m.edit('__**❃ دستور را اشتباه وارد کردید !**__')
    
    textt = textt.split('-')
    await m.delete()
    for i in range(int(textt[1])):
        await c.send_message(m.chat.id, textt[0])
    return

@app.on_message(filters.me & (filters.regex(r'^(میوت فعال)$') | filters.regex(r'^([Mm][Uu][Tt][Ee] [Oo][Nn])$')))
async def activemute(c:Client, m:Message):
    cur.execute('SELECT * FROM mute')
    x = cur.fetchall()[0][0]
    mm = 0 if x == 1 else 1
    cur.execute(f'UPDATE mute SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ میوت با موفقیت فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(میوت غیرفعال)$') | filters.regex(r'^([Mm][Uu][Tt][Ee] [Oo][Ff][Ff])$')))
async def inactivemute(c:Client, m:Message):
    cur.execute('SELECT * FROM mute')
    x = cur.fetchall()[0][0]
    mm = 0 if x == 1 else 1
    cur.execute(f'UPDATE mute SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ میوت غیرفعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(نام فعال)$') | filters.regex(r'^([Nn][Aa][Mm][Ee] [Oo][Nn])$')))
async def activename(c:Client, m:Message):
    cur.execute('SELECT * FROM statusname')
    x = cur.fetchall()[0][0]
    if int(x) == 1:
        return await m.edit('__**❃ تغییر نام از قبل فعال بود !**__')
    mm = 1
    cur.execute(f'UPDATE statusname SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ تغییر نام با موفقیت فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(نام غیرفعال)$') | filters.regex(r'^([Nn][Aa][Mm][Ee] [Oo][Ff][Ff])$')))
async def inactivename(c:Client, m:Message):
    cur.execute('SELECT * FROM statusname')
    x = cur.fetchall()[0][0]
    if int(x) == 0:
        return await m.edit('__**❃ تغییر نام از قبل غیرفعال بود !**__')
    mm = 0
    cur.execute(f'UPDATE statusname SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ تغییر نام با موفقیت غیرفعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(بیو فعال)$') | filters.regex(r'^([Bb][Ii][Oo] [Oo][Nn])$')))
async def activebio(c:Client, m:Message):
    cur.execute('SELECT * FROM statusbio')
    x = cur.fetchall()[0][0]
    if int(x) == 1:
        return await m.edit('__**❃ تغییر بیو از قبل فعال بود !**__')
    mm = 1
    cur.execute(f'UPDATE statusbio SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ تغییر بیو با موفقیت فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(بیو غیرفعال)$') | filters.regex(r'^([Bb][Ii][Oo] [Oo][Ff][Ff])$')))
async def inactivebio(c:Client, m:Message):
    cur.execute('SELECT * FROM statusbio')
    x = cur.fetchall()[0][0]
    if int(x) == 0:
        return await m.edit('__**❃ تغییر بیو از قبل فعال بود !**__')
    mm = 0
    cur.execute(f'UPDATE statusbio SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ تغییر بیو با موفقیت فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(پینگ)$') | filters.regex(r'^([Pp][Ii][Nn][Gg])$')))
async def ping(c:Client, m:Message):
    pong = '__**❃ ربات آنلاین میباشد !**__'
    pong = pong.split()
    char = ''
    for i in pong:
        char += i+' '
        await m.edit(char)
        await asyncio.sleep(0.6)

@app.on_message(filters.me & (filters.regex(r'^(تنظیم فونت)') | filters.regex(r'^([Ss][Ee][Tt][Ff][Oo][Nn][Tt])')))
async def set_font(c:Client, m:Message):
    text = m.text
    pattern = re.search(r'^([Ss][Ee][Tt][Ff][Oo][Nn][Tt])',text)
    try:
        text = text.replace('تنظیم فونت','').strip()
        text = text.replace(pattern[0],'').strip()
    except: pass
    if int(text) >= 10 or int(text) <= 0: return await m.edit('__**❃ فونت های فعلی بین عدد 1 الی 9 میباشند !**__')
    else: pass
    cur.execute('SELECT * FROM fonttype')
    x = cur.fetchall()
    if x == []:
        return
    else:
        status = x[0][0]
        cur.execute(f'UPDATE fonttype SET status={int(text)} WHERE status = {int(status)}')
        db.commit()
        return await m.edit('__**❃ فونت تغییر یافت !**__')

@app.on_message(filters.me & (filters.regex(r'^(راهنما)$') | filters.regex(r'^([Hh][Ee][Ll][Pp])$')))
async def help(c:Client, m:Message):
    await m.edit('''**✅ دستورات ربات ( دو زبانه ) :**

◉ `میوت فعال`
► `Mute On`

◉ `میوت غیرفعال`
‌► `Mute Off`

‌◉ `میوت پیوی`
► `Mute Pv`

◉ `حذف میوت`
► `UnMute Pv`

◉ `لیست میوت`
‌► `MutedList`

▬▭▬▭▬▭▬▬▭▬▭▬▭▬

◉ `بیو فعال`
► `bio On`

◉ `بیو غیرفعال`
‌► `Bio Off`

◉ `افزودن بیو`
‌► `NewBio`

◉ `حذف بیو`
► `DelBio`

◉ `لیست بیو`
► `Bios`

▬▭▬▭▬▭▬▬▭▬▭▬▭▬

◉ `نام فعال`
‌► `Name On`

◉ `نام غیرفعال`
► `Name Off`

◉ `افزودن نام`
► `NewName`

◉ `حذف نام`
► `DelName`

◉ `لیست نام`
► `Names`

▬▭▬▭▬▭▬▬▭▬▭▬▭▬

◉ `افزودن دشمن`
► `Setenemy`

◉ `حذف دشمن`
► `DelEnemy`

◉ `لیست دشمنان`
► `EnemyList`

▬▭▬▭▬▭▬▬▭▬▭▬▭▬

◉ `فلود`
‌► `Flood`

🔹 مثال : `فلود` پاوِر اِسپید -10

🔹 `Flood` PowerSpeed -10

▬▭▬▭▬▭▬▬▭▬▭▬▭▬

◉ `تنظیم فونت`
‌► `SetFont`

🔹 مثال : `تنظیم فونت` 2
🔹 `SetFont` 2

**🗒 شماره فونت ها :**
1 » ⁰⁸:²⁶
2 » 𝟎𝟖:𝟐𝟔
3 »‌‌ ０８:２６
4 » 𝟘𝟠:𝟚𝟞
5 »‌ 08:26
6 » 𝟶𝟾:𝟸𝟼
7 » 𝟬𝟴:𝟮𝟲
8 » 𝟢𝟪:𝟤𝟨
9 » ⓪⑧:②⑥

▬▭▬▭▬▭▬▬▭▬▭▬▭▬

◉ `منشن فعال`
► `Mention On`

◉ `منشن غیرفعال`
► `Mention Off`

◉ `بولد فعال`
► `Bold On`

◉ `بولد غیرفعال`
► `Bold Off`

◉ `استریک فعال`
► `Strik On`

◉ `استریک غیرفعال`
‌► `Strik Off`

◉‌ `ایتالیک فعال`
► `italic On`

◉ `ایتالیک غیرفعال`
► `italic Off`

◉ `اندرلاین فعال`
‌► `Underline On`

◉ اندرلاین غیرفعال
‌► `Underline Off`

▬▭▬▭▬▭▬▬▭▬▭▬▭▬

◉ `پینگ`
► `Ping`

▬▭▬▭▬▭▬▬▭▬▭▬▭▬
||© 2022 **𝐏ᴏᴡᴇʀ 𝐒ᴘᴇᴇᴅ**||
🖥 **برنامه نویسی شده توسط تیم **پاوِر اِسپید
🆔 **@PowerSpeed_TM**''')

@app.on_message(filters.me & (filters.regex(r'^(منشن فعال)$') | filters.regex(r'^([Mm][Ee][Nn][Tt][Ii][Oo][Nn] [Oo][Nn])$')))
async def activemention(c:Client, m:Message):
    cur.execute('SELECT * FROM statusmention')
    x = cur.fetchall()[0][0]
    if int(x) == 1:
        return await m.edit('__**❃ حالت منشن از قبل فعال بود !**__')
    mm = 1
    cur.execute(f'UPDATE statusmention SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت منشن فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(منشن غیرفعال)$') | filters.regex(r'^([Mm][Ee][Nn][Tt][Ii][Oo][Nn] [Oo][Ff][Ff])$')))
async def inactivemention(c:Client, m:Message):
    cur.execute('SELECT * FROM statusmention')
    x = cur.fetchall()[0][0]
    if int(x) == 0:
        return await m.edit('__**❃ حالت منشن از قبل غیرفعال بود !**__')
    mm = 0
    cur.execute(f'UPDATE statusmention SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت منشن غیرفعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(بولد فعال)$') | filters.regex(r'^([Bb][Oo][Ll][Dd] [Oo][Nn])$')))
async def activebold(c:Client, m:Message):
    cur.execute('SELECT * FROM statusbold')
    x = cur.fetchall()[0][0]
    if int(x) == 1:
        return await m.edit('__**❃ حالت بولد از قبل فعال بود !**__')
    mm = 1
    cur.execute(f'UPDATE statusbold SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت بولد با موفقیت فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(بولد غیرفعال)$') | filters.regex(r'^([Bb][Oo][Ll][Dd] [Oo][Ff][Ff])$')))
async def inactivebold(c:Client, m:Message):
    cur.execute('SELECT * FROM statusbold')
    x = cur.fetchall()[0][0]
    if int(x) == 0:
        return await m.edit('__**❃ حالت بولد از قبل غیرفعال بود !**__')
    mm = 0
    cur.execute(f'UPDATE statusbold SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت بولد غیرفعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(استریک فعال)$') | filters.regex(r'^([Ss][Tt][Rr][Ii][Kk] [Oo][Nn])$')))
async def activestrik(c:Client, m:Message):
    cur.execute('SELECT * FROM statusstrik')
    x = cur.fetchall()[0][0]
    if int(x) == 1:
        return await m.edit('__**❃ حالت استریک از قبل فعال بود !**__')
    mm = 1
    cur.execute(f'UPDATE statusstrik SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت استریک فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(استریک غیرفعال)$') | filters.regex(r'^([Ss][Tt][Rr][Ii][Kk] [Oo][Ff][Ff])$')))
async def inactivestrik(c:Client, m:Message):
    cur.execute('SELECT * FROM statusstrik')
    x = cur.fetchall()[0][0]
    if int(x) == 0:
        return await m.edit('__**❃ حالت استریک از قبل غیرفعال بود !**__')
    mm = 0
    cur.execute(f'UPDATE statusstrik SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت استریک غیرفعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(ایتالیک فعال)$') | filters.regex(r'^([Ii][Tt][Aa][Ll][Ii][Cc] [Oo][Nn])$')))
async def activeitalic(c:Client, m:Message):
    cur.execute('SELECT * FROM statusitalic')
    x = cur.fetchall()[0][0]
    if int(x) == 1:
        return await m.edit('__**❃ حالت ایتالیک از قبل فعال بود !**__')
    mm = 1
    cur.execute(f'UPDATE statusitalic SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت ایتالیک فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(ایتالیک غیرفعال)$') | filters.regex(r'^([Ii][Tt][Aa][Ll][Ii][Cc] [Oo][Ff][Ff])$')))
async def inactiveitalic(c:Client, m:Message):
    cur.execute('SELECT * FROM statusitalic')
    x = cur.fetchall()[0][0]
    if int(x) == 0:
        return await m.edit('__**❃ حالت ایتالیک از قبل غیرفعال بود !**__')
    mm = 0
    cur.execute(f'UPDATE statusitalic SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت ایتالیک غیرفعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(اندرلاین فعال)$') | filters.regex(r'^([Uu][Nn][Dd][Ee][Rr][Ll][Ii][Nn][Ee] [Oo][Nn])$')))
async def activeunderline(c:Client, m:Message):
    cur.execute('SELECT * FROM statusunderline')
    x = cur.fetchall()[0][0]
    if int(x) == 1:
        return await m.edit('__**❃ حالت اندرلاین از قبل فعال بود !**__')
    mm = 1
    cur.execute(f'UPDATE statusunderline SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت اندرلاین فعال شد !**__')

@app.on_message(filters.me & (filters.regex(r'^(اندرلاین غیرفعال)$') | filters.regex(r'^([Uu][Nn][Dd][Ee][Rr][Ll][Ii][Nn][Ee] [Oo][Ff][Ff])$')))
async def inactiveunderline(c:Client, m:Message):
    cur.execute('SELECT * FROM statusunderline')
    x = cur.fetchall()[0][0]
    if int(x) == 0:
        return await m.edit('__**❃ حالت اندرلاین از قبل غیرفعال بود !**__')
    mm = 0
    cur.execute(f'UPDATE statusunderline SET status = {mm} WHERE status = {x}')
    db.commit()
    return await m.edit('__**❃ حالت اندرلاین غیرفعال شد !**__')

@app.on_message(filters.me & filters.text)
async def textmode(c:Client, m:Message):
    cur.execute('SELECT * FROM statusbold')
    bold = int(cur.fetchall()[0][0])
    cur.execute('SELECT * FROM statusitalic')
    italic = int(cur.fetchall()[0][0])
    cur.execute('SELECT * FROM statusstrik')
    strik = int(cur.fetchall()[0][0])
    cur.execute('SELECT * FROM statusmention')
    mention = int(cur.fetchall()[0][0])
    cur.execute('SELECT * FROM statusunderline')
    underline = int(cur.fetchall()[0][0])

    text = m.text
    
    if bold == 1:
        return await m.edit(f'**{text}**')
    elif italic == 1:
        return await m.edit(f'__{text}__')
    elif strik == 1:
        return await m.edit(f'~~{text}~~')
    elif mention == 1:
        return await m.edit(f'[{text}](tg://openmessage?user_id={m.from_user.id})')
    elif underline == 1:
        return await m.edit(f'--{text}--')

@app.on_message((filters.private | filters.group) & ~filters.me)
async def enemy(c:Client, m:Message):
    list_fohsh = ['کسکش','پدر کونی','کیر خر تو ننت','ننه کیر دزد','ننه اوبی','صیکتیر جنده','ناموصتو گاییدم','ننه کص پاپیونی','خارکصه','سماور تو کص مادرت','کص ننت','مادر جنده']
    if m.from_user.id in readenemy(): return await m.reply(random.choice(list_fohsh))
    else: m.continue_propagation()

@app.on_message(filters.private & ~filters.me)
async def mute(c:Client, m:Message):
    cur.execute('SELECT * FROM mute')
    x = cur.fetchall()[0][0]
    if x == 0: m.continue_propagation()
    else:
        if m.from_user.id in readmute(): await m.delete(revoke=True)
        else: m.continue_propagation()

#-----------------------+
# ¹²³⁴⁵⁶⁷⁸⁹⁰ -> 1       |
# 𝟏𝟐𝟑️️𝟒𝟓𝟔𝟕𝟖𝟗𝟎 -> 2         |
# １２３️️４５６７８９０ -> 3 |--------> All Fonts
# 𝟙𝟚𝟛️️𝟜𝟝𝟞𝟟𝟠𝟡𝟘 -> 4       |
# 1234567890 -> 5       |
#-----------------------+ 

def fonttype():
    cur.execute('SELECT * FROM fonttype')
    x = cur.fetchall()[0][0]
    if int(x) == 1:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','¹').replace('2','²').replace('3','³').replace('4','⁴').replace('5','⁵')
        hour = hour.replace('6','⁶').replace('7','⁷').replace('8','⁸').replace('9','⁹').replace('0','⁰')
        return hour
    elif int(x) == 2:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','𝟏').replace('2','𝟐').replace('3','𝟑️️').replace('4','𝟒').replace('5','𝟓')
        hour = hour.replace('6','𝟔').replace('7','𝟕').replace('8','𝟖').replace('9','𝟗').replace('0','𝟎')
        return hour
    elif int(x) == 3:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','１').replace('2','２').replace('3','３️️').replace('4','４').replace('5','５')
        hour = hour.replace('6','６').replace('7','７').replace('8','８').replace('9','９').replace('0','０')
        return hour
    elif int(x) == 4:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','𝟙').replace('2','𝟚').replace('3','𝟛️️').replace('4','𝟜').replace('5','𝟝')
        hour = hour.replace('6','𝟞').replace('7','𝟟').replace('8','𝟠').replace('9','𝟡').replace('0','𝟘')
        return hour
    elif int(x) == 5:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','1').replace('2','2').replace('3','3').replace('4','4').replace('5','5')
        hour = hour.replace('6','6').replace('7','7').replace('8','8').replace('9','9').replace('0','0')
        return hour
    elif int(x) == 6:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','𝟷').replace('2','𝟸').replace('3','𝟹️️').replace('4','𝟺').replace('5','𝟻')
        hour = hour.replace('6','𝟼').replace('7','𝟽').replace('8','𝟾').replace('9','𝟿').replace('0','𝟶')
        return hour
    elif int(x) == 7:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','𝟭').replace('2','𝟮').replace('3','𝟯️️').replace('4','𝟰').replace('5','𝟱')
        hour = hour.replace('6','𝟲').replace('7','𝟳').replace('8','𝟴').replace('9','𝟵').replace('0','𝟬')
        return hour
    elif int(x) == 8:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','𝟣').replace('2','𝟤').replace('3','𝟥').replace('4','𝟦').replace('5','𝟧')
        hour = hour.replace('6','𝟨').replace('7','𝟩').replace('8','𝟪').replace('9','𝟫').replace('0','𝟢')
        return hour
    elif int(x) == 9:
        hour = str(jdatetime.datetime.now().strftime("%H:%M")).replace('1','①').replace('2','②').replace('3','③').replace('4','④').replace('5','⑤')
        hour = hour.replace('6','⑥').replace('7','⑦').replace('8','⑧').replace('9','⑨').replace('0','⓪')
        return hour

def checkmute():
    cur.execute('SELECT * FROM muted')
    x = cur.fetchall()
    if x == []: return
    else:
        for i in x :
            now = time.time()
            end = float(i[3])
            if now >= end:
                cur.execute(f'DELETE FROM muted WHERE user_id = {i[0]}')
                db.commit()

async def changename(c:Client, m:Message):
    cur.execute('SELECT * FROM statusname')
    if cur.fetchall()[0][0] == 0:
        return
    else:
        names = []
        cur.execute('SELECT * FROM names')
        for i in cur.fetchall():
            names.append(i[0])
        nam = random.choice(names).replace('time',fonttype())
        print(nam)
        await app.update_profile(first_name = nam)

async def changebio(c:Client, m:Message):
    cur.execute('SELECT * FROM statusbio')
    if cur.fetchall()[0][0] == 0:
        return
    else:
        bios = []
        cur.execute('SELECT * FROM bios')
        for i in cur.fetchall():
            bios.append(i[0])
        try:
            byo = random.choice(bios).replace('time',fonttype())
            print(byo)
            await app.update_profile(bio = byo)
        except:
            pass

cron_1 = aiocron.crontab('*/3 * * * *', func = checkmute)
cron_2 = aiocron.crontab('*/1 * * * *', func = changename,args = (Client, Message))
cron_3 = aiocron.crontab('*/1 * * * *', func = changebio,args = (Client, Message))

idle()