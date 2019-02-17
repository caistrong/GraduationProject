# 基于协同过滤的电影推荐系统🎬

## 推荐算法基本思想

### 用户行为数据

1. 小明喜欢了《指环王》 于2019-01-01
2. 小明喜欢了《哈利波特》 于2019-01-02
3. 小明喜欢了《神探夏洛克》 于2019-01-02
4. 小红喜欢了《哈利波特》 于2019-01-02
5. 小红喜欢了《肖申克的救赎》 于2019-01-02
6. 小蓝喜欢了《肖申克的救赎》 于2019-01-02
7. 小聪喜欢了《哈利波特》 于2019-01-03
8. 小聪喜欢了《指环王》 于2019-01-03

小明|小红|小蓝|小聪
---|----|----|----
哈利波特   | 哈利波特    | 肖申克的救赎  |  哈利波特
指环王     | 肖申克的救赎 |             |  指环王
神探夏洛克 |            |             |

### 系统为小聪推荐电影的运算逻辑(基于用户的协同过滤)

上面用户行为数据存储成类似如下结构

```js
let behavior_store = [
   {
      person: '小明',
      movie: '《指环王》',
      time: '2019-01-01'
   }
   //...
]
// behavior_store.findBehaviorOfUser('小聪') = { person: '小聪', movie: '《哈利波特》', time: '2019-01-03' },{ person: '小聪', movie: '《指环王》', time: '2019-01-03' }
```

#### 找出与小聪在喜欢的电影上有联系的相关人

简化伪代码如下:

```js
let relates = {};
for(let behavior_x of behavior_store.findBehaviorOfUser('小聪')) { 
   for(let behavior_y of behavior_store.findBehaviorAbout(behavior_x.movie)) {
      if(relates[person] === undefined) {
         relates[person] = {
            person: behavior_y.person,
            movie: [behavior_y.movie],
            last_actioned_at: behavior_y.time
         }
      } else {
         relates[person]['movie'].push(behavior_y.movie)
      }
   }
}
// relates处理成如下:
/* 
   [{
      person: '小聪',
      movie: ['哈利波特', '指环王'],
      last_actioned_at: '2019-01-03'
   },
   {
      person: '小明',
      movie: ['哈利波特', '指环王'],
      last_actioned_at: '2019-01-02'
   },
   {
      person: '小红',
      movie: ['哈利波特'],
      last_actioned_at: '2019-01-02'
   }]
*/
```

#### 计算小聪与相关人的余弦相似性

简化伪代码如下:

```js
let similarities = {};
let relatedPeople = relates.map( r => r.person) // ['小聪','小明','小红']
for(let p of relatedPeople) {
   let behaviors_1 = behavior_store.findBehaviorOfUser('小聪'); // 取出小聪的所有行为
   let behaviors_2 = behavior_store.findBehaviorOfUser(p);// 取出待计算相关人的所有行为
   let p1_values = {}; 
   for(let b of behaviors_1) {
      p1_values[b.movie] = calculateWeights(b); // 用户行为的每一部电影的权重不应该一样，比如很久之前喜欢的电影要比最近喜欢的电影权重小,具体计算方法这里略去，假设都返回1
   }// p1_values = { '哈利波特':1 , '指环王': 1}
   let p2_values = {}; // temp data
   for(let b of behaviors_2) {
      p2_values[b.movie] = calculateWeights(b); 
   } // p2_values = { '哈利波特':1 , '指环王': 1, '神探夏洛克': 1} 小明
   let numerator = 0; // 分子
   for (value in p1_values) {
      weight = p1_values[value];
      if (p2_values[value]) { // 相关人小明也喜欢这部电影
         numerator += weight * p2_values[value];
      }
   } // numerator = 2 

   let denominator_1 = 0;
   for (value in p1_values) {
      weight = p1_values[value];
      denominator_1 += Math.pow(weight, 2);
   } // denominator_1 = 1^2 + 1^2 =2

   let denominator_2 = 0;
   for (value in p2_values) {
      weight = p2_values[value];
      denominator_2 += Math.pow(weight, 2);
   } // denominator_2 = 1^2 + 1^2 + 1^2 =3
   const cosinse_similarity = numerator / (Math.sqrt(denominator_1) * Math.sqrt(denominator_2)); // cosinse_similarity = 0.81649658
   // TODO: 文档补上余弦相似度的计算公式
   similarities[p] = cosinse_similarity
}
// similarities处理成如下:
/* 
   {
      '小聪': 1
      '小明': 0.81649658
      '小红': 0.70720678
   }
*/
```

#### 找出所有相关人的所有行为中小聪还没喜欢过的电影

这一步和上一步无先后关系，可以并发进行

简化伪代码如下:

```js
let all_behaviors = [];
let relatedPeople = relates.map( r => r.person) // ['小聪','小明','小红']
for(let p of relatedPeople){
   let behaviors = behavior_store.findBehaviorOfUser(p);// 取出某个相关人的所有行为
   all_behaviors.concat(behaviors)
}
let all_movies = [...new Set(all_behaviors.map(b => b.movie))] // 将所有行为中含有的电影提取出来，并且做unique
let filtered_movies = all_movies.filter(movie => !moviesLikeByUser.includes(movie)) // 过滤掉小聪已经喜欢过的电影 ['肖申克的救赎', '神探夏洛克']

let recommendations = []

for(let b of all_behaviors) {
   if(filtered_movies.includes(b.movie)){
      recommendations.push(b)
   }
}

// recommendations 处理如下：
/* 
   [
      { person: '小明', movie: '《神探夏洛克》', time: '2019-01-02' },
      { person: '小红', movie: '《肖申克的救赎》', time: '2019-01-02' }
   ]
*/
```

#### 根据用户相似度整理推荐数据

简化伪代码如下:

```js
let recommendations_group = {}
for(let rec of recommendations) {
   if(recommendations_group[rec.movie] === undefined) {
      recommendations_group[rec.movie] = {
         movie: rec.movie,
         weight: 0,
         people: []
      }
   }
   recommendations_group[rec.movie].people.push(rec.person) // 可能会有电影是来自多个人的推荐
   recommendations_group[rec.movie].weight += similarities[rec.person]; // 电影推荐的权重来自与有多少个与该用户具有相似度的和
}
const recommendations_list = recommendations.sort((x, y) => y.weight - x.weight);

// 除此之外还有一个计算confidence，也就是对推荐有多少信心的逻辑，这里省略

// recommendations_list 处理如下：
/* 
   [
      { movie: '《神探夏洛克》', people: ['小明'], weight: 0.81649658 },
      { movie: '《肖申克的救赎》', people: ['小红'], weight: 0.70720678 },
   ]
*/
```

### 系统为小聪推荐电影的运算逻辑(基于物品的协同过滤)

除了上面通过找与用户相似度高的用户来推荐电影的方式外，还可以通过为用户喜欢过的电影找与该电影相似度高的电影来推荐给用户。其中电影相似度的计算与上述用户相似度的计算方式一模一样。上述计算用户相似度的方式总结起来说就是依据用户共同喜好的电影的多寡。而电影相似度的计算方式来自于被同一个用户喜欢的多寡。本质上是一样的。这里就不重复具体的计算方式了。

