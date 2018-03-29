# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters , CommandHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup , ReplyKeyboardRemove
import requests
import os
import objects.House
import pygame
import tools.config
def main():
    config = tools.config.Config(False,os.getcwd())
    house = objects.House.House()
    def chat_handler(bot, updater,user_data):
        house.call(updater.message.text)

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
    while running:
        screen.blit(house.draw(),(0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                updater.stop()
                exit(0)


if __name__ == "__main__":
    main()