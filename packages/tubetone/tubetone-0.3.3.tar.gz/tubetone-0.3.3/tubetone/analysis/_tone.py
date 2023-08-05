from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer


def get_tone(text):
    tokenizer = RegexTokenizer()

    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    result = model.predict([text])[0]
    keys = ['negative', 'positive', 'neutral']
    for key in keys:
        result.setdefault(key, 0)

    result['tone'] = _calc_tone(math_result=result)
    return result


def _calc_tone(math_result: dict):
    sum = math_result['positive'] + math_result['negative']
    tone = math_result['positive'] - math_result['negative']
    return tone
