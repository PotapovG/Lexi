"use strict";
(() => {
  const $ = id => document.getElementById(id);
  const STORAGE="lexi-greek-v2";
  const I18N={
   ru:{
    brand:"Мой греческий",pagesLabel:"страниц",language:"Язык интерфейса и перевода",
    eyebrow:"ВАШ ЛИЧНЫЙ ТРЕНАЖЁР",headline1:"Знания",headline2:"на всю жизнь.",
    intro:"Слова и формы, фразы и предложения. Выбирай пройденные страницы или главы — ошибки станут следующим занятием.",
    accuracy:"Точность",allAnswers:"все ответы",reviewDue:"К повторению",cards:"карточек",
    practice:"Занятие",myMistakes:"Мои ошибки",statistics:"Статистика",
    settings:"НАСТРОЙКА ЗАНЯТИЯ",whatPractice:"Что учим сегодня?",
    chooseInfo:"Выбери страницы или конкретные главы. Переводы — из восьми вариантов, ударения — нажатием на букву.",
    scope:"Охват учебника",pagesMode:"По страницам",chaptersMode:"По главам",
    fromPage:"С страницы",toPage:"По страницу",
    pageDisclaimer:"Авторские упражнения по темам учебника. Страницы карточек указаны ориентировочно; границы глав — по оглавлению.",
    selectAll:"Выбрать все",clearAll:"Снять выбор",only:"Только",material:"Материал",
    words:"Слова",numbers:"Числа",phrases:"Фразы",sentences:"Предложения",
    plurals:"Множественное число",alphabet:"Алфавит",accent:"Ударения",
    sessionLength:"Продолжительность",minutes:"мин",
    mixedDirections:"Переводы: греческий ↔ русский/английский. Ударения: выбор буквы.",
    pluralNotice:"ⓘ Множественное число доступно как отдельная дополнительная практика.",
    start:"Начать занятие",keyboard:"Клавиши 1–8 · Enter — дальше",finishNow:"Завершить",
    next:"Следующая →",complete:"ЗАНЯТИЕ ЗАВЕРШЕНО",anotherSession:"Новое занятие ↗",reviewMistakes:"Повторить ошибки",
    answers:"Ответов",correctAnswers:"Верных",streak:"Серия",byChapter:"ПО ГЛАВАМ",
    whereStrong:"Что уже получается",byType:"ПО ТИПАМ",whereWeak:"Что стоит повторить",
    last14:"ПОСЛЕДНИЕ 14 ДНЕЙ",history:"История занятий",
    privacy:"История хранится на сервере и привязана к анонимной сессии этого браузера. На другом устройстве статистика отдельная.",
    weakHeading:"РАБОТА НАД ОШИБКАМИ",weakTitle:"Повторяем то, что не получилось.",
    weakInfo:"Карточки с ошибками возвращаются сюда. Два правильных повтора закрывают ошибку. Направления и языки учитываются отдельно; выбор страниц и типов сохраняется.",
    weakCount:"ошибочных карточек всего",weakStart:"Тренировать ошибки →",
    footer:"Авторские задания по Ελληνικά Α΄ · 20 разделов · 312 страниц",
    loading:"Загрузка...",noCards:"В выбранном диапазоне пока нет карточек. Расширь страницы, главы или типы.",
    noWeak:"В выбранном диапазоне незакрытых ошибок нет.",
    none:"Нет ответов",noHistory:"Пока занятий нет.",right:"✓ Верно!",
    wrong:"✗ Неверно. Правильный ответ: ",queued:" · Записано в повторение.",
    failed:"Не удалось сохранить ответ: ",retry:" Попробуй ещё раз.",
    excellent:"Πολύ καλά! Отлично.",good:"Хороший результат!",practiceMore:"Есть что повторить.",
    result:"Правильно: {good} из {total} ({pct}%). Время: {minutes} мин.",
    session:"ТРЕНИРОВКА",weakSession:"ПОВТОР ОШИБОК",
    chapter:"Глава",review:"Повторение",alphabetName:"Алфавит",appendix:"Приложение",
    errorNoTypes:"Выбери хотя бы один тип материала.",errorNoChapters:"Выбери хотя бы одну главу.",
    available:"{count} карточек в библиотеке",timeOver:"Время занятия истекло.",
    pauseNo:"Занятие идёт по таймеру; переключать язык можно после завершения."
   },
   en:{
    brand:"My Greek",pagesLabel:"pages",language:"Interface and translation language",
    eyebrow:"YOUR PERSONAL LANGUAGE TRAINER",headline1:"Greek that",headline2:"stays with you.",
    intro:"Words, forms, useful phrases and sentences. Choose textbook pages or chapters and revisit your mistakes.",
    accuracy:"Accuracy",allAnswers:"all answers",reviewDue:"To review",cards:"cards",
    practice:"Practice",myMistakes:"My mistakes",statistics:"Statistics",
    settings:"SESSION SETTINGS",whatPractice:"What will you study today?",
    chooseInfo:"Pick page ranges or individual chapters. Translations use eight choices; accents use letter selection.",
    scope:"Textbook coverage",pagesMode:"By pages",chaptersMode:"By chapters",
    fromPage:"First page",toPage:"Last page",
    pageDisclaimer:"Original exercises aligned to textbook topics. Card page tags are approximate; chapter boundaries follow the contents.",
    selectAll:"Select all",clearAll:"Clear selection",only:"Only this",material:"Material",
    words:"Words",numbers:"Numbers",phrases:"Phrases",sentences:"Sentences",
    plurals:"Noun plurals",alphabet:"Alphabet",accent:"Accents",
    sessionLength:"Session duration",minutes:"min",
    mixedDirections:"Translations: Greek ↔ Russian/English. Accents: choose the letter.",
    pluralNotice:"ⓘ Noun plurals are available as optional additional practice.",
    start:"Start practice",keyboard:"Keys 1–8 · Enter to continue",finishNow:"Finish",
    next:"Next →",complete:"SESSION COMPLETED",anotherSession:"New session ↗",reviewMistakes:"Review mistakes",
    answers:"Answers",correctAnswers:"Correct",streak:"Streak",byChapter:"BY CHAPTER",
    whereStrong:"Your strong chapters",byType:"BY TYPE",whereWeak:"Areas to review",
    last14:"LAST 14 PRACTICE DAYS",history:"Practice history",
    privacy:"Progress is stored on the server under an anonymous browser session. Other browsers/devices have separate progress.",
    weakHeading:"MISTAKE PRACTICE",weakTitle:"Revisit what you haven't mastered yet.",
    weakInfo:"Incorrect cards return here. Two correct reviews clear each error. Directions and translation languages are tracked separately; page and type filters still apply.",
    weakCount:"mistake cards overall",weakStart:"Practice weak cards →",
    footer:"Independent exercises aligned to Ελληνικά Α΄ · 20 units · 312 pages",
    loading:"Loading...",noCards:"No cards in this selection yet. Extend the range, chapters or material types.",
    noWeak:"No outstanding mistakes in the selected material.",
    none:"No answers",noHistory:"No sessions recorded yet.",right:"✓ Correct!",
    wrong:"✗ Not quite. Correct answer: ",queued:" · Added to review.",
    failed:"Could not save answer: ",retry:" Please try again.",
    excellent:"Πολύ καλά! Excellent.",good:"Good result!",practiceMore:"Keep practising.",
    result:"Correct: {good} out of {total} ({pct}%). Time: {minutes} min.",
    session:"PRACTICE",weakSession:"MISTAKE REVIEW",
    chapter:"Chapter",review:"Review",alphabetName:"Alphabet",appendix:"Appendix",
    errorNoTypes:"Please choose at least one material type.",errorNoChapters:"Choose at least one chapter.",
    available:"{count} cards in the library",timeOver:"Your session time is up.",
    pauseNo:"A timed session is in progress; you can change language after finishing."
   },
   zh:{"brand":"我的希腊语","pagesLabel":"页","language":"界面和翻译语言","eyebrow":"你的个人希腊语训练器","headline1":"学好希腊语","headline2":"记得更牢。","intro":"练习希腊语单词、词形、短语和句子。选择已学的页码或章节，反复巩固错题。","accuracy":"正确率","allAnswers":"全部答题","reviewDue":"待复习","cards":"张卡片","practice":"练习","myMistakes":"错题","statistics":"统计","settings":"练习设置","whatPractice":"今天学习什么？","chooseInfo":"按页码或章节选择内容。翻译题有八个选项，重音题请点击字母。","scope":"教材范围","pagesMode":"按页码","chaptersMode":"按章节","fromPage":"起始页","toPage":"结束页","pageDisclaimer":"题目按教材主题原创编写。卡片页码为大致位置，章节范围以目录为准。","selectAll":"全选","clearAll":"清空","only":"只选此章","material":"练习类型","words":"单词","numbers":"数字","phrases":"短语","sentences":"句子","plurals":"名词单复数","alphabet":"字母","accent":"重音","sessionLength":"练习时长","minutes":"分钟","mixedDirections":"翻译：希腊语 ↔ 中文。重音：选择正确字母。","pluralNotice":"ⓘ 名词复数可作为额外练习。","start":"开始练习","keyboard":"数字键 1–9 · Enter 继续","finishNow":"结束","next":"下一题 →","complete":"练习结束","anotherSession":"再练一次 ↗","reviewMistakes":"复习错题","answers":"答题数","correctAnswers":"答对","streak":"连续正确","byChapter":"各章节","whereStrong":"掌握较好的章节","byType":"各题型","whereWeak":"需要加强的部分","last14":"最近14天","history":"练习记录","privacy":"进度按此浏览器的匿名会话保存在服务器上。不同设备的记录互不共享。","weakHeading":"错题训练","weakTitle":"再练习还没掌握的内容。","weakInfo":"答错的卡片会出现在这里。连续两次正确复习后移除。翻译方向和语言分别统计，页码及类型筛选仍有效。","weakCount":"张待复习卡片","weakStart":"练习错题 →","footer":"按《Ελληνικά Α΄》主题编写的原创题目 · 20课 · 312页","loading":"加载中...","noCards":"当前选择没有题目，请扩大范围或更换题型。","noWeak":"当前筛选范围内没有待复习的错题。","none":"暂无答题","noHistory":"还没有练习记录。","right":"✓ 正确！","wrong":"✗ 不正确。正确答案：","queued":" · 已加入错题复习。","failed":"保存答案失败：","retry":" 请重试。","excellent":"Πολύ καλά! 太棒了。","good":"答得不错！","practiceMore":"继续加油！","result":"答对 {good}/{total}（{pct}%），用时 {minutes} 分钟。","session":"练习","weakSession":"错题复习","chapter":"第","review":"复习","alphabetName":"字母表","appendix":"附录","errorNoTypes":"请至少选择一个练习类型。","errorNoChapters":"请至少选择一章。","available":"题库共有 {count} 张卡片","timeOver":"练习时间结束。","pauseNo":"计时练习进行中，结束后可切换语言。","translationNote":"中文翻译由机器辅助生成，个别词义可能不够准确。"},
  };
  I18N.es={"brand":"Mi griego","pagesLabel":"páginas","language":"Idioma de la interfaz y traducción","eyebrow":"TU ENTRENADOR DE GRIEGO","headline1":"Aprende griego","headline2":"y recuérdalo.","intro":"Practica palabras, formas, frases y oraciones en griego. Elige páginas o capítulos y repasa tus errores.","accuracy":"Precisión","allAnswers":"respuestas","reviewDue":"Por repasar","cards":"tarjetas","practice":"Practicar","myMistakes":"Mis errores","statistics":"Estadísticas","settings":"CONFIGURACIÓN","whatPractice":"¿Qué estudiamos hoy?","chooseInfo":"Elige páginas o capítulos. Ocho opciones por traducción; selecciona la letra para los acentos.","scope":"Material del libro","pagesMode":"Por páginas","chaptersMode":"Por capítulos","fromPage":"Desde la página","toPage":"Hasta la página","pageDisclaimer":"Ejercicios originales por temas. Las páginas de cada tarjeta son aproximadas; los capítulos siguen el índice.","selectAll":"Seleccionar todo","clearAll":"Borrar selección","only":"Solo este","material":"Material","words":"Palabras","numbers":"Números","phrases":"Frases","sentences":"Oraciones","plurals":"Singular y plural","alphabet":"Alfabeto","accent":"Acentos","sessionLength":"Duración","minutes":"min","mixedDirections":"Traducción: griego ↔ español. Acentos: elegir la letra.","pluralNotice":"ⓘ El plural se puede practicar por separado.","start":"Empezar","keyboard":"Teclas 1–9 · Intro para continuar","finishNow":"Terminar","next":"Siguiente →","complete":"SESIÓN TERMINADA","anotherSession":"Otra sesión ↗","reviewMistakes":"Repasar errores","answers":"Respuestas","correctAnswers":"Aciertos","streak":"Racha","byChapter":"POR CAPÍTULO","whereStrong":"Tus puntos fuertes","byType":"POR TIPO","whereWeak":"Qué repasar","last14":"ÚLTIMOS 14 DÍAS","history":"Historial","privacy":"Los datos se guardan en el servidor con una cookie anónima de este navegador. Otros dispositivos tienen historiales separados.","weakHeading":"REPASO DE ERRORES","weakTitle":"Repasa lo que aún te cuesta.","weakInfo":"Las tarjetas falladas vuelven aquí. Dos respuestas correctas eliminan el error. La dirección y el idioma se siguen por separado.","weakCount":"tarjetas por repasar","weakStart":"Repasar errores →","footer":"Ejercicios originales basados en Ελληνικά Α΄ · 20 unidades · 312 páginas","loading":"Cargando...","noCards":"No hay tarjetas en esta selección. Amplía las páginas, capítulos o tipos.","noWeak":"No quedan errores pendientes en esta selección.","none":"Sin respuestas","noHistory":"Sin sesiones todavía.","right":"✓ ¡Correcto!","wrong":"✗ Incorrecto. Respuesta: ","queued":" · Añadido al repaso.","failed":"No se pudo guardar: ","retry":" Inténtalo de nuevo.","excellent":"Πολύ καλά! ¡Excelente!","good":"¡Buen trabajo!","practiceMore":"¡Sigue practicando!","result":"Correctas: {good}/{total} ({pct} %). Tiempo: {minutes} min.","session":"PRÁCTICA","weakSession":"REPASO","chapter":"Capítulo","review":"Repaso","alphabetName":"Alfabeto","appendix":"Anexo","errorNoTypes":"Elige al menos un tipo de ejercicio.","errorNoChapters":"Elige al menos un capítulo.","available":"{count} tarjetas en la biblioteca","timeOver":"Se acabó el tiempo.","pauseNo":"Hay una sesión activa; cambia el idioma al terminar.","translationNote":"Traducción asistida por máquina. Algunas expresiones pueden ser imprecisas."};
  I18N.pt={"brand":"O meu grego","pagesLabel":"páginas","language":"Língua da interface e tradução","eyebrow":"O TEU TREINADOR DE GREGO","headline1":"Aprende grego","headline2":"e não te esqueças.","intro":"Pratica palavras, formas, expressões e frases em grego. Escolhe páginas ou capítulos e revê os erros.","accuracy":"Precisão","allAnswers":"respostas","reviewDue":"Por rever","cards":"cartões","practice":"Praticar","myMistakes":"Os meus erros","statistics":"Estatísticas","settings":"CONFIGURAÇÃO","whatPractice":"O que vamos estudar hoje?","chooseInfo":"Escolhe páginas ou capítulos. Oito opções na tradução; escolhe a letra para os acentos.","scope":"Matéria do livro","pagesMode":"Por páginas","chaptersMode":"Por capítulos","fromPage":"Da página","toPage":"Até à página","pageDisclaimer":"Exercícios originais por tema. As páginas de cada cartão são aproximadas; os capítulos seguem o índice.","selectAll":"Selecionar tudo","clearAll":"Limpar seleção","only":"Só este","material":"Material","words":"Palavras","numbers":"Números","phrases":"Expressões","sentences":"Frases","plurals":"Singular e plural","alphabet":"Alfabeto","accent":"Acentos","sessionLength":"Duração","minutes":"min","mixedDirections":"Tradução: grego ↔ português. Acentos: escolhe a letra.","pluralNotice":"ⓘ Os plurais podem ser praticados separadamente.","start":"Começar","keyboard":"Teclas 1–9 · Enter para continuar","finishNow":"Terminar","next":"Seguinte →","complete":"SESSÃO CONCLUÍDA","anotherSession":"Outra sessão ↗","reviewMistakes":"Rever erros","answers":"Respostas","correctAnswers":"Certas","streak":"Sequência","byChapter":"POR CAPÍTULO","whereStrong":"Os teus pontos fortes","byType":"POR TIPO","whereWeak":"O que deves rever","last14":"ÚLTIMOS 14 DIAS","history":"Histórico","privacy":"O progresso fica no servidor com uma cookie anónima deste navegador. Outros dispositivos têm progresso separado.","weakHeading":"REVISÃO DOS ERROS","weakTitle":"Revê o que ainda não dominas.","weakInfo":"Os cartões errados voltam aqui. Duas respostas certas eliminam o erro. As direções e línguas são contadas em separado.","weakCount":"cartões a rever","weakStart":"Rever erros →","footer":"Exercícios originais baseados em Ελληνικά Α΄ · 20 unidades · 312 páginas","loading":"A carregar...","noCards":"Não há cartões nesta seleção. Alarga as páginas, capítulos ou tipos.","noWeak":"Não tens erros pendentes nesta seleção.","none":"Sem respostas","noHistory":"Ainda não há sessões.","right":"✓ Certo!","wrong":"✗ Errado. Resposta correta: ","queued":" · Adicionado à revisão.","failed":"Não foi possível guardar: ","retry":" Tenta novamente.","excellent":"Πολύ καλά! Excelente!","good":"Muito bem!","practiceMore":"Continua a praticar!","result":"Certas: {good}/{total} ({pct}%). Tempo: {minutes} min.","session":"TREINO","weakSession":"REVISÃO","chapter":"Capítulo","review":"Revisão","alphabetName":"Alfabeto","appendix":"Anexo","errorNoTypes":"Escolhe pelo menos um tipo.","errorNoChapters":"Escolhe pelo menos um capítulo.","available":"{count} cartões na biblioteca","timeOver":"O tempo acabou.","pauseNo":"Há uma sessão a decorrer; muda a língua depois de terminar.","translationNote":"Tradução assistida por máquina. Algumas expressões podem ser imprecisas."};
  Object.assign(I18N.ru,{"leaders":"Рейтинг","studentName":"Твой учебный псевдоним","leaderTitle":"Лидеры недели","leaderIntro":"Последние 7 дней. Время — оценка активных ответов; открытая вкладка без занятий не учитывается.","leaderTime":"Активность","leaderAnswers":"Ответы","leaderErrors":"Ошибки","leaderPrecision":"Точность","leaderWeak":"Нерешено","leaderYou":"Это ты","leaderEmpty":"Пока никто не занимался. Самое время начать!","leaderMembers":"Участников","leaderPersonal":"Твоё место","leaderEstimate":"Время ориентировочное: по интервалам между ответами (с ограничением долгих пауз).","leaderDays":"за 7 дней"});
  Object.assign(I18N.en,{"leaders":"Leaderboard","studentName":"Your study nickname","leaderTitle":"Weekly leaderboard","leaderIntro":"Rolling 7 days. Time estimates active answer activity; leaving a tab open earns nothing.","leaderTime":"Active time","leaderAnswers":"Answers","leaderErrors":"Mistakes","leaderPrecision":"Accuracy","leaderWeak":"Unresolved","leaderYou":"You","leaderEmpty":"No practice yet. Be the first!","leaderMembers":"Learners","leaderPersonal":"Your rank","leaderEstimate":"Time is estimated from answer intervals, with long gaps capped.","leaderDays":"past 7 days"});
  Object.assign(I18N.zh,{"leaders":"排行榜","studentName":"你的学习昵称","leaderTitle":"本周排行榜","leaderIntro":"最近7天。仅根据答题活动估算时间，空闲网页不计时。","leaderTime":"活跃时间","leaderAnswers":"答题","leaderErrors":"错误","leaderPrecision":"正确率","leaderWeak":"待复习","leaderYou":"你","leaderEmpty":"还没有人答题，快来当第一名！","leaderMembers":"学习者","leaderPersonal":"你的排名","leaderEstimate":"学习时间根据答题间隔估算，长时间停顿不计入。","leaderDays":"最近7天"});
  Object.assign(I18N.es,{"leaders":"Clasificación","studentName":"Tu apodo de estudiante","leaderTitle":"Clasificación semanal","leaderIntro":"Últimos 7 días. El tiempo estima la actividad de respuestas; dejar la pestaña abierta no suma.","leaderTime":"Tiempo activo","leaderAnswers":"Respuestas","leaderErrors":"Errores","leaderPrecision":"Precisión","leaderWeak":"Pendientes","leaderYou":"Tú","leaderEmpty":"Aún no hay actividad. ¡Sé el primero!","leaderMembers":"Estudiantes","leaderPersonal":"Tu posición","leaderEstimate":"Tiempo estimado por intervalos entre respuestas, sin pausas largas.","leaderDays":"últimos 7 días"});
  Object.assign(I18N.pt,{"leaders":"Classificação","studentName":"A tua alcunha de estudante","leaderTitle":"Classificação semanal","leaderIntro":"Últimos 7 dias. O tempo estima a atividade de resposta; deixar o separador aberto não conta.","leaderTime":"Tempo ativo","leaderAnswers":"Respostas","leaderErrors":"Erros","leaderPrecision":"Precisão","leaderWeak":"Por resolver","leaderYou":"Tu","leaderEmpty":"Ainda ninguém estudou. Sê o primeiro!","leaderMembers":"Estudantes","leaderPersonal":"A tua posição","leaderEstimate":"Tempo estimado pelos intervalos entre respostas, com pausas longas excluídas.","leaderDays":"últimos 7 dias"});
  // Public leaderboard requires explicit per-browser enrollment.
  Object.assign(I18N.ru,{"leaderJoin":"Вступить в рейтинг","leaderLeave":"Выйти из рейтинга","leaderOptinInfo":"В рейтинге только те, кто сам вступил. До этого результаты остаются личными. При вступлении засчитываются прежние занятия за последние 7 дней.","leaderEnrolledInfo":"Ты участвуешь в публичном рейтинге под своим анонимным прозвищем. Можно выйти в любой момент, не теряя прогресс."});
  Object.assign(I18N.en,{"leaderJoin":"Join leaderboard","leaderLeave":"Leave leaderboard","leaderOptinInfo":"Only users who choose to join appear here. Your progress stays private otherwise. Existing practice from the past 7 days counts when you join.","leaderEnrolledInfo":"You are in the public leaderboard under an anonymous nickname. You can leave at any time without losing progress."});
  Object.assign(I18N.zh,{"leaderJoin":"加入排行榜","leaderLeave":"退出排行榜","leaderOptinInfo":"只有主动加入的学习者会出现在排行榜中。不加入也能保留个人成绩；加入后计入最近7天已有的练习。","leaderEnrolledInfo":"你正以匿名昵称参与公开排行榜。随时可以退出，学习记录仍会保留。"});
  Object.assign(I18N.es,{"leaderJoin":"Unirse a la clasificación","leaderLeave":"Salir de la clasificación","leaderOptinInfo":"Solo aparecen las personas que se inscriben voluntariamente. Tus resultados son privados hasta entonces; al unirte cuentan las prácticas de los últimos 7 días.","leaderEnrolledInfo":"Participas bajo un apodo anónimo. Puedes salir en cualquier momento sin perder tus progresos."});
  Object.assign(I18N.pt,{"leaderJoin":"Entrar na classificação","leaderLeave":"Sair da classificação","leaderOptinInfo":"Só aparecem pessoas que aderem voluntariamente. O progresso é privado até aderires; contam os exercícios dos últimos 7 dias.","leaderEnrolledInfo":"Participas com uma alcunha anónima. Podes sair a qualquer momento sem perder o progresso."});
  Object.assign(I18N.ru,{"authWelcome":"Добро пожаловать в Λέξη","authInfo":"Создай ник или войди по восьмизначному коду, чтобы заниматься с любого устройства.","authRegister":"Регистрация","authLogin":"Вход","authNickname":"Твой никнейм (3–28 символов)","authCodeLogin":"Восьмизначный код","authCreate":"Создать аккаунт","authSignIn":"Войти по коду","authKeep":"Запиши этот код: это твой пароль для входа с других устройств. Потерянный код восстановить нельзя.","authCopy":"Скопировать код","authContinue":"Начать заниматься →","authSecurity":"Код состоит всего из восьми цифр: не пересылай его другим и не показывай на скриншотах.","authAccessCode":"Код входа","authCopyShort":"Копировать","authExit":"Выйти","topicsMode":"Темы A1/A2","verbsMode":"Спряжение Α / Β1 / Β2","selectTopics":"Темы для тренировки","levelTitle":"Уровни","verbGroups":"Группы спряжения","verbNotice":"Выбирай форму настоящего времени для указанного лица. После ответа увидишь полное спряжение.","verbReference":"Показать таблицы спряжения","verbForms":"Спряжение в настоящем времени","authTaken":"Этот ник уже занят.","authBadCode":"Код не найден.","authLimit":"Слишком много попыток. Повтори через 15 минут.","authBadNick":"Ник должен содержать 3–28 символов: буквы, цифры, пробелы, дефис.","authChoose":"Выбери тему и уровень.","authConfirmLogout":"Выйти из аккаунта? Для возвращения понадобится восьмизначный код.","authCodeMissing":"Код сохранён на устройстве регистрации. Если его здесь нет, восстановить его на сервере нельзя.","authCopied":"Код скопирован."});
  Object.assign(I18N.en,{"authWelcome":"Welcome to Λέξη","authInfo":"Create your own nickname or sign in with an eight-digit access code to practice on any device.","authRegister":"Register","authLogin":"Sign in","authNickname":"Your nickname (3–28 characters)","authCodeLogin":"Eight-digit access code","authCreate":"Create account","authSignIn":"Sign in with code","authKeep":"Write down this code — it's your password for your other devices. Lost codes cannot be recovered.","authCopy":"Copy code","authContinue":"Start practicing →","authSecurity":"Eight digits make a weak password. Never share your code or include it in screenshots.","authAccessCode":"Login code","authCopyShort":"Copy","authExit":"Sign out","topicsMode":"A1/A2 topics","verbsMode":"Conjugation Α / Β1 / Β2","selectTopics":"Practice topics","levelTitle":"Levels","verbGroups":"Verb groups","verbNotice":"Choose the present-tense form for the indicated person. After answering, see the complete conjugation.","verbReference":"See conjugation tables","verbForms":"Present-tense conjugation","authTaken":"This nickname is taken.","authBadCode":"Code not found.","authLimit":"Too many attempts. Try again in 15 minutes.","authBadNick":"Nickname must have 3–28 characters: letters, numbers, spaces or hyphens.","authChoose":"Choose a topic and level.","authConfirmLogout":"Sign out? You'll need your eight-digit access code to return.","authCodeMissing":"Your code was saved on the original device. It cannot be recovered from the server.","authCopied":"Code copied."});
  Object.assign(I18N.zh,{"authWelcome":"欢迎来到 Λέξη","authInfo":"创建昵称，或用八位数字登录，在不同设备上继续学习。","authRegister":"注册","authLogin":"登录","authNickname":"昵称（3–28个字符）","authCodeLogin":"八位数字登录码","authCreate":"创建账户","authSignIn":"使用代码登录","authKeep":"请保存此登录码。它是你在其他设备登录的密码，丢失后无法找回。","authCopy":"复制登录码","authContinue":"开始学习 →","authSecurity":"八位数字的安全性有限。不要与他人分享，也不要公开截图。","authAccessCode":"登录码","authCopyShort":"复制","authExit":"退出","topicsMode":"A1/A2 主题","verbsMode":"动词变位 Α / Β1 / Β2","selectTopics":"选择主题","levelTitle":"等级","verbGroups":"动词组","verbNotice":"选择指定人称的现在时形式。答题后会显示完整变位表。","verbReference":"查看动词变位表","verbForms":"现在时变位","authTaken":"此昵称已被使用。","authBadCode":"未找到登录码。","authLimit":"尝试次数过多，请15分钟后再试。","authBadNick":"昵称需包含3–28个字符。","authChoose":"请选择主题和等级。","authConfirmLogout":"退出后需要登录码重新进入。确定退出？","authCodeMissing":"代码保存在首次注册的设备上，服务器无法找回。","authCopied":"已复制。"});
  Object.assign(I18N.es,{"authWelcome":"Bienvenido a Λέξη","authInfo":"Crea tu apodo o entra con un código de ocho cifras para estudiar en cualquier dispositivo.","authRegister":"Registrarse","authLogin":"Entrar","authNickname":"Tu apodo (3–28 caracteres)","authCodeLogin":"Código de ocho cifras","authCreate":"Crear cuenta","authSignIn":"Entrar con código","authKeep":"Guarda este código: es tu contraseña para otros dispositivos y no se puede recuperar.","authCopy":"Copiar código","authContinue":"Empezar →","authSecurity":"Ocho cifras son una contraseña débil. No compartas el código ni lo publiques en capturas.","authAccessCode":"Código de acceso","authCopyShort":"Copiar","authExit":"Salir","topicsMode":"Temas A1/A2","verbsMode":"Conjugación Α / Β1 / Β2","selectTopics":"Elige temas","levelTitle":"Niveles","verbGroups":"Grupos verbales","verbNotice":"Elige la forma de presente correspondiente. Verás toda la conjugación después de responder.","verbReference":"Ver conjugaciones","verbForms":"Conjugación en presente","authTaken":"Ese apodo ya está ocupado.","authBadCode":"No se ha encontrado el código.","authLimit":"Demasiados intentos. Prueba en 15 minutos.","authBadNick":"El apodo debe tener 3–28 caracteres.","authChoose":"Elige un tema y nivel.","authConfirmLogout":"¿Salir? Necesitarás el código de ocho cifras para volver.","authCodeMissing":"El código se guardó en el dispositivo original. No se puede recuperar del servidor.","authCopied":"Código copiado."});
  Object.assign(I18N.pt,{"authWelcome":"Bem-vindo ao Λέξη","authInfo":"Cria uma alcunha ou entra com um código de oito dígitos para estudares em qualquer dispositivo.","authRegister":"Registar","authLogin":"Entrar","authNickname":"A tua alcunha (3–28 caracteres)","authCodeLogin":"Código de oito dígitos","authCreate":"Criar conta","authSignIn":"Entrar com código","authKeep":"Guarda este código: é a tua palavra-passe nos outros dispositivos. Não pode ser recuperado.","authCopy":"Copiar código","authContinue":"Começar →","authSecurity":"Oito dígitos são uma palavra-passe fraca. Não partilhes o código nem o mostres em capturas.","authAccessCode":"Código de acesso","authCopyShort":"Copiar","authExit":"Sair","topicsMode":"Temas A1/A2","verbsMode":"Conjugação Α / Β1 / Β2","selectTopics":"Escolhe os temas","levelTitle":"Níveis","verbGroups":"Grupos de verbos","verbNotice":"Escolhe a forma do presente para a pessoa indicada. A conjugação completa aparece depois.","verbReference":"Ver tabelas de conjugação","verbForms":"Conjugação no presente","authTaken":"A alcunha já está a ser usada.","authBadCode":"Código não encontrado.","authLimit":"Muitas tentativas. Tenta daqui a 15 minutos.","authBadNick":"A alcunha deve ter entre 3 e 28 caracteres.","authChoose":"Escolhe um tema e um nível.","authConfirmLogout":"Sair? Precisas do código de oito dígitos para voltar.","authCodeMissing":"O código ficou guardado no dispositivo original. Não pode ser recuperado do servidor.","authCopied":"Código copiado."});
  Object.assign(I18N.ru,{"previewWords":"Посмотреть слова выбранной темы","previewHide":"Скрыть список слов","previewNoWords":"Выбери хотя бы одну тему A1 или A2."});
  Object.assign(I18N.en,{"previewWords":"Preview topic vocabulary","previewHide":"Hide vocabulary list","previewNoWords":"Select at least one topic and level."});
  Object.assign(I18N.zh,{"previewWords":"预习主题单词","previewHide":"隐藏单词列表","previewNoWords":"请至少选择一个主题和等级。"});
  Object.assign(I18N.es,{"previewWords":"Ver vocabulario del tema","previewHide":"Ocultar vocabulario","previewNoWords":"Elige al menos un tema y nivel."});
  Object.assign(I18N.pt,{"previewWords":"Ver vocabulário do tema","previewHide":"Ocultar vocabulário","previewNoWords":"Escolhe pelo menos um tema e nível."});
  Object.assign(I18N.ru,{"privacy":"История хранится на сервере в твоём аккаунте. Вход по восьмизначному коду позволяет продолжать с другого устройства."});
  Object.assign(I18N.en,{"privacy":"Progress is linked to your account on the server. Sign in with the eight-digit code to continue on another device."});
  Object.assign(I18N.zh,{"privacy":"学习记录保存在服务器上的个人账户中。使用八位数字登录码即可在另一台设备继续。"});
  Object.assign(I18N.es,{"privacy":"El progreso se guarda en tu cuenta en el servidor. Entra con tu código de ocho cifras en otro dispositivo."});
  Object.assign(I18N.pt,{"privacy":"O progresso fica guardado na tua conta no servidor. Entra com o código de oito dígitos noutro dispositivo."});

  I18N.ar={...I18N.en,
    brand:"تعلم اليونانية",pagesLabel:"صفحة",language:"لغة الواجهة والترجمة",eyebrow:"مدرب اللغة اليونانية",
    headline1:"تعلّم اليونانية",headline2:"بثقة",intro:"كلمات وجمل وتصريفات يونانية. اختر الدروس التي درستها وراجع أخطاءك.",
    accuracy:"الدقة",allAnswers:"الإجابات",reviewDue:"للمراجعة",cards:"بطاقات",
    practice:"التدريب",vocabTab:"مفردات A1/A2",myMistakes:"أخطائي",statistics:"الإحصاءات",
    settings:"إعداد الدرس",whatPractice:"ماذا سنتعلم اليوم؟",chooseInfo:"اختر صفحات الكتاب أو فصوله.",
    scope:"نطاق الكتاب",pagesMode:"حسب الصفحات",chaptersMode:"حسب الفصول",fromPage:"من الصفحة",toPage:"إلى الصفحة",
    pageDisclaimer:"تمارين تعليمية أصلية مستوحاة من مواضيع الكتاب. أرقام الصفحات تقريبية.",
    selectAll:"تحديد الكل",clearAll:"مسح التحديد",only:"فقط",material:"المواد",
    words:"كلمات",numbers:"أرقام",phrases:"عبارات",sentences:"جمل",plurals:"الجمع والمفرد",
    alphabet:"الأبجدية",accent:"النبر",sessionLength:"مدة التدريب",minutes:"دقيقة",
    mixedDirections:"من اليونانية وإليها",start:"ابدأ التدريب",keyboard:"الأرقام ١–٨ · Enter للمتابعة",
    finishNow:"إنهاء",next:"التالي ←",complete:"اكتمل التدريب",anotherSession:"درس جديد",
    reviewMistakes:"مراجعة الأخطاء",answers:"إجابات",correctAnswers:"صحيحة",streak:"متتالية",
    byChapter:"حسب الفصل",whereStrong:"نقاط القوة",byType:"حسب النوع",whereWeak:"بحاجة إلى مراجعة",
    last14:"آخر ١٤ يوماً",history:"التاريخ",
    weakHeading:"مراجعة الأخطاء",weakTitle:"لنراجع ما لم نتقنه بعد.",
    weakInfo:"تعود البطاقات الخاطئة إلى قائمة المراجعة، ويزيلها جوابان صحيحان.",
    weakCount:"بطاقات تحتاج مراجعة",weakStart:"راجع الأخطاء",
    footer:"تمارين أصلية مستوحاة من كتاب Ελληνικά Α΄",
    loading:"جارٍ التحميل…",noCards:"لا توجد بطاقات هنا.",noWeak:"لا توجد أخطاء للمراجعة.",
    none:"لا توجد إجابات",noHistory:"لا يوجد تاريخ بعد.",right:"✓ صحيح",wrong:"✗ الصحيح: ",
    queued:" · أضيفت للمراجعة",failed:"تعذر حفظ الإجابة: ",retry:" حاول مرة أخرى.",
    excellent:"ممتاز!",good:"أحسنت!",practiceMore:"تابع التمرين!",
    result:"صحيح: {good} من {total} ({pct}%)، الوقت: {minutes} دقيقة",
    session:"تدريب",weakSession:"مراجعة الأخطاء",chapter:"الفصل",review:"مراجعة",
    alphabetName:"الأبجدية",errorNoTypes:"اختر نوعاً واحداً على الأقل",
    errorNoChapters:"اختر فصلاً واحداً على الأقل",available:"{count} بطاقة",
    timeOver:"انتهى وقت الدرس.",pauseNo:"أنهِ الدرس قبل تغيير اللغة.",
    authWelcome:"أهلاً بك في Λέξη",authInfo:"أنشئ اسماً مستعاراً أو سجّل الدخول برمز من ثمانية أرقام.",
    authRegister:"حساب جديد",authLogin:"دخول",authNickname:"الاسم المستعار (٣–٢٨ حرفاً)",
    authCodeLogin:"رمز الدخول من ٨ أرقام",authCreate:"إنشاء حساب",authSignIn:"تسجيل الدخول",
    authKeep:"احفظ هذا الرمز للعودة من الأجهزة الأخرى. لا يمكن استرداده إذا فقدته.",
    authCopy:"نسخ الرمز",authContinue:"ابدأ التعلّم",authSecurity:"لا تشارك رمز الدخول مع الآخرين.",
    authAccessCode:"رمز الدخول",authCopyShort:"نسخ",authExit:"تسجيل الخروج",
    authTaken:"هذا الاسم مستخدم",authBadCode:"الرمز غير صحيح",
    authLimit:"محاولات كثيرة، حاول بعد ١٥ دقيقة",authBadNick:"الاسم غير صالح",
    authCodeMissing:"الرمز محفوظ في الجهاز الأصلي ولا يمكن استرداده من الخادم.",
    authCopied:"تم النسخ",
    topicsMode:"المواضيع A1/A2",verbsMode:"تصريف الأفعال Α / Β1 / Β2",
    selectTopics:"المواضيع",levelTitle:"المستوى",verbGroups:"مجموعات الأفعال",
    verbNotice:"أولاً اختر تصريف الفعل المناسب للضمير، ثم ترجم الجملة كاملة.",
    verbReference:"جداول التصريف",verbForms:"التصريف",
    previewWords:"عرض الكلمات",previewHide:"إخفاء الكلمات",previewNoWords:"اختر موضوعاً ومستوى",
    translationNote:"تم استكمال الترجمات العربية لجميع كلمات الدورة. بعض الصياغات مولّدة بمساعدة الترجمة الآلية وقد تحتاج إلى مراجعة لغوية.",
    verbTranslate:"ترجمة الجملة ←",verbTranslateHelp:"المرحلة الثانية: ترجم الجملة اليونانية كاملة."
  };
  const GREEK_VARIANT_LABELS={
    ru:{also:"Также употребляют",more:"В греческом есть два правильных варианта"},
    en:{also:"Also used",more:"Both Greek forms are correct"},
    zh:{also:"另一种常见形式",more:"这两种希腊语形式都正确"},
    ar:{also:"تُستعمل أيضاً",more:"كلتا الصيغتين اليونانيتين صحيحتان"},
    es:{also:"También se utiliza",more:"Las dos formas griegas son correctas"},
    pt:{also:"Também se usa",more:"Ambas as formas gregas estão corretas"}
  };
  Object.assign(I18N.ru,{vocabTab:"Словарь A1/A2",verbTranslate:"Перевести предложение →",
    verbTranslateHelp:"Этап 2 из 2: выбери перевод всего греческого предложения.",
    verbNotice:"Сначала выбери форму глагола по местоимению, затем переведи предложение.",
    translationNote:"Словарь переведён на все доступные языки; машинные варианты могут требовать дополнительной языковой проверки."});
  Object.assign(I18N.en,{vocabTab:"A1/A2 vocabulary",verbTranslate:"Translate the sentence →",
    verbTranslateHelp:"Stage 2 of 2: translate the entire Greek sentence."});
  for(const code of ["zh","es","pt"])Object.assign(I18N[code],{
    vocabTab: I18N[code].topicsMode||"A1/A2 vocabulary",
    verbTranslate: I18N.en.verbTranslate,verbTranslateHelp:I18N.en.verbTranslateHelp
  });


  Object.assign(I18N.ru,{
    textbookTraining:"Тренировка учебника",personalizedTraining:"Персонализированная тренировка",
    textbookTrainingInfo:"Задания только из выбранных страниц или глав учебника. Словарный курс не смешивается с ним.",
    personalizedTrainingInfo:"Задания из выбранных страниц или глав + лично освоенные слова из словарного курса. Непройденная лексика не появляется.",
    personalizedProgress:"Освоено слов: {count} · С ошибками: {weak}",
    dialogues:"Диалоги · вставить реплики",
    dialogueInstruction:"Вставь подходящую греческую реплику в пропуск {current} из {total}. Из восьми вариантов часть лишние.",
    dialogueNext:"Следующий пропуск →",dialogueTitle:"Диалог · выбери реплику",
    dialogueLabel:"Диалог"
  });
  Object.assign(I18N.en,{
    textbookTraining:"Textbook practice",personalizedTraining:"Personalized practice",
    textbookTrainingInfo:"Only selected textbook pages or chapters; vocabulary course stays separate.",
    personalizedTrainingInfo:"Selected textbook pages/chapters plus words you've learned in the vocabulary course; unlearned words stay out.",
    personalizedProgress:"Learned words: {count} · Needs review: {weak}",
    dialogues:"Dialogues · complete the gaps",
    dialogueInstruction:"Complete gap {current} of {total} using a Greek line. Some of the eight options are distractors.",
    dialogueNext:"Next gap →",dialogueTitle:"Dialogue · choose a reply",dialogueLabel:"Dialogue"
  });
  Object.assign(I18N.ar,{
    textbookTraining:"تمارين الكتاب",personalizedTraining:"تدريب مخصص لك",
    textbookTrainingInfo:"تمارين صفحات أو فصول الكتاب المختارة فقط.",
    personalizedTrainingInfo:"تمارين الكتاب المختارة والكلمات التي تعلمتها في دروس المفردات.",
    personalizedProgress:"كلمات متقنة: {count} · للمراجعة: {weak}",
    dialogues:"حوارات · أكمل الفراغات",
    dialogueInstruction:"أكمل الفراغ {current} من {total} بجملة يونانية. بعض الخيارات الثمانية غير صحيحة.",
    dialogueNext:"الفراغ التالي",dialogueTitle:"الحوار · اختر العبارة",dialogueLabel:"حوار"
  });
  Object.assign(I18N.zh,{
    textbookTraining:"教材练习",personalizedTraining:"个性化练习",
    textbookTrainingInfo:"只练习所选教材页或章节。",
    personalizedTrainingInfo:"所选教材内容加上你已掌握的词汇课程单词。",
    personalizedProgress:"已掌握词汇：{count} · 待复习：{weak}",
    dialogues:"对话 · 填空",dialogueInstruction:"用希腊语填第 {current}/{total} 个空。八个选项中有干扰项。",
    dialogueNext:"下一个空",dialogueTitle:"希腊语对话",dialogueLabel:"对话"
  });
  Object.assign(I18N.es,{
    textbookTraining:"Práctica del libro",personalizedTraining:"Práctica personalizada",
    textbookTrainingInfo:"Solo las páginas o capítulos seleccionados del libro.",
    personalizedTrainingInfo:"El libro seleccionado más las palabras aprendidas en tu curso.",
    personalizedProgress:"Palabras aprendidas: {count} · Por repasar: {weak}",
    dialogues:"Diálogos · completar huecos",
    dialogueInstruction:"Completa el hueco {current} de {total} en griego. Algunas de las ocho respuestas son distractores.",
    dialogueNext:"Siguiente hueco",dialogueTitle:"Diálogo en griego",dialogueLabel:"Diálogo"
  });
  Object.assign(I18N.pt,{
    textbookTraining:"Treino do manual",personalizedTraining:"Treino personalizado",
    textbookTrainingInfo:"Só as páginas ou capítulos selecionados do manual.",
    personalizedTrainingInfo:"O manual selecionado e as palavras já aprendidas no curso.",
    personalizedProgress:"Palavras aprendidas: {count} · Para rever: {weak}",
    dialogues:"Diálogos · preencher lacunas",
    dialogueInstruction:"Completa a lacuna {current} de {total} em grego. Algumas das oito opções são distratores.",
    dialogueNext:"Próxima lacuna",dialogueTitle:"Diálogo em grego",dialogueLabel:"Diálogo"
  });

  // Display-only UI strings: missing translations in non-Russian locales must
  // fall back to ENGLISH, never to the Russian source language.
  const EXTRA_UI={
    ru:{nicknamePlaceholder:"Сонный Академик",footerBrand:"Λέξη · тренажёр греческого"},
    en:{nicknamePlaceholder:"Curious Learner",footerBrand:"Λέξη · Greek practice",translationNote:"Some learning translations are machine-assisted and may need review."},
    zh:{nicknamePlaceholder:"希腊语学习者",footerBrand:"Λέξη · 希腊语练习"},
    ar:{nicknamePlaceholder:"متعلم اليونانية",footerBrand:"Λέξη · تدريب على اليونانية"},
    es:{nicknamePlaceholder:"Estudiante de griego",footerBrand:"Λέξη · Práctica de griego"},
    pt:{nicknamePlaceholder:"Estudante de grego",footerBrand:"Λέξη · Prática de grego"}
  };
  for(const locale of Object.keys(EXTRA_UI))Object.assign(I18N[locale],EXTRA_UI[locale]);
  // These 12 topic-mode names previously showed English under ZH/AR/ES/PT.
  const TOPIC_NAMES={
    zh:{shopping:"购物",road:"交通与汽车",home:"家庭与厨房",food:"食物与杂货",family:"家庭与人际",work:"工作与学习",city:"城市与服务",health:"健康",time:"时间与日程",travel:"旅行",leisure:"休闲",nature:"自然与天气"},
    ar:{shopping:"التسوق",road:"النقل والسيارات",home:"المنزل والمطبخ",food:"الطعام والبقالة",family:"العائلة والناس",work:"العمل والدراسة",city:"المدينة والخدمات",health:"الصحة",time:"الوقت والجدول",travel:"السفر",leisure:"الترفيه",nature:"الطبيعة والطقس"},
    es:{shopping:"Compras",road:"Transporte y coche",home:"Hogar y cocina",food:"Comida y alimentación",family:"Familia y personas",work:"Trabajo y estudios",city:"Ciudad y servicios",health:"Salud",time:"Tiempo y horarios",travel:"Viajes",leisure:"Ocio",nature:"Naturaleza y clima"},
    pt:{shopping:"Compras",road:"Transportes e automóvel",home:"Casa e cozinha",food:"Alimentação e mercearia",family:"Família e pessoas",work:"Trabalho e estudos",city:"Cidade e serviços",health:"Saúde",time:"Tempo e horários",travel:"Viagens",leisure:"Lazer",nature:"Natureza e clima"}
  };
  const WEAK_LOCALES={
    ru:["Ошибки со всех страниц, типов заданий и языков. Каждая карточка повторяется на языке первоначального ответа. Два правильных повтора закрывают ошибку.","доступных ошибок","Тренировать все ошибки →","Нет доступных ошибок для повторения.","{count} старых записей недоступны в текущем каталоге. История сохранена.","Язык ответа: {lang}"],
    en:["Mistakes from all pages, exercise types and languages. Each card keeps its original answer language. Two correct reviews clear it.","reviewable mistakes","Review all mistakes →","No reviewable mistakes remain.","{count} old entries are absent from the current catalog. History was kept.","Answer language: {lang}"],
    zh:["复习所有章节、题型和语言的错题，保留原来的答题语言。答对两次后移除。","可复习的错题","复习全部错题 →","没有可复习的错题。","{count} 条旧记录不在当前题库中，历史已保留。","答题语言：{lang}"],
    ar:["راجع أخطاء جميع الدروس واللغات؛ تحتفظ كل بطاقة بلغتها الأصلية. إجابتان صحيحتان تنهيان المراجعة.","أخطاء متاحة للمراجعة","مراجعة جميع الأخطاء ←","لا توجد أخطاء متاحة للمراجعة.","{count} سجلات قديمة لم تعد في بنك التمارين. تم الاحتفاظ بالسجل.","لغة الإجابة: {lang}"],
    es:["Repasa los errores de todas las páginas, ejercicios e idiomas. Se conserva el idioma de cada respuesta. Dos repasos correctos cierran el error.","errores disponibles","Repasar todos los errores →","No quedan errores para repasar.","{count} registros antiguos ya no están en el catálogo. Se conserva el historial.","Idioma de respuesta: {lang}"],
    pt:["Revê os erros de todas as páginas, exercícios e línguas. Cada resposta mantém a língua original. Duas revisões certas resolvem o erro.","erros disponíveis","Rever todos os erros →","Não há erros disponíveis para rever.","{count} registos antigos já não constam do catálogo. O histórico foi preservado.","Língua da resposta: {lang}"]
  };
  for(const [loc,values] of Object.entries(WEAK_LOCALES)){
    const names=["weakInfo","weakCount","weakStart","weakNoAvailable","weakArchived","weakLanguage"];
    for(let i=0;i<names.length;i++)I18N[loc][names[i]]=values[i];
  }
  const LANGUAGE_LABELS={ru:"Русский",en:"English",zh:"中文",ar:"العربية",es:"Español",pt:"Português"};
  // The dialogue advances by GAP only while another gap exists. After the
  // last reply, the next action advances the practice session (or shows its
  // results), so it must never retain the label "Next gap".
  const DIALOGUE_LAST_STEP={
    ru:{dialogueComplete:"Все пропуски заполнены. Нажми «Далее», чтобы продолжить тренировку.",dialogueContinue:"Далее →",finishNow:"Завершить тренировку"},
    en:{dialogueComplete:"All gaps are filled. Press Continue to proceed with the practice session.",dialogueContinue:"Continue →",finishNow:"End practice"},
    zh:{dialogueComplete:"所有空格已填写。点击“继续”进入下一步。",dialogueContinue:"继续 →",finishNow:"结束练习"},
    ar:{dialogueComplete:"اكتملت جميع الفراغات. اضغط «متابعة» لمواصلة التدريب.",dialogueContinue:"متابعة ←",finishNow:"إنهاء التدريب"},
    es:{dialogueComplete:"Has completado todos los huecos. Pulsa Continuar para seguir practicando.",dialogueContinue:"Continuar →",finishNow:"Terminar práctica"},
    pt:{dialogueComplete:"Preencheste todas as lacunas. Carrega em Continuar para prosseguir.",dialogueContinue:"Continuar →",finishNow:"Terminar treino"}
  };
  for(const [locale,strings] of Object.entries(DIALOGUE_LAST_STEP))Object.assign(I18N[locale],strings);
  const SESSION_UNIQUE_NOTE={
    ru:"Без повторов: одно слово или фраза — один раз за обычную тренировку, даже в обратном направлении. Ошибки повторяются отдельно.",
    en:"No repeated vocabulary in a regular session, even in reverse translation. Mistakes are reviewed separately.",
    zh:"普通练习中不重复同一个词语，即使翻译方向相反。错题另行复习。",
    ar:"لا تتكرر الكلمة في الجلسة العادية، حتى عند عكس اتجاه الترجمة. تُراجع الأخطاء بشكل منفصل.",
    es:"Sin repeticiones: cada palabra o frase aparece una sola vez por sesión, incluso en sentido inverso. Los errores se repasan aparte.",
    pt:"Sem repetições: cada palavra ou expressão surge uma vez por sessão, mesmo no sentido inverso. Os erros são revistos à parte."
  };
  for(const [locale,msg] of Object.entries(SESSION_UNIQUE_NOTE))I18N[locale].sessionUniqueNote=msg;
  const GRAMMAR_UI={
    ru:{articlesMode:"Артикли и предлоги",orderMode:"Собрать предложение",orderDraft:"Твоя фраза",orderUndo:"Назад",orderReset:"Сбросить",orderCheck:"Проверить предложение",orderInstruction:"Нажимай на греческие слова по порядку, чтобы восстановить исходную фразу.",manyCorrect:"Может быть несколько правильных переводов."},
    en:{articlesMode:"Articles and cases",orderMode:"Build a sentence",orderDraft:"Your sentence",orderUndo:"Undo",orderReset:"Clear",orderCheck:"Check sentence",orderInstruction:"Tap Greek words in order to reconstruct the sample sentence.",manyCorrect:"More than one translation may be correct."},
    zh:{articlesMode:"冠词和格",orderMode:"组装句子",orderDraft:"你的句子",orderUndo:"撤销",orderReset:"清空",orderCheck:"检查句子",orderInstruction:"按顺序点击希腊语单词，还原示例句子。",manyCorrect:"可能有不止一个正确翻译。"},
    ar:{articlesMode:"أدوات التعريف وحالات الإعراب",orderMode:"تركيب جملة",orderDraft:"جملتك",orderUndo:"تراجع",orderReset:"مسح",orderCheck:"تحقق من الجملة",orderInstruction:"اضغط الكلمات اليونانية بالترتيب لإعادة تركيب الجملة النموذجية.",manyCorrect:"قد توجد أكثر من ترجمة صحيحة."},
    es:{articlesMode:"Artículos y casos",orderMode:"Construir una frase",orderDraft:"Tu frase",orderUndo:"Deshacer",orderReset:"Borrar",orderCheck:"Comprobar frase",orderInstruction:"Toca las palabras griegas en orden para reconstruir la frase modelo.",manyCorrect:"Puede haber más de una traducción correcta."},
    pt:{articlesMode:"Artigos e casos",orderMode:"Construir uma frase",orderDraft:"A tua frase",orderUndo:"Desfazer",orderReset:"Limpar",orderCheck:"Verificar frase",orderInstruction:"Toca nas palavras gregas por ordem para reconstruir a frase do exemplo.",manyCorrect:"Pode haver mais de uma tradução correta."}
  };
  for(const [loc,labels] of Object.entries(GRAMMAR_UI))Object.assign(I18N[loc],labels);
  const FINAL_N_LABELS={
    ru:{articleVariantHint:"Варианты написания артикля могут различаться конечным -ν.",preferredSpelling:"По учебнику",spellingGuide:"Примечание о конечном -ν"},
    en:{articleVariantHint:"Article spelling variants may differ by a final -ν.",preferredSpelling:"Book spelling",spellingGuide:"Note on final -ν"},
    zh:{articleVariantHint:"冠词的写法可能因词尾 -ν 而不同。",preferredSpelling:"教材推荐",spellingGuide:"关于词尾 -ν 的说明"},
    ar:{articleVariantHint:"قد تختلف كتابة أداة التعريف بوجود -ν في النهاية.",preferredSpelling:"صيغة الكتاب",spellingGuide:"ملاحظة عن -ν النهائية"},
    es:{articleVariantHint:"Las variantes ortográficas del artículo pueden diferir por la -ν final.",preferredSpelling:"Según el libro",spellingGuide:"Nota sobre -ν final"},
    pt:{articleVariantHint:"As variantes ortográficas do artigo podem diferir no -ν final.",preferredSpelling:"No manual",spellingGuide:"Nota sobre -ν final"},
  };
  for(const [loc,labels] of Object.entries(FINAL_N_LABELS))Object.assign(I18N[loc],labels);
  const STAGE_ACCENT_UI={
    ru:{verbStageLabel:"Спрягать глаголы, изученные до главы",verbStageNotice:"Ограничение по учебному этапу: у поздних глаголов могут быть более ранние отдельные употребления.",verbStageCount:"Доступно глаголов: {count}. Заданий на лица: {forms}.",accentExplanationTitle:"Почему здесь ударение",accentChoiceHelp:"Выбери гласную, на которой пишется ударение."},
    en:{verbStageLabel:"Practice verbs introduced by book unit",verbStageNotice:"A learning-stage guide, not a claim about the very first printed occurrence of each verb.",verbStageCount:"Verbs available: {count}. Person-form questions: {forms}.",accentExplanationTitle:"Why the accent goes here",accentChoiceHelp:"Select the vowel which carries the written accent."},
    zh:{verbStageLabel:"练习截至教材章节的动词",verbStageNotice:"这是教学阶段的分组，不一定是词语在书中首次出现的页码。",verbStageCount:"可用动词：{count}。人称变位题：{forms}。",accentExplanationTitle:"重音位置的说明",accentChoiceHelp:"选择应标注重音符号的元音。"},
    ar:{verbStageLabel:"تدرّب على الأفعال حتى وحدة الكتاب",verbStageNotice:"هذا تصنيف للمستوى الدراسي، وليس ادعاءً بأول ظهور حرفي لكل فعل في الكتاب.",verbStageCount:"الأفعال المتاحة: {count}. أسئلة التصريف: {forms}.",accentExplanationTitle:"لماذا يوضع النبر هنا",accentChoiceHelp:"اختر حرف العلة الذي يحمل علامة النبر."},
    es:{verbStageLabel:"Practicar verbos hasta la unidad",verbStageNotice:"Esta es una guía por nivel de estudio, no la primera página exacta donde aparece cada verbo.",verbStageCount:"Verbos disponibles: {count}. Preguntas de personas: {forms}.",accentExplanationTitle:"Por qué lleva ese acento",accentChoiceHelp:"Elige la vocal que lleva el acento escrito."},
    pt:{verbStageLabel:"Praticar verbos até à unidade",verbStageNotice:"É uma divisão por etapa de estudo, não a primeira página exata em que aparece cada verbo.",verbStageCount:"Verbos disponíveis: {count}. Perguntas por pessoa: {forms}.",accentExplanationTitle:"Porquê este acento",accentChoiceHelp:"Escolhe a vogal que recebe o acento escrito."}
  };
  for(const [locale,labels] of Object.entries(STAGE_ACCENT_UI))Object.assign(I18N[locale],labels);
  const CAPACITY_I18N={
    ru:{capacityButton:"Проверить запас карточек",capacityEnough:"Примерно {available} уникальных карточек при текущих фильтрах. Для {duration} минут при {pace} сек./карточку нужно около {needed}. Запаса достаточно.",capacityShort:"Доступно около {available} уникальных карточек, а для {duration} минут при {pace} сек./карточку нужно примерно {needed}. Занятие может закончиться раньше: расширь главы, диапазон или типы упражнений.",capacityDisclaimer:"Оценка, а не гарантия времени: диалоги и спряжения могут занимать дольше одной карточки."},
    en:{capacityButton:"Check available cards",capacityEnough:"About {available} unique items. A {duration}-minute session at {pace} seconds/item needs about {needed}. Enough material.",capacityShort:"About {available} unique items, versus {needed} for {duration} minutes at {pace} seconds/item. Try expanding the selection.",capacityDisclaimer:"Estimate, not a time guarantee. Multi-step dialogues and verbs can take longer."},
    zh:{capacityButton:"检查题量",capacityEnough:"约 {available} 道不同的题；{duration} 分钟按每题{pace}秒约需 {needed} 道。题量充足。",capacityShort:"约 {available} 道不同的题，而 {duration} 分钟按每题{pace}秒约需 {needed} 道。请扩大范围。",capacityDisclaimer:"仅为估算。多步骤对话和变位题可能需要更多时间。"},
    ar:{capacityButton:"التحقق من عدد البطاقات",capacityEnough:"نحو {available} بطاقة فريدة؛ لجلسة {duration} دقيقة بمعدل {pace} ثانية لكل بطاقة تحتاج نحو {needed}. المادة كافية.",capacityShort:"المتاح نحو {available} بطاقة فريدة، والمطلوب نحو {needed} لجلسة {duration} دقيقة. وسّع الاختيار.",capacityDisclaimer:"تقدير لا يضمن مدة الجلسة. الحوارات والتصريف قد تستغرق وقتًا أطول."},
    es:{capacityButton:"Comprobar tarjetas disponibles",capacityEnough:"Aprox. {available} tarjetas distintas. Para {duration} minutos a {pace} segundos por tarjeta hacen falta unas {needed}. Hay suficientes.",capacityShort:"Solo hay unas {available} tarjetas distintas; para {duration} minutos necesitas unas {needed}. Amplía la selección.",capacityDisclaimer:"Es una estimación, no una garantía: los diálogos y verbos pueden llevar más tiempo."},
    pt:{capacityButton:"Verificar cartões disponíveis",capacityEnough:"Cerca de {available} cartões únicos. Para {duration} minutos a {pace} segundos por cartão precisas de cerca de {needed}. São suficientes.",capacityShort:"Há cerca de {available} cartões únicos; para {duration} minutos seriam necessários cerca de {needed}. Alarga a seleção.",capacityDisclaimer:"É uma estimativa, não uma garantia: diálogos e verbos podem demorar mais."}
  };
  for(const [loc,labels] of Object.entries(CAPACITY_I18N))Object.assign(I18N[loc],labels);
  const LISTENING_I18N={
    ru:{listenMode:"🎧 Аудирование",listenScopeHelp:"Выбери главы, которые уже проходил. Греческая фраза скрыта до ответа. Аудио создано бесплатно и заранее.",listenPlay:"▶ Прослушать",listenSlow:"0,8× Медленнее",listenReplay:"↻ Прослушать ещё раз",listenPlayed:"Выбери подходящий перевод.",listenPlaying:"Воспроизведение…",listenError:"Не удалось воспроизвести аудио. Проверь звук и подключение; ответ пока заблокирован.",listenText:"Ты услышал:",listenNotYet:"Сначала послушай запись.",listenProgress:"Озвученных карточек: {count}. Никаких платных API."},
    en:{listenMode:"🎧 Listening",listenScopeHelp:"Choose studied chapters. The Greek text is hidden until you answer. Audio is generated offline at no per-user cost.",listenPlay:"▶ Play audio",listenSlow:"0.8× Slower",listenReplay:"↻ Play again",listenPlayed:"Now choose the correct meaning.",listenPlaying:"Playing audio…",listenError:"Could not play audio. Check sound and connection; answers are disabled.",listenText:"You heard:",listenNotYet:"Listen before choosing an answer.",listenProgress:"Recorded items: {count}. No paid API calls."},
    zh:{listenMode:"🎧 听力",listenScopeHelp:"选择已学章节。答题前隐藏希腊语文字。音频离线生成，无按次费用。",listenPlay:"▶ 播放音频",listenSlow:"0.8× 慢速",listenReplay:"↻ 再听一次",listenPlayed:"请选择正确的含义。",listenPlaying:"正在播放…",listenError:"无法播放音频，请检查网络和声音。此时无法作答。",listenText:"你听到的是：",listenNotYet:"请先听录音。",listenProgress:"已录制卡片：{count}。不使用付费 API。"},
    ar:{listenMode:"🎧 الاستماع",listenScopeHelp:"اختر الوحدات التي درستها. يُخفى النص اليوناني حتى تجيب. أُنتج الصوت دون تكلفة لكل مستخدم.",listenPlay:"▶ استمع",listenSlow:"0.8× أبطأ",listenReplay:"↻ استمع مرة أخرى",listenPlayed:"اختر المعنى الصحيح.",listenPlaying:"جارٍ التشغيل…",listenError:"تعذّر تشغيل الصوت. تحقق من الاتصال والصوت؛ الإجابات معطّلة.",listenText:"سمعت:",listenNotYet:"استمع إلى التسجيل أولاً.",listenProgress:"مقاطع جاهزة: {count}. من دون واجهات مدفوعة."},
    es:{listenMode:"🎧 Comprensión auditiva",listenScopeHelp:"Elige las unidades estudiadas. Se oculta el griego hasta responder. Audio generado sin coste por usuario.",listenPlay:"▶ Escuchar",listenSlow:"0,8× Más lento",listenReplay:"↻ Escuchar de nuevo",listenPlayed:"Elige el significado correcto.",listenPlaying:"Reproduciendo…",listenError:"No se pudo reproducir el audio. Comprueba la conexión y el sonido.",listenText:"Has escuchado:",listenNotYet:"Escucha primero.",listenProgress:"Grabaciones: {count}. Sin API de pago."},
    pt:{listenMode:"🎧 Compreensão oral",listenScopeHelp:"Escolhe as unidades estudadas. O grego fica oculto até responderes. Áudio pré-gerado, sem custo por utilizador.",listenPlay:"▶ Ouvir",listenSlow:"0,8× Mais lento",listenReplay:"↻ Ouvir de novo",listenPlayed:"Escolhe o significado correto.",listenPlaying:"A reproduzir…",listenError:"Não foi possível reproduzir o áudio. Verifica a ligação e o som.",listenText:"Ouviste:",listenNotYet:"Ouve primeiro.",listenProgress:"Gravações disponíveis: {count}. Sem API paga."}
  };
  for(const [loc,labels] of Object.entries(LISTENING_I18N))Object.assign(I18N[loc],labels);
  const AUDIO_ALPHA_LABELS={
    ru:{listenAlphaMode:"🎧 Аудирование · ALPHA — недоступно",listenAlphaNotice:"🎧 Аудирование · ALPHA: временно не работает. Некачественные записи отключены, результаты очищены."},
    en:{listenAlphaMode:"🎧 Listening · ALPHA — unavailable",listenAlphaNotice:"🎧 Listening ALPHA is temporarily disabled due to poor audio quality. Listening results were reset."},
    zh:{listenAlphaMode:"🎧 听力 · ALPHA — 暂不可用",listenAlphaNotice:"🎧 听力 ALPHA 因音质问题暂时停用。听力成绩已清除。"},
    ar:{listenAlphaMode:"🎧 الاستماع · ALPHA — غير متاح",listenAlphaNotice:"🎧 الاستماع ALPHA غير متاح مؤقتًا بسبب جودة الصوت. تم مسح نتائج الاستماع."},
    es:{listenAlphaMode:"🎧 Audición · ALPHA — no disponible",listenAlphaNotice:"🎧 La audición ALPHA está desactivada por la mala calidad del sonido. Resultados restablecidos."},
    pt:{listenAlphaMode:"🎧 Audição · ALPHA — indisponível",listenAlphaNotice:"🎧 A audição ALPHA está desativada por má qualidade do áudio. Resultados repostos."}
  };
  for(const [lang,labels] of Object.entries(AUDIO_ALPHA_LABELS))Object.assign(I18N[lang],labels);
  const LISTENING_RELEASE_I18N={
    ru:{listenRangeTitle:"Материал аудирования",listenRangeLabel:"Выбрать упражнения",listenByChapters:"По главам",listenByPages:"По страницам",listenCredit:"Озвучка: Pocket TTS Greek (myned-ai), CC BY 4.0.",listenDifficultyTitle:"Сложность аудирования",listenLevelWords:"1 · Отдельные слова",listenLevelPhrases:"2 · Фразы",listenLevelSentences:"3 · Предложения",listenDifficultyNotice:"Это сложность задания, а не официальная маркировка CEFR. Страницы отдельных карточек ориентировочные."},
    en:{listenRangeTitle:"Listening material",listenRangeLabel:"Select exercises",listenByChapters:"By units",listenByPages:"By pages",listenCredit:"Audio: Pocket TTS Greek (myned-ai), CC BY 4.0.",listenDifficultyTitle:"Listening difficulty",listenLevelWords:"1 · Words",listenLevelPhrases:"2 · Phrases",listenLevelSentences:"3 · Sentences",listenDifficultyNotice:"These are exercise difficulties, not official CEFR labels. Individual page anchors are approximate."},
    zh:{listenRangeTitle:"听力材料",listenRangeLabel:"选择范围",listenByChapters:"按章节",listenByPages:"按页码",listenCredit:"语音来源：Pocket TTS Greek (myned-ai)，CC BY 4.0。",listenDifficultyTitle:"听力难度",listenLevelWords:"1 · 单词",listenLevelPhrases:"2 · 短语",listenLevelSentences:"3 · 句子",listenDifficultyNotice:"这里按题型难度分类，不是官方 CEFR 等级。单题页码为近似值。"},
    ar:{listenRangeTitle:"مواد الاستماع",listenRangeLabel:"اختر النطاق",listenByChapters:"حسب الوحدات",listenByPages:"حسب الصفحات",listenCredit:"الصوت: Pocket TTS Greek (myned-ai)، CC BY 4.0.",listenDifficultyTitle:"صعوبة الاستماع",listenLevelWords:"1 · كلمات",listenLevelPhrases:"2 · عبارات",listenLevelSentences:"3 · جمل",listenDifficultyNotice:"هذه مستويات لصعوبة التمرين وليست تصنيف CEFR رسميًا. أرقام صفحات التمارين تقريبية."},
    es:{listenRangeTitle:"Material auditivo",listenRangeLabel:"Elegir rango",listenByChapters:"Por unidades",listenByPages:"Por páginas",listenCredit:"Audio: Pocket TTS Greek (myned-ai), CC BY 4.0.",listenDifficultyTitle:"Dificultad auditiva",listenLevelWords:"1 · Palabras",listenLevelPhrases:"2 · Frases",listenLevelSentences:"3 · Oraciones",listenDifficultyNotice:"La dificultad es por tipo de ejercicio, no una clasificación oficial CEFR. Las páginas individuales son aproximadas."},
    pt:{listenRangeTitle:"Material de audição",listenRangeLabel:"Escolher intervalo",listenByChapters:"Por unidades",listenByPages:"Por páginas",listenCredit:"Áudio: Pocket TTS Greek (myned-ai), CC BY 4.0.",listenDifficultyTitle:"Dificuldade de audição",listenLevelWords:"1 · Palavras",listenLevelPhrases:"2 · Expressões",listenLevelSentences:"3 · Frases completas",listenDifficultyNotice:"São níveis de dificuldade do exercício, não CEFR oficial. As páginas individuais são aproximadas."}
  };
  for(const [locale,labels] of Object.entries(LISTENING_RELEASE_I18N))Object.assign(I18N[locale],labels);
  const ENGINE_I18N={
    ru:{adaptiveMode:"Адаптивная сложность по моим ответам",srsOptIn:"Включить интервальные повторения новых ответов",srsNotice:"Расписание включается добровольно; прежняя история не изменяется.",srsStart:"Повторить по расписанию",srsStatus:"К повторению: {due}; в расписании: {total}",srsSession:"ИНТЕРВАЛЬНЫЕ ПОВТОРЫ",srsEmpty:"Нет карточек к повторению.",masteryTitle:"КАРТА ОСВОЕНИЯ ГЛАВ",masteryHeading:"Прогресс по главам",masteryNotice:"20 глав; цвет отражает точность, менее 8 ответов — предварительные данные. Страницы ориентировочны.",masteryTip:"Глава {chapter}: {pct}% из {count} ответов",masteryUnseen:"Глава {chapter}: пока без ответов",explanationTitle:"Пояснение",paceKind:"Твой темп: около {pace} сек./задание.",paceDefault:"Примерный темп: {pace} сек./задание."},
    en:{adaptiveMode:"Adaptive difficulty based on my answers",srsOptIn:"Enable spaced repetition for new answers",srsNotice:"Opt-in only; earlier results stay unchanged.",srsStart:"Review scheduled cards",srsStatus:"Due: {due}; scheduled: {total}",srsSession:"SPACED REVIEW",srsEmpty:"No cards due for review.",masteryTitle:"CHAPTER MASTERY MAP",masteryHeading:"Progress by chapter",masteryNotice:"20 chapters, colour indicates accuracy; under 8 answers is provisional. Page tags are approximate.",masteryTip:"Chapter {chapter}: {pct}% of {count} answers",masteryUnseen:"Chapter {chapter}: no answers yet",explanationTitle:"Explanation",paceKind:"Your pace: around {pace} sec/item.",paceDefault:"Estimated pace: {pace} sec/item."},
    zh:{adaptiveMode:"按答题情况调整难度",srsOptIn:"对新答案开启间隔复习",srsNotice:"自愿启用，不更改以往进度。",srsStart:"复习到期卡片",srsStatus:"待复习：{due}；已安排：{total}",srsSession:"间隔复习",srsEmpty:"暂无到期卡片。",masteryTitle:"章节掌握地图",masteryHeading:"各章进度",masteryNotice:"共20章；颜色代表正确率，少于8次作答仅供参考。页码近似。",masteryTip:"第{chapter}章：{count}次，{pct}%正确",masteryUnseen:"第{chapter}章：尚无答题",explanationTitle:"说明",paceKind:"你的速度：约每题{pace}秒。",paceDefault:"估计每题{pace}秒。"},
    ar:{adaptiveMode:"صعوبة متكيفة مع إجاباتي",srsOptIn:"تفعيل المراجعة المتباعدة للإجابات الجديدة",srsNotice:"تُفعّل اختياريًا ولا تغيّر النتائج السابقة.",srsStart:"مراجعة البطاقات المستحقة",srsStatus:"مستحقة: {due}؛ مجدولة: {total}",srsSession:"مراجعة متباعدة",srsEmpty:"لا توجد بطاقات للمراجعة الآن.",masteryTitle:"خريطة إتقان الوحدات",masteryHeading:"التقدم حسب الوحدة",masteryNotice:"20 وحدة؛ اللون يوضح الدقة، وأقل من 8 إجابات تقدير أولي. الصفحات تقريبية.",masteryTip:"الوحدة {chapter}: دقة {pct}% من {count} إجابات",masteryUnseen:"الوحدة {chapter}: دون إجابات",explanationTitle:"التفسير",paceKind:"سرعتك: نحو {pace} ثانية للسؤال.",paceDefault:"السرعة المقدرة: {pace} ثانية للسؤال."},
    es:{adaptiveMode:"Dificultad adaptativa según mis respuestas",srsOptIn:"Activar repetición espaciada para respuestas nuevas",srsNotice:"Opcional; no modifica tu historial.",srsStart:"Repasar tarjetas programadas",srsStatus:"Pendientes: {due}; programadas: {total}",srsSession:"REPASO ESPACIADO",srsEmpty:"No hay tarjetas pendientes.",masteryTitle:"MAPA DE DOMINIO POR UNIDAD",masteryHeading:"Progreso por unidad",masteryNotice:"20 unidades; color según precisión, menos de 8 respuestas es provisional. Páginas aproximadas.",masteryTip:"Unidad {chapter}: {pct}% en {count} respuestas",masteryUnseen:"Unidad {chapter}: sin respuestas",explanationTitle:"Explicación",paceKind:"Tu ritmo: unos {pace} s/pregunta.",paceDefault:"Ritmo estimado: {pace} s/pregunta."},
    pt:{adaptiveMode:"Dificuldade adaptativa segundo as respostas",srsOptIn:"Ativar repetição espaçada para novas respostas",srsNotice:"É opcional e não altera o histórico.",srsStart:"Rever cartões agendados",srsStatus:"Pendentes: {due}; agendados: {total}",srsSession:"REVISÃO ESPAÇADA",srsEmpty:"Não há cartões pendentes.",masteryTitle:"MAPA DE DOMÍNIO POR UNIDADE",masteryHeading:"Progresso por unidade",masteryNotice:"20 unidades; cor pela precisão, menos de 8 respostas é provisório. Páginas aproximadas.",masteryTip:"Unidade {chapter}: {pct}% em {count} respostas",masteryUnseen:"Unidade {chapter}: sem respostas",explanationTitle:"Explicação",paceKind:"O teu ritmo: cerca de {pace} s/cartão.",paceDefault:"Ritmo estimado: {pace} s/cartão."}
  };
  for(const [loc,labels] of Object.entries(ENGINE_I18N))Object.assign(I18N[loc],labels);
  const PEDAGOGY_ANALYTICS={
    ru:{skillMasteryTitle:"НАВЫКИ",skillMasteryHeading:"Что тренируем",skillMasteryNotice:"Прямые грамматические упражнения отделены от контекстных примеров. Точность — не экзаменационная оценка.",pageMasteryTitle:"ПО СТРАНИЦАМ",pageMasteryHeading:"Где больше всего ошибок",pageMasteryNotice:"Ориентировочные страницы авторских заданий, не страницы конкретных упражнений книги. Только страницы с ≥3 ответами.",pageNumber:"Стр. ",skillName:{article_case:"Артикли и падежи",conjugation:"Спряжения",stress:"Ударения",stress_syllables:"Слоги и ударения",enclitic_stress:"Двойное ударение",grammar_morphology:"Грамматические формы",noun_number:"Число существительных",word_order:"Порядок слов",dialogue_context:"Диалоги",listening:"Аудирование",aorist_examples:"Прошедшее (примеры)",future_examples:"Будущее (примеры)",subjunctive_examples:"Να-конструкции (примеры)",conditional_examples:"Условия (примеры)"}},
    en:{skillMasteryTitle:"SKILLS",skillMasteryHeading:"Skills in practice",skillMasteryNotice:"Direct grammar drills are separate from context examples; accuracy is not a certified level.",pageMasteryTitle:"BY PAGE",pageMasteryHeading:"Pages to revisit",pageMasteryNotice:"Approximate anchors for our own exercises, not original textbook exercises. Only pages with ≥3 answers.",pageNumber:"p. ",skillName:{article_case:"Articles & cases",conjugation:"Conjugation",stress:"Stress marks",stress_syllables:"Syllable stress",enclitic_stress:"Enclitic stress",grammar_morphology:"Grammar forms",noun_number:"Noun number",word_order:"Word order",dialogue_context:"Dialogues",listening:"Listening",aorist_examples:"Past (examples)",future_examples:"Future (examples)",subjunctive_examples:"Subjunctive (examples)",conditional_examples:"Conditions (examples)"}},
    zh:{skillMasteryTitle:"技能",skillMasteryHeading:"技能练习",skillMasteryNotice:"语法专项与语境示例分开统计；正确率不等于认证等级。",pageMasteryTitle:"按页码",pageMasteryHeading:"需要复习的页码",pageMasteryNotice:"作者自编题目的近似页码，不对应教材中的具体习题。仅显示答题≥3次的页码。",pageNumber:"第",skillName:{article_case:"冠词和格",conjugation:"动词变位",stress:"重音",stress_syllables:"音节重音",enclitic_stress:"附着代词双重音",grammar_morphology:"语法词形",noun_number:"名词单复数",word_order:"语序",dialogue_context:"对话",listening:"听力",aorist_examples:"过去时示例",future_examples:"将来时示例",subjunctive_examples:"虚拟式示例",conditional_examples:"条件句示例"}},
    ar:{skillMasteryTitle:"المهارات",skillMasteryHeading:"مهارات نتدرّب عليها",skillMasteryNotice:"تمارين القواعد منفصلة عن الأمثلة السياقية؛ نسبة الصحة ليست مستوى رسميًا.",pageMasteryTitle:"حسب الصفحة",pageMasteryHeading:"صفحات للمراجعة",pageMasteryNotice:"صفحات تقريبية لتماريننا وليست إحالات دقيقة لتمارين الكتاب. تُعرض الصفحات التي لها 3 إجابات على الأقل.",pageNumber:"ص. ",skillName:{article_case:"الأدوات والحالات",conjugation:"تصريف الأفعال",stress:"علامات النبر",stress_syllables:"نبر المقاطع",enclitic_stress:"النبر المزدوج",grammar_morphology:"صيغ القواعد",noun_number:"المفرد والجمع",word_order:"ترتيب الكلمات",dialogue_context:"الحوارات",listening:"الاستماع",aorist_examples:"الماضي (أمثلة)",future_examples:"المستقبل (أمثلة)",subjunctive_examples:"الاحتمال (أمثلة)",conditional_examples:"الشرط (أمثلة)"}},
    es:{skillMasteryTitle:"DESTREZAS",skillMasteryHeading:"Habilidades practicadas",skillMasteryNotice:"La gramática directa se separa de ejemplos contextuales; la precisión no certifica nivel.",pageMasteryTitle:"POR PÁGINA",pageMasteryHeading:"Páginas para repasar",pageMasteryNotice:"Páginas aproximadas de ejercicios originales nuestros, no del libro. Solo páginas con ≥3 respuestas.",pageNumber:"p. ",skillName:{article_case:"Artículos y casos",conjugation:"Conjugación",stress:"Acentos",stress_syllables:"Sílaba tónica",enclitic_stress:"Acento doble",grammar_morphology:"Formas gramaticales",noun_number:"Singular y plural",word_order:"Orden de palabras",dialogue_context:"Diálogos",listening:"Comprensión oral",aorist_examples:"Pasado (ejemplos)",future_examples:"Futuro (ejemplos)",subjunctive_examples:"Subjuntivo (ejemplos)",conditional_examples:"Condicionales (ejemplos)"}},
    pt:{skillMasteryTitle:"COMPETÊNCIAS",skillMasteryHeading:"O que praticamos",skillMasteryNotice:"Exercícios de gramática separados de exemplos de contexto; precisão não é nível certificado.",pageMasteryTitle:"POR PÁGINA",pageMasteryHeading:"Páginas a rever",pageMasteryNotice:"Páginas aproximadas dos nossos exercícios, não exercícios exatos do livro. Apenas páginas com ≥3 respostas.",pageNumber:"p. ",skillName:{article_case:"Artigos e casos",conjugation:"Conjugação",stress:"Acentuação",stress_syllables:"Sílaba tónica",enclitic_stress:"Acento duplo",grammar_morphology:"Formas gramaticais",noun_number:"Singular e plural",word_order:"Ordem das palavras",dialogue_context:"Diálogos",listening:"Compreensão oral",aorist_examples:"Passado (exemplos)",future_examples:"Futuro (exemplos)",subjunctive_examples:"Conjuntivo (exemplos)",conditional_examples:"Condicionais (exemplos)"}}
  };
  for(const [loc,labels] of Object.entries(PEDAGOGY_ANALYTICS)){
    const {skillName,...strings}=labels;
    Object.assign(I18N[loc],strings);
  }
  const LEARNING_UPGRADE_I18N={
    ru:{topicEvidenceTitle:"ТЕМЫ",topicEvidenceHeading:"Словарные темы",topicEvidenceNotice:"Точность по словам темы. Карточка может относиться к нескольким темам. Это не оценка CEFR.",grammarEvidenceTitle:"ГРАММАТИКА",grammarEvidenceHeading:"Грамматические конструкции",grammarEvidenceNotice:"Только прямые упражнения; менее 8 ответов или 3 разных заданий — предварительная оценка.",knowledgeEarly:"пока мало данных",knowledgeUnique:"разных",capacityTaskNote:"С учётом типа и нескольких шагов: около {minutes} мин материала (примерный диапазон {low}–{high}). Это прогноз, а не гарантия."},
    en:{topicEvidenceTitle:"TOPICS",topicEvidenceHeading:"Vocabulary topics",topicEvidenceNotice:"Word answers by topic; one word may count in several topics. Not a certified CEFR level.",grammarEvidenceTitle:"GRAMMAR",grammarEvidenceHeading:"Grammar patterns",grammarEvidenceNotice:"Only direct exercises; fewer than 8 attempts or 3 different targets is preliminary.",knowledgeEarly:"early estimate",knowledgeUnique:"distinct",capacityTaskNote:"Task-aware estimate: around {minutes} min of material (range {low}–{high}); not a guarantee."},
    zh:{topicEvidenceTitle:"主题",topicEvidenceHeading:"词汇主题",topicEvidenceNotice:"按主题统计词汇回答；一词可属于多个主题，并非正式等级。",grammarEvidenceTitle:"语法",grammarEvidenceHeading:"语法练习",grammarEvidenceNotice:"仅统计直接练习，少于8次回答或3个不同目标仅是初步估计。",knowledgeEarly:"数据较少",knowledgeUnique:"不同目标",capacityTaskNote:"考虑各题型及多步骤：约 {minutes} 分钟（{low}–{high}）；不保证实际时长。"},
    ar:{topicEvidenceTitle:"المواضيع",topicEvidenceHeading:"مواضيع المفردات",topicEvidenceNotice:"الإجابات حسب الموضوع؛ قد تظهر الكلمة في أكثر من موضوع. ليس تصنيف CEFR رسميًا.",grammarEvidenceTitle:"القواعد",grammarEvidenceHeading:"تراكيب القواعد",grammarEvidenceNotice:"التمارين المباشرة فقط؛ أقل من 8 إجابات أو 3 عناصر مختلفة تقدير أولي.",knowledgeEarly:"بيانات قليلة",knowledgeUnique:"مختلفة",capacityTaskNote:"تقدير يشمل الخطوات وأنواع المهام: {minutes} دقيقة تقريبًا ({low}–{high}) وليس ضمانًا."},
    es:{topicEvidenceTitle:"TEMAS",topicEvidenceHeading:"Temas de vocabulario",topicEvidenceNotice:"Respuestas por tema; una palabra puede aparecer en varios. No certifica MCER.",grammarEvidenceTitle:"GRAMÁTICA",grammarEvidenceHeading:"Construcciones gramaticales",grammarEvidenceNotice:"Solo ejercicios directos; menos de 8 respuestas o 3 elementos es provisional.",knowledgeEarly:"pocos datos",knowledgeUnique:"diferentes",capacityTaskNote:"Incluye tipos y etapas de ejercicios: ≈{minutes} min (rango {low}–{high}), no garantizado."},
    pt:{topicEvidenceTitle:"TEMAS",topicEvidenceHeading:"Temas do vocabulário",topicEvidenceNotice:"Respostas por tema; a mesma palavra pode pertencer a vários. Não certifica QECR.",grammarEvidenceTitle:"GRAMÁTICA",grammarEvidenceHeading:"Construções gramaticais",grammarEvidenceNotice:"Só exercícios diretos; menos de 8 respostas ou 3 itens é provisório.",knowledgeEarly:"poucos dados",knowledgeUnique:"distintos",capacityTaskNote:"Considera os tipos e etapas dos exercícios: ≈{minutes} min ({low}–{high}), sem garantia."}
  };
  for(const [locale,strings] of Object.entries(LEARNING_UPGRADE_I18N))Object.assign(I18N[locale],strings);
  const LEARNING_GRAMMAR_LABELS={
    ru:{alphabet:"Алфавит",greeting_be:"Знакомство",address_home_present:"Адреса и местонахождение",family_profession_question:"Семья и профессии",languages_b1_and_object_articles:"Языки и артикли",transport_and_time:"Транспорт и время",routine_and_days:"Распорядок",plural_nouns:"Множественное число",clothing_adjective_agreement:"Согласование",home_comparatives:"Сравнения",aorist_narrative:"Прошедшее",future_tense:"Будущее",subjunctive_na:"Конструкции с να",imperative:"Повелительное",medical_conditional:"Условия"},
    en:{alphabet:"Alphabet",greeting_be:"Introductions",address_home_present:"Addresses",family_profession_question:"Family and jobs",languages_b1_and_object_articles:"Languages and articles",transport_and_time:"Transport and time",routine_and_days:"Routine",plural_nouns:"Plurals",clothing_adjective_agreement:"Adjective agreement",home_comparatives:"Comparatives",aorist_narrative:"Past",future_tense:"Future",subjunctive_na:"Να constructions",imperative:"Imperative",medical_conditional:"Conditionals"},
    zh:{alphabet:"字母",greeting_be:"自我介绍",address_home_present:"地址",family_profession_question:"家庭和职业",languages_b1_and_object_articles:"语言和冠词",transport_and_time:"交通时间",routine_and_days:"日常活动",plural_nouns:"复数",clothing_adjective_agreement:"形容词配合",home_comparatives:"比较级",aorist_narrative:"过去",future_tense:"将来",subjunctive_na:"Να 结构",imperative:"祈使句",medical_conditional:"条件句"},
    ar:{alphabet:"الأبجدية",greeting_be:"التعارف",address_home_present:"العناوين",family_profession_question:"الأسرة والمهن",languages_b1_and_object_articles:"اللغات والأدوات",transport_and_time:"النقل والوقت",routine_and_days:"الروتين",plural_nouns:"الجمع",clothing_adjective_agreement:"تطابق الصفات",home_comparatives:"المقارنة",aorist_narrative:"الماضي",future_tense:"المستقبل",subjunctive_na:"تراكيب να",imperative:"الأمر",medical_conditional:"الشرط"},
    es:{alphabet:"Alfabeto",greeting_be:"Presentaciones",address_home_present:"Direcciones",family_profession_question:"Familia y profesiones",languages_b1_and_object_articles:"Idiomas y artículos",transport_and_time:"Transporte y tiempo",routine_and_days:"Rutina",plural_nouns:"Plurales",clothing_adjective_agreement:"Concordancia",home_comparatives:"Comparativos",aorist_narrative:"Pasado",future_tense:"Futuro",subjunctive_na:"Construcciones να",imperative:"Imperativo",medical_conditional:"Condicionales"},
    pt:{alphabet:"Alfabeto",greeting_be:"Apresentações",address_home_present:"Moradas",family_profession_question:"Família e profissões",languages_b1_and_object_articles:"Línguas e artigos",transport_and_time:"Transporte e tempo",routine_and_days:"Rotina",plural_nouns:"Plurais",clothing_adjective_agreement:"Concordância",home_comparatives:"Comparativos",aorist_narrative:"Passado",future_tense:"Futuro",subjunctive_na:"Construções να",imperative:"Imperativo",medical_conditional:"Condicionais"}
  };

  const VOCAB_KNOWLEDGE_I18N={
    ru:{vocabEvidenceTitle:"СЛОВАРЬ A1/A2",vocabEvidenceHeading:"Темы отдельного словаря",vocabEvidenceNotice:"Точность по десятисловным урокам A1/A2; отдельно от тренировки учебника."},
    en:{vocabEvidenceTitle:"A1/A2 VOCABULARY",vocabEvidenceHeading:"Standalone vocabulary topics",vocabEvidenceNotice:"Performance on ten-word A1/A2 lessons, kept separate from textbook exercises."},
    zh:{vocabEvidenceTitle:"A1/A2 词汇",vocabEvidenceHeading:"独立词汇主题",vocabEvidenceNotice:"来自十词一组的学习进度，与教材练习分开统计。"},
    ar:{vocabEvidenceTitle:"مفردات A1/A2",vocabEvidenceHeading:"مواضيع المفردات المستقلة",vocabEvidenceNotice:"النتائج من دروس العشر كلمات، منفصلة عن تدريب الكتاب."},
    es:{vocabEvidenceTitle:"VOCABULARIO A1/A2",vocabEvidenceHeading:"Temas del curso independiente",vocabEvidenceNotice:"Resultados de las lecciones de diez palabras, separados del manual."},
    pt:{vocabEvidenceTitle:"VOCABULÁRIO A1/A2",vocabEvidenceHeading:"Temas do vocabulário independente",vocabEvidenceNotice:"Resultados das lições de dez palavras, separados do manual."}
  };
  for(const [locale,strings] of Object.entries(VOCAB_KNOWLEDGE_I18N))Object.assign(I18N[locale],strings);

  const SYLLABLE_I18N={
    ru:{syllableMode:"Ударный слог",syllableHelp:"Выбери слог, на который падает ударение. Слоги показаны без ударений.",syllableExplanation:"Ударение по слогам"},
    en:{syllableMode:"Stressed syllable",syllableHelp:"Choose the stressed syllable. All syllables are shown without accents.",syllableExplanation:"Syllable stress"},
    zh:{syllableMode:"重读音节",syllableHelp:"选择重读音节；音节均不标重音。",syllableExplanation:"音节重音"},
    ar:{syllableMode:"المقطع المشدد",syllableHelp:"اختر المقطع المشدد. المقاطع معروضة دون علامات النبر.",syllableExplanation:"نبر المقاطع"},
    es:{syllableMode:"Sílaba tónica",syllableHelp:"Elige la sílaba tónica. Los fragmentos no llevan tilde.",syllableExplanation:"Acento por sílabas"},
    pt:{syllableMode:"Sílaba tónica",syllableHelp:"Escolhe a sílaba tónica. As sílabas são mostradas sem acentos.",syllableExplanation:"Acentuação por sílabas"}
  };
  for(const [l,x] of Object.entries(SYLLABLE_I18N))Object.assign(I18N[l],x);
  const WORD_AUDIO_I18N={
    ru:{wordListen:"🔊 Послушать слово",wordListenSlow:"0,8× Медленно",wordAudioPocket:"Воспроизводится запись Pocket TTS.",wordAudioUnavailable:"Запись Pocket TTS для этого слова пока не готова.",wordAudioError:"Не удалось воспроизвести запись.",wordAudioDone:"Готово."},
    en:{wordListen:"🔊 Hear the word",wordListenSlow:"0.8× Slower",wordAudioPocket:"Playing the offline Pocket TTS recording.",wordAudioUnavailable:"Pocket TTS recording for this word is not ready yet.",wordAudioError:"Could not play this word.",wordAudioDone:"Finished."},
    zh:{wordListen:"🔊 听单词",wordListenSlow:"0.8× 慢速",wordAudioPocket:"正在播放 Pocket TTS 离线录音。",wordAudioUnavailable:"这个词的 Pocket TTS 录音尚未准备好。",wordAudioError:"无法播放这个单词。",wordAudioDone:"播放完毕。"},
    ar:{wordListen:"🔊 استمع إلى الكلمة",wordListenSlow:"0.8× أبطأ",wordAudioPocket:"يُشغّل تسجيل Pocket TTS المحفوظ.",wordAudioUnavailable:"تسجيل Pocket TTS لهذه الكلمة غير جاهز بعد.",wordAudioError:"تعذّر تشغيل الكلمة.",wordAudioDone:"انتهى التشغيل."},
    es:{wordListen:"🔊 Escuchar palabra",wordListenSlow:"0,8× Más despacio",wordAudioPocket:"Reproduciendo grabación sin conexión de Pocket TTS.",wordAudioUnavailable:"La grabación Pocket TTS de esta palabra aún no está lista.",wordAudioError:"No se pudo reproducir la palabra.",wordAudioDone:"Reproducción terminada."},
    pt:{wordListen:"🔊 Ouvir a palavra",wordListenSlow:"0,8× Devagar",wordAudioPocket:"A reproduzir gravação offline Pocket TTS.",wordAudioUnavailable:"A gravação Pocket TTS desta palavra ainda não está pronta.",wordAudioError:"Não foi possível reproduzir a palavra.",wordAudioDone:"Reprodução terminada."}
  };
  for(const [loc,strings] of Object.entries(WORD_AUDIO_I18N))Object.assign(I18N[loc],strings);

  const GRAMMAR_AUDIO_I18N={
    ru:{encliticMode:"Двойное ударение",encliticExplanation:"Ударения и энклитики",mixListeningLabel:"Добавлять аудирование в обычные занятия (около 20%)"},
    en:{encliticMode:"Double accent",encliticExplanation:"Enclitics and stress",mixListeningLabel:"Include listening questions in regular lessons (about 20%)"},
    zh:{encliticMode:"双重音",encliticExplanation:"附着代词与重音",mixListeningLabel:"普通课程中加入听力题（约20%）"},
    ar:{encliticMode:"النبر المزدوج",encliticExplanation:"الضمائر المتصلة والنبر",mixListeningLabel:"إضافة الاستماع إلى الدروس العادية (نحو 20٪)"},
    es:{encliticMode:"Doble acento",encliticExplanation:"Enclíticos y acentuación",mixListeningLabel:"Incluir audición en clases normales (aprox. 20 %)"},
    pt:{encliticMode:"Acento duplo",encliticExplanation:"Ênclises e acentuação",mixListeningLabel:"Incluir audição nas aulas normais (cerca de 20%)"}
  };
  for(const [l,strings] of Object.entries(GRAMMAR_AUDIO_I18N))Object.assign(I18N[l],strings);

  const GRAMMAR2_I18N={
    ru:{grammarMode:"Грамматика 2.0",grammarExplanation:"Разбор формы"},
    en:{grammarMode:"Grammar 2.0",grammarExplanation:"Grammar form"},
    zh:{grammarMode:"语法 2.0",grammarExplanation:"词形讲解"},
    ar:{grammarMode:"القواعد 2.0",grammarExplanation:"شرح الصيغة"},
    es:{grammarMode:"Gramática 2.0",grammarExplanation:"Forma gramatical"},
    pt:{grammarMode:"Gramática 2.0",grammarExplanation:"Forma gramatical"}
  };
  for(const [lang,strings] of Object.entries(GRAMMAR2_I18N))Object.assign(I18N[lang],strings);
  const kindIds=["word","number","phrase","sentence","dialogue","plural","letter","accent","syllable","enclitic","grammar","verb","article","order","listening"];
  const kinds={word:"words",number:"numbers",phrase:"phrases",sentence:"sentences",dialogue:"dialogues",plural:"plurals",letter:"alphabet",accent:"accent",syllable:"syllableMode",enclitic:"encliticMode",grammar:"grammarMode",verb:"verbsMode",article:"articlesMode",order:"orderMode",listening:"listenMode"};
  const CROSS_DEVICE_I18N={
    ru:{continueRemotePrompt:"У тебя есть незавершённое занятие на другом устройстве. Продолжить его здесь? Другое устройство прекратит отправку новых ответов.",resumeRemoteNotice:"Занятие перенесено с другого устройства.",handoffStopped:"Занятие продолжено на другом устройстве. Здесь оно остановлено.",sessionSyncUnavailable:"Серверная синхронизация временно недоступна; занятие сохраняется в этом браузере."},
    en:{continueRemotePrompt:"An unfinished lesson exists on another device. Continue here? The other device will no longer submit new answers.",resumeRemoteNotice:"Lesson transferred from another device.",handoffStopped:"This lesson moved to another device and is now stopped here.",sessionSyncUnavailable:"Server sync temporarily unavailable; the lesson is saved in this browser."},
    zh:{continueRemotePrompt:"其他设备上有未完成的课程。要在这里继续吗？原设备将停止提交新答案。",resumeRemoteNotice:"课程已从其他设备转移。",handoffStopped:"课程已在其他设备继续，本设备已停止。",sessionSyncUnavailable:"服务器同步暂时不可用；课程仍保存在此浏览器中。"},
    ar:{continueRemotePrompt:"لديك درس غير مكتمل على جهاز آخر. هل تتابعه هنا؟ سيتوقف الجهاز الآخر عن إرسال إجابات جديدة.",resumeRemoteNotice:"نُقل الدرس من جهاز آخر.",handoffStopped:"استُكمل الدرس على جهاز آخر وتوقف هنا.",sessionSyncUnavailable:"المزامنة غير متاحة مؤقتًا؛ الدرس محفوظ في هذا المتصفح."},
    es:{continueRemotePrompt:"Tienes una lección sin terminar en otro dispositivo. ¿Continuar aquí? El otro dispositivo dejará de enviar nuevas respuestas.",resumeRemoteNotice:"Lección transferida desde otro dispositivo.",handoffStopped:"La lección se ha transferido a otro dispositivo y se ha detenido aquí.",sessionSyncUnavailable:"Sincronización temporalmente no disponible; la lección se guarda en este navegador."},
    pt:{continueRemotePrompt:"Tens uma lição por terminar noutro dispositivo. Continuar aqui? O outro deixará de enviar novas respostas.",resumeRemoteNotice:"Lição transferida de outro dispositivo.",handoffStopped:"A lição foi transferida para outro dispositivo e parou aqui.",sessionSyncUnavailable:"Sincronização temporariamente indisponível; a lição fica guardada neste navegador."}
  };
  for(const [lang,strings] of Object.entries(CROSS_DEVICE_I18N))Object.assign(I18N[lang],strings);
  const SESSION_STORAGE_KEY="greek-active-session-v2";
  const SESSION_TEXT={
    ru:{resumeNotice:"Занятие восстановлено после перезагрузки.",retryAnswer:"Повторить отправку ответа",recoveryInfo:"Ответ мог сохраниться на сервере. Повторная отправка безопасна и не начислит вторую попытку.",resumeExpired:"Время сохранённого занятия истекло."},
    en:{resumeNotice:"Your session was restored.",retryAnswer:"Retry answer safely",recoveryInfo:"The server may have saved this answer. Retrying cannot count it twice.",resumeExpired:"The saved session has expired."},
    zh:{resumeNotice:"已恢复上次的练习。",retryAnswer:"安全重试答案",recoveryInfo:"服务器可能已记录此答案。重复发送不会重复计分。",resumeExpired:"上次练习的时间已结束。"},
    ar:{resumeNotice:"استُعيدت الجلسة السابقة.",retryAnswer:"إعادة إرسال الإجابة بأمان",recoveryInfo:"ربما سُجّلت الإجابة بالفعل؛ إعادة المحاولة لا تحتسبها مرتين.",resumeExpired:"انتهى وقت الجلسة المحفوظة."},
    es:{resumeNotice:"Se ha recuperado la sesión.",retryAnswer:"Reintentar respuesta sin duplicados",recoveryInfo:"El servidor podría haber guardado la respuesta. Repetir no la contabiliza dos veces.",resumeExpired:"La sesión guardada ha caducado."},
    pt:{resumeNotice:"A sessão foi recuperada.",retryAnswer:"Reenviar resposta sem duplicar",recoveryInfo:"O servidor poderá ter guardado a resposta. Reenviar não conta duas vezes.",resumeExpired:"A sessão guardada expirou."}
  };
  for(const [lang,strings] of Object.entries(SESSION_TEXT))Object.assign(I18N[lang],strings);
  const newRequestId=()=>window.crypto?.randomUUID?.()||
    "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,c=>{
      const r=Math.floor(Math.random()*16);return (c==="x"?r:(r&3|8)).toString(16);
    });
  const DEVICE_KEY="greek-student-device-v1";
  const deviceId=(()=>{
    try{
      let id=localStorage.getItem(DEVICE_KEY);
      if(!id||!/^[a-f0-9-]{36}$/i.test(id)){
        id=newRequestId();localStorage.setItem(DEVICE_KEY,id);
      }
      return id;
    }catch{return newRequestId();}
  })();
  let remoteTimer=null;
  let pendingRemoteSnapshot=null;
  let remoteQueue=Promise.resolve();
  function flushRemoteSnapshot(){
    if(remoteTimer){clearTimeout(remoteTimer);remoteTimer=null;}
    const snapshot=pendingRemoteSnapshot;
    pendingRemoteSnapshot=null;
    if(!snapshot||!state.remoteEnabled||!state.remoteSessionId)return remoteQueue;
    const epoch=state.remoteEpoch;
    const sid=state.remoteSessionId;
    remoteQueue=remoteQueue.catch(()=>{}).then(async()=>{
      if(epoch!==state.remoteEpoch||!state.loggedIn)return;
      const op=state.remoteRevision?'save':'start';
      const body={op,sessionId:sid,deviceId,revision:state.remoteRevision||0,snapshot};
      try{
        const reply=await api("session",{method:"POST",
          headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
        if(epoch===state.remoteEpoch&&sid===state.remoteSessionId){
          state.remoteRevision=reply.revision;
          state.remoteSynced=true;
        }
      }catch(err){
        if(epoch!==state.remoteEpoch)return;
        if(err.message==="session_conflict"){
          state.remoteLost=true;
          if(!$("quiz").hidden){
            state.finishing=true;clearInterval(state.timer);
            window.LexiWordAudio?.stop();
            show("quiz",false);show("setup",true);
            txt("setup-error",t("handoffStopped"));show("setup-error",true);
          }
        }else{
          state.remoteSynced=false;
          if(!$("quiz").hidden)txt("resume-message",t("sessionSyncUnavailable"));
        }
      }
    });
    return remoteQueue;
  }
  function queueRemoteSnapshot(snapshot){
    if(!state.remoteEnabled||!state.remoteSessionId||state.remoteLost)return;
    pendingRemoteSnapshot=snapshot;
    if(remoteTimer)clearTimeout(remoteTimer);
    remoteTimer=setTimeout(flushRemoteSnapshot,200);
  }
  function persistActiveSession(){
    if(state.restoring||!state.loggedIn||!state.profile?.nickname||!state.deadline||state.finishing)return;
    const snapshot={
      version:2,nickname:state.profile.nickname,deadline:state.deadline,started:state.started,
      sessionId:state.remoteSessionId,
      settings:state.settings,mode:state.mode,questions:state.questions,index:state.index,
      seen:state.seen,count:state.count,correct:state.correct,wrong:state.wrong,
      answered:state.answered,verbStage:state.verbStage,dialogueStep:state.dialogueStep,
      dialogueFilled:state.dialogueFilled,orderIndices:state.orderIndices,
      pendingAnswer:state.pendingAnswer||null,savedAt:Date.now()
    };
    try{localStorage.setItem(SESSION_STORAGE_KEY,JSON.stringify(snapshot));}catch{}
    queueRemoteSnapshot(snapshot);
  }
  function clearActiveSession(clearRemote=false){
    state.pendingAnswer=null;
    try{localStorage.removeItem(SESSION_STORAGE_KEY);}catch{}
    if(remoteTimer){clearTimeout(remoteTimer);remoteTimer=null;}
    pendingRemoteSnapshot=null;
    const sid=state.remoteSessionId;
    const revision=state.remoteRevision;
    if(clearRemote&&sid&&state.remoteEnabled&&revision){
      remoteQueue=remoteQueue.catch(()=>{}).then(async()=>{
        try{
          await api("session",{method:"POST",headers:{"Content-Type":"application/json"},
            body:JSON.stringify({op:"clear",sessionId:sid,deviceId,
                                 revision})});
        }catch{} // A transferred session must never be deleted by its former owner.
      });
    }
    state.remoteEpoch=(state.remoteEpoch||0)+1;
    state.remoteSessionId=null;state.remoteRevision=0;state.remoteLost=false;
  }
  async function retryPendingAnswer(){
    if(!state.pendingAnswer||state.busy)return;
    const pending={...state.pendingAnswer};
    await choose(pending.index,pending.overrideSelected,pending.requestId);
  }
  async function restoreActiveSession(){
    if(!state.loggedIn||!state.profile?.nickname)return;
    let saved=null;
    try{saved=JSON.parse(localStorage.getItem(SESSION_STORAGE_KEY)||"null");}catch{}
    if(saved?.nickname!==state.profile.nickname)saved=null;
    let remote=null;
    try{remote=await api("session");state.remoteEnabled=true;}
    catch{state.remoteEnabled=false;}
    let transferred=false;
    if(remote?.exists&&remote.snapshot?.deadline>Date.now()){
      if(remote.ownerDevice!==deviceId){
        if(!window.confirm(t("continueRemotePrompt")))return;
        try{
          const claimed=await api("session",{method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({op:"takeover",sessionId:remote.sessionId,deviceId,
                                 revision:remote.revision})});
          saved=claimed.snapshot;transferred=true;
          state.remoteSessionId=remote.sessionId;
          state.remoteRevision=claimed.revision;
          if(saved.pendingAnswer?.body){
            saved.pendingAnswer.body.deviceId=deviceId;
            saved.pendingAnswer.body.sessionId=remote.sessionId;
          }
        }catch{return;}
      }else{
        state.remoteSessionId=remote.sessionId;state.remoteRevision=remote.revision;
        if(!saved||saved.sessionId!==remote.sessionId||
           Number(remote.snapshot.savedAt)>Number(saved.savedAt))
          saved=remote.snapshot;
      }
    }
    if(!saved)return;
    if(!state.remoteSessionId){
      state.remoteSessionId=saved.sessionId||newRequestId();
      state.remoteRevision=0;
    }
    if(saved.version!==2||saved.nickname!==state.profile.nickname||
       !Array.isArray(saved.questions)||saved.questions.length>60||
       !Number.isInteger(saved.index)||saved.index<0||saved.index>=saved.questions.length||
       !saved.settings||!Number.isFinite(saved.deadline)){
      clearActiveSession();return;
    }
    if(saved.deadline<=Date.now()){
      clearActiveSession();return;
    }
    state.restoring=true;
    state.settings=saved.settings;state.mode=saved.mode||"all";
    state.questions=saved.questions;state.index=saved.index;
    state.seen=Array.isArray(saved.seen)?saved.seen:[];
    state.count=Number(saved.count)||0;state.correct=Number(saved.correct)||0;state.wrong=Number(saved.wrong)||0;
    state.started=saved.started;state.deadline=saved.deadline;
    state.finishing=false;state.busy=false;
    $("lang").value=state.settings.lang||"ru";updateLanguage();$("lang").disabled=true;
    show("setup",false);show("quiz",true);show("finished",false);setPage("practice");
    renderQuestion();
    if(saved.verbStage===2&&state.current.kind==="verb")renderVerbTranslation();
    if(state.current.kind==="dialogue"&&saved.dialogueStep>0){
      state.dialogueStep=Math.min(saved.dialogueStep,state.current.gapIndices.length-1);
      state.dialogueFilled=saved.dialogueFilled||{};
      renderDialogueGap();
    }
    if(state.current.kind==="order"&&Array.isArray(saved.orderIndices)&&!saved.pendingAnswer){
      state.orderIndices=saved.orderIndices.filter(x=>Number.isInteger(x)&&x>=0&&x<state.current.tokens.length);
      renderOrder();
    }
    state.pendingAnswer=saved.pendingAnswer||null;
    state.restoring=false;
    updateTimer();clearInterval(state.timer);state.timer=setInterval(updateTimer,1000);
    if(state.pendingAnswer){
      show("retry-answer",true);
      txt("recovery-note",t("recoveryInfo"));show("recovery-note",true);
      // Same immutable request ID; server returns the first committed result,
      // including cases where a reverse-proxy 502 hid the original response.
      await retryPendingAnswer();
    }else if(saved.answered){
      state.answered=true;
      await nextQuestion();
    }else{
      persistActiveSession();
    }
    if(!$("quiz").hidden)txt("resume-message",t(transferred?"resumeRemoteNotice":"resumeNotice"));
  }

  const state={joinedLeaderboard:false,catalog:null,topicCatalog:null,profile:null,loggedIn:false,authMode:"register",questions:[],index:0,current:null,mode:"all",answered:false,busy:false,
    correct:0,wrong:0,seen:[],count:0,deadline:0,started:0,timer:null,finishing:false,settings:null,
    remoteEpoch:0,remoteSessionId:null,remoteRevision:0,remoteEnabled:true,remoteSynced:false,remoteLost:false};
  const t=key => I18N[$("lang").value]?.[key] ?? I18N.en[key] ?? key;
  const hint=(value,en)=>$("lang").value!=="en"&&en&&value.trim().toLowerCase()!==en.trim().toLowerCase()?value+" ("+en+")":value;
  const training=()=>document.querySelector('input[name=training]:checked')?.value||"textbook";
  async function updatePersonalizedStatus(){
    if(!state.loggedIn||training()!=="personalized")return;
    try{
      const data=await api("personalized/status");
      txt("personalized-status",t("personalizedProgress").replace("{count}",data.learned).replace("{weak}",data.needsReview));
    }catch{txt("personalized-status",t("loading"));}
  }
  function updateTraining(){
    const personal=training()==="personalized";
    show("verb-scope-option",!personal);
    if(personal&&mode()==="verbs"){
      document.querySelector('input[name="scope"][value="pages"]').checked=true;
      showScope();return;
    }
    txt("training-description",t(personal?"personalizedTrainingInfo":"textbookTrainingInfo"));
    show("personalized-status",personal);
    if(personal)updatePersonalizedStatus();
  }
  const show=(id,visible)=>{$(id).hidden=!visible;};
  const txt=(id,value)=>{$(id).textContent=String(value);};
  const duration=()=>Number(document.querySelector('input[name=duration]:checked')?.value||20);
  const mode=()=>document.querySelector('input[name=scope]:checked')?.value||"pages";
  const selectedChapters=()=>Array.from($("chapter-grid").querySelectorAll('input:checked')).map(x=>Number(x.value));
  const listeningRange=()=>$("listening-range").value;
  const selectedListeningKinds=()=>Array.from($("listening-difficulty").querySelectorAll('input:checked')).map(x=>x.value);
  const selectedKinds=()=>Array.from($("kind-options").querySelectorAll('input:checked')).map(x=>x.value);
  async function api(path,options){
    const res=await fetch("/greek/api/"+path,{credentials:"same-origin",cache:"no-store",...options});
    if(!res.ok){
      let message="HTTP "+res.status;
      try{const body=await res.json();if(body?.error)message=body.error;}catch{}
      throw new Error(message);
    }
    return res.json();
  }
  function saveSettings(){
    try {localStorage.setItem(STORAGE,JSON.stringify({
       chapterNumberingVersion:2,kindSchemaVersion:5,
       lang:$("lang").value,scope:mode(),training:training(),from:$("page-from").value,to:$("page-to").value,
       chapters:state.bookChapters||selectedChapters(),listeningChapters:state.listeningChapters||[1,2,3,4],types:selectedKinds(),duration:duration(),
       topics:selectedTopics(),levels:selectedLevels(),groups:selectedGroups(),maxUnit:verbMaxUnit(),
       listeningRange:listeningRange(),listeningKinds:selectedListeningKinds(),listenMix:$("listen-mix").checked,
       adaptive:$("adaptive-mode").checked,srsOptIn:$("srs-optin").checked
    }));}catch{}
  }
  function restoreSettings(){
    let o={};try{o=JSON.parse(localStorage.getItem(STORAGE)||"{}")||{};}catch{}
    if(["ru","en","zh","ar","es","pt"].includes(o.lang))$("lang").value=o.lang;
    if(o.training==="personalized")document.querySelector('input[name="training"][value="personalized"]').checked=true;
    if(["chapters","verbs","listening"].includes(o.scope))
       document.querySelector('input[name=scope][value="'+(o.scope==="listening"&&document.querySelector('input[name=scope][value="listening"]').disabled?"chapters":o.scope)+'"]').checked=true;
    if(["chapters","pages"].includes(o.listeningRange))$("listening-range").value=o.listeningRange;
    $("listen-mix").checked=o.listenMix!==false;
    $("adaptive-mode").checked=o.adaptive===true;
    $("srs-optin").checked=o.srsOptIn===true;
    if(Array.isArray(o.listeningKinds))$("listening-difficulty").querySelectorAll('input').forEach(x=>x.checked=o.listeningKinds.includes(x.value));
    if(Array.isArray(o.levels))$("level-options").querySelectorAll('input').forEach(x=>x.checked=o.levels.includes(x.value));
    if(Array.isArray(o.groups))$("verb-group-options").querySelectorAll('input').forEach(x=>x.checked=o.groups.includes(x.value));
    if(o.maxUnit!==undefined){
      const value=String(Math.max(2,Math.min(20,Number(o.maxUnit)||4)));
      if([...$("verb-max-unit").options].some(x=>x.value===value))$("verb-max-unit").value=value;
    }
    $("page-from").value=Math.min(312,Math.max(1,parseInt(o.from,10)||1));
    $("page-to").value=Math.min(312,Math.max(1,parseInt(o.to,10)||56));
    if(Array.isArray(o.types)){
      const types=new Set(o.types);
      // One-time upgrade for existing learners: introduce the new optional
      // double-stress skill without erasing any prior selected material types.
      if(!o.kindSchemaVersion)types.add("enclitic");
      if((Number(o.kindSchemaVersion)||0)<5)types.add("grammar");
      $("kind-options").querySelectorAll('input').forEach(x=>x.checked=types.has(x.value));
    }
    if([10,15,20,30,45,60].includes(Number(o.duration)))document.querySelector('input[name=duration][value="'+o.duration+'"]').checked=true;
    // Settings saved before the PDF-aligned release used 16 *teaching*
    // chapters. Preserve the user's selected topics when switching to the
    // printed 20-unit numbering; migrate only once on subsequent save.
    if(o.chapterNumberingVersion!==2 && Array.isArray(o.chapters)){
      const oldToPrinted={1:1,2:2,3:3,4:4,5:6,6:7,7:8,8:9,9:11,10:12,11:13,12:14,13:16,14:17,15:18,16:19,0:0,"-1":5,"-2":10,"-3":15,"-4":20,"-5":-5};
      o.chapters=[...new Set(o.chapters.map(x=>oldToPrinted[x]).filter(x=>x!==undefined))];
    }
    return o;
  }
  function updateLanguage(){
    document.documentElement.lang=$("lang").value;
    document.documentElement.dir=$("lang").value==="ar"?"rtl":"ltr";
    document.querySelectorAll("[data-i18n]").forEach(el=>el.textContent=t(el.dataset.i18n));
    // Labels computed after fetch must be refreshed on every language change.
    // Previously catalog-summary kept Russian even when the selector said PT.
    if(state.catalog)txt("catalog-summary",t("available").replace("{count}",state.catalog.practiceCardCount||state.catalog.cardCount));
    $("auth-name").placeholder=t("nicknamePlaceholder");
    document.title=t("footerBrand");
    document.querySelector(".brand").setAttribute("aria-label",t("footerBrand"));
    if($("auth-lang"))$("auth-lang").value=$("lang").value;
    if(window.lexiVocab)window.lexiVocab.onLanguageChange();
    if(state.catalog)renderChapters();
    showScope();
    if(state.profile?.registered)txt("student-nickname",state.profile.nickname);
    if(state.topicCatalog){renderTopics();renderVerbReference();renderVerbStageSummary();}
    if(!$("study-word-list").hidden)loadTopicWords();
    txt("preview-topic-words",t($("study-word-list").hidden?"previewWords":"previewHide"));
    showAuthMode();updateTraining();
    if(!$("leaderboard-view").hidden)refreshLeaderboard();
    show("translation-note",["zh","ar","es","pt"].includes($("lang").value));
    txt("translation-note",t("translationNote"));
    if(state.loggedIn)refreshStats();
  }
  function showScope(){
    const value=mode();
    show("listening-filter",value==="listening");
    show("listen-mix-setting",["pages","chapters"].includes(value));
    const listeningPages=value==="listening"&&listeningRange()==="pages";
    show("page-controls",value==="pages"||listeningPages);
    show("chapter-controls",value==="chapters"||(value==="listening"&&!listeningPages));
    show("listen-scope-help",value==="listening"&&!listeningPages);
    if(state.catalog){
      // Chapter grid itself is rendered below using separate printed-unit
      // metadata in listening mode. Never relabel old legacy chapter IDs.
    }
    if(value==="chapters"||value==="listening")renderChapters();
    show("topic-controls",value==="topics");
    show("verb-controls",value==="verbs");
    show("level-controls",["topics","verbs"].includes(value));
    show("material-config-group",!["topics","verbs","listening"].includes(value));
    show("page-disclaimer",["pages","chapters","listening"].includes(value));
    updateTraining();
    updateRangeSummary();
  }
  function updateRangeSummary(){
    const from=Number($("page-from").value)||1,to=Number($("page-to").value)||56;
    txt("range-summary",from+"–"+to+" / 312");
  }
  function renderChapters(){
    if(!state.catalog)return;
    const listening=mode()==="listening";
    const existing=new Set(listening?(state.listeningChapters||[1,2,3,4]):(state.bookChapters||selectedChapters()));
    const group=$("chapter-grid");group.replaceChildren();
    (listening?state.catalog.listeningChapters:state.catalog.chapters).forEach(c=>{
      const label=document.createElement("div");label.className="chapter-option";
      const checkbox=document.createElement("input");checkbox.type="checkbox";checkbox.value=c.id;
      checkbox.checked=existing.has(c.id);
      checkbox.setAttribute("aria-label",(c.id>0?t("chapter")+" "+c.id+": ":"")+c.title);
      const name=document.createElement("label");name.className="chapter-name";
      const short=c.id>0?t("chapter")+" "+c.id+" · "+(c.review?t("review")+" · ":""):
                   c.id===0?t("alphabetName")+" · ":t("appendix")+" · ";
      name.append(checkbox,document.createTextNode(short+c.title));
      const meta=document.createElement("span");meta.className="chapter-page";
      const count=state.catalog.listeningByChapter?.[String(c.id)]||0;
      meta.textContent=c.start+"–"+c.end+(listening?" · 🎧 "+count:"");
      const focus=document.createElement("small");focus.className="chapter-focus";focus.lang="el";
      focus.textContent=c.focus||"";
      const only=document.createElement("button");only.type="button";only.className="text-button only";only.textContent=t("only");
      const persist=()=>{
        if(listening)state.listeningChapters=selectedChapters();
        else state.bookChapters=selectedChapters();
        saveSettings();
      };
      only.addEventListener("click",()=>{group.querySelectorAll('input[type=checkbox]').forEach(x=>x.checked=x===checkbox);persist();});
      checkbox.addEventListener("change",persist);
      label.append(name,meta,focus,only);group.append(label);
    });
  }

  const ACCESS_CODE_KEY="greek-login-code-v1";
  const selectedTopics=()=>Array.from($("topic-grid").querySelectorAll("input:checked")).map(x=>x.value);
  const selectedLevels=()=>Array.from($("level-options").querySelectorAll("input:checked")).map(x=>x.value);
  const selectedGroups=()=>Array.from($("verb-group-options").querySelectorAll("input:checked")).map(x=>x.value);
  const verbMaxUnit=()=>Number($("verb-max-unit").value)||4;
  function renderVerbStageSummary(){
    if(!state.topicCatalog)return;
    const max=verbMaxUnit(),groups=selectedGroups(),levels=selectedLevels();
    const available=state.topicCatalog.verbs.filter(x=>x.introducedUnit<=max&&groups.includes(x.group)&&levels.includes(x.level));
    txt("verb-stage-summary",t("verbStageCount").replace("{count}",available.length).replace("{forms}",available.length*6));
  }
  function showAuthMode(){
    if(!$("auth-success").hidden)return;
    const login=state.authMode==="login";
    show("auth-name-wrap",!login);show("auth-code-wrap",login);
    $("mode-register").classList.toggle("active",!login);
    $("mode-login").classList.toggle("active",login);
    txt("auth-submit",t(login?"authSignIn":"authCreate"));
    show("auth-error",false);
  }
  function setAuthMode(value){
    state.authMode=value;
    show("auth-success",false);show("auth-modes",true);show("auth-form",true);showAuthMode();
  }
  function showAccountCode(code){txt("account-code",code||"••••••••");}
  function authError(err){
    const dict={nickname_taken:"authTaken",invalid_credentials:"authBadCode",rate_limited:"authLimit",nickname_invalid:"authBadNick"};
    txt("auth-error",dict[err.message]?t(dict[err.message]):t("failed")+err.message);show("auth-error",true);
  }
  async function submitAuth(event){
    event.preventDefault();
    const login=state.authMode==="login",nickname=$("auth-name").value.trim(),code=$("auth-input-code").value.trim();
    if(!login&&(nickname.length<3||nickname.length>28)){authError(new Error("nickname_invalid"));return;}
    if(login&&!/^[0-9]{8}$/.test(code)){authError(new Error("invalid_credentials"));return;}
    $("auth-submit").disabled=true;show("auth-error",false);
    try{
      const result=await api(login?"auth/login":"auth/register",{
        method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(login?{code}:{nickname})});
      const savedCode=login?code:result.code;
      localStorage.setItem(ACCESS_CODE_KEY,savedCode);showAccountCode(savedCode);
      state.loggedIn=true;state.profile={registered:true,nickname:result.nickname,avatar:"🎓"};
      txt("student-nickname",result.nickname);await refreshStats();
      if(login){show("auth-gate",false);setAuthMode("register");await restoreActiveSession();}
      else{
        txt("auth-created-code",savedCode);
        show("auth-modes",false);show("auth-form",false);show("auth-success",true);
      }
    }catch(err){authError(err);}
    finally{$("auth-submit").disabled=false;}
  }
  async function copyAccessCode(){
    const code=localStorage.getItem(ACCESS_CODE_KEY);
    if(!code||!/^[0-9]{8}$/.test(code)){alert(t("authCodeMissing"));return;}
    try{await navigator.clipboard.writeText(code);alert(t("authCopied"));}
    catch{alert(t("authCodeMissing"));}
  }
  async function signOut(){
    if(!confirm(t("authConfirmLogout")))return;
    try{
      await api("auth/logout",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"});
      clearActiveSession();
      localStorage.removeItem(ACCESS_CODE_KEY);state.profile=null;state.loggedIn=false;
      showAccountCode("");setPage("practice");show("setup",true);show("quiz",false);show("finished",false);
      clearInterval(state.timer);state.deadline=0;state.finishing=true;
      await loadProfile();
    }catch(err){alert(t("failed")+err.message);}
  }
  function renderTopics(){
    if(!state.topicCatalog)return;
    const group=$("topic-grid"),existing=new Set(selectedTopics());group.replaceChildren();
    for(const topic of state.topicCatalog.topics){
      const option=document.createElement("label");option.className="topic-option";
      const checkbox=document.createElement("input");checkbox.type="checkbox";
      checkbox.value=topic.id;checkbox.checked=existing.has(topic.id);
      const label=document.createElement("span");const lang=$("lang").value;label.textContent=TOPIC_NAMES[lang]?.[topic.id]||(lang==="ru"?topic.ru:topic.en);
      const count=document.createElement("small");count.textContent=String(state.topicCatalog.counts[topic.id]||0);
      option.append(checkbox,label,count);checkbox.addEventListener("change",()=>{saveSettings();if(!$("study-word-list").hidden)loadTopicWords();});group.append(option);
    }
  }

  async function loadTopicWords(){
    const list=$("study-word-list");list.replaceChildren();
    const topics=selectedTopics(),levels=selectedLevels();
    if(!topics.length||!levels.length){list.textContent=t("previewNoWords");return;}
    const label=document.createElement("p");label.className="quiet";label.textContent=t("loading");
    list.append(label);
    try{
      const data=await api("topic-words?"+new URLSearchParams({lang:$("lang").value,topics:topics.join(","),levels:levels.join(",")}));
      list.replaceChildren();
      const info=document.createElement("p");info.className="quiet";
      info.textContent=String(data.count)+" · A1/A2";list.append(info);
      data.words.forEach(word=>{
        const row=document.createElement("div");row.className="topic-study-row";
        const gr=document.createElement("strong");gr.lang="el";gr.textContent=word.gr;
        const tr=document.createElement("span");tr.textContent=word.translation;
        const level=document.createElement("small");level.textContent=word.level;
        row.append(gr,tr,level);list.append(row);
      });
    }catch(err){list.textContent=t("failed")+err.message;}
  }
  async function toggleTopicWords(){
    const reveal=$("study-word-list").hidden;
    show("study-word-list",reveal);
    txt("preview-topic-words",t(reveal?"previewHide":"previewWords"));
    if(reveal)await loadTopicWords();
  }
  function renderParadigm(container,data){
    container.replaceChildren();
    const title=document.createElement("strong");title.className="conjugation-heading";
    title.textContent=data.lemma+" · "+data.group;
    const table=document.createElement("table");table.className="conjugation-table";
    const names=data.persons||["εγώ","εσύ","αυτός / αυτή","εμείς","εσείς","αυτοί / αυτές"];
    names.forEach((name,i)=>{
      const tr=document.createElement("tr"),th=document.createElement("th"),td=document.createElement("td");
      th.textContent=name;td.textContent=data.forms[i];
      if(i===data.person)tr.className="active";
      tr.append(th,td);table.append(tr);
    });
    container.append(title,table);
    if(data.accepted?.length>1){
      const note=document.createElement("p");note.className="quiet";
      note.textContent=data.accepted.join(" / ");container.append(note);
    }
  }
  function renderVerbReference(){
    if(!state.topicCatalog)return;
    const holder=$("verb-reference-table");holder.replaceChildren();
    for(const group of ["A","B1","B2"]){
      const data=state.topicCatalog.verbs.find(x=>x.group===group&&x.introducedUnit<=verbMaxUnit()&&selectedLevels().includes(x.level));
      if(!data)continue;
      const block=document.createElement("div");block.className="verb-ref-group";
      renderParadigm(block,{...data,person:-1});holder.append(block);
    }
  }
  function config(weak){
    const value=mode();
    const types=value==="topics"?["word"]:value==="verbs"?["verb"]:value==="listening"?selectedListeningKinds():selectedKinds();
    if(training()==="personalized"&&!["verbs","listening"].includes(value)&&!types.includes("word"))types.push("word");
    if(!types.length)throw Error(t("errorNoTypes"));
    const cfg={types:types.join(","),lang:$("lang").value,study:value==="listening"?"textbook":training(),mode:weak?"weak":"all",count:"60"};
    if(["pages","chapters"].includes(value))cfg.listenMix=$("listen-mix").checked?"1":"0";
    if(value==="topics" || value==="verbs"){
      const levels=selectedLevels();
      if(!levels.length)throw Error(t("authChoose"));
      cfg.scope=value;cfg.levels=levels.join(",");
      if(value==="topics"){
        const topics=selectedTopics();
        if(!topics.length)throw Error(t("authChoose"));
        cfg.topics=topics.join(",");
      }else{
        const groups=selectedGroups();
        if(!groups.length)throw Error(t("authChoose"));
        cfg.groups=groups.join(",");
        cfg.maxUnit=verbMaxUnit();
      }
    }else if(value==="chapters"||(value==="listening"&&listeningRange()==="chapters")){
      const chapters=selectedChapters();
      if(!chapters.length)throw Error(t("errorNoChapters"));
      cfg.chapters=chapters.join(",");
      if(value==="listening")cfg.scope="listening";
    }else{
      const start=Math.min(312,Math.max(1,Math.floor(Number($("page-from").value)||1)));
      const end=Math.min(312,Math.max(start,Math.floor(Number($("page-to").value)||start)));
      $("page-from").value=start;$("page-to").value=end;
      cfg.from=start;cfg.to=end;
      if(value==="listening")cfg.scope="listening";
    }
    if($("adaptive-mode").checked)cfg.adaptive="1";
    return cfg;
  }
  async function estimateCapacity(){
    const button=$("estimate-capacity");
    try{
      const opts=config(false);
      opts.duration=duration();
      button.disabled=true;
      txt("capacity-result",t("loading"));
      const r=await api("capacity?"+new URLSearchParams(opts).toString());
      const taskAware=r.taskAware===true;
      const sufficient=taskAware?r.enoughAtEstimatedPace:r.enoughAt20Seconds;
      const pattern=t(sufficient?"capacityEnough":"capacityShort");
      const average=taskAware?r.averageSecondsPerUnique:r.paceSeconds;
      const needed=taskAware?r.requiredUniqueAtEstimatedPace:r.requiredAt20Seconds;
      const explanation=taskAware?t("capacityTaskNote")
        .replace("{minutes}",r.estimatedMinutes)
        .replace("{low}",r.expectedRangeMinutes[0]).replace("{high}",r.expectedRangeMinutes[1])
        :t("capacityDisclaimer");
      txt("capacity-result",pattern.replace("{available}",r.uniqueCards)
        .replace("{duration}",r.durationMinutes).replace("{needed}",needed).replace("{pace}",average)
        +" "+t(r.paceModel==="observed"?"paceKind":"paceDefault").replace("{pace}",average)
        +" "+explanation);
    }catch(err){txt("capacity-result",t("failed")+err.message);}
    finally{button.disabled=false;}
  }
  function setPage(page){
    for(const id of ["practice","vocab","weak","stats","leaderboard"])show(id+"-view",id===page);
    document.querySelectorAll(".tab").forEach(button=>{
      const active=button.dataset.page===page;
      button.classList.toggle("active",active);
      if(active)button.setAttribute("aria-current","page");else button.removeAttribute("aria-current");
    });
    if(page==="leaderboard")refreshLeaderboard();
    else if(page==="vocab")window.lexiVocab?.onOpen();
    else if(page!=="practice")refreshStats();
  }
  async function loadQuestions(){
    const opts={...state.settings};
    // One compact semantic fingerprint per answered normal-practice card.
    // Keeps regular sessions repeat-free across the 60-question API batches.
    // Weak mode instead excludes individual answered directions until retry.
    if(state.seen.length&&state.seen.length<310)opts.exclude=state.seen.join(",");
    const result=await api("quiz?"+new URLSearchParams(opts).toString());
    // A regular session finishes once the selected material is exhausted;
    // never restart an already completed dialogue just to fill the timer.
    // Weak review is different: the same failed item may require two correct
    // passes, so retry its still-outstanding debt after all items were seen.
    if(!result.questions?.length&&state.seen.length&&state.mode==="weak"){
      state.seen=[];delete opts.exclude;
      const retry=await api("quiz?"+new URLSearchParams(opts).toString());
      return retry.questions||[];
    }
    return result.questions||[];
  }
  function formatClock(ms){
    const secs=Math.max(0,Math.ceil(ms/1000));
    return String(Math.floor(secs/60)).padStart(2,"0")+":"+String(secs%60).padStart(2,"0");
  }
  function updateTimer(){
    if(!state.deadline||state.finishing)return;
    const remain=Math.max(0,state.deadline-Date.now());
    txt("time-left",formatClock(remain));
    $("progress-fill").style.width=(100*(1-remain/(duration()*60000)))+"%";
    if(remain<=0)finishQuiz(true);
  }
  async function startQuiz(weak,due=false){
    if(state.deadline&&!state.finishing)return;
    if(!state.loggedIn){show("auth-gate",true);return;}
    try{state.settings=due?{mode:"srs_due",lang:$("lang").value,count:"60"}:
      (weak?{mode:"weak_all",lang:$("lang").value,count:"60"}:config(false));
      show("setup-error",false);}
    catch(err){txt("setup-error",err.message);show("setup-error",true);return;}
    saveSettings();
    $("start").disabled=true;$("weak-start").disabled=true;
    clearActiveSession();
    state.remoteSessionId=newRequestId();
    state.remoteRevision=0;state.remoteEnabled=true;
    state.mode=due?"due":weak?"weak":"all";state.seen=[];state.count=0;state.correct=0;state.wrong=0;
    state.finishing=false;state.answered=false;state.busy=false;
    try{
      const questions=await loadQuestions();
      if(!questions.length){
        if(weak){txt("weak-empty",t("weakNoAvailable"));setPage("weak");}
        else {txt("setup-error",t(due?"srsEmpty":"noCards"));show("setup-error",true);}
        return;
      }
      state.questions=questions;state.index=0;
      state.started=Date.now();state.deadline=state.started+duration()*60000;
      persistActiveSession();
      $("lang").disabled=true;
      show("setup",false);show("quiz",true);show("finished",false);
      setPage("practice");renderQuestion();
      updateTimer();clearInterval(state.timer);state.timer=setInterval(updateTimer,1000);
      $("practice-view").scrollIntoView({behavior:"smooth",block:"start"});
    }catch(err){txt("setup-error",t("failed")+err.message);show("setup-error",true);}
    finally{$("start").disabled=false;$("weak-start").disabled=false;}
  }
  async function playCurrentWord(slow=false){
    const q=state.current;
    if(!q?.wordAudio||!window.LexiWordAudio)return;
    await window.LexiWordAudio.play(q.wordAudio,{
      slow,onStatus:code=>{if(state.current===q)txt("word-audio-status",t("wordAudio"+code[0].toUpperCase()+code.slice(1))); }
    });
  }
  function renderQuestion(){
    if(state.finishing)return;
    const q=state.questions[state.index];
    if(!q)return;
    if(state.current?.kind==="listening")try{$("listening-audio").pause();}catch{}
    window.LexiWordAudio?.stop();
    const phoneticAudio=["accent","syllable","enclitic"].includes(q.kind)&&!!q.wordAudio;
    show("word-pronounce-controls",phoneticAudio);
    const phoneticAvailable=window.LexiWordAudio?.available(q.wordAudio)??false;
    $("word-pronounce").disabled=!phoneticAvailable;
    $("word-pronounce-slow").disabled=!phoneticAvailable;
    txt("word-audio-status",phoneticAudio&&!phoneticAvailable?t("wordAudioUnavailable"):"");
    state.current=q;state.answered=false;state.busy=false;state.verbStage=1;
    state.listenPlayed=false;
    state.dialogueStep=0;state.dialogueFilled={};state.orderIndices=[];
    state.pendingAnswer=null;persistActiveSession();show("retry-answer",false);show("recovery-note",false);
    $("answers").classList.remove("order-tokens");
    $("question-prompt").classList.remove("unaccented-word");
    $("question-prompt").lang=["article","syllable","enclitic","grammar"].includes(q.kind)?"el":$("lang").value;
    $("question-prompt").dir=["article","syllable","enclitic","grammar"].includes(q.kind)?"ltr":"auto";
    txt("next",t("next"));
    txt("quiz-mode",state.mode==="due"?t("srsSession"):
      state.mode==="weak"?t("weakSession"):t("session"));
    txt("question-num",String(state.count+1).padStart(2,"0"));
    let chapter=(q.kind==="listening"?state.catalog?.listeningChapters:state.catalog?.chapters)?.find(x=>x.id===q.chapter);
    const topic=q.kind==="dialogue"?t("dialogueLabel")+" · "+q.topic :
      q.kind==="word"&&q.chapter===-10?t("personalizedTraining") :
      q.kind==="verb"?"Ρήματα · "+q.verbGroup :
      q.chapter===-8?(state.topicCatalog?.topics.find(x=>x.id===q.topic)?.[$("lang").value==="ru"?"ru":"en"]||q.topic):
      q.chapter>0?t("chapter")+" "+q.chapter+" · "+(chapter?.title||q.topic):
       (q.chapter===0?t("alphabetName"):t("review"))+" · "+(chapter?.title||"");
    txt("question-topic",q.page>0?topic+" · p. "+q.page+(q.sourcePageVerified?" ✓":" ~"):topic);
    const pageHints={
      ru:"✓ Страница подтверждена по примеру или таблице учебника. Не обязательно первое появление слова.",
      en:"✓ This page contains a verified example or model in the textbook; not necessarily the word's first appearance.",
      zh:"✓ 该页的例句或表格已人工核实，不一定是此词首次出现的位置。",
      ar:"✓ تم التحقق من المثال أو الجدول في هذه الصفحة، لكنها قد لا تكون أول ظهور للكلمة.",
      es:"✓ Página comprobada con un ejemplo del libro; no tiene por qué ser la primera aparición.",
      pt:"✓ Página confirmada por um exemplo do livro; não é necessariamente a primeira ocorrência."};
    $("question-topic").title=q.sourcePageVerified?pageHints[$("lang").value]||pageHints.en:"";
    if(state.mode==="weak"&&q.lang&&q.lang!==state.settings.lang&&q.kind!=="dialogue")txt("question-topic",$("question-topic").textContent+" · "+t("weakLanguage").replace("{lang}",LANGUAGE_LABELS[q.lang]||q.lang));
    const greekVariantLabels=GREEK_VARIANT_LABELS[q.lang||$("lang").value]||GREEK_VARIANT_LABELS.en;
    const visibleVariant=Array.isArray(q.greekVariants)&&q.greekVariants.length>0 &&
      (q.direction==="gr-ru");
    const greekVariantHint=visibleVariant?
      " · "+greekVariantLabels.also+": "+q.greekVariants.join(" / "):
      (q.greekVariants?.length?" · "+greekVariantLabels.more:"");
    txt("question-note",(q.kind==="accent"?t("accentChoiceHelp"):q.kind==="syllable"?t("syllableHelp"):q.note)+(q.articleSpellingVariant?" · "+t("articleVariantHint"):(q.multipleValid&&q.direction!=="ru-gr"?" · "+t("manyCorrect"):""))+greekVariantHint);
    txt("question-prompt",q.promptEn?hint(q.prompt,q.promptEn):q.prompt);
    show("feedback",false);show("next",false);show("verb-reveal",false);
    show("listening-controls",q.kind==="listening");
    show("listening-reveal",false);
    if(q.kind==="listening"){
      $("listening-audio").src=q.audioUrl;
      $("listening-audio").playbackRate=1;
      txt("listening-status",t("listenNotYet"));
      txt("listen-play",t("listenPlay"));
    }
    show("dialogue-lines",q.kind==="dialogue");
    show("order-builder",q.kind==="order");
    show("order-tools",q.kind==="order");
    show("question-prompt",q.kind!=="dialogue");
    if(q.kind==="dialogue"){renderDialogueGap();return;}
    if(q.kind==="order"){renderOrder();return;}
    if(q.kind==="verb"&&state.mode==="weak"&&q.direction==="translate"){renderVerbTranslation();return;}
    $("feedback").className="feedback";
    const answers=$("answers");answers.replaceChildren();
    const isAccent=q.kind==="accent";
    answers.classList.toggle("accent-letters",isAccent);
    // Readable answer choices: long phrases/sentences and very long translations
    // are full width on mobile, instead of squeezing into two tiny columns.
    const longChoices=!isAccent && (["phrase","sentence","enclitic","grammar"].includes(q.kind) ||
      q.choices.some((x,i)=>x.length>36||(q.choicesEn?.[i]&&hint(x,q.choicesEn[i]).length>42)));
    answers.classList.toggle("wide-choices",longChoices);
    if(isAccent)$("question-prompt").classList.add("unaccented-word");
    else $("question-prompt").classList.remove("unaccented-word");
    const letters=isAccent?q.letters:q.choices;
    letters.forEach((choice,i)=>{
      const b=document.createElement("button");b.type="button";
      b.className=isAccent?"answer accent-letter":"answer";
      if(isAccent){
        b.textContent=choice;
        b.setAttribute("aria-label",(i+1)+": "+choice);
        b.title=String(i+1);
      }else{
        const n=document.createElement("span");n.className="key";n.textContent=String(i+1);
        const val=document.createElement("span");val.textContent=q.choicesEn?hint(choice,q.choicesEn[i]):choice;
        val.dir="auto";b.append(n,val);
      }
      if(q.kind==="listening"){
        b.disabled=true;
        b.addEventListener("click",()=>choose(i));
      }else if(isAccent&&!q.accentableIndices.includes(i)){
        b.disabled=true;b.classList.add("unaccentable");b.setAttribute("aria-hidden","true");
      }else b.addEventListener("click",()=>choose(i));
      answers.append(b);
    });
  }

  async function playListening(slow=false){
    const q=state.current;
    if(!q||q.kind!=="listening"||state.finishing)return;
    const audio=$("listening-audio");
    audio.playbackRate=slow?0.8:1;
    try{
      audio.currentTime=0;
      txt("listening-status",t("listenPlaying"));
      await audio.play();
      if(state.current!==q||state.finishing)return;
      state.listenPlayed=true;
      if(!state.answered)Array.from($("answers").children).forEach(b=>b.disabled=false);
      txt("listening-status",t("listenPlayed"));
      txt("listen-play",t("listenReplay"));
    }catch{
      if(state.current===q)txt("listening-status",t("listenError"));
    }
  }

  function renderOrder(){
    const q=state.current;
    if(!q||q.kind!=="order")return;
    txt("question-note",t("orderInstruction"));
    txt("order-draft-label",t("orderDraft"));
    txt("order-undo",t("orderUndo"));
    txt("order-reset",t("orderReset"));
    txt("order-check",t("orderCheck"));
    const selected=state.orderIndices||[];
    txt("order-draft",selected.map(i=>q.tokens[i]).join(" ")||"…");
    $("order-draft").lang="el";
    const answers=$("answers");answers.replaceChildren();
    answers.classList.remove("accent-letters");answers.classList.add("order-tokens");
    q.tokens.forEach((word,i)=>{
      const b=document.createElement("button");b.type="button";b.className="answer order-word";
      b.lang="el";b.dir="ltr";b.textContent=word;
      b.disabled=selected.includes(i)||state.answered;
      b.addEventListener("click",()=>{
        if(state.answered||state.busy||selected.includes(i))return;
        state.orderIndices.push(i);renderOrder();
      });answers.append(b);
    });
    $("order-check").disabled=state.answered||selected.length!==q.tokens.length;
    $("order-undo").disabled=state.answered||selected.length===0;
    $("order-reset").disabled=state.answered||selected.length===0;
    show("feedback",state.answered);
    show("next",state.answered);
    persistActiveSession();
  }
  function editOrder(action){
    if(!state.current||state.current.kind!=="order"||state.answered)return;
    if(action==="undo")state.orderIndices.pop();
    else state.orderIndices=[];
    renderOrder();
  }
  function submitOrder(){
    const q=state.current;
    if(!q||q.kind!=="order"||state.answered||state.orderIndices.length!==q.tokens.length)return;
    choose(-1,state.orderIndices.map(i=>q.tokens[i]).join(" "));
  }

  function renderDialogueGap(){
    const q=state.current;
    if(!q||q.kind!=="dialogue")return;
    const gaps=q.gapIndices||[0,1];
    const target=gaps[state.dialogueStep];
    txt("next",t("next")); // Reset stale label from a previous dialogue gap.
    txt("question-note",t("dialogueInstruction").replace("{current}",state.dialogueStep+1).replace("{total}",gaps.length));
    txt("question-topic",t("dialogueTitle")+" · "+q.topic);
    txt("question-num",String(state.count+1).padStart(2,"0"));
    const wrapper=$("dialogue-lines");wrapper.replaceChildren();
    q.dialogueLines.forEach(line=>{
      const p=document.createElement("p");p.className="dialogue-line";
      // Generalized 1–3+ Greek gaps (previous client only recognized [[0]]/[[1]]).
      const expression=/\[\[(\d+)\]\]/g;
      let previous=0,match;
      while((match=expression.exec(line))!==null){
        const i=Number(match[1]);
        p.append(document.createTextNode(line.slice(previous,match.index)));
        const active=i===target,done=Object.hasOwn(state.dialogueFilled,i)||!gaps.includes(i);
        const span=document.createElement("span");
        span.dataset.gapIndex=String(i);
        span.className="dialogue-blank"+(active?" current":done?" filled":"");
        span.textContent=done?state.dialogueFilled[i]||q.dialogueGaps[i]:(active?"＿＿ "+(i+1)+" ＿＿":"＿＿＿");
        p.append(span);
        previous=expression.lastIndex;
      }
      p.append(document.createTextNode(line.slice(previous)));
      wrapper.append(p);
    });
    const answers=$("answers");answers.replaceChildren();
    answers.classList.remove("accent-letters");answers.classList.add("wide-choices");
    q.choices.forEach((choice,i)=>{
      const b=document.createElement("button");b.type="button";b.className="answer";
      if(Object.values(state.dialogueFilled).includes(choice))b.disabled=true;
      const n=document.createElement("span");n.className="key";n.textContent=String(i+1);
      const val=document.createElement("span");val.lang="el";val.dir="ltr";val.textContent=choice;
      b.append(n,val);b.addEventListener("click",()=>choose(i));answers.append(b);
    });
    show("feedback",false);show("next",false);state.answered=false;state.busy=false;
    persistActiveSession();
  }

  async function choose(index,overrideSelected,replayId=null){
    const q=state.current;
    if(!q||state.finishing||state.answered||state.busy)return;
    // A lost reply to an already-heard listening answer must be replayable
    // on the new device with the exact original request UUID; no new
    // listening answer can be submitted until audio was actually played.
    if(q.kind==="listening"&&!state.listenPlayed&&!replayId){
      txt("listening-status",t("listenNotYet"));return;
    }
    if(Date.now()>=state.deadline){finishQuiz(true);return;}
    if(state.pendingAnswer&&!replayId){await retryPendingAnswer();return;}
    const isTranslation=q.kind==="verb"&&state.verbStage===2;
    const actualDirection=q.kind==="dialogue"?"gap"+q.gapIndices[state.dialogueStep]:(isTranslation?"translate":q.direction);
    const options=isTranslation?q.phraseChoices:(q.kind==="order"?q.tokens:q.choices);
    const selected=q.kind==="order"?overrideSelected:(q.kind==="accent"?String(index):options[index]);
    if(q.kind==="accent" && (!q.letters || index<0 || index>=q.letters.length || !q.accentableIndices.includes(index)))return;
    if(selected===undefined)return;
    state.busy=true;
    const requestId=replayId||newRequestId();
    const immutableBody=(replayId&&state.pendingAnswer?.requestId===replayId&&state.pendingAnswer.body)
      ?state.pendingAnswer.body
      :{id:q.id,direction:actualDirection,lang:q.lang||state.settings.lang,selected,requestId,
         srsOptIn:$("srs-optin").checked||state.mode==="due",
         sessionId:state.remoteSessionId,deviceId};
    state.pendingAnswer={index,overrideSelected,requestId,body:immutableBody};
    persistActiveSession();
    const buttons=Array.from($("answers").children);buttons.forEach(b=>b.disabled=true);
    try{
      const result=await api("answer",{method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(immutableBody)});
      state.pendingAnswer=null;
      show("retry-answer",false);show("recovery-note",false);
      state.answered=true;state.count++;
      const answerLang=q.lang||state.settings.lang;
      state.seen.push((state.mode==="weak"||state.mode==="due")
        ? q.id+":"+actualDirection+(q.kind==="accent"||q.kind==="dialogue"||answerLang==="ru"?"":":"+answerLang)
        : (q.semanticId||q.id));
      if(result.correct)state.correct++;else state.wrong++;
      buttons.forEach((b,i)=>{
        if(q.kind==="order")return;
        if(q.kind==="accent" ? i===result.correctIndex :
           q.kind==="verb"&&!isTranslation ? result.conjugation?.accepted.includes(q.choices[i]) :
           (result.acceptedAnswers||[result.answer]).includes(options[i]))
          b.classList.add("is-correct");
        if(i===index&&!result.correct)b.classList.add("is-wrong");
      });
      if(q.kind==="syllable"&&result.syllableBreakdown){
        txt("question-prompt",result.syllableBreakdown);
      }
      if(q.kind==="accent"){
        txt("question-prompt",result.answer);
        $("question-prompt").classList.remove("unaccented-word");
      }
      if(q.kind==="listening"&&result.transcript){
        const panel=$("listening-reveal");panel.replaceChildren();
        const prefix=document.createElement("strong");prefix.textContent=t("listenText")+" ";
        const greek=document.createElement("span");greek.lang="el";greek.dir="ltr";
        greek.textContent=result.transcript;
        panel.append(prefix,greek);
        show("listening-reveal",true);
      }
      $("feedback").className="feedback "+(result.correct?"good":"bad");
      $("feedback").replaceChildren(document.createTextNode(result.correct?t("right"):t("wrong")));
      if(q.kind==="article"&&result.preferredAnswer&&result.acceptedAnswers?.length>1){
        buttons.forEach((b,i)=>{
          if(options[i]===result.preferredAnswer){
            b.classList.add("is-preferred");
            const tag=document.createElement("small");tag.className="preferred-form-label";
            tag.textContent=t("preferredSpelling");
            b.append(tag);
          }
        });
      }
      if(q.kind==="verb"&&result.conjugation){
        renderParadigm($("verb-reveal"),result.conjugation);
        show("verb-reveal",true);
      }
      if(q.kind==="accent"||q.kind==="enclitic"||q.kind==="grammar" || !result.correct){
        const bold=document.createElement("strong");
        const englishCorrect=q.kind==="verb"&&isTranslation
          ?q.phraseChoicesEn?.[q.phraseChoices.indexOf(result.answer)]
          :q.choicesEn?.[q.choices.indexOf(result.answer)];
        bold.textContent=q.kind!=="dialogue"?hint(result.answer,englishCorrect):result.answer;
        $("feedback").append(document.createTextNode("  "),bold);
        if(!result.correct)$("feedback").append(document.createTextNode(t("queued")));
      }
      if((q.kind==="accent"||q.kind==="syllable"||q.kind==="enclitic")&&result.tonosHint){
        const note=document.createElement("p");note.className="spelling-guidance";
        const label=document.createElement("strong");label.textContent=t(q.kind==="enclitic"?"encliticExplanation":q.kind==="syllable"?"syllableExplanation":"accentExplanationTitle")+": ";
        note.append(label,document.createTextNode(result.tonosHint));$("feedback").append(note);
      }
      if(result.greekVariants?.length){
        const variantNote=document.createElement("p");variantNote.className="spelling-guidance";
        const title=document.createElement("strong");
        const vlabels=GREEK_VARIANT_LABELS[answerLang]||GREEK_VARIANT_LABELS.en;
        title.textContent=vlabels.also+": ";
        const form=document.createElement("span");form.lang="el";form.dir="ltr";
        form.textContent=result.greekVariants.join(" / ");
        variantNote.append(title,form);$("feedback").append(variantNote);
      }
      if(q.kind==="grammar"&&result.grammarTip&&result.correct){
        const tip=document.createElement("p");tip.className="spelling-guidance";
        const label=document.createElement("strong");label.textContent=t("grammarExplanation")+": ";
        tip.append(label,document.createTextNode(result.grammarTip));
        $("feedback").append(tip);
      }
      if(result.explanation){
        const note=document.createElement("p");note.className="spelling-guidance";
        const heading=document.createElement("strong");heading.textContent=t("explanationTitle")+": ";
        note.append(heading,document.createTextNode(result.explanation));$("feedback").append(note);
      }
      if(result.spellingNote){
        const note=document.createElement("p");note.className="spelling-guidance";
        const heading=document.createElement("strong");heading.textContent=t("spellingGuide")+": ";
        note.append(heading,document.createTextNode(result.spellingNote));
        $("feedback").append(note);
      }
      show("feedback",true);show("next",true);
      if(q.kind==="order"){
        $("order-check").disabled=true;$("order-undo").disabled=true;$("order-reset").disabled=true;
        show("order-builder",true);
      }
      if(q.kind==="verb"&&!isTranslation)txt("next",t("verbTranslate"));
      if(q.kind==="dialogue"){
        const filledIndex=q.gapIndices[state.dialogueStep];
        state.dialogueFilled[filledIndex]=result.answer;
        // Show the completed Greek line immediately, not only after another click.
        const blank=$("dialogue-lines").querySelector('.dialogue-blank[data-gap-index="'+filledIndex+'"]');
        if(blank){
          blank.textContent=result.answer;
          blank.classList.remove("current");
          blank.classList.add("filled");
        }
        const anotherGap=state.dialogueStep<q.gapIndices.length-1;
        txt("next",t(anotherGap?"dialogueNext":"dialogueContinue"));
        if(!anotherGap)txt("question-note",t("dialogueComplete"));
      }
      persistActiveSession();
    }catch(err){
      if(err.message==="session_conflict"){
        state.finishing=true;clearInterval(state.timer);
        clearActiveSession();
        show("quiz",false);show("setup",true);
        txt("setup-error",t("handoffStopped"));show("setup-error",true);
        return;
      }
      $("feedback").className="feedback bad";txt("feedback",t("failed")+err.message+" "+t("recoveryInfo"));show("feedback",true);
      show("retry-answer",true);buttons.forEach(b=>b.disabled=true);
      persistActiveSession();
    }finally{state.busy=false;}
  }
  function renderVerbTranslation(){
    const q=state.current;
    state.verbStage=2;state.answered=false;state.busy=false;
    txt("next",t("next"));show("feedback",false);show("next",false);show("verb-reveal",false);
    txt("question-note",t("verbTranslateHelp"));
    txt("question-prompt",q.phrasePrompt);
    txt("question-num",String(state.count+1).padStart(2,"0"));
    const answers=$("answers");answers.replaceChildren();
    answers.classList.remove("accent-letters");
    answers.classList.add("wide-choices");
    persistActiveSession();
    q.phraseChoices.forEach((choice,i)=>{
      const b=document.createElement("button");b.type="button";b.className="answer";
      const n=document.createElement("span");n.className="key";n.textContent=String(i+1);
      const label=document.createElement("span");label.textContent=hint(choice,q.phraseChoicesEn?.[i]);label.dir="auto";b.append(n,label);
      b.addEventListener("click",()=>choose(i));answers.append(b);
    });
  }
  async function nextQuestion(){
    if(!state.answered||state.finishing)return;
    if(state.current?.kind==="verb"&&state.verbStage===1&&state.mode!=="weak"){
      renderVerbTranslation();return;
    }
    if(state.current?.kind==="dialogue"&&state.dialogueStep<state.current.gapIndices.length-1){
      state.dialogueStep++;renderDialogueGap();return;
    }
    if(Date.now()>=state.deadline){finishQuiz(true);return;}
    state.pendingAnswer=null;
    state.index++;
    if(state.index>=state.questions.length){
      $("next").disabled=true;txt("next",t("loading"));
      try{
        state.questions=await loadQuestions();state.index=0;
        if(!state.questions.length){finishQuiz(false);return;}
      }catch(err){txt("feedback",t("failed")+err.message);return;}
      finally{$("next").disabled=false;txt("next",t("next"));}
    }
    renderQuestion();
  }
  async function finishQuiz(expired=false){
    if(state.finishing)return;
    state.finishing=true;clearInterval(state.timer);
    await Promise.race([flushRemoteSnapshot(),new Promise(resolve=>setTimeout(resolve,1600))]);
    clearActiveSession(true);
    window.LexiWordAudio?.stop();
    const elapsed=state.started?Math.round((Date.now()-state.started)/60000):0;
    if(state.current?.kind==="listening")try{$("listening-audio").pause();}catch{}
    state.deadline=0;state.current=null;$("lang").disabled=false;
    show("quiz",false);show("finished",true);show("setup",false);
    const total=state.correct+state.wrong,pct=total?Math.round(100*state.correct/total):0;
    txt("finish-title",pct>=90?t("excellent"):pct>=70?t("good"):t("practiceMore"));
    txt("finish-copy",(expired?t("timeOver")+" ":"")+t("result").replace("{good}",state.correct).replace("{total}",total).replace("{pct}",pct).replace("{minutes}",elapsed));
    await refreshStats();
  }
  function drawMetrics(id,metrics){
    const el=$(id);el.replaceChildren();
    metrics.forEach(m=>{
      if(!m.attempts)return; // More signal, less empty chart noise.
      const wrap=document.createElement("div");wrap.className="metric";
      const heading=document.createElement("div");heading.className="metric-label";
      const label=document.createElement("span");label.textContent=m.name;
      const number=document.createElement("span");number.textContent=Math.round(100*m.correct/m.attempts)+"% · "+m.attempts;
      if(m.uniqueTargets!==undefined)number.textContent+=" · "+m.uniqueTargets+" "+t("knowledgeUnique");
      if(m.provisional)number.textContent+=" · "+t("knowledgeEarly");
      heading.append(label,number);
      const bar=document.createElement("div");bar.className="bar";
      const fill=document.createElement("span");fill.style.width=(100*m.correct/m.attempts)+"%";
      bar.append(fill);wrap.append(heading,bar);el.append(wrap);
    });
    if(!el.children.length){const p=document.createElement("p");p.className="quiet";p.textContent=t("none");el.append(p);}
  }
  function drawMastery(rows){
    const el=$("mastery-heatmap");el.replaceChildren();
    for(const m of rows||[]){
      const cell=document.createElement("span");cell.className="mastery-chip "+m.status;
      cell.textContent=String(m.chapter);
      cell.title=m.attempts?t("masteryTip").replace("{chapter}",m.chapter)
        .replace("{pct}",m.accuracy).replace("{count}",m.attempts):
        t("masteryUnseen").replace("{chapter}",m.chapter);
      cell.setAttribute("aria-label",cell.title);el.append(cell);
    }
  }
  function drawDaily(rows){
    const el=$("daily");el.replaceChildren();
    if(!rows?.length){const p=document.createElement("p");p.className="quiet";p.textContent=t("noHistory");el.append(p);return;}
    const max=Math.max(1,...rows.map(x=>x.attempts));
    rows.forEach(x=>{
      const div=document.createElement("div");div.className="daily-row";
      const date=document.createElement("span");date.textContent=x.date.slice(5);
      const bar=document.createElement("div");bar.className="daily-bar";
      const fill=document.createElement("div");fill.style.width=(100*x.attempts/max)+"%";
      const txtNode=document.createElement("span");txtNode.textContent=x.correct+"/"+x.attempts;
      bar.append(fill);div.append(date,bar,txtNode);el.append(div);
    });
  }
  async function refreshStats(){
    try{
      const s=await api("stats");
      txt("hero-accuracy",s.attempts?s.accuracy+"%":"—");
      txt("hero-weak",s.weak);txt("weak-bubble",s.weak);txt("weak-count",s.weak);
      txt("stat-attempts",s.attempts);txt("stat-correct",s.correct);
      txt("stat-accuracy",s.attempts?s.accuracy+"%":"—");txt("stat-streak",s.streak);
      const units=(state.catalog?.chapters||[]).filter(x=>x.id>0);
      drawMetrics("unit-stats",units.map(x=>({name:t("chapter")+" "+x.id+" · "+x.title,...(s.units[String(x.id)]||{attempts:0,correct:0})})));
      drawMetrics("kind-stats",kindIds.map(kind=>({name:t(kinds[kind]),...(s.categories[kind]||{attempts:0,correct:0})})));
      drawDaily(s.daily);drawMastery(s.mastery);
      const extra=s.details||{};
      const skillNames=PEDAGOGY_ANALYTICS[$("lang").value].skillName;
      drawMetrics("skill-stats",(extra.skills||[])
        .map(x=>({name:skillNames[x.skill]||x.skill,...x}))
        .sort((a,b)=>(a.accuracy-b.accuracy)||(b.attempts-a.attempts)));
      const topicsById=Object.fromEntries((state.topicCatalog?.topics||[]).map(x=>[x.id,x]));
      const currentLang=$("lang").value;
      drawMetrics("topic-mastery",(extra.topics||[])
        .map(x=>({name:topicsById[x.id]?.[currentLang==="ru"?"ru":"en"]||x.id,...x}))
        .sort((a,b)=>Number(a.provisional)-Number(b.provisional)||a.accuracy-b.accuracy||b.attempts-a.attempts)
        .slice(0,18));
      drawMetrics("vocab-topic-mastery",(extra.vocabTopics||[])
        .map(x=>({name:topicsById[x.id]?.[currentLang==="ru"?"ru":"en"]||x.id,...x}))
        .sort((a,b)=>Number(a.provisional)-Number(b.provisional)||a.accuracy-b.accuracy||b.attempts-a.attempts));
      const grammarNames=LEARNING_GRAMMAR_LABELS[currentLang]||LEARNING_GRAMMAR_LABELS.en;
      drawMetrics("grammar-mastery",(extra.grammar||[])
        .map(x=>({name:grammarNames[x.id]||x.id.replaceAll("_"," "),...x}))
        .sort((a,b)=>Number(a.provisional)-Number(b.provisional)||a.accuracy-b.accuracy||b.attempts-a.attempts));
      drawMetrics("page-stats",(extra.pages||[])
        .filter(x=>x.attempts>=3)
        .sort((a,b)=>(a.accuracy-b.accuracy)||(b.attempts-a.attempts))
        .slice(0,15)
        .map(x=>({name:t("pageNumber")+x.page+" ≈",...x})));
      const due=s.srs?.due||0;
      txt("srs-status",t("srsStatus").replace("{due}",due).replace("{total}",s.srs?.scheduled||0));
      $("srs-due-start").disabled=due===0;
      $("weak-start").disabled=s.weak===0;
      const archived=s.weakUnavailable||0;
      txt("weak-empty",archived?t("weakArchived").replace("{count}",archived):(s.weak===0?t("weakNoAvailable"):""));
    }catch(err){txt("hero-accuracy","—");txt("weak-empty",t("failed")+err.message);}
  }
  async function refreshLeaderboard(){
    const list=$("leader-list");list.replaceChildren();
    const loading=document.createElement("p");loading.className="quiet";
    loading.textContent=t("loading");list.append(loading);
    try{
      const data=await api("leaderboard");
      state.joinedLeaderboard=Boolean(data.joined);
      txt("leader-enrollment-hint",t(state.joinedLeaderboard?"leaderEnrolledInfo":"leaderOptinInfo"));
      txt("leader-toggle",t(state.joinedLeaderboard?"leaderLeave":"leaderJoin"));
      list.replaceChildren();
      txt("leader-members",t("leaderMembers")+": "+data.members);
      txt("leader-mine",data.me?t("leaderPersonal")+": #"+data.me.rank:"");
      if(!data.rows.length){
        const empty=document.createElement("p");empty.className="quiet";
        empty.textContent=t("leaderEmpty");list.append(empty);return;
      }
      const fmtTime=s=>s>=3600?(s/3600).toFixed(1)+" h":(s/60).toFixed(1)+" min";
      for(const result of data.rows){
        const row=document.createElement("article");
        row.className="leader-item"+(result.isMe?" me":"");
        const head=document.createElement("div");head.className="leader-person";
        const rank=document.createElement("span");rank.className="leader-rank";
        rank.textContent="#"+result.rank;
        const avatar=document.createElement("span");avatar.className="leader-avatar";
        avatar.textContent=result.avatar;
        const who=document.createElement("div");who.className="leader-who";
        const nickname=document.createElement("strong");
        nickname.textContent=$("lang").value==="ru"?result.name:result.english;
        who.append(nickname);
        if(result.isMe){
          const my=document.createElement("span");my.className="leader-me";
          my.textContent=t("leaderYou");who.append(my);
        }
        head.append(rank,avatar,who);
        const metrics=document.createElement("div");metrics.className="leader-metrics";
        for(const [label,value] of [
          [t("leaderTime"),fmtTime(result.seconds)],
          [t("leaderAnswers"),result.answers],
          [t("leaderErrors"),result.errors],
          [t("leaderPrecision"),result.accuracy+"%"],
          [t("leaderWeak"),result.weak]
        ]){
          const cell=document.createElement("div");cell.className="leader-metric";
          const name=document.createElement("span");name.textContent=label;
          const val=document.createElement("strong");val.textContent=String(value);
          cell.append(name,val);metrics.append(cell);
        }
        row.append(head,metrics);list.append(row);
      }
    }catch(err){
      list.replaceChildren();
      const msg=document.createElement("p");msg.className="feedback bad";
      msg.textContent=t("failed")+err.message;list.append(msg);
    }
  }
  async function toggleLeaderboard(){
    const button=$("leader-toggle");
    button.disabled=true;
    try{
      const path=state.joinedLeaderboard?"leaderboard/leave":"leaderboard/join";
      const result=await api(path,{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"});
      state.joinedLeaderboard=Boolean(result.joined);
      await refreshLeaderboard();
    }catch(err){
      txt("leader-enrollment-hint",t("failed")+err.message);
    }finally{button.disabled=false;}
  }
  async function loadProfile(){
    try{
      state.profile=await api("profile");
      state.loggedIn=Boolean(state.profile.registered);
      if(state.loggedIn){
        txt("student-avatar",state.profile.avatar);
        txt("student-nickname",state.profile.nickname);
        txt("account-code",localStorage.getItem("greek-login-code-v1")||"••••••••");
        show("auth-gate",false);
        await refreshStats();
      }else{
        txt("student-nickname","—");
        show("auth-gate",true);
        showAuthMode();
      }
    }catch{
      txt("student-nickname","—");
      show("auth-gate",true);
    }
  }
  async function init(){
    const saved=restoreSettings();
    for(const radio of document.querySelectorAll('input[name=scope]'))radio.addEventListener("change",()=>{showScope();saveSettings();});
    for(const radio of document.querySelectorAll('input[name=training]'))radio.addEventListener("change",()=>{updateTraining();saveSettings();});
    for(const n of ["page-from","page-to"])$(n).addEventListener("change",()=>{updateRangeSummary();saveSettings();});
    $("kind-options").addEventListener("change",saveSettings);
    $("listen-mix").addEventListener("change",saveSettings);
    $("level-options").addEventListener("change",()=>{saveSettings();if(!$("study-word-list").hidden)loadTopicWords();});
    $("verb-group-options").addEventListener("change",saveSettings);
    $("duration-options").addEventListener("change",saveSettings);
    $("adaptive-mode").addEventListener("change",saveSettings);
    $("srs-optin").addEventListener("change",saveSettings);
    $("srs-due-start").addEventListener("click",()=>startQuiz(false,true));
    $("mode-register").addEventListener("click",()=>setAuthMode("register"));
    $("mode-login").addEventListener("click",()=>setAuthMode("login"));
    $("auth-form").addEventListener("submit",submitAuth);
    $("auth-enter").addEventListener("click",()=>show("auth-gate",false));
    $("auth-copy").addEventListener("click",copyAccessCode);
    $("account-copy").addEventListener("click",copyAccessCode);
    $("account-logout").addEventListener("click",signOut);
    $("listening-range").addEventListener("change",()=>{showScope();saveSettings();});
    $("listening-difficulty").addEventListener("change",saveSettings);
    $("estimate-capacity").addEventListener("click",estimateCapacity);
    $("setup").addEventListener("change",()=>{
      txt("capacity-result","");
    });
    $("verb-max-unit").addEventListener("change",()=>{renderVerbReference();renderVerbStageSummary();saveSettings();});
    $("verb-group-options").addEventListener("change",()=>{renderVerbStageSummary();saveSettings();});
    $("level-options").addEventListener("change",()=>{renderVerbReference();renderVerbStageSummary();saveSettings();});
    $("lang").addEventListener("change",()=>{updateLanguage();saveSettings();});
    $("auth-lang").addEventListener("change",()=>{
      $("lang").value=$("auth-lang").value;updateLanguage();saveSettings();
    });
    $("preview-topic-words").addEventListener("click",toggleTopicWords);
    const persistChapterChecks=()=>{
      if(mode()==="listening")state.listeningChapters=selectedChapters();
      else state.bookChapters=selectedChapters();
      saveSettings();
    };
    $("all-chapters").addEventListener("click",()=>{$("chapter-grid").querySelectorAll('input').forEach(x=>x.checked=true);persistChapterChecks();});
    $("clear-chapters").addEventListener("click",()=>{$("chapter-grid").querySelectorAll('input').forEach(x=>x.checked=false);persistChapterChecks();});
    document.querySelectorAll(".tab").forEach(b=>b.addEventListener("click",()=>setPage(b.dataset.page)));
    $("leader-toggle").addEventListener("click",toggleLeaderboard);
    $("start").addEventListener("click",()=>startQuiz(false));
    $("weak-start").addEventListener("click",()=>startQuiz(true));
    $("review").addEventListener("click",()=>{state.finishing=false;startQuiz(true);});
    $("finish-now").addEventListener("click",()=>finishQuiz(false));
    $("next").addEventListener("click",nextQuestion);
    $("retry-answer").addEventListener("click",retryPendingAnswer);
    $("listen-play").addEventListener("click",()=>playListening(false));
    $("listen-slow").addEventListener("click",()=>playListening(true));
    $("word-pronounce").addEventListener("click",()=>playCurrentWord(false));
    $("word-pronounce-slow").addEventListener("click",()=>playCurrentWord(true));
  $("order-check").addEventListener("click",submitOrder);
  $("order-undo").addEventListener("click",()=>editOrder("undo"));
  $("order-reset").addEventListener("click",()=>editOrder("reset"));
    $("again").addEventListener("click",()=>{state.finishing=false;show("finished",false);show("setup",true);});
    window.addEventListener("keydown",event=>{
      if($("quiz").hidden||event.altKey||event.ctrlKey||event.metaKey||["INPUT","TEXTAREA","SELECT"].includes(document.activeElement?.tagName))return;
      if(/^[1-9]$/.test(event.key)&&!state.answered){event.preventDefault();choose(Number(event.key)-1);}
      else if(event.key==="Enter"&&state.answered){event.preventDefault();nextQuestion();}
    });
    try{
      state.catalog=await api("catalog");
      state.bookChapters=Array.isArray(saved.chapters)?saved.chapters:[1,2,3,4];
      state.listeningChapters=Array.isArray(saved.listeningChapters)?saved.listeningChapters:[1,2,3,4];
      renderChapters();
      txt("catalog-summary",t("available").replace("{count}",state.catalog.practiceCardCount||state.catalog.cardCount));
    }catch(err){txt("catalog-summary",t("failed")+err.message);}
    try{
      state.topicCatalog=await api("topics");
      renderTopics();renderVerbReference();renderVerbStageSummary();
      const topics=Array.isArray(saved.topics)?saved.topics:["shopping","road","home"];
      $("topic-grid").querySelectorAll("input").forEach(x=>x.checked=topics.includes(x.value));
    }catch(err){txt("setup-error",t("failed")+err.message);show("setup-error",true);}
    updateLanguage();
    await loadProfile();
    await restoreActiveSession();
  }
  init();
})();
