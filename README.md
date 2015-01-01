Arrange-collections-for-your-account-in-zhihu.com
=================================================
People say that the importing of Quora.com gave rise to two portal sites. One is guokr.com, the other one is zhihu.com
Although the latter one came later, it grows much more fast than the formmer one, especially in recent years.
Users have been complaining about the poor function of collection folder function of zhihu.com for some time.
Together with its terrible searching capability, I have to say that the content of zhihu.com is so good that users could live with all these uncomfortable feeling instead of running away.

============================
This is my first complete script in python after learning for like one week. Since zhihu.com is poor in its collection function, I'm thinking maybe combine all the answers you have ever collected, whatever folder it is, in one webpage would be easy for search.

Some obstacles that I encountered:
1.Some folders may have been set as private folders which is only visitable by user alone. So you have to log in and use cookies.(cookies are not a must in this version of logging in)
2.Get Chinese charactors and displaying them without showing messy codes.
3.Repaired the bug when a collection folder has more than one pages.

功能及说明（Functions&instruction）：
1.Three modules are imported in the code. For the first two you need to install first.
2.该程序会生成两个网页文件mycollections.html和Answers.html，前者为您的收藏夹首页，后者即为所得的所有收藏回答合集，您可以直接用ctrl+f搜索
3.程序开始时会要求输入您的知乎账号信息
