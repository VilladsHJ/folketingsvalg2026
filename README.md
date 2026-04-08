# folketingsvalg2026
An explorative analysis of agreement between candidates and their corresponding party. The analysis was done out of interest during the Danish parliamentary election in 2026.

The data was scraped from DR.DK own webpage (see ETL.py).

Some interesting findings were the huge outliers. Some were explained by simply not having answered the questions, thus having a score of the middle value (a value you cannot pick in the test)
Other candidates like Ali Qais were interesting findings. The answers were ~70% in line with his party. This is quite low considereing most other candidates.
Another intereting observations was that Mette Frederiksen, the sitting prime minister at the election was not present in the test. This was because she never took the test and was therefore skipped by the scraping algorithm.

Each answer was ranged either 1 (agree a lot), 2 (agree), 4 (disagree) or 5 (disagree alot). There was no middle (neutral) option. Thus the maximum distance a candidate could have was 4.

The method used to find agreeability with a party was the modal score and the averaage.
Modal score: The party's most common answer/score - or the 'democratic' answer for each party. If the score was tied between two answers the score was the average of the two answers. 
The average: The party's average answer/score for each question.

The agreeability score for each candidate was calculated as the sum of differences between the party's answer/score and the candidates answer/score for each question, divided by the maximum distance.

<img width="1315" height="737" alt="image" src="https://github.com/user-attachments/assets/da8230da-80f6-4471-adb5-2aab6d7c54fc" />
