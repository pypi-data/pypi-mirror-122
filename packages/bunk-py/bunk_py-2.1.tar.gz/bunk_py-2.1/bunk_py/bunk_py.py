import requests
import datetime
import json

class Error(Exception):
    pass

class InvalidTokenOrUser(Error):
    pass

class BunkResult:
    def __init__(self,method,image,raw,title=None,subreddit=None,author=None,id=None,upvote=None,downvote=None,comments=None,nsfw=None,created_at=None,score=None):
        self.method = method
        self.title = title
        self.subreddit = subreddit
        self.author = author
        self.image = image
        self.id = id
        self.upvote = upvote
        self.downvote = downvote
        self.comments = comments
        self.nsfw = nsfw
        if created_at != None:
            self.created_at = datetime.datetime.fromtimestamp(float(created_at))
        self.score = score

class BunkAPI:
    def __init__(self,token,id,version=1):
        self.token = token
        self.id = id
        self.version = version
        self.credits = 'Created and Maintained by DaWinnerIsHere#1264.'

    def donkey(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/donkey/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='donkey',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def meme(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/meme/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='meme',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def llama(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/llama/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='llama',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def alpaca(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/alpaca/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='alpaca',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def giraffe(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/giraffe/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='giraffe',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def potato(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/potato/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='potato',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def aww(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/aww/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='aww',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def moose(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/moose/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='moose',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def camel(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/camel/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='camel',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def seal(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/seal/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='seal',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def elephant(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/elephant/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='elephant',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def zebra(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/zebra/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='zebra',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def amongus(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/amongus/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            title = x['data']['title']
            subreddit = x['data']['subreddit']
            author = x['data']['author']
            image = x['data']['image']
            id = x['data']['id']
            upvote = x['data']['ups']
            downvote = x['data']['downs']
            nsfw = x['data']['nsfw']
            comments = x['data']['comments']
            created_at = x['data']['createdUtc']
            score = x['data']['score']
            return BunkResult(method='amongus',title=title,subreddit=subreddit,author=author,image=image,id=id,upvote=upvote,downvote=downvote,comments=comments,nsfw=nsfw,created_at=created_at,score=score,raw=x)

    def space(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/space/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            image = x['image']
            return BunkResult(method='space',image=image,raw=x)

    def anime_wallpaper(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/anime-wallpaper/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            image = x['data']['title']
            image = x['data']['image']
            return BunkResult(method='anime_wallpaper',title=title,image=image,raw=x)

    def _8ball(self):
        x = requests.get(f'https://bunkapi.xyz/api/v{self.version}/8ball/{self.id}?token={self.token}')
        x = x.json()
        if x['status'] != 200:
            raise InvalidTokenOrUser
        else:
            return x['data']
