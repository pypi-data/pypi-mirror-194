
# Chinese Moral Foundation Dictionary 2.0
----

Chinese Moral Foundation Dictionary 2.0 for Python.  This project was inspired by  https://github.com/civictechlab/cmfd

## Introduction
----
The Chinese Moral Foundation Dictionary 2.0 (C-MFD 2.0) is a dictionary to assist the automated moral intuition detection and analysis in the Chinese language context. Starting from the existing Chinese translation of the English MFD, two experts selected additional Chinese moral concepts and used word2vec to fetch related words from an extensive Chinese dictionary. Four experts went through four-rounds of coding, followed by the validation from 202 crowd coders. The CMFD identifies not only the classic five moral foundations but also several potentially novel moral foundation candidates.



## Team members
----
Devloped by Weiyu Zhang (National University of Singapore) and Yixiang Calvin Cheng (Oxford University), with assistance by Zhuo Chen (Shenzhen University), Yipeng Xi (Shanghai Jiaotong University), Haodong Liu (City University of Hong Kong) and Chuyao Wang (King's College London)



## Example
----

> text_test = """
> 她一见他就倾心， 但他却偏要为非作歹。 结果两人败俱伤， 她心碎， 他惨遭报应。
> 他本来是一个英勇战斗的将军， 但因为一纸空文， 被诬陷入狱。 再加上尔虞我诈的诡计， 他最终丧失了自己的荣誉和尊严。
> 他曾认为自己是无所不能， 却不知道一念之间， 一切都会化为乌有。 如果他当初没有欺骗她， 如果他当初没有撕毁那张契约， 也许他们现在还在幸福的生活中。
> 现在， 他身陷囹圄， 只能思念那些曾经的日子。 他懊悔不已， 只能悔恨自己的软弱和自私。 他希望能有机会改正错误， 重新取回自己的荣誉， 但现实却是那么残酷。"""

```python
import cmfd

result = cmfd.moral_quantity(text_test, duplicate=False, with_word=True)
print(result)  
```
  
> {'altr': {'num': 0.0, 'word': ''},
> 'auth': {'num': 0.21428571428571427, 'word': '荣誉;将军;都会'},
> 'care': {'num': 0.2857142857142857, 'word': '为非作歹;心碎;残酷;惨遭'},
> 'dili': {'num': 0.0, 'word': ''},
> 'fair': {'num': 0.2857142857142857, 'word': '一纸空文;报应;尔虞我诈;欺骗'},
> 'general': {'num': 0.07142857142857142, 'word': '幸福'},
> 'libe': {'num': 0.0, 'word': ''},
> 'loya': {'num': 0.07142857142857142, 'word': '英勇战斗'},
> 'mode': {'num': 0.0, 'word': ''},
> 'resi': {'num': 0.0, 'word': ''},
> 'sanc': {'num': 0.07142857142857142, 'word': '尊严'},
> 'wast': {'num': 0.0, 'word': ''}}