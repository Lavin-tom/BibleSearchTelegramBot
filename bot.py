import telebot
import xml.etree.ElementTree as ET
from telebot import types

TOKEN = open('api-key.txt').readline()
bot = telebot.TeleBot(TOKEN)
print("Bot is online")

root = None  # Declare root as a global variable initially

hey_msg = ['Hi','Hello','Hey']
knownUsers = []
userStep = {}

book_id_to_search = []
chapter_to_search = []
language = 'malayalam'  #default language 

hideBoard = types.ReplyKeyboardRemove()  # hide the keyboard

language_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
language_select.add('English','മലയാളം')

testament_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
testament_select.add('പഴയ_നിയമം','പുതിയ_നിയമം')

def language_change_fun(language):
    global root
    # First, clear the existing keyboard options
    testament_select.keyboard.clear()

    if language == 'malayalam':
        testament_select.add('പഴയ_നിയമം', 'പുതിയ_നിയമം')
        # Load the XML file for Malayalam
        xml_file_path = 'res/bible_mal.xml'
    elif language == 'english':
        testament_select.add('Old', 'New')
        # Load the XML file for English
        xml_file_path = 'res/bible_eng.xml'

    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

New_testement_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
New_testement_select.add('മത്തായി','മർക്കൊസ്','ലൂക്കോസ്','യോഹന്നാൻ','പ്രവൃത്തികൾ','റോമർ','1_കൊരിന്ത്യർ','2_കൊരിന്ത്യർ','ഗലാത്യർ','എഫെസ്യർ','ഫിലിപ്പിയർ','കൊലൊസ്സ്യർ',
'1_തെസ്സലൊനീക്യർ','2_തെസ്സലൊനീക്യർ','1_തിമൊഥെയൊസ്','2_തിമൊഥെയൊസ്','തീത്തൊസ്','ഫിലേമോൻ','എബ്രായർ','യാക്കോബ്','1_പത്രൊസ്','2_പത്രൊസ്','1_യോഹന്നാൻ','2_യോഹന്നാൻ','3_യോഹന്നാൻ','യൂദാ','വെളിപ്പാട്')

Old_testement_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
Old_testement_select.add('ഉല്പത്തി','പുറപ്പാട്','ലേവ്യപുസ്തകം','സംഖ്യാപുസ്തകം','ആവർത്തനം','യോശുവ','ന്യായാധിപന്മാർ','രൂത്ത്',
'1_ശമൂവേൽ','2_ശമൂവേൽ','1_രാജാക്കന്മാർ','2_രാജാക്കന്മാർ','1_ദിനവൃത്താന്തം','2_ദിനവൃത്താന്തം','എസ്രാ','നെഹെമ്യാവു','എസ്ഥേർ','ഇയ്യോബ്','സങ്കീർത്തനങ്ങൾ','സദൃശ്യവാക്യങ്ങൾ',
'സഭാപ്രസംഗി','ഉത്തമഗീതം','യെശയ്യാ','യിരമ്യാവു','വിലാപങ്ങൾ','യെഹേസ്കേൽ','ദാനീയേൽ','ഹോശേയ','യോവേൽ','ആമോസ്','ഓബദ്യാവു','യോനാ','മീഖാ','നഹൂം','ഹബക്കൂക്ക്',
'സെഫന്യാവു','ഹഗ്ഗായി','സെഖര്യാവു','മലാഖി')

New_testement_english_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
New_testement_english_select.add('Matthew','Mark','Luke','John','Acts','Romans','1_Corinthians','2_Corinthians','Galatians','Ephesians','Philippians','Colossians',
'1_Thessalonians','2_Thessalonians','1_Timothy','2_Timothy','Titus','Philemon','Hebrews','James','1_Peter','2_Peter','1_John','2_John','3_John','Jude','Revelation')

Old_testement_english_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
Old_testement_english_select.add('Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth',
'1_Samuel','2_Samuel','1_Kings','2_Kings','1_Chronicles','2_Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs',
'Ecclesiastes','Song_of_Solomon','Isaiah','Jeremiah','Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk',
'Zephaniah','Haggai','Zechariah','Malachi')

chapter_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)

commands = {'search': 'Search Bible',
            'change_language': 'Change language',
			'all':'List all commands',
            'about':'About me'}

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected")
        return 0

def find_chapter(book_id_to_search):
    text = ' '
    chapter_count = 0
    verse_count = 0

    # Find the book element with the specified book ID
    Book = root.find(f"./Book[@id='{book_id_to_search}']")

    if Book is not None:
        chapters = Book.findall('Chapter')
        chapter_count = len(chapters)
        for chapter in chapters:
            verses = chapter.findall('Verse')
            verse_count += len(verses)
    text += str(chapter_count)
    text += ' '
    text += str(verse_count)
    for i in range(1, chapter_count + 1):
        chapter_select.add(str(i))

def search_result(book_id_to_search, chapter,m):
    print(book_id_to_search,chapter)
    cid = m.chat.id
    userStep[cid] = 0
    text = ' '
    text += book_id_to_search
    text += ' '
    text += chapter
    text += '\n\n'
    Book = root.find(f"./Book[@id='{book_id_to_search}']")

    if Book is not None:
        Chapter = Book.find(f"./Chapter[@id='{chapter}']")
        if Chapter is not None:
            for Verse in Chapter.findall('Verse'):
                verse_id = Verse.get('id')
                verse_text = Verse.text
                #print(f"{verse_id}. {verse_text}")
                text+= verse_id
                text+= '.'
                text+= verse_text
                text+= '\n\n'
                if len(text) > 1000:    #to solve the issue of max char in one message in Telegram 
                    bot.send_message(m.chat.id,text)
                    text = ' '
        else:
            print("Chapter not found.")
    else:
        print("Book not found.")

#---------------------main commands-----------------
#show all available commands
@bot.message_handler(commands=['all'])
def command_all(m):
    text = "All available commands :\n"
    for key in commands:
        text += "🔸 /" + key + " : "
        text += commands[key] + "\n\n"
    bot.send_message(m.chat.id,text)

#show about
@bot.message_handler(commands=['about'])
def handle_about(m):
    bot.send_chat_action(m.chat.id,'typing')
    note = "About notes here"
    bot.send_message(m.chat.id,note,parse_mode='Markdown')

#show source
@bot.message_handler(commands=['source'])
def handle_source(m):
        bot.send_chat_action(m.chat.id,'typing')
        link = "https://github.com/Lavin-tom/Telegram_Bot"
        formatted_message = f"[Click here]({link}) to visit the GitHub repository."
        bot.reply_to(m, formatted_message, parse_mode='Markdown')

#show start
@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	if cid not in knownUsers:
		knownUsers.append(cid)
		userStep[cid] = 0

#search bible
@bot.message_handler(commands=['change_language'])
def command_change_language(m):
    cid = m.chat.id
    bot.send_message(cid, "Now choose English or മലയാളം ",reply_markup=language_select)
    userStep[cid] = 'change_language'

#search bible
@bot.message_handler(commands=['search'])
def command_search(m):
    cid = m.chat.id
    bot.send_message(cid, "what do you want Old or New ?",reply_markup=testament_select)
    userStep[cid] = 'search'

#--------------------------------------Bible Search-------------------------------#
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'search')
def msg_search_select(m):
    cid = m.chat.id
    userStep[cid] = 0
    bot.send_chat_action(cid, 'typing')
    userQuery = m.text.lower()
    if userQuery == 'പഴയ_നിയമം':
        bot.send_message(cid, "പുസ്‌തകം തിരഞ്ഞെടുക്കുക !!",reply_markup=Old_testement_select)
        userStep[cid] = 'select_chapter'

    elif userQuery == 'പുതിയ_നിയമം':
        bot.send_message(cid, "പുസ്‌തകം തിരഞ്ഞെടുക്കുക !!",reply_markup=New_testement_select)
        userStep[cid] = 'select_chapter'
        
    elif userQuery == 'old':
        bot.send_message(cid, "Choose any book?",reply_markup=Old_testement_english_select)
        userStep[cid] = 'select_chapter'

    elif userQuery == 'new':
        bot.send_message(cid, "Choose any book?",reply_markup=New_testement_english_select)    
        userStep[cid] = 'select_chapter'
    else:
        bot.send_message(cid,"Invalid Commmands")

#[chapter selection]
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'select_chapter')
def handle_select_chapter(m):
    cid = m.chat.id
    userStep[cid] = 0

    find_chapter(m.text)        #to find no of chapters
    book_id_to_search.clear()
    book_id_to_search.append(m.text)
    try:
        bot.send_message(m.chat.id, "Select chapter",reply_markup=chapter_select)
        userStep[cid] = 'searching'
    except Exception as e:
        bot.send_message(m.chat.id, "Search error!! error while selecting chapter")

#[verses selection]
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'searching')
def handle_user_old_test_search(m):
    cid = m.chat.id
    userStep[cid] = 0
    try:
        chapter_to_search.append(m.text)
        search_result(book_id_to_search[0],chapter_to_search[0],m)
        print(book_id_to_search[0],chapter_to_search[0])
        chapter_select.keyboard.clear()
        userStep[cid] = 'search_bible'
    except Exception as e:
        bot.send_message(m.chat.id, "Search error!! error while selecting verses")
 
#language change  
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'change_language')
def msg_search_select(m):
    cid = m.chat.id
    userStep[cid] = 0
    bot.send_chat_action(cid, 'typing')
    userQuery = m.text.lower()
    if userQuery == 'malayalam':
        language_change_fun(userQuery)
        bot.send_message(m.chat.id, "ഭാഷ മലയാളത്തിലേക്ക് മാറിയിരിക്കുന്നു m /search")
    elif userQuery == 'english':
        language_change_fun(userQuery)
        bot.send_message(m.chat.id, "Language changed to English now /search")        
        
        
bot.infinity_polling()
