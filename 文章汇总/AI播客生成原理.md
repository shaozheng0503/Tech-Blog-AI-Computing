# AI 播客原理解析

最近看到一个一篇很好的文章：《The Prompt Engineering Playbook for Programmers》，不过太长了一点，完整看完要不少时间，所以我直接把链接直接发给豆包的 AI 播客，直接就生成了一篇高质量播客，几乎没有等待，当时就可以收听。AI 是如何把一篇文章变成语音播客的？🧵（1/n）

文章地址：https://addyo.substack.com/p/the-prompt-engineering-playbook-for
生成这条播客的会话：https://doubao.com/thread/wd27f5d2b3a01ab6b

播客有个好处就是你不占用你的眼睛和手，开车、遛狗这样在外面的时间就捎带着把它听完了，能帮我快速了解了文章的主要内容，又可以充分利用在外面的碎片时间。

我还经常把晦涩难懂的论文生成 AI 播客，通过两个人一问一答的模式，其中一个 AI 角色总能提出我关心的问题，而另一个 AI 又能很浅显易懂甚至生动有趣的解答问题，这种对话形式能很快帮我了解论文的要点，而且比起 AI 直接生成的文字摘要，要生动有趣多了。

以前我用 NotebookLM 多一些，最近主要用豆包的 AI 播客，相对来说中文语音听起来更自然，生成速度也快，生成后不需要等马上就能听了。

AI 是如何把一篇文章变成很逼真的真人对话式的语音播客的

可能你会好奇，AI 是如何把一篇文章变成很逼真的真人对话式的语音播客的？

这里面有两个核心技术，一个是提示词工程，一个是文字转语音技术。

如果简化一下，整体架构大概是下图这样：
1. 用户输入一个 URL 或者 上传 PDF，借助工具把输入解析成文本
2. 借助提示词和语言模型把输入的文本内容变成对话形式的播客脚本
3. 生成的播客脚本要做一次安全检查，避免有政治敏感、暴力色情等内容
4. 使用文本生成语音模型把生成的播客脚本生成播客音频

从技术实现看似乎也不复杂，但每一个环节细节都蛮多的：
1. 要根据用户的输入，完整的抓取内容、对网页内容、PDF 内容要做好解析，避免遗漏重要信息

2. 生成对话脚本时：
- 要模拟出两个不同的角色，一个热情讲述，一个冷静分析，很想说相声时的捧哏与逗哏两个角色
- 要能抓住文章的要点，根据文章内容生成客观中立，又有趣的洞见
- 能引发听众的思考，甚至能采取行动，收获认知上的价值，产生啊哈的顿悟感

3. 要保证生成内容的安全，无论是海外还是国内，都对内容安全性很敏感，不会让用户绕过模型限制生成政治敏感、暴力色情的内容，这方面一直就像猫鼠游戏，用户总是在想各种办法绕过限制，而平台必须确保没有不安全的内容

4. 最后就是文本生成语音，虽然现在文本生成语音技术也不稀奇，甚至有些泛滥，但是要想模拟出播客那种一唱一和自然的对话效果，也没那么容易，即使是 Google、OpenAI 这些顶尖的 AI 公司，在中文的效果上都比较声音，这方面反倒是国内模型公司要做的好得多，像豆包的 AI 播客，已经听不太出来是 AI 生成的感觉。

这里面我还是重点分析一下 AI 播客在生成播客对话时用到的提示词，这部分相对好理解，另外还能应用上，其他技术虽然也很牛，但是相对比较复杂，我们一般也用不上，需要的时候用现成的服务就好了。（2/n）


如何使用提示词把文本生成播客脚本？

提示词是我们用来控制 AI 帮我们完成任务的指令，可以理解为给 AI 的说明书。好比你现在是导演，你要做一起播客，那么你先要让编剧去根据话题来写脚本，提示词就相当于给编剧的说明书，让他们知道该怎么去写播客的脚本。

让我们从简单的提示词开始，看怎么写出相对专业的提示词。

1. 简单直接版本

比如我刚看到有一篇文章《GitHub CEO: manual coding remains key despite AI boom》https://techinasia.com/news/github-ceo-manual-coding-remains-key-despite-ai-boom 值得看看，我们把它变成播客的形式。

****

{文章内容文本}

请基于上面的文章，写成一篇两人对话博客的形式，输出为播客脚本。

***

（参考图1，完整会话链接：https://doubao.com/share/doc/8feb6cad3aff3c80 ）

基于这样的版本， AI 就能帮我生成一份还不错的脚本了。优点是提示词简单，缺点是内容完全取决于 AI 自己的发挥，有时候风格不一定是我们想要的，我们可以基于它增加一些控制，让它更有趣，读者听了有收获。
（3/n）


2. 设定对话的角色和目标

在上一个版本基础上，为了让我们的播客更吸引人，可以给提示词加上一些具体要求，比如：
- 说明播客的听众是谁，比如是普通人、小学生、专业人士，那么生成的结果会不一样
- 播客对话时，两位主播的角色有什么不同，让说的内容更有特色
- 我们希望播客传递什么样的价值，让听众有什么收获

=== 参考提示词开始 ===

请基于上面的文章，写成一篇两人对话博客的形式，输出为播客脚本。

目标听众

- 听众渴望高效学习，又追求较深入的理解和多元视角。
- 易感到信息过载，需要协助筛选核心内容，并期待获得“啊哈”或恍然大悟的时刻。
- 重视学习体验的趣味性与应用价值。

角色定义：

- 创建两位不同风格主播：主播1（引导者）和主播2（分析者）。

1. 引导者（Enthusiastic Guide）
- 风格：热情、有亲和力，善于使用比喻、故事或幽默来介绍概念。
- 职责：
  - 引起兴趣，突出信息与“你”的关联性。
  - 将复杂内容用通俗易懂的方式呈现。
  - 帮助“你”快速进入主题，并营造轻松氛围。

2. 分析者（Analytical Voice）
- 风格：冷静、理性，注重逻辑与深度解析。
- 职责：
  - 提供背景信息、数据或更深入的思考。
  - 指出概念间的联系或差异，保持事实准确性。

关键目标：
- 高效传递信息：在最短的时间内给听众（“你”）提供最有价值、最相关的知识。
- 深入且易懂：兼顾信息深度与可理解性，避免浅尝辄止或过度专业化。
- 保持中立，尊重来源：严格依照给定的材料进行信息整理，不额外添加未经验证的内容，不引入主观立场。
- 营造有趣且启发性的氛围：提供适度的幽默感和“啊哈”时刻，引发对信息的兴趣和更深的思考。
- 量身定制：用口语化、直呼“你”的方式，与听众保持近距离感，让信息与“你”的需求相连接。

=== 参考提示词结束 ===

（效果参考图 1，完整对话：https://doubao.com/thread/wa36c2f7f2bfb2685）

再看看新版，是不是就生动有趣多了，甚至还能给你编段子：
> 连我家楼下卖煎饼的大爷都问我：“小伙子，AI 能帮我写摊饼机器人的程序不？”

因为现在 AI 知道你这的播客是要讲给谁听的，该给用户传递什么样的价值，每个主播在对话中如何分工扮演好各自的角色。
（4/n）



3. 增加约束和输出格式要求

上面的提示词如果你多运行几次，可能会发现随机性比较大，有时候特别好，有时候主播会有些话唠，会衍生出文章没有的观点，有时候不经意还会把对方称呼为“引导者”、“分析者”这样提示词内的角色，这样就会给听众不专业的感觉。

那么我们可以在前面提示词的基础上增加一些约束，比如：
- 始终聚焦核心观点，删除冗余内容，防止啰嗦或离题，有条理地呈现信息，避免对听众造成信息过载。
- 严格基于给定材料：所有观点、事实或数据只能来自用户提供的来源文本。
- 面对矛盾观点：如来源材料出现互相矛盾的说法，需中立呈现，不评判、不选边
- 强调与听众的关联性：在信息选择与呈现时，关注哪些点可能对“你”最有用或最有启发。

另外如果这个结果是给人看的，那么我们不需要特别指定输出的格式，但如果我们是需要程序解析，还需要将输出结果指定为容易解析的 xml 格式，解析后调用文本转语音的 API 就可以直接生成音频，这样可以让整个过程自动化。

（继续完善后的提示词参考图1，完整对话：https://doubao.com/share/doc/ecac38b0275022ff）

（5/n）



如果用户上传的内容很长，是怎么处理的呢？

可能还有人会问，如果用户上传的内容很长，是怎么处理的呢？

这需要借助长文摘要技术，比如像下图这样先按照章节对内容分块，然后对每一块进行摘要，最后合并在一起，就可以保证抓住文章主要信息而不会让内容太长。当然还有其他技术这里就不一一介绍了，LangChain 有一篇《Summarize Text》https://python.langchain.com/docs/tutorials/summarization/ 把各种摘要结束都介绍了一下，可以参考。

最后

当然上面的提示词只是作为一个参考，你可以根据自己的需要做出调整，重点是向以这个为例，分享一下提示词写作和优化的过程：
从简单开始，先让它能工作
提供更完整的上下文和要求，让它知道目标听众、任务目标这些信息
进一步完善，添加约束，让结果不至于太发散，可以稳定的输出想要的结果

如果你还没有试过 AI 播客，可以自己试试看，如果你自己做播客，也可以试试用上面的提示词去把一篇文章让 AI 帮你生成播客脚本。

我自己常用的播客产品：
豆包 AI 播客：更适合中文用户，中文效果自然 https://doubao.com
Google NotebookLM：最早的 AI 播客产品 http://notebooklm.google

（n/n）