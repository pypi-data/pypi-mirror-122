import requests
from dataclasses import dataclass, field

import json
from attrify import Attrify


url = 'https://nksamamemeapi.pythonanywhere.com'




@dataclass(unsafe_hash=True)
class Meme():
    subreddit : str = field(init=True)

    if subreddit:
        url = url+"/get/{}".format(subreddit)

    else:
        url = url
    

    def random(self):
        res = requests.get(url).json()
        return Attrify(res)





if __name__ == "__main__":
    rand = Meme(
        "ProgrammerHumor"
    ).random()

    print(rand.title)
    print(rand.image)
    print(rand.reddit)
    

    """

    >>> Meme Returns 3 values 
    >>> title , image , reddit
    
    """



