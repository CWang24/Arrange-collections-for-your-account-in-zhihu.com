Arrange-collections-for-your-account-in-zhihu.com
=================================================

My first complete script in python. Since zhihu.com is poor in its collection function, I'm thinking maybe combine all the answers in one webpage would be easy for search.

Note:
1.
import requests
import re
import os

Your need to import these three modules in your code. For the first two you need to install first.

2.
In line 10, enter your own account information.
This script will creat a file named Answers.html with all your answers from all your collections, and open this file with the last line.
If your don't want this file to be opened automatically, you could just comment the last line.
