"""
MIT License

Copyright (c) 2021 TheFarGG & TheGenocides

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .user import User
from typing import Optional, Dict, Any

class Tweet:
    """
    Represent a tweet message from Twitter.
    A Tweet is any message posted to Twitter which may contain photos, videos, links, and text.

    Parameters:
    ===================
    data: Dict[str, Any] -> The complete data of a tweet keep inside a dictionary.

    Attributes:
    ===================
    :property: author: Optional[User] -> Return a user (object) who posted the tweet.

    :property: text: str -> Return the tweet's text. 
    
    :property: id: int -> Return the tweet's id. 
    """
    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data['data']
    
    @property
    def author(self) -> Optional[User]:
        return User(self.original_payload.get("includes").get("users")[0])
    #)
    @property
    def text(self) -> str:
        return self._payload.get('text')

    @property
    def id(self) -> int:
        return self._payload.get('id')