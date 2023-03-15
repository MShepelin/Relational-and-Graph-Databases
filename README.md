### Домашнее задание по графовым базам данных

Шепелин Дмитрий БМПИ-1910

#### Описание задачи

В этом домашнем задании предлагается сравнить работу графовых баз данных и реляционных баз данных на примере анализа французского словаря с помощью SQL в SQLite и Cypher в neo4j.

#### Решение

1. ER-диаграмма и диаграмма отношений (2 балла)

   ![Diagrams](C:\Users\shepe\PythonProj\PSem\Diagrams.png)

2. Реализация наполнения баз реляционной БД и графовой БД (2 балла)

   В обеих базах данных для наполнения используются следующие запросы, написанные на SQL и Cypher соответственно:

   1. Команды в файлах CreateTables инициализируют таблицы и ограничения. Подразумевается, что совершенно БД пустая.
   2. Команды из генератора добавляют все информацию о слове. Начинаются команды с вставки букв из выбранного слова.
   3. Следующая команда добавляет отношение связи диакритических символов с их базовыми версиями символов.
   4. Для добавления самого слова в БД используется отдельная команда. В случае с SQLite также добавляется связь с последним символов слова, в случае с neo4j эта связь добавляется отдельной командой.
   5. Для каждой пары соседних символов в слове добавляется соответствующая связь, которая описывает, что символы идут друг за другом. Это отношение в обеих БД неуникально, иными словами между двумя символами может быть сколько угодно таких связей, что поможет посчитать частоту их следования друг за другом.
   6. Последние команды отвечают за добавление связи вхождения буквы в слово.

   В дополнение к этому:

   - Для реализации на Python написаны автотесты с помощью pytest.
   - Для вставки данных в графовой БД учтена уникальность элементов. Например, если буква 'à' уже есть в БД, она повторно вставлена не будет. То же касается и неповторяющихся отношений EndsWith, Contains, IsDiactricOf.

3. Запросы, отвечающие на вопросы предметной области к разным БД (2 балла).

   По полученным данным можно ответить на вопросы: 

   - Какие пары символов встречаются наиболее часто?

     ```sql
     -- SQL Query
     SELECT first_letter, unicode as second_letter, count_pairs 
     FROM (SELECT unicode as first_letter, count_pairs, letter_after_id 
     	FROM (SELECT letter_before_id, letter_after_id, count(*) as count_pairs
     		FROM (SELECT * FROM GoesAfter 
             	UNION ALL 
                 SELECT letter_after_id, letter_before_id 
                 FROM GoesAfter)
     		WHERE letter_before_id <= letter_after_id 
     		GROUP BY letter_before_id, letter_after_id
     		ORDER BY -count_pairs
     		LIMIT 3) AS Top 
         LEFT JOIN Letter 
         ON Top.letter_before_id=Letter.letter_id) AS Top2 
     LEFT JOIN letter 
     ON Top2.letter_after_id=Letter.letter_id
     ```

     Это самый сложный запрос, поэтому приведем пример выхода

     | first_letter | second_letter | count_pairs |
     | ------------ | ------------- | ----------- |
     | e            | ç             | 3           |
     | ç            | à             | 3           |
     | a            | b             | 2           |

     ```cypher
     // Cypher Query
     MATCH (a:Letter)-[:GoesAfter]-(b:Letter) 
     WHERE a.unicode <= b.unicode 
     RETURN a.unicode AS first_letter, b.unicode AS second_letter, COUNT(*) AS count_pairs
     ORDER BY -count_pairs
     LIMIT 3
     ```

   - Какие буквы встречаются наиболее часто в французских словах?

     ```sql
     -- SQL Query
     SELECT unicode, count_words 
     FROM (SELECT letter_id, COUNT(*) AS count_words
          FROM Contains 
          GROUP BY letter_id 
          ORDER BY -count_words
          LIMIT 3) AS Top
     LEFT JOIN Letter 
     ON Top.letter_id=Letter.letter_id
     ```

     ```cypher
     // Cypher Query
     MATCH (w:WordCore)-[:Contains]->(a:Letter) 
     RETURN a.unicode, COUNT(*) AS count_words 
     ORDER BY -count_words 
     LIMIT 3 
     ```

   - Какова средняя длина слов?

     ```sql
     -- SQL Query
     SELECT AVG(length) AS mean_length FROM WordCore
     ```

     ```cypher
     // Cypher Query
     MATCH (w:WordCore) RETURN AVG(w.length) AS mean_length
     ```

   - Какое окончание (последняя буква) характерно для длинных слов (с длинной больше средней)? В примере средняя длина слова 6, но вместо этого числа можно вставить запрос выше

     ```sql
     -- SQL Query
     SELECT unicode as letter, count_words 
     FROM (SELECT last_letter_id, COUNT(*) AS count_words 
           FROM (SELECT word_id, last_letter_id 
                 FROM WordCore 
                 WHERE WordCore.length >= 6) 
           GROUP BY last_letter_id 
           ORDER BY -count_words
           LIMIT 3) AS Top
     LEFT JOIN Letter
     ON Top.last_letter_id=Letter.letter_id
     ```
     
     ```cypher
     // Cypher Query
     MATCH (word:WordCore)-[:EndsWith]->(letter:Letter) 
     WHERE word.length >= 6 
     RETURN letter.unicode AS letter, COUNT(*) AS count_words
     ORDER BY -count_words
     LIMIT 3
     ```

4. Оформление работы и представление выводов и результатов (1 балл).

   - Результаты представлены в виде репозитория на GitHub.
   - В README описаны запросы к обеим БД.
   - В коде генерации запросов добавлены комментарии с объяснениями.

5. Сравнительный анализ реляционной и графовой модели в контексте
   используемой предметной области (1 балл).

   Для данной предметной области удобнее использовать графовые БД. Во-первых, графовые БД проще поддерживают уникальные элементы и прочие ограничения (ключевое слово CONSTRAINT). К тому же они  легче поддерживают большое число уникальных связей между словами. Например, так можно добавить связи однокоренных слов или построить цепочки происхождения слов.

   К тому же в контексте NLP большую популярность набирают глубинные нейросети на графовых данных, которые анализируют графы знаний в том числе с пропущенными данными (см. графы знаний, transE, эмбеддинг нод, Graph Convolutional Networks). Для таких моделей представление данных в виде реляционных таблиц не характерно.

   Дополнительным преимуществом является краткость записи запросов к БД. Конечно, это не имеет прямого отношения к производительности, но все равно является преимуществом для читабельности.

