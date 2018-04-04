# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters , CommandHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup , ReplyKeyboardRemove
import watson_developer_cloud
import os
import objects.House
import pygame
import tools.config
messager = {}
def main():
    assistant = watson_developer_cloud.AssistantV1(
        username='d9a6b2ae-44fd-4cb4-9602-95a3cc357363',
        password='Rxs5YCzznkbY',
        version='2018-02-16'
    )


    config = tools.config.Config(False,os.getcwd())
    house = objects.House.House()
    def chat_handler(bot, updater,user_data):
        global messager
        response = assistant.message(
            workspace_id='adcfa951-1a99-4127-bfbc-e09101075716',
            input={
                'text': updater.message.text
            }
        )
        if response["intents"]: house.call(response["intents"][0]["intent"])
        messager = updater

    updater = Updater(config.get("botKey"))

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,chat_handler,pass_user_data=True))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    #updater.idle()
    size = width, height = 800,600
    screen = pygame.display.set_mode(size,pygame.DOUBLEBUF)
    running = True
    fps = 2
    clock = pygame.time.Clock()
    while running:
        screen.blit(house.draw(1/fps),(0,0))
        pygame.display.flip()
        #callback = house.callback()
        #if callback and messager:
        #    messager.message.reply_text(callback)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                updater.stop()
                exit(0)
        clock.tick(fps)


if __name__ == "__main__":
    main()