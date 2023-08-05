from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer


def get_tone(text):
    tokenizer = RegexTokenizer()

    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    result = model.predict([text])[0]
    keys = ['negative', 'positive', 'neutral']
    for key in keys:
        result.setdefault(key, 0)

    result['tone'] = result['positive'] - result['negative']
    return result
