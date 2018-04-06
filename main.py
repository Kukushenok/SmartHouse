# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters , CommandHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup , ReplyKeyboardRemove
import watson_developer_cloud
import os
import objects.Manager
import pygame
messager = {}
calling = {}
def main():
    print("Запускаем программу...")
    users = 0
    assistant = watson_developer_cloud.ConversationV1(
        username='d9a6b2ae-44fd-4cb4-9602-95a3cc357363',
        password='Rxs5YCzznkbY',
        version='2018-02-16'
    )
    def starting(bot, updater,user_data):
        if user_data.get("getted_started"):
            updater.message.reply_text('Не... Лень рассказывать заного функционал дома... Ааах, ну ладно, уговорил.\n'
                                       'Функционал дома:\n'
                                       'Всего 6 комнат: коридор, зал (кухня), бойлерная, ванная,большая и малая спальни.\n'
                                       'В них можно либо включить/выключить свет, либо установить температуру.\n')
        if not objects.Manager.Manager.getPassHandler().CheckOnWhitelist(updater["message"]["chat"]["username"]):
            updater.message.reply_text("Вас нет в белом списке, Вы не можете войти")
            return None
        user_data["attempts"] = int(objects.Manager.Manager.getConfig().get("maxAttemps"))
        user_data["getted_started"] = True
        user_data["pass_input"] = True
        print(updater["message"]["chat"]["username"] + " пытается войти в систему")
        updater.message.reply_text('Добро пожаловать в систему "Умный дом"! \n'
                                   'Мне можно задавать команды на "человеческом" языке! \n'
                                   'Функционал дома:\n'
                                   'Всего 6 комнат: коридор, зал (кухня), бойлерная, ванная,большая и малая спальни.\n'
                                   'В них можно либо включить/выключить свет, либо установить температуру.\n'
                                   'Систему "Умный дом" легко настроить: если Вам надо добавить других жильцов дома, просто впишите в этот список! \n'
                                   'Конечно, им нужно сказать пароль, чтобы войти...\n'
                                   'О! Начнём с Вас! Скажите мне пароль, и я впущу Вас :D')

    def chat_handler(bot, updater,user_data):
        global messager,calling
        if not objects.Manager.Manager.getPassHandler().CheckOnWhitelist(updater["message"]["chat"]["username"]):
            updater.message.reply_text("Вас нет в белом списке, Вы не можете войти")
            return None
        print(updater.message.text)
        response = assistant.message(
            workspace_id='adcfa951-1a99-4127-bfbc-e09101075716',
            input={
                'text': updater.message.text
            }
        )
        response = assistant.message(
            workspace_id="adcfa951-1a99-4127-bfbc-e09101075716",
            input={
                'text': ''
            }
        )
        if user_data.get("logged_in"):
            for output in response["output"]["text"]:
                updater.message.reply_text(output)
                if output[:3] == "Поп":
                    calling["ready"] = True
            calling["ready"] = False
            if response["intents"] and response["intents"][0]["intent"] == "log_out":
                updater.message.reply_text(response["output"]["text"][0])
                user_data["logged_in"] = False
                objects.Manager.Manager.getUsers().remove_user(updater["message"]["chat"]["username"])
                return None
            if response["intents"]:
                if not calling.get("intent") or calling["intent"]["conf"]<response["intents"][0]["confidence"]:
                    calling["intent"] = {"type":response["intents"][0]["intent"],"conf":response["intents"][0]["confidence"]}
            if response["entities"]:
                if not calling.get("params"):
                    calling["params"] = {}
                    for entity in response["entities"]:
                        calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
                else:
                    for entity in response["entities"]:
                        if not calling["params"].get(entity["entity"]):
                            calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
                        elif calling["params"][entity["entity"]]["conf"]<entity["confidence"]:
                            calling["params"][entity["entity"]] = {"value":entity["value"],"conf":entity["confidence"]}
            if not messager: messager = updater
            print(response)
            fast_callback = objects.Manager.Manager.getHouse().call(calling)
            if fast_callback == "Busy": updater.message.reply_text("Простите, но данный запрос был отклонён из-за посторонней операцией над этой комнатой")
            if calling["ready"]: calling = {}
        else:
            if response["intents"] and response["intents"][0]["intent"] == "log_in":
                user_data["attempts"] = int(objects.Manager.Manager.getConfig().get("maxAttemps"))
                user_data["pass_input"] = True
                print(updater["message"]["chat"]["username"] + " пытается войти в систему")
                updater.message.reply_text(response["output"]["text"][0])
            elif not response["intents"]:
                if objects.Manager.Manager.getPassHandler().LogIn(updater.message.text):
                    user_data["logged_in"] = True
                    user_data["pass_input"] = False
                    updater.message.reply_text("Вы вошли в систему!")
                    print(updater["message"]["chat"]["username"] + " вошёл в систему")
                    objects.Manager.Manager.getUsers().add_user(updater["message"]["chat"]["username"])
                    return None
                elif user_data.get("attempts") and user_data["attempts"] > 1 and user_data["pass_input"]:
                    user_data["attempts"] -=1
                    updater.message.reply_text("Неверный пароль! У вас осталось до иcключения из белого списка попыток: "+str(user_data["attempts"]))
                elif user_data["pass_input"]:
                    objects.Manager.Manager.getPassHandler().whitelist.pop(objects.Manager.Manager.getPassHandler().whitelist.index(updater["message"]["chat"]["username"]))
                    whitelist = objects.Manager.Manager.getConfig().getAsList("whitelist")
                    whitelist.pop(whitelist.index(updater["message"]["chat"]["username"]))
                    objects.Manager.Manager.getConfig().config["SETTINGS"]["whitelist"] = ",".join(whitelist)
                    objects.Manager.Manager.getConfig().SaveChanges()
                    updater.message.reply_text("Неверный пароль! Вы были удалены из белого списка...")
                    print("ВНИМАНИЕ. "+updater["message"]["chat"]["username"]+" был удалён из белого списка за сомнительное количество попыток входа.")



    updater = Updater(objects.Manager.Manager.getConfig().get("botKey"))

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text,chat_handler,pass_user_data=True))
    dp.add_handler(CommandHandler("start",starting,pass_user_data=True))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    #updater.idle()
    size = width, height = 800,600
    screen = pygame.display.set_mode(size,pygame.DOUBLEBUF)
    running = True
    fps = 2
    clock = pygame.time.Clock()

    print("ОК!")
    while running:
        callback = objects.Manager.Manager.getHouse().draw(1/fps)
        screen.blit(callback[0],(0,0))
        if callback[1] and messager:
            messager.message.reply_text(callback[1])
        objects.Manager.Manager.getUsers().render(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                updater.stop()
                exit(0)
        clock.tick(fps)


if __name__ == "__main__":
    main()