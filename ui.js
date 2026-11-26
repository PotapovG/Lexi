"use strict";
(() => {
  const locales=["ru","en","zh","ar","es","pt"];
  const rows={
  "lessons": [
    "Уроки",
    "Lessons",
    "课程",
    "الدروس",
    "Lecciones",
    "Lições"
  ],
  "vocabulary": [
    "Словарь",
    "Vocabulary",
    "词汇",
    "المفردات",
    "Vocabulario",
    "Vocabulário"
  ],
  "more": [
    "Ещё",
    "More",
    "更多",
    "المزيد",
    "Más",
    "Mais"
  ],
  "account": [
    "Аккаунт и настройки",
    "Account and settings",
    "账户与设置",
    "الحساب والإعدادات",
    "Cuenta y ajustes",
    "Conta e definições"
  ],
  "theme": [
    "Тема",
    "Appearance",
    "外观",
    "المظهر",
    "Apariencia",
    "Aspeto"
  ],
  "system": [
    "Как в системе",
    "System",
    "跟随系统",
    "حسب النظام",
    "Sistema",
    "Sistema"
  ],
  "light": [
    "Светлая",
    "Light",
    "浅色",
    "فاتح",
    "Claro",
    "Claro"
  ],
  "dark": [
    "Тёмная",
    "Dark",
    "深色",
    "داكن",
    "Oscuro",
    "Escuro"
  ],
  "showCode": [
    "Показать код",
    "Show code",
    "显示登录码",
    "إظهار الرمز",
    "Mostrar código",
    "Mostrar código"
  ],
  "hideCode": [
    "Скрыть код",
    "Hide code",
    "隐藏登录码",
    "إخفاء الرمز",
    "Ocultar código",
    "Ocultar código"
  ],
  "classic": [
    "Классический тренажёр",
    "Classic practice",
    "经典练习",
    "التدريب الكلاسيكي",
    "Práctica clásica",
    "Prática clássica"
  ],
  "classicNotice": [
    "Прежний интерфейс с настройками и таймером. Основной курс доступен в «Уроках».",
    "The previous interface with settings and a timer. Find the guided course in Lessons.",
    "保留原有设置和计时器的经典界面。主课程位于“课程”。",
    "الواجهة السابقة بإعداداتها ومؤقتها. المسار الدراسي متاح في الدروس.",
    "La interfaz anterior con ajustes y temporizador. El curso guiado está en Lecciones.",
    "A interface anterior com definições e temporizador. O curso orientado está em Lições."
  ],
  "legacy": [
    "Прежний интерфейс",
    "Previous interface",
    "旧版界面",
    "الواجهة السابقة",
    "Interfaz anterior",
    "Interface anterior"
  ],
  "loading": [
    "Загружаем занятие…",
    "Loading your practice…",
    "正在加载练习…",
    "جارٍ تحميل التدريب…",
    "Cargando tu práctica…",
    "A carregar a prática…"
  ],
  "network": [
    "Не удалось связаться с сервером. Проверь подключение и повтори загрузку.",
    "Couldn't reach the server. Check your connection and try again.",
    "无法连接服务器。请检查网络后重试。",
    "تعذّر الاتصال بالخادم. تحقّق من الاتصال وحاول مجددًا.",
    "No se pudo conectar con el servidor. Revisa la conexión e inténtalo de nuevo.",
    "Não foi possível contactar o servidor. Verifica a ligação e tenta novamente."
  ],
  "retry": [
    "Повторить",
    "Try again",
    "重试",
    "إعادة المحاولة",
    "Reintentar",
    "Tentar novamente"
  ],
  "loginRequired": [
    "Войди по своему коду, чтобы продолжить.",
    "Sign in with your code to continue.",
    "请使用登录码登录以继续。",
    "سجّل الدخول برمزك للمتابعة.",
    "Accede con tu código para continuar.",
    "Entra com o teu código para continuar."
  ],
  "continueTitle": [
    "Продолжим греческий",
    "Let's continue your Greek",
    "继续学习希腊语",
    "لنواصل تعلّم اليونانية",
    "Sigamos con tu griego",
    "Vamos continuar o grego"
  ],
  "nextStep": [
    "Следующий шаг",
    "Next step",
    "下一步",
    "الخطوة التالية",
    "Siguiente paso",
    "Próximo passo"
  ],
  "chapter": [
    "Глава",
    "Chapter",
    "章",
    "الفصل",
    "Capítulo",
    "Capítulo"
  ],
  "scope": [
    "Материал изучен до главы",
    "Material studied through chapter",
    "已学教材范围至",
    "المادة المدروسة حتى الفصل",
    "Material estudiado hasta el capítulo",
    "Matéria estudada até ao capítulo"
  ],
  "scopeNote": [
    "Это граница доступного материала, а не число завершённых глав.",
    "This limits available material; it is not your completed chapter count.",
    "这是可用教材的范围，不代表已完成的章节数。",
    "هذا حدّ المادة المتاحة، وليس عدد الفصول المكتملة.",
    "Limita el material disponible; no indica los capítulos completados.",
    "Limita a matéria disponível; não indica os capítulos concluídos."
  ],
  "scopeSettings": [
    "Настроить материал",
    "Material settings",
    "教材范围设置",
    "إعدادات المادة",
    "Ajustar material",
    "Definir matéria"
  ],
  "lesson": [
    "Урок",
    "Lesson",
    "课",
    "الدرس",
    "Lección",
    "Lição"
  ],
  "inChapter": [
    "В этой главе",
    "In this chapter",
    "本章课程",
    "في هذا الفصل",
    "En este capítulo",
    "Neste capítulo"
  ],
  "complete": [
    "Пройдено",
    "Completed",
    "已完成",
    "مكتمل",
    "Completado",
    "Concluído"
  ],
  "current": [
    "Текущий урок",
    "Current lesson",
    "当前课程",
    "الدرس الحالي",
    "Lección actual",
    "Lição atual"
  ],
  "locked": [
    "Следующий урок",
    "Next lesson",
    "后续课程",
    "الدرس التالي",
    "Próxima lección",
    "Próxima lição"
  ],
  "lockedNote": [
    "Откроется после предыдущего",
    "Opens after the previous lesson",
    "完成上一课后开放",
    "يُفتح بعد الدرس السابق",
    "Se abre tras la lección anterior",
    "Abre após a lição anterior"
  ],
  "start": [
    "Начать урок",
    "Start lesson",
    "开始课程",
    "ابدأ الدرس",
    "Empezar lección",
    "Começar lição"
  ],
  "resume": [
    "Продолжить",
    "Continue",
    "继续",
    "متابعة",
    "Continuar",
    "Continuar"
  ],
  "savedPosition": [
    "Можно продолжить с сохранённого места.",
    "Continue from where you left off.",
    "从上次保存的位置继续。",
    "تابع من حيث توقفت.",
    "Continúa desde donde lo dejaste.",
    "Continua de onde ficaste."
  ],
  "toLessons": [
    "К урокам",
    "Back to lessons",
    "返回课程",
    "العودة للدروس",
    "Volver a lecciones",
    "Voltar às lições"
  ],
  "question": [
    "Задание",
    "Question",
    "题目",
    "السؤال",
    "Pregunta",
    "Pergunta"
  ],
  "of": [
    "из",
    "of",
    "/",
    "من",
    "de",
    "de"
  ],
  "remaining": [
    "Осталось заданий: {count}",
    "Questions remaining: {count}",
    "剩余题目：{count}",
    "الأسئلة المتبقية: {count}",
    "Preguntas pendientes: {count}",
    "Perguntas restantes: {count}"
  ],
  "count": [
    "Заданий: {count}",
    "Questions: {count}",
    "题目数：{count}",
    "عدد الأسئلة: {count}",
    "Preguntas: {count}",
    "Perguntas: {count}"
  ],
  "gap": [
    "Реплика {at} из {count}",
    "Reply {at} of {count}",
    "回答 {at}/{count}",
    "الرد {at} من {count}",
    "Respuesta {at} de {count}",
    "Resposta {at} de {count}"
  ],
  "activeGap": [
    "Твой ответ",
    "Your answer",
    "你的答案",
    "إجابتك",
    "Tu respuesta",
    "A tua resposta"
  ],
  "futureGap": [
    "Следующая реплика",
    "Next reply",
    "下一句回答",
    "الرد التالي",
    "Próxima respuesta",
    "Próxima resposta"
  ],
  "choose": [
    "Выбери ответ, затем нажми «Проверить».",
    "Choose an answer, then select Check.",
    "选择答案，然后点击“检查”。",
    "اختر إجابة ثم اضغط «تحقّق».",
    "Elige una respuesta y pulsa Comprobar.",
    "Escolhe uma resposta e carrega em Verificar."
  ],
  "check": [
    "Проверить",
    "Check",
    "检查",
    "تحقّق",
    "Comprobar",
    "Verificar"
  ],
  "draft": [
    "До отправки выбор можно изменить.",
    "You can change your choice before sending.",
    "提交前可以更改选择。",
    "يمكنك تغيير اختيارك قبل الإرسال.",
    "Puedes cambiar la respuesta antes de enviarla.",
    "Podes alterar a escolha antes de enviar."
  ],
  "typeGreek": [
    "Напиши ответ по-гречески",
    "Write your answer in Greek",
    "请用希腊语回答",
    "اكتب إجابتك باليونانية",
    "Escribe tu respuesta en griego",
    "Escreve a resposta em grego"
  ],
  "emptyAnswer": [
    "Сначала введи ответ.",
    "Enter an answer first.",
    "请先输入答案。",
    "أدخل إجابة أولًا.",
    "Escribe primero una respuesta.",
    "Escreve primeiro uma resposta."
  ],
  "longAnswer": [
    "Ответ должен быть не длиннее {count} символов.",
    "Use no more than {count} characters.",
    "答案不能超过 {count} 个字符。",
    "استخدم {count} حرفًا على الأكثر.",
    "Usa como máximo {count} caracteres.",
    "Usa no máximo {count} caracteres."
  ],
  "saving": [
    "Сохраняем ответ…",
    "Saving your answer…",
    "正在保存答案…",
    "جارٍ حفظ الإجابة…",
    "Guardando la respuesta…",
    "A guardar a resposta…"
  ],
  "saved": [
    "Ответ сохранён",
    "Answer saved",
    "答案已保存",
    "تم حفظ الإجابة",
    "Respuesta guardada",
    "Resposta guardada"
  ],
  "unknown": [
    "Проверяем, сохранился ли ответ. Твой выбор сохранён здесь.",
    "Checking whether the answer was saved. Your choice is kept here.",
    "正在确认答案是否已保存。此处保留你的选择。",
    "نتحقّق من حفظ الإجابة. اختيارك محفوظ هنا.",
    "Comprobando si se guardó la respuesta. Tu elección se conserva aquí.",
    "A confirmar se a resposta foi guardada. A tua escolha mantém-se aqui."
  ],
  "conflict": [
    "Занятие изменилось на другом устройстве. Загружено актуальное состояние.",
    "This lesson changed on another device. The latest state is loaded.",
    "课程在另一台设备上发生了变化。已加载最新状态。",
    "تغيّر الدرس على جهاز آخر. تم تحميل الحالة الحالية.",
    "La lección cambió en otro dispositivo. Se ha cargado el estado actual.",
    "A lição mudou noutro dispositivo. Foi carregado o estado atual."
  ],
  "correct": [
    "Верно",
    "Correct",
    "正确",
    "صحيح",
    "Correcto",
    "Certo"
  ],
  "wrong": [
    "Есть ошибка",
    "Not quite",
    "有误",
    "الإجابة غير صحيحة",
    "Hay un error",
    "Há um erro"
  ],
  "unverified": [
    "Вариант не подтверждён — без штрафа.",
    "Unverified answer — no penalty.",
    "此答案尚未确认，不扣分。",
    "إجابة غير مؤكدة — دون عقوبة.",
    "Respuesta sin confirmar, sin penalización.",
    "Resposta não confirmada, sem penalização."
  ],
  "yourAnswer": [
    "Твой ответ",
    "Your answer",
    "你的答案",
    "إجابتك",
    "Tu respuesta",
    "A tua resposta"
  ],
  "correction": [
    "Правильный вариант",
    "Correct answer",
    "正确答案",
    "الإجابة الصحيحة",
    "Respuesta correcta",
    "Resposta correta"
  ],
  "explanation": [
    "Объяснение",
    "Explanation",
    "解释",
    "التوضيح",
    "Explicación",
    "Explicação"
  ],
  "meaning": [
    "Смысл",
    "Meaning",
    "含义",
    "المعنى",
    "Significado",
    "Significado"
  ],
  "alternatives": [
    "Другие допустимые варианты",
    "Other accepted answers",
    "其他可接受的答案",
    "إجابات أخرى مقبولة",
    "Otras respuestas aceptadas",
    "Outras respostas aceites"
  ],
  "details": [
    "Подробнее",
    "More details",
    "详细说明",
    "تفاصيل إضافية",
    "Más detalles",
    "Mais detalhes"
  ],
  "finalAnswer": [
    "Ответ оценён. Его результат уже не меняется.",
    "This answer has been assessed. Its result is final.",
    "答案已评分，结果不再更改。",
    "تم تقييم الإجابة ونتيجتها نهائية.",
    "La respuesta está evaluada; el resultado es definitivo.",
    "A resposta foi avaliada; o resultado é definitivo."
  ],
  "next": [
    "Дальше",
    "Next",
    "下一题",
    "التالي",
    "Siguiente",
    "Seguinte"
  ],
  "finish": [
    "Завершить урок",
    "Finish lesson",
    "完成课程",
    "إنهاء الدرس",
    "Terminar lección",
    "Concluir lição"
  ],
  "done": [
    "Урок завершён",
    "Lesson completed",
    "课程已完成",
    "اكتمل الدرس",
    "Lección completada",
    "Lição concluída"
  ],
  "lessonResult": [
    "Результат этого урока",
    "This lesson's result",
    "本课结果",
    "نتيجة هذا الدرس",
    "Resultado de esta lección",
    "Resultado desta lição"
  ],
  "practised": [
    "Сегодня практиковали",
    "Today you practised",
    "今天练习了",
    "تدرّبت اليوم على",
    "Hoy has practicado",
    "Hoje praticaste"
  ],
  "attempts": [
    "Ответы",
    "Answers",
    "回答数",
    "الإجابات",
    "Respuestas",
    "Respostas"
  ],
  "errors": [
    "Ошибки",
    "Mistakes",
    "错题",
    "الأخطاء",
    "Errores",
    "Erros"
  ],
  "accuracy": [
    "Точность ответов",
    "Answer accuracy",
    "答题正确率",
    "دقّة الإجابات",
    "Precisión de las respuestas",
    "Precisão das respostas"
  ],
  "activeTime": [
    "Примерное активное время",
    "Approx. active time",
    "估计练习时间",
    "الوقت النشط التقريبي",
    "Tiempo activo aproximado",
    "Tempo ativo aproximado"
  ],
  "elapsed": [
    "С начала главы",
    "Since chapter start",
    "本章开始至今",
    "منذ بدء الفصل",
    "Desde el inicio del capítulo",
    "Desde o início do capítulo"
  ],
  "chapterResult": [
    "Результат главы",
    "Chapter result",
    "本章结果",
    "نتيجة الفصل",
    "Resultado del capítulo",
    "Resultado do capítulo"
  ],
  "allDone": [
    "Все доступные главы пройдены",
    "All available chapters completed",
    "所有可用章节均已完成",
    "اكتملت جميع الفصول المتاحة",
    "Todos los capítulos disponibles completados",
    "Todos os capítulos disponíveis concluídos"
  ],
  "continueChapter": [
    "Следующая глава",
    "Next chapter",
    "下一章",
    "الفصل التالي",
    "Siguiente capítulo",
    "Próximo capítulo"
  ],
  "backlog": [
    "Повторение в уроках",
    "Review in lessons",
    "课程中的复习",
    "المراجعة في الدروس",
    "Repaso en las lecciones",
    "Revisão nas lições"
  ],
  "backlogNote": [
    "Эти задания назначены на повторение в следующих уроках.",
    "These questions are scheduled for review in later lessons.",
    "这些题目已安排在后续课程中复习。",
    "هذه الأسئلة مجدولة للمراجعة في الدروس التالية.",
    "Estas preguntas están programadas para repasar en próximas lecciones.",
    "Estas perguntas estão agendadas para revisão nas próximas lições."
  ],
  "noBacklog": [
    "Сейчас нет заданий, назначенных на повторение.",
    "No questions are scheduled for review now.",
    "目前没有安排复习的题目。",
    "لا توجد أسئلة مجدولة للمراجعة الآن.",
    "No hay preguntas pendientes de repaso.",
    "Não há perguntas agendadas para revisão."
  ],
  "jump": [
    "Начать с выбранной главы",
    "Start at selected chapter",
    "从所选章节开始",
    "ابدأ من الفصل المحدّد",
    "Empezar en el capítulo elegido",
    "Começar no capítulo escolhido"
  ],
  "jumpNote": [
    "Пропущенные главы не считаются освоенными.",
    "Skipped chapters are not marked mastered.",
    "跳过的章节不计为已掌握。",
    "لا تُعتبر الفصول المتجاوزة متقنة.",
    "Los capítulos omitidos no se consideran dominados.",
    "Os capítulos saltados não contam como dominados."
  ],
  "skipped": [
    "Пропущено",
    "Skipped",
    "已跳过",
    "متجاوز",
    "Omitido",
    "Ignorado"
  ],
  "paused": [
    "Занятие приостановлено",
    "Lesson paused",
    "课程已暂停",
    "تم إيقاف الدرس مؤقتًا",
    "Lección en pausa",
    "Lição em pausa"
  ],
  "listen": [
    "Слушать",
    "Listen",
    "播放",
    "استمع",
    "Escuchar",
    "Ouvir"
  ],
  "slow": [
    "0,8× Медленнее",
    "0.8× Slower",
    "0.8× 慢速",
    "0.8× أبطأ",
    "0,8× Más lento",
    "0,8× Mais lento"
  ],
  "audioUnavailable": [
    "Запись недоступна",
    "Recording unavailable",
    "录音不可用",
    "التسجيل غير متاح",
    "Grabación no disponible",
    "Gravação indisponível"
  ],
  "clock": [
    "Аналоговые часы",
    "Analogue clock",
    "模拟时钟",
    "ساعة بعقارب",
    "Reloj analógico",
    "Relógio analógico"
  ],
  "noMaterial": [
    "В этом диапазоне пока нет подходящих заданий.",
    "No suitable questions are available in this range yet.",
    "当前范围内暂无合适题目。",
    "لا توجد أسئلة مناسبة في هذا النطاق حاليًا.",
    "Aún no hay preguntas adecuadas en este intervalo.",
    "Ainda não há perguntas adequadas neste intervalo."
  ],
  "seconds": [
    "с",
    "s",
    "秒",
    "ث",
    "s",
    "s"
  ],
  "minutes": [
    "мин",
    "min",
    "分钟",
    "د",
    "min",
    "min"
  ],
  "family_book": [
    "Учебник и фразы",
    "Textbook and phrases",
    "教材与短语",
    "الكتاب والعبارات",
    "Libro y frases",
    "Livro e expressões"
  ],
  "family_lexicon": [
    "Слова главы",
    "Chapter vocabulary",
    "本章词汇",
    "مفردات الفصل",
    "Vocabulario del capítulo",
    "Vocabulário do capítulo"
  ],
  "family_verb": [
    "Глаголы в действии",
    "Verbs in action",
    "动词练习",
    "الأفعال في الاستعمال",
    "Verbos en acción",
    "Verbos em ação"
  ],
  "family_grammar": [
    "Грамматика",
    "Grammar",
    "语法",
    "القواعد",
    "Gramática",
    "Gramática"
  ],
  "family_listening": [
    "Слушаем греческий",
    "Greek listening",
    "希腊语听力",
    "الاستماع لليونانية",
    "Escucha en griego",
    "Compreensão oral"
  ],
  "family_dialogue": [
    "Разговоры",
    "Conversations",
    "对话",
    "المحادثات",
    "Conversaciones",
    "Conversas"
  ],
  "family_clock": [
    "Часы и расписание",
    "Time and schedules",
    "时间与日程",
    "الوقت والجداول",
    "Horas y horarios",
    "Horas e horários"
  ],
  "family_life": [
    "Реальная жизнь",
    "Everyday life",
    "日常生活",
    "الحياة اليومية",
    "Vida cotidiana",
    "Vida quotidiana"
  ],
  "lifeIntro": [
    "Практикуй греческий в знакомых жизненных ситуациях.",
    "Practise Greek in familiar everyday situations.",
    "在熟悉的日常情境中练习希腊语。",
    "تدرّب على اليونانية في مواقف يومية مألوفة.",
    "Practica griego en situaciones cotidianas.",
    "Pratica grego em situações do dia a dia."
  ],
  "scene": [
    "Ситуация",
    "Situation",
    "情境",
    "الموقف",
    "Situación",
    "Situação"
  ],
  "mission": [
    "Твоя задача",
    "Your task",
    "你的任务",
    "مهمّتك",
    "Tu tarea",
    "A tua tarefa"
  ],
  "hint": [
    "Подсказка",
    "Hint",
    "提示",
    "تلميح",
    "Pista",
    "Pista"
  ],
  "sceneProgress": [
    "Завершённые ситуации",
    "Completed situations",
    "已完成情境",
    "المواقف المكتملة",
    "Situaciones completadas",
    "Situações concluídas"
  ],
  "fresh": [
    "Новая ситуация",
    "New situation",
    "新情境",
    "موقف جديد",
    "Nueva situación",
    "Nova situação"
  ],
  "reviewAgain": [
    "Повторение знакомого",
    "Practise again",
    "再次练习",
    "مراجعة",
    "Volver a practicar",
    "Voltar a praticar"
  ],
  "guided": [
    "С подсказкой",
    "With hints",
    "有提示",
    "مع تلميحات",
    "Con pistas",
    "Com pistas"
  ],
  "independent": [
    "Без подсказок",
    "Without hints",
    "无提示",
    "دون تلميحات",
    "Sin pistas",
    "Sem pistas"
  ],
  "nextScene": [
    "Следующая ситуация",
    "Next situation",
    "下一个情境",
    "الموقف التالي",
    "Siguiente situación",
    "Próxima situação"
  ],
  "translationUnavailable": [
    "Перевод на выбранный язык пока недоступен.",
    "A translation in the selected language is not available yet.",
    "所选语言暂无翻译。",
    "الترجمة باللغة المختارة غير متاحة بعد.",
    "Aún no hay traducción al idioma elegido.",
    "Ainda não há tradução para a língua escolhida."
  ],
  "classicStats": [
    "История ответов по учебным карточкам",
    "Book-card answer history",
    "教材卡片答题记录",
    "سجل إجابات بطاقات الكتاب",
    "Historial de respuestas del libro",
    "Histórico de respostas do livro"
  ],
  "classicReview": [
    "Здесь — ошибки по учебным карточкам. Повторение словаря и жизненных ситуаций доступно в соответствующих разделах.",
    "This queue covers book cards. Vocabulary and everyday situations have review in their own sections.",
    "此处复习教材卡片的错题。词汇和生活场景请在相应页面复习。",
    "تشمل هذه القائمة بطاقات الكتاب. راجع المفردات والمواقف اليومية في أقسامها.",
    "Esta cola reúne tarjetas del libro. El vocabulario y las situaciones se repasan en sus secciones.",
    "Esta fila reúne cartões do livro. O vocabulário e as situações revêem-se nas respetivas secções."
  ],
  "statsNotice": [
    "Уроки, словарь и жизненные ситуации учитываются отдельно. Ответы по учебным карточкам из уроков также входят в историю ниже; эти числа не нужно складывать.",
    "Lessons, vocabulary and everyday situations have separate records. Book-card answers in lessons also appear in the history below; these counts overlap.",
    "课程、词汇和生活场景分别统计。课程中的教材卡片答案也包含在下方记录中；请勿将这些数字相加。",
    "للدروس والمفردات والمواقف اليومية سجلات منفصلة. تظهر إجابات بطاقات الكتاب من الدروس في السجل أدناه أيضاً؛ لا تُجمع هذه الأعداد.",
    "Las lecciones, el vocabulario y las situaciones tienen registros propios. Las respuestas del libro en las lecciones también aparecen abajo; los recuentos se solapan.",
    "As lições, o vocabulário e as situações têm registos próprios. As respostas do livro nas lições também aparecem abaixo; as contagens sobrepõem-se."
  ],
  "progressByActivity": [
    "Прогресс по занятиям",
    "Progress by activity",
    "各项学习进度",
    "التقدم حسب النشاط",
    "Progreso por actividad",
    "Progresso por atividade"
  ],
  "lessonsCompleted": [
    "Уроков завершено",
    "Lessons completed",
    "已完成课程",
    "الدروس المكتملة",
    "Lecciones completadas",
    "Lições concluídas"
  ],
  "practicedWords": [
    "Слов отработано",
    "Words practised",
    "已练习单词",
    "الكلمات المتدرّب عليها",
    "Palabras practicadas",
    "Palavras praticadas"
  ],
  "reviewDue": [
    "К повторению",
    "Ready for review",
    "待复习",
    "جاهزة للمراجعة",
    "Por repasar",
    "Por rever"
  ],
  "openActivity": [
    "Перейти к занятию",
    "Open activity",
    "前往练习",
    "فتح النشاط",
    "Abrir actividad",
    "Abrir atividade"
  ],
  "contentLanguage": [
    "Материал текущего урока остаётся на языке, выбранном при его начале.",
    "This lesson’s material keeps the language chosen when it started.",
    "本课内容保留开始时选择的语言。",
    "تحتفظ مواد هذا الدرس باللغة المختارة عند بدايته.",
    "El material de esta lección mantiene el idioma elegido al comenzarla.",
    "O material desta lição mantém o idioma escolhido ao iniciá-la."
  ],
  "reviewRouteInfo": [
    "Рекомендация относится к учебным карточкам. Здесь доступна ваша очередь повторения.",
    "The recommendation concerns book cards. Your available review queue is shown here.",
    "建议针对教材卡片。这里显示你当前可复习的内容。",
    "تتعلق التوصية ببطاقات الكتاب. تظهر هنا قائمة المراجعة المتاحة لك.",
    "La recomendación se refiere a tarjetas del libro. Aquí tienes tu cola de repaso disponible.",
    "A recomendação refere-se a cartões do livro. Aqui tens a tua fila de revisão disponível."
  ],
  "lastResult": [
    "Последний результат урока",
    "Latest lesson result",
    "最近一次课程结果",
    "نتيجة آخر درس",
    "Resultado de la última lección",
    "Resultado da última lição"
  ]
};
  const lang=()=>document.getElementById("lang")?.value||"ru";
  function t(key,values={}){
    const item=rows[key];let result=item?item[Math.max(0,locales.indexOf(lang()))]:key;
    for(const [name,value] of Object.entries(values))result=result.replaceAll("{"+name+"}",String(value));
    return result;
  }
  function apply(root=document){
    for(const el of root.querySelectorAll("[data-ui]"))el.textContent=t(el.dataset.ui);
    for(const el of root.querySelectorAll("[data-ui-aria]"))el.setAttribute("aria-label",t(el.dataset.uiAria));
  }
  let shellState="loading",authVisible=false,returnFocus=null;
  const site=()=>document.querySelector(".site");
  function inert(){if(site())site().inert=authVisible||shellState!=="ready";}
  function auth(visible){
    const gate=document.getElementById("auth-gate");if(!gate)return;
    if(visible&&!authVisible)returnFocus=document.activeElement;
    gate.hidden=!visible;authVisible=visible;inert();
    if(visible)queueMicrotask(()=>{
      const input=gate.querySelector("#auth-success:not([hidden]) button, #auth-form:not([hidden]) div:not([hidden]) input, button");
      input?.focus();
    });else if(returnFocus?.isConnected&&!returnFocus.closest("[hidden]"))returnFocus.focus();
  }
  function shell(value,callback){
    shellState=value;const box=document.getElementById("app-state");
    if(box){box.hidden=value==="ready";box.querySelector("p").textContent=t(value==="error"?"network":"loading");
      const retry=box.querySelector("button");retry.hidden=value!=="error";retry.textContent=t("retry");retry.onclick=callback||null;}
    inert();
  }
  function applyTheme(value){
    const selected=["light","dark"].includes(value)?value:"system";
    document.documentElement.dataset.theme=selected;
    const actual=selected==="system"?(window.matchMedia?.("(prefers-color-scheme: dark)").matches?"dark":"light"):selected;
    document.documentElement.style.colorScheme=actual;
    const meta=document.querySelector('meta[name="theme-color"]');if(meta)meta.content=actual==="dark"?"#111e28":"#f6f4ed";
    try{localStorage.setItem("lexi-theme",selected);}catch{}
  }
  document.getElementById("auth-gate")?.addEventListener("keydown",event=>{
    if(event.key!=="Tab")return;
    const all=[...event.currentTarget.querySelectorAll("button,input,select,a[href]")].filter(el=>!el.disabled&&!el.closest("[hidden]")&&el.getClientRects().length);
    if(!all.length)return;
    const first=all[0],last=all[all.length-1];
    if(event.shiftKey&&(document.activeElement===first||!all.includes(document.activeElement))){event.preventDefault();last.focus();}
    else if(!event.shiftKey&&(document.activeElement===last||!all.includes(document.activeElement))){event.preventDefault();first.focus();}
  });
  // Native disclosure navigation keeps normal Tab order, with predictable dismissal.
  const popovers=[...document.querySelectorAll(".tab-more,.account-menu")];
  for(const details of popovers){
    details.addEventListener("toggle",()=>{
      if(details.open)for(const other of popovers)if(other!==details)other.open=false;
    });
    details.addEventListener("keydown",event=>{
      if(event.key!=="Escape"||!details.open)return;
      event.preventDefault();details.open=false;
      details.querySelector("summary")?.focus();
    });
  }
  for(const type of ["click","focusin"])document.addEventListener(type,event=>{
    for(const details of popovers)if(details.open&&!details.contains(event.target))details.open=false;
  });
  const choice=document.getElementById("theme-select");
  let theme="system";try{theme=localStorage.getItem("lexi-theme")||theme;}catch{}
  if(choice){choice.value=theme;choice.addEventListener("change",()=>applyTheme(choice.value));}
  applyTheme(theme);
  window.matchMedia?.("(prefers-color-scheme: dark)").addEventListener?.("change",()=>{if(document.documentElement.dataset.theme==="system")applyTheme("system");});
  document.getElementById("lang")?.addEventListener("change",()=>apply());
  window.LexiUI={t,lang,apply,auth,shell,locales,keys:Object.keys(rows)};
  apply();shell("loading");
})();
