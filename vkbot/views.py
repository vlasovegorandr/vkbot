from django.shortcuts import render
from vkbot.server import Listener
from threading import Thread

#def start_new_thread(function):
#    def decorator(*args, **kwargs):
#        thread = Thread(target=function, args=args, kwargs=kwargs)
#        thread.daemon = True
#        thread.start()
#    return decorator

def run_server(request):
    thread1 = Thread(target=Listener())
    thread1.start()
    thread2 = Thread(target=render(request, 'homepage.html'))
    #thread2.start()
    return thread2.start() 
    
    
