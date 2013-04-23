Summarization
=

This is just a little code to play around with the approximate oracle score
sentence ranking algorithm for topic-oriented summarization.

J. Conroy, J. Schlesinger, and D. O'Leary, "Topic-Focused Multi-sentenceument
Summarization Using an Approximate Oracle Score," in *Proceedings of the COLING/ACL’06*.

```.py
import topic_oriented_summary as summary
import topic_signatures

>>> sents = ['This is a news article from NYTimes.', 
...      'This is a news article from AP.',
...      'This is a sports 49ers video.',
...      'This is a football soccer sports video.']

data = [('news',   (sents[0] + ' ' + sents[1]).split() * 100 ),
...     ('sports', (sents[1] + ' ' + sents[2]).split() * 100)]

sigs = topic_signatures.topic_signatures(data);

summary.summarize('news articles', sigs['news'], sents)
[(0.17741935483870969, 'This is a news article from AP.'),
 (0.15277777777777779, 'This is a news article from NYTimes.'),
 (0.1206896551724138, 'This is a sports 49ers video.'),
 (0.11538461538461539, 'This is a football soccer sports video.')]
```
