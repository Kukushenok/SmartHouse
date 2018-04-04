# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters , CommandHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup , ReplyKeyboardRemove
import watson_developer_cloud
import os
import objects.House
import pygame
import tools.config
messager = {}
calling = {}
def main():
    assistant = watson_developer_cloud.AssistantV1(
        username='d9a6b2ae-44fd-4cb4-9602-95a3cc357363',
        password='Rxs5YCzznkbY',
        version='2018-02-16'
    )


    config = tools.config.Config(False,os.getcwd())
    house = objects.House.House()
    def chat_handler(bot, updater):
        global messager,calling
        response = assistant.message(
            workspace_id='adcfa951-1a99-4127-bfbc-e09101075716',
            input={
                'text': updater.message.text
            }
        )
        print(response)
        calling["ready"] = False
        changed = False
        if response["intents"]:
            if not calling.get("intent") or calling["intent"]["conf"]<response["intents"][0]["confidence"]:
                calling["intent"] = {"type":response["intents"][0]["intent"],"conf":response["intents"][0]["confidence"]}
                changed = True
        if response["entities"]:
            if not calling.get("params"):
                calling["params"] = {}
                changed = True
                for entity in response["entities"]:
                    calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
            else:
                for entity in response["entities"]:
                    if not calling["params"].get(entity["entity"]):
                        changed = True
                        calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
                    elif calling["params"][entity["entity"]]["conf"]<entity["confidence"]:
                        changed = True
                        calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
        if not messager: messager = updater
        if changed:
            for output in response["output"]["text"]:
                updater.message.reply_text(output)
                if output[:3] == "Поп":
                    calling["ready"] = True
        house.call(calling)
        if calling["ready"]: calling = {}

    updater = Updater(config.get("botKey"))

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,chat_handler))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    #updater.idle()
    size = width, height = 800,600
    screen = pygame.display.set_mode(size,pygame.DOUBLEBUF)
    running = True
    fps = 2
    clock = pygame.time.Clock()
    while running:
        callback = house.draw(1/fps)
        screen.blit(callback[0],(0,0))
        if callback[1] and messager:
            messager.message.reply_text(callback[1])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                updater.stop()
                exit(0)
        clock.tick(fps)


if __name__ == "__main__":
    main()