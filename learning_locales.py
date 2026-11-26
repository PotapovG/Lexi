"""Localized learner-facing labels for the existing lesson and Life paths.

Greek source sentences and persistent card identities are unchanged.
Locale completeness is tested separately from independent linguistic review.
"""
LANGUAGES=("ru","en","zh","ar","es","pt")
_ROWS={
"book":("Учебник и фразы","Textbook and phrases","课本与短语","الكتاب والعبارات","Libro y frases","Manual e frases"),
"lexicon":("Слова главы","Chapter vocabulary","本章词汇","مفردات الفصل","Vocabulario del capítulo","Vocabulário do capítulo"),
"verb":("Глаголы в действии","Verbs in action","动词练习","الأفعال في الاستعمال","Verbos en acción","Verbos em ação"),
"grammar":("Грамматика","Grammar","语法","القواعد","Gramática","Gramática"),
"listening":("Слушаем греческий","Greek listening","希腊语听力","الاستماع إلى اليونانية","Comprensión oral en griego","Compreensão oral em grego"),
"dialogue":("Разговоры","Conversations","对话","المحادثات","Conversaciones","Conversas"),
"clock":("Часы и расписание","Time and schedules","时间与日程","الوقت والجداول","La hora y los horarios","As horas e os horários"),
"life":("Реальная жизнь","Everyday life","日常生活","الحياة اليومية","La vida cotidiana","A vida quotidiana"),
"review_chapters":("Повторение глав 1–4","Review chapters 1–4","复习第1–4章","مراجعة الفصول 1–4","Repaso de los capítulos 1–4","Revisão dos capítulos 1–4"),
"review_words":("Повторение слов","Vocabulary review","词汇复习","مراجعة المفردات","Repaso de vocabulario","Revisão de vocabulário"),
"phrase_practice":("Практика фраз","Phrase practice","短语练习","تدريب على العبارات","Práctica de frases","Prática de frases"),
"language_review":("Практика языка","Language practice","语言练习","تدريب لغوي","Práctica de lengua","Prática da língua"),
"word_review":("Повторение слов","Word review","单词复习","مراجعة الكلمات","Repaso de palabras","Revisão de palavras"),
"chapter_practice":("Практика главы","Chapter practice","本章练习","تدريب الفصل","Práctica del capítulo","Prática do capítulo"),
"dialogue_instruction":("Дополните выделенную реплику.","Complete the highlighted reply.","补全突出显示的回答。","أكمل الرد المحدد.","Completa la respuesta resaltada.","Completa a resposta destacada."),
"lexicon_review":("Запомни перевод; слово появится снова в повторении.","Review this meaning; the word will return.","记住这个意思；这个词会在复习中再次出现。","راجع هذا المعنى؛ ستعود الكلمة في المراجعة.","Repasa este significado; la palabra volverá en el repaso.","Revê este significado; a palavra voltará na revisão."),
"goal_book":("Понимать слова и фразы изученной главы.","Understand words and phrases from the studied chapter.","理解已学章节中的单词和短语。","فهم كلمات وعبارات الفصل المدروس.","Comprender palabras y frases del capítulo estudiado.","Compreender palavras e frases do capítulo estudado."),
"goal_lexicon":("Вспомнить значения уже изученных слов.","Recall the meanings of words already studied.","回忆已学单词的意思。","تذكّر معاني الكلمات التي سبق تعلمها.","Recordar el significado de las palabras ya estudiadas.","Recordar o significado das palavras já estudadas."),
"goal_verb":("Практиковать доступные формы глаголов.","Practise the verb forms introduced so far.","练习已经学过的动词形式。","التدرّب على صيغ الأفعال التي سبق تقديمها.","Practicar las formas verbales ya introducidas.","Praticar as formas verbais já introduzidas."),
"goal_grammar":("Применять знакомые языковые формы в контексте.","Apply familiar language forms in context.","在语境中运用熟悉的语言形式。","استخدام الصيغ اللغوية المألوفة في سياقها.","Aplicar formas lingüísticas conocidas en contexto.","Aplicar formas linguísticas conhecidas em contexto."),
"goal_listening":("Распознавать знакомые слова и фразы на слух.","Recognise familiar words and phrases by listening.","通过听力识别熟悉的单词和短语。","تمييز الكلمات والعبارات المألوفة عند سماعها.","Reconocer de oído palabras y frases conocidas.","Reconhecer palavras e frases conhecidas ao ouvi-las."),
"goal_dialogue":("Выбирать подходящие реплики в знакомых разговорах.","Choose appropriate replies in familiar conversations.","在熟悉的对话中选择合适的回答。","اختيار الردود المناسبة في المحادثات المألوفة.","Elegir respuestas adecuadas en conversaciones conocidas.","Escolher respostas adequadas em conversas conhecidas."),
"goal_clock":("Читать время и понимать знакомые расписания.","Read the time and understand familiar schedules.","读懂时间和熟悉的日程。","قراءة الوقت وفهم الجداول المألوفة.","Leer la hora y comprender horarios conocidos.","Ler as horas e compreender horários conhecidos."),
"goal_life":("Составлять короткие ответы для знакомых ситуаций.","Form short replies for familiar situations.","为熟悉的情境组织简短回答。","تكوين ردود قصيرة لمواقف مألوفة.","Formar respuestas breves para situaciones conocidas.","Formar respostas curtas para situações conhecidas."),
"accent_note":("Ответ засчитан. Обрати внимание на ударения: {correct}","Accepted. Note the accent marks: {correct}","答案已接受。请注意重音符号：{correct}","قُبلت الإجابة. انتبه إلى علامات النبر: {correct}","Respuesta aceptada. Fíjate en las tildes: {correct}","Resposta aceite. Repara nos acentos: {correct}"),
"wrong_form":("Здесь нужна форма «{wanted}», а не «{actual}». Проверь предлог, род или падеж.","Use «{wanted}» rather than «{actual}». Check the preposition, gender or case.","这里需要«{wanted}»，而不是«{actual}»。请检查介词、性或格。","الصيغة المطلوبة هنا هي «{wanted}» بدلًا من «{actual}». تحقّق من حرف الجر والجنس والحالة الإعرابية.","Aquí se necesita «{wanted}» en lugar de «{actual}». Comprueba la preposición, el género o el caso.","Aqui é preciso «{wanted}» em vez de «{actual}». Verifica a preposição, o género ou o caso."),
"plural_likes":("С несколькими предметами употребляется «αρέσουν».","Use «αρέσουν» for plural things.","表示多个事物时用«αρέσουν»。","استخدم «αρέσουν» مع الأشياء بصيغة الجمع.","Usa «αρέσουν» con cosas en plural.","Usa «αρέσουν» com coisas no plural."),
"singular_likes":("С одним предметом употребляется «αρέσει».","Use «αρέσει» for singular things.","表示单个事物时用«αρέσει»。","استخدم «αρέσει» مع الشيء بصيغة المفرد.","Usa «αρέσει» con una cosa en singular.","Usa «αρέσει» com uma coisa no singular."),
"typo":("Похоже, опечатка в слове «{actual}». Проверь написание: «{wanted}».","Likely a typo in «{actual}». Check the spelling: «{wanted}».","«{actual}»可能有拼写错误。请检查正确拼写：«{wanted}»。","يبدو أن هناك خطأً إملائيًا في «{actual}». تحقّق من كتابة «{wanted}».","Parece haber una errata en «{actual}». Comprueba la escritura: «{wanted}».","Parece haver um erro em «{actual}». Verifica a grafia: «{wanted}»."),
"missing_na":("Пропущена частица «να» перед глаголом.","The particle «να» is missing before the verb.","动词前缺少小品词«να»。","الأداة «να» مفقودة قبل الفعل.","Falta la partícula «να» delante del verbo.","Falta a partícula «να» antes do verbo."),
"missing_den":("Пропущено отрицание «δεν», и смысл стал противоположным.","Missing «δεν» changes the sentence into an affirmative.","缺少否定词«δεν»，句子变成了肯定句。","حذف أداة النفي «δεν» يحوّل الجملة إلى جملة مثبتة.","Al faltar «δεν», la frase se vuelve afirmativa.","A ausência de «δεν» torna a frase afirmativa."),
"extra_den":("Лишнее отрицание «δεν» меняет смысл фразы.","Extra «δεν» changes the sentence's meaning.","多余的否定词«δεν»改变了句子的意思。","إضافة «δεν» تغيّر معنى الجملة.","El «δεν» añadido cambia el significado de la frase.","O «δεν» a mais altera o significado da frase."),
"missing_article":("Перед этим словом нужна форма «{wanted}» — проверь предлог и артикль.","The form «{wanted}» is needed here. Check preposition and article.","这里需要«{wanted}»。请检查介词和冠词。","الصيغة «{wanted}» مطلوبة هنا. تحقّق من حرف الجر وأداة التعريف.","Aquí se necesita «{wanted}». Comprueba la preposición y el artículo.","Aqui é preciso «{wanted}». Verifica a preposição e o artigo."),
"unverified":("Этот вариант отличается от проверенных. Возможно, он допустим — не буду считать его грамматической ошибкой. Сравни с примером ниже.","This wording differs from reviewed options. It might be valid; no grammar mistake will be recorded. Compare the example below.","这个表达与已核实的答案不同，但可能正确；不会记为语法错误。请与下面的示例比较。","تختلف هذه الصياغة عن الإجابات التي تم التحقّق منها، وقد تكون صحيحة. لن تُسجَّل كخطأ نحوي. قارنها بالمثال أدناه.","Esta formulación difiere de las opciones revisadas y podría ser válida. No se registrará como error gramatical. Compárala con el ejemplo de abajo.","Esta formulação difere das opções revistas e pode ser válida. Não será registada como erro gramatical. Compara-a com o exemplo abaixo."),
"route":("Автобусные маршруты","Bus routes","公交路线","خطوط الحافلات","Rutas de autobús","Percursos de autocarro"),
"periptero":("Περίπτερο · магазин","Περίπτερο · mini market","Περίπτερο · 便利店","Περίπτερο · متجر صغير","Περίπτερο · quiosco","Περίπτερο · quiosque"),
"likes":("Мне нравится / не нравится","Likes and dislikes","喜欢与不喜欢","الإعجاب وعدم الإعجاب","Gustos y preferencias","Gostos e preferências"),
}
assert all(len(values)==len(LANGUAGES) for values in _ROWS.values())
TEXT={lang:{key:values[i] for key,values in _ROWS.items()} for i,lang in enumerate(LANGUAGES)}
def text(lang,key,**values):
    if lang not in TEXT:raise ValueError("invalid_language")
    return TEXT[lang][key].format(**values)

# Existing scenes, translations only: no Greek answer text is changed.
SCENE_LOCALES={
"meet":{
 "zh":("自我介绍","请介绍自己：“我叫玛丽亚”。","我叫玛丽亚。"),
 "ar":("التعارف","قدّم نفسك: «اسمي ماريا».","اسمي ماريا."),
 "es":("Conocer a alguien","Preséntate: «Me llamo María».","Me llamo María."),
 "pt":("Conhecer alguém","Apresenta-te: «Chamo-me Maria».","Chamo-me Maria.")},
"home_city":{
 "zh":("你住在哪里？","请说：“我住在尼科西亚”。","我住在尼科西亚。"),
 "ar":("أين تسكن؟","قل: «أسكن في نيقوسيا».","أسكن في نيقوسيا."),
 "es":("¿Dónde vives?","Di: «Vivo en Nicosia».","Vivo en Nicosia."),
 "pt":("Onde moras?","Diz: «Moro em Nicósia».","Moro em Nicósia.")},
"family":{
 "zh":("我的家人","请说：“我有一个兄弟”。","我有一个兄弟。"),
 "ar":("عائلتي","قل: «لديّ أخ واحد».","لديّ أخ واحد."),
 "es":("Mi familia","Di: «Tengo un hermano».","Tengo un hermano."),
 "pt":("A minha família","Diz: «Tenho um irmão».","Tenho um irmão.")},
"languages":{
 "zh":("语言","请说：“我会说希腊语”。","我会说希腊语。"),
 "ar":("اللغات","قل: «أتحدث اليونانية».","أتحدث اليونانية."),
 "es":("Idiomas","Di: «Hablo griego».","Hablo griego."),
 "pt":("Línguas","Diz: «Falo grego».","Falo grego.")},
"ticket":{
 "zh":("购买车票","请要一张去利马索尔的车票。","请给我一张去利马索尔的车票。"),
 "ar":("شراء تذكرة","اطلب تذكرة واحدة إلى ليماسول.","تذكرة واحدة إلى ليماسول، من فضلك."),
 "es":("Comprar un billete","Pide un billete a Limassol.","Un billete a Limassol, por favor."),
 "pt":("Comprar um bilhete","Pede um bilhete para Limassol.","Um bilhete para Limassol, por favor.")},
"daily":{
 "zh":("日常生活","请说：“我八点吃早餐”。","我八点吃早餐。"),
 "ar":("روتيني اليومي","قل: «أتناول الفطور في الساعة الثامنة».","أتناول الفطور في الساعة الثامنة."),
 "es":("Mi día","Di: «Desayuno a las ocho».","Desayuno a las ocho."),
 "pt":("O meu dia","Diz: «Tomo o pequeno-almoço às oito».","Tomo o pequeno-almoço às oito.")},
"groceries":{
 "zh":("购买食品","请要一公斤西红柿。","请给我一公斤西红柿。"),
 "ar":("شراء المواد الغذائية","اطلب كيلوغرامًا واحدًا من الطماطم.","كيلوغرام واحد من الطماطم، من فضلك."),
 "es":("La compra","Pide un kilo de tomates.","Un kilo de tomates, por favor."),
 "pt":("As compras","Pede um quilo de tomates.","Um quilo de tomates, por favor.")},
"clothes":{
 "zh":("购买衣服","请说：“我想要这条连衣裙”。","我想要这条连衣裙。"),
 "ar":("شراء الملابس","قل: «أريد هذا الفستان».","أريد هذا الفستان."),
 "es":("Comprar ropa","Di: «Quiero este vestido».","Quiero este vestido."),
 "pt":("Comprar roupa","Diz: «Quero este vestido».","Quero este vestido.")},
"directions":{
 "zh":("房子在哪里？","请说：“房子在市中心附近”。","房子在市中心附近。"),
 "ar":("أين المنزل؟","قل: «المنزل قريب من وسط المدينة».","المنزل قريب من وسط المدينة."),
 "es":("¿Dónde está la casa?","Di: «La casa está cerca del centro».","La casa está cerca del centro."),
 "pt":("Onde fica a casa?","Diz: «A casa fica perto do centro».","A casa fica perto do centro.")},
"cafe":{
 "zh":("点咖啡","请礼貌地点一杯咖啡。","我想要一杯咖啡，谢谢。"),
 "ar":("طلب قهوة","اطلب قهوة واحدة بأدب.","أودّ قهوة واحدة، من فضلك."),
 "es":("Pedir un café","Pide un café con cortesía.","Quisiera un café, por favor."),
 "pt":("Pedir um café","Pede um café de forma educada.","Queria um café, por favor.")},
"plans":{
 "zh":("周末计划","请说：“我喜欢散步”。","我喜欢散步。"),
 "ar":("خطط عطلة نهاية الأسبوع","قل: «أحبّ المشي».","أحبّ المشي."),
 "es":("Planes para el fin de semana","Di: «Me gusta pasear».","Me gusta pasear."),
 "pt":("Planos para o fim de semana","Diz: «Gosto de passear».","Gosto de passear.")}
}
def scene_text(scene,field,lang):
    if lang not in LANGUAGES:raise ValueError("invalid_language")
    if field not in ("name","prompt","translation"):raise ValueError("invalid_scene_field")
    if lang=="ru":return scene[field]
    if lang=="en":return scene[{"name":"en","prompt":"promptEN","translation":"translationEN"}[field]]
    return SCENE_LOCALES[scene["id"]][lang][("name","prompt","translation").index(field)]
