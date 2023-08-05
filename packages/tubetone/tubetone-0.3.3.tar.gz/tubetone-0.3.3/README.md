## Tone Tube

Analyzes youtube videos using [pytube](https://github.com/pytube/pytube)
, [transcripts](https://github.com/jdepoix/youtube-transcript-api)
and [dostoevsky](https://github.com/bureaucratic-labs/dostoevsky). Can save values into the db.

`pip install tonetube`

Then you'll need to download binary model for [dostoevsky](https://github.com/bureaucratic-labs/dostoevsky):
`python -m dostoevsky download fasttext-social-network-model`

See [tests](https://github.com/solovieff/text-anal/tree/master/tests) directory for more details.

Run to load the given playlist video tones:
`tubetone --id=PLL5fTqvjKv3JaH8SofJ89geu2VwJL5R04`

For environment variables,
see [constants file](https://github.com/solovieff/text-anal/blob/master/tubetone/constants.py).
