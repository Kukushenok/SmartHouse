# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters , CommandHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup , ReplyKeyboardRemove
from watson_developer_cloud import AssistantV1
import os
import objects.House
import pygame
import tools.config
messager = {}
def main():
    config = tools.config.Config(False,os.getcwd())
    house = objects.House.House()
    def chat_handler(bot, updater,user_data):
        global messager
        house.call(updater.message.text)
        messager = updater

    updater = Updater(config.get("botKey"))

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text,chat_handler,pass_user_data=True))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    #updater.idle()
    size = width, height = 800,600
    screen = pygame.display.set_mode(size)
    running = True
    fps = 30
    clock = pygame.time.Clock()
    while running:
        screen.blit(house.draw(),(0,0))
        pygame.display.flip()
        callback = house.callback()
        if callback and messager:
            messager.message.reply_text(callback)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                updater.stop()
                exit(0)
        clock.tick(fps)


if __name__ == "__main__":
    main()