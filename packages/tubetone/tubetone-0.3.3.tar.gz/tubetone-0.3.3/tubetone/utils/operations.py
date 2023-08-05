def eyesore(string_to_check):
    eyesores = ['музыка', 'апплодисменты']
    for text in eyesores:
        if (string_to_check.find(text) == True):
            return True
    return False
