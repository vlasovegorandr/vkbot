import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import random
from vkbot.settings_and_data import menu_names



def auth():
    return vk_api.VkApi(token='c92d4598663069b52b1357531cb07425e1cc21a33bd98f7c7279d740df941d12cfa88fe4abc1c6b74f9cd')

class Listener:

    def __init__(self):
        self.previous_menu = 'main_menu'
        self.current_menu = 'main_menu'
        self.vk_auth = auth()
        self.vk = self.vk_auth.get_api()
        self.upload = vk_api.VkUpload(self.vk)
        self.run_longpoll(current_menu=self.current_menu)


    def run_longpoll(self, **kwargs):

        if 'current_menu' in kwargs:
            current_menu = kwargs['current_menu']
        else:
            current_menu = self.current_menu

        longpoll = VkBotLongPoll(self.vk_auth, '179142825')
        keyboard = VkKeyboard(one_time=True)

        if current_menu == 'main_menu':
            keyboard.add_button('Tenses and moods', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('Conjugations', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('Word lookup', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('Daily Tasks', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('Excercises', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('Settings', color=VkKeyboardColor.POSITIVE)

        elif current_menu == 'tenses':
            keyboard.add_button('Past')
            keyboard.add_button('Present')
            keyboard.add_button('Future')
            keyboard.add_button('Back')

        elif current_menu == 'conjugations':
            keyboard.add_button('Back')

        elif current_menu == 'settings':
            keyboard.add_button('Send test message')
            keyboard.add_button('Send test file')
            keyboard.add_button('Back')



        if current_menu != 'main_menu':
            keyboard.add_line()
            keyboard.add_button('Return to main menu', color=VkKeyboardColor.POSITIVE)

        self.send_keyboard(keyboard = keyboard, message=self.current_menu)

        #self.send_keyboard(keyboard = keyboard) leave it here and delete others from all if clauses

        for event in longpoll.listen():
            if event.obj.text == 'Tenses and moods':
                self.previous_menu = 'main_menu'
                self.current_menu = 'tenses'
                self.run_longpoll()
                #current_menu='tenses'
            elif event.obj.text == 'Settings':
                self.previous_menu = 'main_menu'
                self.current_menu = 'settings'
                self.run_longpoll()
            elif event.obj.text == 'Conjugations':
                self.previous_menu = 'main_menu'
                self.current_menu = 'conjugations'
                self.run_longpoll()
            elif current_menu == 'conjugations' and event.obj.text and event.obj.text.startswith(('conj', 'Conj')):
                self.send_text(f'conjugator.reverso.net/conjugation-french-verb-{event.obj.text[5:]}.html')
                self.run_longpoll()
            elif current_menu == 'settings' and event.obj.text == 'Send test message':
                self.send_text('test message')
                self.run_longpoll()
            elif event.obj.text == 'Back':
                self.current_menu = self.previous_menu
                self.run_longpoll()
            elif event.obj.text == 'Return to main menu':
                self.current_menu = 'main_menu'
                self.run_longpoll()

## --------------------------------------------------------------

            if event.obj.text == 'question':
                self.send_text('answer')
                self.run_longpoll()
            elif event.obj.text == 'file':
                self.send_file('test.py')
                self.run_longpoll()
            elif event.obj.text == 'keyboard':
                self.send_text(keyboard)
                self.run_longpoll()
            elif event.obj.text and 'conjugate' in event.obj.text:
                verb = event.obj.text.split(' ')[-1]
                self.send_text(f'http://www.conjugation-fr.com/conjugate.php?verb={verb}&x=0&y=0')
                self.run_longpoll()


    def send_text(self, message):

        self.vk.messages.send(
            # peer_id = 97294531,
            domain = 'e_vlasov',
            random_id = int(random()*10000),
            message = message
        )

    def send_file(self, document_path, *args):
        '''
        Uploads a file then sends it
        Specify file tags as a list (tags=[one, two])
        not sure if tags are working though
        '''
        if args:
            tags = args
        else:
            tags = None

        uploaded_file_link = self.upload.document_message(
            peer_id = 97294531,
            title = document_path.split('/')[-1].split('.')[0],
            tags = tags,
            doc = document_path
        )

        owner_id = uploaded_file_link['doc']['owner_id']
        document_id = uploaded_file_link['doc']['id']

        self.vk.messages.send(
            domain = 'e_vlasov',
            random_id = int(random()*10000),
            message = None, ## -------------------------WORK ON IT
            attachment = f'doc{owner_id}_{document_id}'

        )

    def send_keyboard(self, **kwargs):

        if 'keyboard' in kwargs:
            keyboard = kwargs['keyboard']
        else:
            keyboard = VkKeyboard()

        if 'message' in kwargs:
            menu_name = kwargs['message']
            message = menu_names(menu_name)

        else:
            message = int(random()*10000)

        keyboard = keyboard.get_keyboard()

        self.vk.messages.send(
            peer_id = 97294531,
            random_id = int(random()*10000),
            keyboard = keyboard,
            message = message       ## use '&#13;' if you want to send empty messages
        )




if __name__ == '__main__':
    lstnr = Listener()
