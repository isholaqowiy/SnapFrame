import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
import database
import handlers
from config import BOT_TOKEN

def main():
    # Enforce clear asynchronous lifecycle setup hooks to safely initialize local SQLite instances
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(database.init_db())

    if not BOT_TOKEN:
        print("Fatal Error: Missing BOT_TOKEN.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    convo_flow = ConversationHandler(
        entry_points=[CallbackQueryHandler(handlers.start_beautify_flow, pattern="^btn_start_beautify$")],
        states={handlers.SCREENSHOT_STAGE: [MessageHandler(filters.PHOTO, handlers.process_screenshot_input)]},
        fallbacks=[CommandHandler("start", handlers.start)]
    )

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CallbackQueryHandler(handlers.menu_navigation_routing, pattern="^(btn_|set_|goto_)"))
    app.add_handler(convo_flow)

    print("SnapFrame Rendering Processing Core Polling Live...")
    app.run_polling()

if __name__ == '__main__':
    main()

