

def menu_names(name):
    menu_names = {
        'main_menu': "French bot homepage. Anything I can help you with?",
        'conjugations': "To see a verb's conjugation write 'conj' + verb infinitive (e.g. 'conj manger')",
        'tenses': "List of french tenses and moods",
        'daily_tasks': "Your task for the day",
        'word_lookup': "Find word definitions and translations",
        'excercises': "Practice makes perfect",
        'settings': "Edit your preferences"
    }
    yield menu_names[name]
