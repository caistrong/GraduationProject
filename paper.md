（一）前置部分
1. 封面
略
2. 诚信书
略
3. 致谢
在厦门大学软件学院四年学习生涯即将结束，这四年来，我不仅学习了很多有用的知识也丰富了很多人生的阅历。毕业设计是对我大学四年的一个很好的总结。在这里我首先要感谢我的指导老师高星老师、廖明宏老师，在我完成毕业论文的期间，悉心指导，为我提供了许多宝贵的改进意见。同时还应该感谢软件学院所有教导过我的老师，因为他们的辛勤授课，才帮助我打下了厚实的基础，得以完成这篇毕业论文。
4. 摘要和关键词

关键词：推荐系统、电影推荐、冷启动、协同过滤、推荐系统后台开发

摘要：
为了解决用户选择电影时的信息过载问题，更好地发掘电影库里的长尾。我基于成熟的协同过滤推荐算法，构建了一个电影推荐系统。每日为用户推荐一个电影列表。用户可以对推荐的结果进行反馈以辅助后台系统的协同过滤算法更好地去寻找相似用户，同时更好地完善电影相似度计算。以为后续提供更好的推荐结果。在一开始并不积累大量用户数据的时候，利用电影类别标签、热门排行榜等方式完成推荐系统的冷启动。电影推荐系统的服务端程序以Node.js作为开发语言，Node.js使用事件驱动的单线程Event Loop模型，可以满足互联网应用高并发，IO操作密集的需求，使得服务可以快速响应请求。同时使用了扩展性良好的web框架koa2，保证web服务有足够的灵活性。数据存储使用了开源且十分成熟的mysql，保证了服务的稳定性，数据的安全性等问题。前端使用了taro统一框架，可以保证一套代码多端运行，有效覆盖大多数用户。

5. 目录

（二）正文

（三）参考文献