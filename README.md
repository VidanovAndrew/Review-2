# Simple Tg news bot
It can parse, save and give user date
Parser use json queries from Parse_list.txt. You can try to add your own web pages
# It support commands
new_docs <N> - показать N самых свежих новостей
new_topics <N> - показать N самых свежих тем
doc <doc_title> - показать текст документа с заданным заголовком
words <topic_name> - показать 5 слов, лучше всего характеризующих тему. Алгоритм оценки слов выберите/придумайте сами
describe_doc <doc_title> - вывести статистику по документу. Статистика:
распределение частот слов 
распределение длин слов
<свой вариант, который по-вашему мнению полезно было бы знать>
describe_topic <topic_name> - вывести статистику по теме. Статистика: