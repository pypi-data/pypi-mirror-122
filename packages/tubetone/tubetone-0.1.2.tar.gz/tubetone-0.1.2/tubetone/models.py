import inspect
import pprint
from dataclasses import dataclass, asdict
from typing import List


@dataclass()
class ToneInfo:
    playlist_id: str
    video_id: str
    publish_date: str
    tone: float

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass()
class AnalysisToneTube:
    video_id: str
    title: str
    playlist_id: str
    views: int
    publish_date: str
    author: str
    tone_analysis: dict
    morph_analysis: dict
    rating: float
    keywords: List[str]
    lang: str

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })

    def view_main(self):
        dict_to_view = asdict(self)
        pprint.pprint(dict_to_view)


@dataclass
class ToneTube(AnalysisToneTube):
    description: str
    url: str
    playlist_name: str
    transcript: List[dict]
    full_text: str

    def view_main(self):
        dict_to_view = asdict(self)
        dict_to_view.pop("full_text")
        dict_to_view.pop("transcript")
        dict_to_view.pop("description")
        pprint.pprint(dict_to_view)
