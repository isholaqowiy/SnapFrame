import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
import database
import image_editor
import utils
from config import TEMP_DIR

SCREENSHOT_STAGE = range(1)

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📸 Beautify Screenshot", callback_data="btn_start_beautify")],
        [InlineKeyboardButton("🎨 Background Style", callback_data="btn_bg_menu"),
         InlineKeyboardButton("📱 Device Frame", callback_data="btn_frame_menu")],
        [InlineKeyboardButton("❓ Help Manual", callback_data="btn_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utils.ensure_temp_directory()
    uid = update.effective_user.id
    await database.register_user(uid)
    
    welcome = (
        "👋 Welcome to *SnapFrame Bot*!\n"
        "Turn ordinary screenshots into beautiful, presentation-ready visuals.\n\n"
        "📸 *Upload your screenshot raw image*\n"
        "🎨 *Add premium vertical linear gradients*\n"
        "📱 *Wrap content inside realistic device frames*\n"
        "✨ *Customize padding parameters dynamically*\n\n"
        "Send a screenshot image or choose an option below to get started."
    )
    if update.message:
        await update.message.reply_text(welcome, reply_markup=get_main_menu(), parse_mode="Markdown")
    return ConversationHandler.END

async def start_beautify_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📥 Excellent! Please send your screenshot image asset as a Photo now:")
    return SCREENSHOT_STAGE

async def process_screenshot_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    photo = update.message.photo[-1]
    
    tg_file = await context.bot.get_file(photo.file_id)
    input_path = os.path.join(TEMP_DIR, f"ss_{uid}.png")
    await tg_file.download_to_drive(input_path)
    
    await update.message.reply_text("⚡ Processing your high-resolution render design matrix layers... Please wait.")
    
    user_settings = await database.get_user_settings(uid)
    output_file = image_editor.beautify(input_path, uid, user_settings)
    
    if os.path.exists(output_file):
        with open(output_file, 'rb') as f:
            await update.message.reply_document(document=f, filename="beautified_shot.png", caption="✨ Render complete! Generated successfully via SnapFrame Engine.")
        utils.clean_user_files(uid)
    else:
        await update.message.reply_text("❌ A processing exception constraint occurred during design layer alignment.")
        
    return ConversationHandler.END

async def menu_navigation_routing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    
    if query.data == "btn_bg_menu":
        kb = [[InlineKeyboardButton("Sunset Gradient", callback_data="set_bg_Sunset")],
              [InlineKeyboardButton("Ocean Gradient", callback_data="set_bg_Ocean")],
              [InlineKeyboardButton("Aurora Light", callback_data="set_bg_Aurora")],
              [InlineKeyboardButton("Dark Onyx", callback_data="set_bg_Dark")],
              [InlineKeyboardButton("🔙 Back to Menu", callback_data="goto_root")]]
        await query.edit_message_text("🎨 *Select your background canvas gradient style template:*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        
    elif query.data == "btn_frame_menu":
        kb = [[InlineKeyboardButton("Minimal Device Frame", callback_data="set_fr_Device Frame")],
              [InlineKeyboardButton("No Hardware Border", callback_data="set_fr_No Frame")],
              [InlineKeyboardButton("🔙 Back to Menu", callback_data="goto_root")]]
        await query.edit_message_text("📱 *Select device frame wrapper profiling schema rules:*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        
    elif query.data.startswith("set_bg_"):
        val = query.data.split("_")[2]
        await database.update_setting(uid, "background", val)
        await query.message.reply_text(f"✅ Canvas background color schema set to: `{val}`")
        
    elif query.data.startswith("set_fr_"):
        val = query.data.split("_")[2]
        await database.update_setting(uid, "frame", val)
        await query.message.reply_text(f"✅ Hardware device layout constraint set to: `{val}`")
        
    elif query.data == "goto_root":
        await query.edit_message_text("Send a screenshot or choose an option below to get started.", reply_markup=get_main_menu())
    elif query.data == "btn_help":
        await query.message.reply_text("❓ *Quick Help:* Tap 'Beautify Screenshot', upload your raw layout image, and customize style vectors instantly using our background presets controllers.")

