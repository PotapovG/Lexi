/* Optional AI practice lives inside the existing lesson result. No provider keys or automatic paid work. */
(() => {
  "use strict";
  const langs=["ru","en","zh","ar","es","pt"];
  const rows={
    title:["Практика с ИИ","Practice with AI","AI 练习","تدريب بالذكاء الاصطناعي","Práctica con IA","Prática com IA"],
    optional:["По желанию","Optional","自愿使用","اختياري","Opcional","Opcional"],
    intro:["Разбор урока, чтение вслух и короткий разговор. Оценки урока не меняются.","Reflect on the lesson, read aloud or try a short conversation. Your lesson grades stay the same.","回顾课程、朗读或进行简短对话。不会改变课程成绩。","راجع الدرس أو اقرأ بصوت عالٍ أو جرّب حواراً قصيراً. تبقى درجات الدرس كما هي.","Repasa la lección, lee en voz alta o prueba una conversación breve. Las notas de la lección se conservan.","Revê a lição, lê em voz alta ou experimenta uma conversa breve. As notas da lição mantêm-se."],
    summary:["Разбор урока","Lesson reflection","课程反馈","مراجعة الدرس","Comentario de la lección","Comentário da lição"],
    createSummary:["Получить разбор","Get lesson feedback","获取课程反馈","الحصول على ملاحظات","Recibir comentarios","Receber comentários"],
    reading:["Чтение вслух","Read aloud","朗读","القراءة بصوت عالٍ","Lectura en voz alta","Leitura em voz alta"],
    dialogue:["Короткий диалог","Short dialogue","简短对话","حوار قصير","Diálogo breve","Diálogo breve"],
    back:["К вариантам практики","Back to practice options","返回练习选项","العودة إلى خيارات التدريب","Volver a las opciones","Voltar às opções"],
    privacy:["Данные и конфиденциальность","Data and privacy","数据与隐私","البيانات والخصوصية","Datos y privacidad","Dados e privacidade"],
    privacyText:["Выбранные ответы или отправленная запись передаются OpenAI для анализа. В Lexi тексты хранятся до {days} дней, аудио удаляется после обработки, не позднее {hours} ч. Можно удалить данные ИИ, сохранив обычный прогресс.","Selected answers or a recording you send are shared with OpenAI for analysis. Lexi keeps text for up to {days} days and deletes audio after processing, within {hours} hour(s). You can erase AI data and keep ordinary progress.","所选答案或您发送的录音会传给 OpenAI 进行分析。Lexi 最多保存文字 {days} 天；音频处理后删除，最迟不超过 {hours} 小时。删除 AI 数据不会删除普通学习进度。","تُرسل الإجابات المختارة أو التسجيل الذي ترسله إلى OpenAI للتحليل. تحتفظ Lexi بالنصوص حتى {days} يوماً وتحذف الصوت بعد المعالجة خلال {hours} ساعة. يمكنك حذف بيانات الذكاء الاصطناعي مع الاحتفاظ بالتقدم العادي.","Las respuestas seleccionadas o la grabación que envíes se comparten con OpenAI para su análisis. Lexi guarda el texto hasta {days} días y elimina el audio tras procesarlo, en un máximo de {hours} hora(s). Puedes borrar los datos de IA y conservar el progreso habitual.","As respostas selecionadas ou a gravação que enviares são partilhadas com a OpenAI para análise. A Lexi guarda texto até {days} dias e elimina o áudio após o processamento, num máximo de {hours} hora(s). Podes apagar os dados de IA e manter o progresso habitual."],
    providerPolicy:["У OpenAI действуют отдельные правила хранения. Удаление здесь относится к данным в Lexi.","OpenAI has separate retention rules. Deletion here applies to data held by Lexi.","OpenAI 有独立的数据保留规则。此处删除的是 Lexi 保存的数据。","لدى OpenAI قواعد احتفاظ منفصلة. الحذف هنا يخص البيانات المحفوظة لدى Lexi.","OpenAI tiene sus propias reglas de conservación. El borrado aquí se aplica a los datos guardados por Lexi.","A OpenAI tem regras próprias de retenção. A eliminação aqui aplica-se aos dados guardados pela Lexi."],
    providerLink:["Как OpenAI обрабатывает данные","How OpenAI handles data","OpenAI 如何处理数据","كيف تتعامل OpenAI مع البيانات","Cómo trata OpenAI los datos","Como a OpenAI trata os dados"],
    consentTitle:["Отправить для анализа?","Send for analysis?","发送并分析？","إرسال للتحليل؟","¿Enviar para analizar?","Enviar para análise?"],
    consentText:["ИИ может ошибаться. Разбор опирается на сохранённые ответы, а не на оценку общего уровня языка.","AI can make mistakes. Feedback uses saved answers and does not certify your overall language level.","AI 可能出错。反馈依据已保存的答案，不代表对整体语言水平的认证。","قد يخطئ الذكاء الاصطناعي. تعتمد الملاحظات على الإجابات المحفوظة ولا تثبت مستوى لغتك العام.","La IA puede equivocarse. Los comentarios se basan en respuestas guardadas y no certifican tu nivel general.","A IA pode enganar-se. Os comentários usam respostas guardadas e não certificam o teu nível geral."],
    agree:["Отправить","Send","发送","إرسال","Enviar","Enviar"],
    cancel:["Отмена","Cancel","取消","إلغاء","Cancelar","Cancelar"],
    close:["Закрыть","Close","关闭","إغلاق","Cerrar","Fechar"],
    loading:["Загружаем практику…","Loading practice…","正在加载练习…","جارٍ تحميل التدريب…","Cargando práctica…","A carregar a prática…"],
    sending:["Отправляем…","Sending…","正在发送…","جارٍ الإرسال…","Enviando…","A enviar…"],
    queued:["Запрос ожидает обработки.","Your request is queued.","请求正在排队。","طلبك في قائمة الانتظار.","La solicitud está en espera.","O pedido está em espera."],
    running:["Готовим обратную связь…","Preparing feedback…","正在准备反馈…","جارٍ إعداد الملاحظات…","Preparando comentarios…","A preparar comentários…"],
    interpreting:["Запись распознана. Готовим ответ…","Audio transcribed. Preparing a response…","录音已转写，正在准备回复…","تم تحويل الصوت إلى نص. جارٍ إعداد الرد…","Audio transcrito. Preparando la respuesta…","Áudio transcrito. A preparar a resposta…"],
    pollPaused:["Обработка ещё не закончена. Можно проверить позже; запрос повторно не отправляется.","Processing is still underway. Check again later; the request is not being resent.","处理仍在进行中。可以稍后查询；不会重新发送请求。","المعالجة مستمرة. يمكنك التحقق لاحقاً؛ لن يُعاد إرسال الطلب.","El procesamiento continúa. Puedes consultarlo más tarde; no se vuelve a enviar la solicitud.","O processamento continua. Podes consultar mais tarde; o pedido não é reenviado."],
    checkStatus:["Проверить статус","Check status","查询状态","التحقق من الحالة","Consultar estado","Consultar estado"],
    network:["Не удалось связаться с сервисом. Сохранённые результаты доступны после восстановления связи.","The service could not be reached. Saved results remain available when the connection returns.","无法连接服务。网络恢复后可查看已保存的结果。","تعذّر الاتصال بالخدمة. تبقى النتائج المحفوظة متاحة عند عودة الاتصال.","No se pudo conectar con el servicio. Los resultados guardados seguirán disponibles al recuperar la conexión.","Não foi possível contactar o serviço. Os resultados guardados ficam disponíveis quando a ligação voltar."],
    unavailable:["Эта практика сейчас недоступна. Можно продолжить обычный урок.","This practice is unavailable right now. You can continue the regular course.","此练习暂时不可用。可以继续普通课程。","هذا التدريب غير متاح الآن. يمكنك متابعة الدروس العادية.","Esta práctica no está disponible ahora. Puedes continuar el curso habitual.","Esta prática está indisponível neste momento. Podes continuar o curso habitual."],
    failed:["Не удалось подготовить результат. Обычный прогресс сохранён.","A result could not be prepared. Your ordinary progress is saved.","未能生成结果。普通学习进度已保存。","تعذّر إعداد النتيجة. تقدمك العادي محفوظ.","No se pudo preparar el resultado. El progreso habitual está guardado.","Não foi possível preparar o resultado. O progresso habitual está guardado."],
    unknown:["Исход прошлого запроса неизвестен. Сначала проверь статус. Автоматического повтора не будет.","The previous request's outcome is unknown. Check its status first. It will not be resent automatically.","上次请求的结果未知。请先查询状态。不会自动重发。","نتيجة الطلب السابق غير معروفة. تحقّق من حالته أولاً. لن يُعاد إرساله تلقائياً.","Se desconoce el resultado de la solicitud anterior. Consulta primero su estado. No se reenviará automáticamente.","O resultado do pedido anterior é desconhecido. Consulta primeiro o estado. Não será reenviado automaticamente."],
    missingOperation:["Сервис пока не нашёл этот запрос. Повторная отправка возможна только по твоему нажатию.","The service has not found this request. Resending requires your explicit action.","服务尚未找到此请求。只有您主动点击才会重新发送。","لم تعثر الخدمة على هذا الطلب. لا تتم إعادة الإرسال إلا بطلب منك.","El servicio no ha encontrado la solicitud. Solo se reenviará si tú lo indicas.","O serviço não encontrou este pedido. Só será reenviado por tua indicação."],
    retrySend:["Повторить ту же отправку","Resend the same request","重发同一请求","إعادة إرسال الطلب نفسه","Reenviar la misma solicitud","Reenviar o mesmo pedido"],
    lostRecording:["Локальная запись уже закрыта. После проверки статуса можно сделать новую.","The local recording has been cleared. After checking status, you can make a new one.","本地录音已清除。查询状态后可以重新录制。","تم مسح التسجيل المحلي. بعد التحقق من الحالة يمكنك إنشاء تسجيل جديد.","La grabación local se ha borrado. Tras consultar el estado puedes grabar otra.","A gravação local foi eliminada. Depois de consultares o estado, podes gravar outra."],
    resetAttempt:["Начать новую попытку","Start a new attempt","开始新的尝试","بدء محاولة جديدة","Empezar otro intento","Iniciar outra tentativa"],
    limited:["Лимит ИИ на сегодня достигнут. Обычные занятия доступны.","Today's AI allowance has been reached. Regular practice remains available.","今日 AI 额度已用完。普通练习仍然可用。","تم بلوغ حد الذكاء الاصطناعي اليوم. التدريب العادي ما زال متاحاً.","Se ha alcanzado el límite de IA de hoy. La práctica habitual sigue disponible.","O limite de IA de hoje foi atingido. A prática habitual continua disponível."],
    queueFull:["Сервис занят. Попробуй позже.","The service is busy. Try again later.","服务繁忙，请稍后再试。","الخدمة مشغولة. حاول لاحقاً.","El servicio está ocupado. Inténtalo más tarde.","O serviço está ocupado. Tenta mais tarde."],
    login:["Войди снова, чтобы продолжить.","Sign in again to continue.","请重新登录以继续。","سجّل الدخول مجدداً للمتابعة.","Vuelve a iniciar sesión para continuar.","Inicia sessão novamente para continuar."],
    cancelled:["Запрос отменён.","Request cancelled.","请求已取消。","تم إلغاء الطلب.","Solicitud cancelada.","Pedido cancelado."],
    cancelJob:["Отменить обработку","Cancel processing","取消处理","إلغاء المعالجة","Cancelar procesamiento","Cancelar processamento"],
    stopped:["Практика приостановлена. Микрофон выключен, локальная запись удалена.","Practice paused. The microphone is off and the local recording has been cleared.","练习已暂停。麦克风已关闭，本地录音已清除。","تم إيقاف التدريب مؤقتاً. الميكروفون مغلق والتسجيل المحلي محذوف.","Práctica en pausa. El micrófono está apagado y la grabación local se ha borrado.","Prática em pausa. O microfone está desligado e a gravação local foi eliminada."],
    resume:["Продолжить практику","Resume practice","继续练习","متابعة التدريب","Continuar práctica","Retomar prática"],
    chooseReading:["Текст для чтения","Reading text","朗读文本","نص القراءة","Texto para leer","Texto para ler"],
    textNumber:["Текст {n} · глава {chapter}","Text {n} · chapter {chapter}","文本 {n} · 第 {chapter} 章","النص {n} · الفصل {chapter}","Texto {n} · capítulo {chapter}","Texto {n} · capítulo {chapter}"],
    noReadings:["Для этой главы пока нет подходящего текста.","No suitable reading is available for this chapter yet.","本章暂无合适的朗读文本。","لا يوجد نص مناسب لهذا الفصل بعد.","Todavía no hay un texto adecuado para este capítulo.","Ainda não há um texto adequado para este capítulo."],
    localOnly:["Запись остаётся на устройстве до нажатия «Отправить». Можно прослушать и перезаписать.","Your recording stays on this device until you press Send. Listen back or record again first.","点击“发送”前，录音只保留在当前设备上。可以先试听或重录。","يبقى التسجيل على جهازك حتى تضغط إرسال. يمكنك الاستماع إليه أو إعادة التسجيل أولاً.","La grabación permanece en este dispositivo hasta que pulses Enviar. Puedes escucharla o repetirla antes.","A gravação fica neste dispositivo até carregares em Enviar. Podes ouvi-la ou voltar a gravar antes."],
    contentOnly:["Это сравнение распознанного текста с образцом. Произношение и акцент не оцениваются.","This compares recognized text with the reference. It does not assess pronunciation or accent.","此功能比较识别文字与参考文本，不评估发音或口音。","تتم مقارنة النص المتعرّف عليه بالنموذج. لا يتم تقييم النطق أو اللكنة.","Se compara el texto reconocido con el modelo. No se evalúan la pronunciación ni el acento.","Compara-se o texto reconhecido com o modelo. A pronúncia e o sotaque não são avaliados."],
    permission:["Разреши доступ к микрофону в окне браузера.","Allow microphone access in your browser prompt.","请在浏览器提示中允许使用麦克风。","اسمح بالوصول إلى الميكروفون في نافذة المتصفح.","Permite el acceso al micrófono en el aviso del navegador.","Permite o acesso ao microfone no aviso do navegador."],
    permissionDenied:["Доступ к микрофону не разрешён. Можно изменить разрешение браузера или ответить текстом в диалоге.","Microphone access was denied. Change browser permission or use a typed dialogue answer.","未获得麦克风权限。可修改浏览器权限，或在对话中输入文字回答。","لم يُسمح بالوصول إلى الميكروفون. غيّر إذن المتصفح أو أجب كتابةً في الحوار.","No se permitió el acceso al micrófono. Cambia el permiso del navegador o responde por escrito en el diálogo.","O acesso ao microfone foi recusado. Altera a permissão do navegador ou responde por escrito no diálogo."],
    unsupported:["Запись звука здесь недоступна. В диалоге можно практиковать смысл ответа текстом.","Audio recording is unavailable here. You can practise meaning with typed dialogue answers.","此环境无法录音。可以在对话中通过文字练习表达意思。","التسجيل الصوتي غير متاح هنا. يمكنك تدريب المعنى بإجابات مكتوبة في الحوار.","No se puede grabar audio aquí. Puedes practicar el significado con respuestas escritas en el diálogo.","Não é possível gravar áudio aqui. Podes praticar o significado com respostas escritas no diálogo."],
    record:["Записать голос","Record voice","录音","تسجيل الصوت","Grabar voz","Gravar voz"],
    recording:["Идёт запись","Recording","正在录音","جارٍ التسجيل","Grabando","A gravar"],
    stop:["Остановить запись","Stop recording","停止录音","إيقاف التسجيل","Detener grabación","Parar gravação"],
    rerecord:["Перезаписать","Record again","重新录制","إعادة التسجيل","Volver a grabar","Gravar novamente"],
    preview:["Прослушать свою запись","Listen to your recording","试听录音","الاستماع إلى تسجيلك","Escuchar tu grabación","Ouvir a tua gravação"],
    audioLimit:["Не более {seconds} секунд.","Up to {seconds} seconds.","最长 {seconds} 秒。","حتى {seconds} ثانية.","Hasta {seconds} segundos.","Até {seconds} segundos."],
    sendAudio:["Отправить запись","Send recording","发送录音","إرسال التسجيل","Enviar grabación","Enviar gravação"],
    emptyAudio:["Запись слишком короткая или пустая. Попробуй ещё раз.","The recording is empty or too short. Please try again.","录音为空或过短，请重试。","التسجيل فارغ أو قصير جداً. حاول مجدداً.","La grabación está vacía o es demasiado corta. Inténtalo de nuevo.","A gravação está vazia ou é demasiado curta. Tenta novamente."],
    transcript:["Распознанный текст","Recognized text","识别文字","النص المتعرّف عليه","Texto reconocido","Texto reconhecido"],
    editTranscript:["Исправить распознанный текст","Edit recognized text","修改识别文字","تعديل النص المتعرّف عليه","Corregir texto reconocido","Corrigir texto reconhecido"],
    saveTranscript:["Сравнить исправленный текст","Review edited text","检查修改后的文字","مراجعة النص المعدّل","Revisar texto corregido","Rever texto corrigido"],
    edited:["Текст исправлен вручную. Это не новое доказательство произношения.","Text was edited by hand. This is not new pronunciation evidence.","文字经手动修改，不构成新的发音证据。","تم تعديل النص يدوياً. هذا ليس دليلاً جديداً على النطق.","El texto se ha editado a mano. No es una nueva prueba de pronunciación.","O texto foi editado à mão. Não é nova evidência de pronúncia."],
    originalTranscript:["Исходное распознавание","Original recognition","原始识别结果","النص الأصلي المتعرّف عليه","Reconocimiento original","Reconhecimento original"],
    sameContent:["Распознанный текст совпадает по содержанию.","The recognized content matches the reference.","识别内容与参考文本一致。","المحتوى المتعرّف عليه مطابق للنموذج.","El contenido reconocido coincide con el modelo.","O conteúdo reconhecido corresponde ao modelo."],
    differences:["Места для повторного чтения","Places to read again","可再读的部分","مواضع لإعادة القراءة","Partes para volver a leer","Partes para voltar a ler"],
    reference:["В образце","Reference","参考文本","في النموذج","En el modelo","No modelo"],
    recognized:["Распознано","Recognized","识别为","ما تم التعرّف عليه","Reconocido","Reconhecido"],
    noWords:["Слов нет","No words","无文字","لا توجد كلمات","Sin palabras","Sem palavras"],
    asrCaution:["Расхождение может быть ошибкой распознавания. Сначала проверь текст.","A difference may be a recognition error. Check the transcript first.","差异可能来自语音识别，请先核对文字。","قد يكون الاختلاف خطأ في التعرّف على الكلام. تحقّق من النص أولاً.","Una diferencia puede ser un error de reconocimiento. Comprueba primero el texto.","Uma diferença pode ser um erro de reconhecimento. Confere primeiro o texto."],
    moreDifferences:["Есть и другие различия; сейчас показаны два.","There are more differences; two are shown here.","还有其他差异，此处显示两项。","توجد اختلافات أخرى؛ يظهر هنا اثنان.","Hay más diferencias; aquí se muestran dos.","Há mais diferenças; aqui são mostradas duas."],
    repeatPhrase:["Повторить фрагмент","Practise this phrase","练习此片段","تدريب هذه العبارة","Practicar este fragmento","Praticar este trecho"],
    focusPhrase:["Обрати внимание на этот фрагмент. Для сравнения снова прочитай весь текст.","Focus on this phrase. Read the whole text again for comparison.","请关注这个片段。再次比较时请朗读全文。","ركّز على هذه العبارة. اقرأ النص كاملاً مجدداً للمقارنة.","Fíjate en este fragmento. Lee de nuevo el texto completo para compararlo.","Presta atenção a este trecho. Lê novamente o texto completo para comparar."],
    observation:["Наблюдение по уроку","Lesson observation","课程观察","ملاحظة عن الدرس","Observación de la lección","Observação da lição"],
    improvements:["Что стоит потренировать","What to practise next","接下来可练习的内容","ما يستحق التدريب","Qué conviene practicar","O que convém praticar"],
    example:["Пример из урока","Example from your lesson","课程中的例子","مثال من درسك","Ejemplo de tu lección","Exemplo da tua lição"],
    nextStep:["Следующий шаг","Next step","下一步","الخطوة التالية","Siguiente paso","Próximo passo"],
    existingReview:["Открыть «Мои ошибки»","Open My mistakes","打开“我的错题”","فتح «أخطائي»","Abrir Mis errores","Abrir Os meus erros"],
    reviewNote:["Откроется существующая очередь повторения; конкретная карточка может быть не первой.","This opens the existing review queue; the suggested card may not be first.","将打开现有复习队列，建议卡片可能不在首位。","ستُفتح قائمة المراجعة الحالية؛ قد لا تكون البطاقة المقترحة أولاً.","Se abrirá la cola de repaso existente; puede que la tarjeta sugerida no sea la primera.","Abre a fila de revisão existente; a ficha sugerida pode não ser a primeira."],
    partialEvidence:["Сохранена только часть ответов этого урока. Разбор ограничен ими.","Only part of this lesson's answers were recorded. Feedback covers those answers only.","仅保存了本课部分答案，反馈只涵盖这些答案。","حُفظ جزء فقط من إجابات هذا الدرس. الملاحظات تقتصر عليها.","Solo se guardó parte de las respuestas de esta lección. Los comentarios se limitan a ellas.","Só foi guardada parte das respostas desta lição. Os comentários limitam-se a essas respostas."],
    advisory:["Совет ИИ, а не новая оценка. Можно сообщить о неточности.","AI advice, not a new grade. You can report an inaccuracy.","这是 AI 建议，不是新的评分。可以报告不准确之处。","نصيحة من الذكاء الاصطناعي وليست درجة جديدة. يمكنك الإبلاغ عن خطأ.","Es una sugerencia de IA, no una nota nueva. Puedes señalar una imprecisión.","É uma sugestão de IA, não uma nova nota. Podes assinalar uma imprecisão."],
    scenario:["Первый вопрос","First question","第一个问题","السؤال الأول","Primera pregunta","Primeira pergunta"],
    turns:["Количество ответов","Number of answers","回答次数","عدد الإجابات","Número de respuestas","Número de respostas"],
    startDialogue:["Начать диалог","Start dialogue","开始对话","بدء الحوار","Empezar diálogo","Iniciar diálogo"],
    resumeDialogue:["Продолжить сохранённый диалог","Resume saved dialogue","继续已保存的对话","متابعة الحوار المحفوظ","Continuar diálogo guardado","Retomar diálogo guardado"],
    viewDialogue:["Посмотреть диалог","View dialogue","查看对话","عرض الحوار","Ver diálogo","Ver diálogo"],
    noDialogue:["Для этой главы диалог ещё не подготовлен. Можно потренировать чтение.","Dialogue is not ready for this chapter yet. You can practise reading.","本章对话尚未准备好，可以练习朗读。","الحوار غير جاهز لهذا الفصل بعد. يمكنك تدريب القراءة.","El diálogo aún no está preparado para este capítulo. Puedes practicar la lectura.","O diálogo ainda não está preparado para este capítulo. Podes praticar a leitura."],
    turnProgress:["Ответов: {count} из {total}","Answers: {count} of {total}","已回答：{count}/{total}","الإجابات: {count} من {total}","Respuestas: {count} de {total}","Respostas: {count} de {total}"],
    question:["Вопрос","Question","问题","السؤال","Pregunta","Pergunta"],
    yourAnswer:["Твой ответ","Your answer","你的回答","إجابتك","Tu respuesta","A tua resposta"],
    reply:["Ответ собеседника","Partner's reply","对方回复","رد الطرف الآخر","Respuesta del interlocutor","Resposta do interlocutor"],
    correction:["Возможная корректировка","Suggested correction","建议修改","تصحيح مقترح","Corrección sugerida","Correção sugerida"],
    explanation:["Почему","Why","说明","السبب","Por qué","Porquê"],
    typedButton:["Ответить текстом","Answer by typing","输入文字回答","الإجابة كتابةً","Responder por escrito","Responder por escrito"],
    voiceButton:["Ответить голосом","Answer by voice","用语音回答","الإجابة صوتياً","Responder con voz","Responder por voz"],
    typeAnswer:["Напиши ответ по-гречески","Type your answer in Greek","用希腊语输入回答","اكتب إجابتك باليونانية","Escribe tu respuesta en griego","Escreve a tua resposta em grego"],
    sendText:["Отправить ответ","Send answer","发送回答","إرسال الإجابة","Enviar respuesta","Enviar resposta"],
    typedOnly:["Текстовый ответ: проверяется только смысл. Голос и произношение не оценивались.","Typed answer: meaning only. Voice and pronunciation were not assessed.","文字回答仅检查意思，未评估声音或发音。","إجابة مكتوبة: المعنى فقط. لم يُقيّم الصوت أو النطق.","Respuesta escrita: solo se valora el significado. No se evaluaron la voz ni la pronunciación.","Resposta escrita: avalia-se apenas o significado. A voz e a pronúncia não foram avaliadas."],
    finishDialogue:["Завершить диалог сейчас","Finish dialogue now","现在结束对话","إنهاء الحوار الآن","Terminar el diálogo ahora","Terminar o diálogo agora"],
    completedDialogue:["Диалог завершён","Dialogue completed","对话已完成","اكتمل الحوار","Diálogo completado","Diálogo concluído"],
    partialDialogue:["Диалог завершён досрочно. Сохранённые ответы доступны ниже.","Dialogue ended early. Saved answers are shown below.","对话已提前结束。下方可查看已保存的回答。","انتهى الحوار مبكراً. الإجابات المحفوظة معروضة أدناه.","El diálogo terminó antes de tiempo. Las respuestas guardadas aparecen abajo.","O diálogo terminou mais cedo. As respostas guardadas aparecem abaixo."],
    uncertain:["Ответ не удалось уверенно понять. Ход не засчитан как ошибка и вопрос остался прежним. Перезапиши или ответь текстом.","The answer could not be understood reliably. No error was assigned and the question is unchanged. Record again or type your answer.","未能可靠理解回答。未计为错误，问题保持不变。请重录或输入文字回答。","تعذّر فهم الإجابة بثقة. لم يُسجّل خطأ وبقي السؤال كما هو. أعد التسجيل أو أجب كتابةً.","No se pudo entender la respuesta con suficiente seguridad. No se contó como error y la pregunta no cambió. Graba de nuevo o escribe.","Não foi possível compreender a resposta com segurança. Não foi contado um erro e a pergunta mantém-se. Grava novamente ou escreve."],
    savedConversations:["Сохранённые диалоги","Saved dialogues","已保存的对话","الحوارات المحفوظة","Diálogos guardados","Diálogos guardados"],
    report:["Сообщить о неточности","Report an issue","报告问题","الإبلاغ عن مشكلة","Señalar un problema","Assinalar um problema"],
    reportTitle:["Что не так с ответом ИИ?","What is wrong with this AI response?","这条 AI 回复有什么问题？","ما المشكلة في رد الذكاء الاصطناعي؟","¿Qué problema tiene esta respuesta de IA?","Qual é o problema desta resposta de IA?"],
    incorrect:["Неточность","Incorrect","不准确","غير صحيح","Incorrecta","Incorreta"],
    irrelevant:["Не по теме","Irrelevant","不相关","غير ذي صلة","No pertinente","Irrelevante"],
    unclear:["Непонятно","Unclear","不清楚","غير واضح","Poco clara","Pouco clara"],
    reportText:["Будет сохранена отметка для этого ответа. Твоя оценка урока не изменится.","A report will be saved for this response. Your lesson grade will not change.","将为此回复保存问题标记，不会改变课程成绩。","سيُحفظ بلاغ عن هذا الرد. لن تتغير درجة الدرس.","Se guardará un aviso sobre esta respuesta. La nota de la lección no cambiará.","Será guardada uma sinalização desta resposta. A nota da lição não muda."],
    reported:["Отметка сохранена","Report saved","已保存反馈","حُفظ البلاغ","Aviso guardado","Sinalização guardada"],
    erase:["Удалить мои данные ИИ","Erase my AI data","删除我的 AI 数据","حذف بيانات الذكاء الاصطناعي الخاصة بي","Borrar mis datos de IA","Apagar os meus dados de IA"],
    eraseTitle:["Удалить все данные ИИ?","Erase all AI data?","删除所有 AI 数据？","حذف كل بيانات الذكاء الاصطناعي؟","¿Borrar todos los datos de IA?","Apagar todos os dados de IA?"],
    eraseText:["Удалятся записи, распознанный текст, разборы и диалоги ИИ в Lexi. Обычные уроки, ответы и повторения сохранятся. Вернуть удалённый разбор не получится.","This removes recordings, transcripts, AI feedback and dialogues from Lexi. Regular lessons, answers and reviews are preserved. Deleted feedback cannot be restored.","这会从 Lexi 删除录音、转写文字、AI 反馈和对话。普通课程、答案与复习记录将保留。已删除的反馈无法恢复。","سيُحذف من Lexi التسجيلات والنصوص وملاحظات الذكاء الاصطناعي والحوارات. تبقى الدروس والإجابات والمراجعات العادية. لا يمكن استعادة الملاحظات المحذوفة.","Se borrarán de Lexi las grabaciones, transcripciones, comentarios y diálogos de IA. Se conservan las lecciones, respuestas y repasos habituales. Los comentarios borrados no se pueden recuperar.","Isto remove da Lexi gravações, transcrições, comentários e diálogos de IA. Mantêm-se as lições, respostas e revisões habituais. Os comentários apagados não podem ser recuperados."],
    erased:["Данные ИИ удалены. Обычный прогресс сохранён. Новая практика будет доступна после следующего урока.","AI data erased. Ordinary progress is preserved. New practice will be available after your next lesson.","AI 数据已删除，普通进度已保留。完成下一课后可开始新的练习。","حُذفت بيانات الذكاء الاصطناعي وحُفظ التقدم العادي. يتاح تدريب جديد بعد الدرس التالي.","Datos de IA borrados. Se conserva el progreso habitual. Habrá nueva práctica tras la próxima lección.","Dados de IA apagados. O progresso habitual foi mantido. Haverá nova prática após a próxima lição."],
    erasing:["Удаляем данные ИИ…","Erasing AI data…","正在删除 AI 数据…","جارٍ حذف بيانات الذكاء الاصطناعي…","Borrando datos de IA…","A apagar dados de IA…"],
    eraseUnknown:["Не удалось подтвердить удаление. Повтори запрос, чтобы завершить его.","Deletion could not be confirmed. Retry the request to finish it.","无法确认是否删除。请重试以完成删除。","تعذّر تأكيد الحذف. أعد الطلب لإتمامه.","No se pudo confirmar el borrado. Repite la solicitud para terminar.","Não foi possível confirmar a eliminação. Repete o pedido para a concluir."],
    retryErase:["Повторить удаление","Retry deletion","重试删除","إعادة محاولة الحذف","Reintentar borrado","Repetir eliminação"],
    contentLanguage:["Язык сохранённого разбора: {language}.","Saved feedback language: {language}.","已保存反馈的语言：{language}。","لغة الملاحظات المحفوظة: {language}.","Idioma de los comentarios guardados: {language}.","Idioma dos comentários guardados: {language}."],
    stale:["Состояние изменилось в другой вкладке. Загружаем сохранённый результат.","State changed in another tab. Loading the saved result.","状态已在另一标签页中改变，正在加载已保存的结果。","تغيّرت الحالة في تبويب آخر. جارٍ تحميل النتيجة المحفوظة.","El estado cambió en otra pestaña. Cargando el resultado guardado.","O estado mudou noutro separador. A carregar o resultado guardado."]
  };
  for(const [key,value] of Object.entries(rows))if(value.length!==6)throw new Error("Incomplete AI locale: "+key);
  const names={ru:"Русский",en:"English",zh:"中文",ar:"العربية",es:"Español",pt:"Português"};
  const app=()=>window.LexiApp;
  const lang=()=>langs.includes(app()?.currentLang?.())?app().currentLang():"en";
  const t=(key,values={})=>Object.entries(values).reduce((out,[k,v])=>out.replaceAll("{"+k+"}",String(v)),rows[key]?.[langs.indexOf(lang())]||key);
  const el=(tag,text,className)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=String(text);if(className)node.className=className;return node;};
  const greek=text=>{const node=el("p",text,"lexi-ai-greek");node.lang="el";node.dir="ltr";return node;};
  const mixed=text=>{const node=el("p",text);node.dir="auto";return node;};
  const activeStatus=job=>job&&["queued","running"].includes(job.status);
  const key="lexi-ai-pending-v1";
  let current=null,epoch=0,uid=0;
  const uuid=()=>crypto.randomUUID?.()||Array.from(crypto.getRandomValues(new Uint8Array(16)),x=>x.toString(16).padStart(2,"0")).join("");
  const valid=(ctx,version=ctx?.epoch)=>Boolean(ctx&&current===ctx&&ctx.epoch===version&&ctx.host.isConnected&&!ctx.paused&&app()?.loggedIn?.()&&ctx.owner===app()?.accountKey?.());
  function button(label,action,id,primary=false){
    const node=el("button",label,"lexi-ai-button"+(primary?" lexi-ai-button-primary":""));node.type="button";
    if(id)node.dataset.aiFocus=id;node.addEventListener("click",()=>{Promise.resolve(action()).catch(()=>{});});return node;
  }
  function persist(ctx){
    try{
      if(ctx?.operation){
        const op=ctx.operation;
        sessionStorage.setItem(key,JSON.stringify({owner:ctx.owner,runId:ctx.runId,operationId:op.id,kind:op.kind,readingId:op.readingId,conversationId:op.conversationId}));
      }else sessionStorage.removeItem(key);
    }catch{}
  }
  function restore(ctx){
    try{
      const saved=JSON.parse(sessionStorage.getItem(key)||"null");
      if(saved?.owner===ctx.owner&&saved.runId===ctx.runId&&typeof saved.operationId==="string"){
        ctx.operation={id:saved.operationId,kind:saved.kind,readingId:saved.readingId,conversationId:saved.conversationId,restored:true};
      }
    }catch{}
  }
  function errorKey(error){
    const code=error?.body?.error||error?.message||"";
    if(error?.status===401||code==="login_required")return "login";
    if(["ai_budget_limit","ai_daily_limit","conversation_attempt_limit"].includes(code))return "limited";
    if(code==="ai_queue_full"||code==="ai_preparation_busy")return "queueFull";
    if(["ai_unavailable","lesson_evidence_unavailable","reading_unavailable","scenario_unavailable","conversation_expired"].includes(code))return "unavailable";
    if(code==="audio_empty"||code==="audio_duration"||code==="asr_empty")return "emptyAudio";
    if(["audio_type","audio_decode","audio_decoder_unavailable"].includes(code))return "unsupported";
    if(error?.name==="AbortError"||error instanceof TypeError||!error?.status)return "network";
    return "failed";
  }
  async function request(ctx,path,body,raw){
    const version=ctx.epoch,controller=new AbortController();
    ctx.controllers.add(controller);
    const timeout=setTimeout(()=>controller.abort(),15000);
    try{
      let result;
      if(raw){
        const response=await fetch("/greek/api/"+path,{method:"POST",credentials:"same-origin",cache:"no-store",signal:controller.signal,headers:{"Content-Type":raw.type.split(";")[0],"X-Lexi-Owner":ctx.owner},body:raw});
        if(!response.ok){let data={};try{data=await response.json();}catch{}const e=new Error(data.error||"audio_request_failed");e.status=response.status;e.body=data;throw e;}
        result=await response.json();
      }else result=await app().api(path,{signal:controller.signal,...(body!==undefined?{method:"POST",headers:{"Content-Type":"application/json","X-Lexi-Owner":ctx.owner},body:JSON.stringify(body)}:{})});
      if(!valid(ctx,version)){const e=new Error("inactive");e.name="AbortError";throw e;}
      return result;
    }catch(error){
      if(error?.status===409&&(error.body?.error||error.message)==="account_changed"&&current===ctx){
        destroy(true);
        Promise.resolve(app()?.reconcileAccount?.()).catch(()=>{});
      }
      throw error;
    }finally{clearTimeout(timeout);ctx.controllers.delete(controller);}
  }

  function stopMedia(ctx){
    ctx.mediaEpoch++;
    const media=ctx.media;ctx.media=null;
    if(media){
      clearInterval(media.timer);
      if(media.recorder?.state==="recording")try{media.recorder.stop();}catch{}
      media.stream?.getTracks().forEach(track=>track.stop());
      if(media.url)URL.revokeObjectURL(media.url);
      media.blob=null;
    }
    ctx.host.querySelectorAll("audio").forEach(audio=>{audio.pause();audio.removeAttribute("src");audio.load();});
  }
  function stopAsync(ctx){
    for(const watch of ctx.watches.values())clearTimeout(watch.timer);
    ctx.watches.clear();
    for(const controller of ctx.controllers)controller.abort();
    ctx.controllers.clear();
    if(ctx.dialog?.open)ctx.dialog.close();
  }
  function suspend(ctx){
    if(!ctx||ctx.paused)return;
    ctx.epoch=++epoch;ctx.paused=true;ctx.posting=false;
    stopMedia(ctx);stopAsync(ctx);
    if(ctx.operation){ctx.operation.raw=null;ctx.operation.body=null;ctx.operation.lostPayload=true;persist(ctx);}
    ctx.notice="stopped";render(ctx);
  }
  function destroy(clear=false){
    const ctx=current;if(!ctx)return;
    suspend(ctx);ctx.edit=null;ctx.typedText="";ctx.operation=null;
    if(clear){try{sessionStorage.removeItem(key);}catch{}ctx.host.replaceChildren();ctx.host.hidden=true;}
    current=null;
  }
  async function confirmDialog(ctx,{title,message,confirmLabel,choices,destructive=false,policy=false}){
    if(!valid(ctx)||ctx.dialog)return false;
    const previous=document.activeElement,dialog=el("dialog",undefined,"lexi-ai-dialog");
    const heading=el("h2",title);heading.id="lexi-ai-dialog-"+(++uid);dialog.setAttribute("aria-labelledby",heading.id);
    const description=el("p",message);description.id=heading.id+"-description";dialog.setAttribute("aria-describedby",description.id);
    dialog.dir=lang()==="ar"?"rtl":"ltr";dialog.lang=lang();dialog.append(heading,description);
    if(policy)dialog.append(providerLink());
    let select;
    if(choices){
      const label=el("label",t("reportTitle"));select=el("select");select.id=heading.id+"-reason";label.htmlFor=select.id;
      for(const [value,text] of choices){const option=el("option",text);option.value=value;select.append(option);}
      dialog.append(label,select);
    }
    const actions=el("div",undefined,"lexi-ai-actions");
    const cancel=button(t("cancel"),()=>dialog.close(""),"dialog-cancel");
    const confirm=button(confirmLabel,()=>dialog.close(select?.value||"yes"),"dialog-confirm",!destructive);
    if(destructive)confirm.classList.add("lexi-ai-destructive");
    actions.append(cancel,confirm);dialog.append(actions);document.body.append(dialog);ctx.dialog=dialog;
    dialog.addEventListener("keydown",event=>{
      if(event.key!=="Tab")return;
      const focusable=[...dialog.querySelectorAll("a[href],button,select,textarea,input")].filter(node=>!node.disabled&&!node.hidden);
      const first=focusable[0],last=focusable.at(-1);
      if(event.shiftKey&&(document.activeElement===first||!focusable.includes(document.activeElement))){event.preventDefault();last?.focus();}
      else if(!event.shiftKey&&(document.activeElement===last||!focusable.includes(document.activeElement))){event.preventDefault();first?.focus();}
    });
    return await new Promise(resolve=>{
      dialog.addEventListener("close",()=>{
        const value=dialog.returnValue;ctx.dialog=null;dialog.remove();
        if(previous?.isConnected&&!previous.closest("[hidden]")&&valid(ctx))previous.focus();
        resolve(value||false);
      },{once:true});
      try{dialog.showModal();cancel.focus();}catch{ctx.dialog=null;dialog.remove();resolve(false);}
    });
  }
  function providerLink(){
    const link=el("a",t("providerLink"));link.href="https://developers.openai.com/api/docs/guides/your-data";
    link.target="_blank";link.rel="noopener noreferrer";return link;
  }
  async function consent(ctx,kind){
    if(ctx.consents.has(kind))return true;
    const accepted=await confirmDialog(ctx,{title:t("consentTitle"),message:t("privacyText",{days:ctx.caps.textRetentionDays,hours:ctx.caps.audioRetentionHours})+" "+t("providerPolicy")+" "+t("consentText"),confirmLabel:t("agree"),policy:true});
    if(accepted&&valid(ctx)){ctx.consents.add(kind);return true;}
    return false;
  }
  const busy=ctx=>Boolean(ctx.posting||ctx.operation||ctx.needsConversationRefresh||ctx.media?.phase==="permission"||ctx.media?.phase==="recording"||activeStatus(ctx.dialogueJob)||activeStatus(ctx.summary)||[...ctx.readingJobs.values()].some(activeStatus));
  function jobForReading(ctx){return ctx.readingJobs.get(ctx.readingId);}
  function rememberConversation(ctx,conversation,select=true){
    if(select)ctx.conversation=conversation;
    const list=ctx.options.conversations||[];
    ctx.options.conversations=[conversation,...list.filter(x=>x.id!==conversation.id)];
  }
  async function refreshConversation(ctx,id=ctx.conversation?.id){
    if(!id)return;
    const version=ctx.epoch,selected=ctx.conversation?.id===id;
    if(selected){ctx.needsConversationRefresh=true;render(ctx);}
    try{
      const value=await request(ctx,"ai/conversations/"+encodeURIComponent(id));
      if(valid(ctx,version)){
        const stillSelected=selected&&ctx.conversation?.id===id;
        rememberConversation(ctx,value,stillSelected);
        if(stillSelected)ctx.needsConversationRefresh=false;
        render(ctx);
      }
    }catch(error){
      if(valid(ctx,version)&&selected&&ctx.conversation?.id===id){ctx.error=errorKey(error);ctx.needsConversationRefresh=true;render(ctx);}
    }
  }
  async function adopt(ctx,value,meta={}){
    if(!valid(ctx))return;
    if(Array.isArray(value.history)&&typeof value.targetTurns==="number"){
      // A restored creation may select its own conversation; a delayed response
      // must never replace a different conversation selected in the meantime.
      if(ctx.conversation&&ctx.conversation.id!==value.id){rememberConversation(ctx,value,false);render(ctx);return;}
      rememberConversation(ctx,value);ctx.mode="dialogue";ctx.typedText="";ctx.dialogueJob=null;
      if(value.pendingJob){
        try{await adopt(ctx,await request(ctx,"ai/jobs/"+encodeURIComponent(value.pendingJob)),{conversationId:value.id});}
        catch(error){if(valid(ctx)){ctx.error=errorKey(error);render(ctx);}}
      }else render(ctx,true);
      return;
    }
    if(value.kind==="summary")ctx.summary=value;
    else if(value.kind==="reading"){
      const readingId=meta.readingId||value.readingId||value.result?.readingId||
        [...ctx.readingJobs.entries()].find(([,job])=>job.id===value.id)?.[0]||ctx.readingId;
      ctx.readingJobs.set(readingId,value);
    }else if(value.kind==="dialogue"||value.kind==="dialogue_edit"){
      const conversationId=value.conversationId||meta.conversationId;
      if(!ctx.conversation&&meta.restored){
        const saved=ctx.options.conversations.find(x=>x.id===conversationId);
        if(saved){rememberConversation(ctx,saved);ctx.mode="dialogue";}
      }
      if(ctx.conversation?.id===conversationId)ctx.dialogueJob=value;
      if(!activeStatus(value)){
        await refreshConversation(ctx,conversationId);
        if(!valid(ctx))return;
        if(ctx.conversation?.id===conversationId&&ctx.dialogueJob?.id===value.id){
          if(value.result?.status==="recognition_uncertain"){
            ctx.notice="uncertain";ctx.typedText=value.result.transcript||"";
          }else if(value.status==="succeeded"){ctx.typedText="";ctx.notice=null;ctx.edit=null;}
        }
      }
    }
    render(ctx);
    if(activeStatus(value))watchJob(ctx,value,meta);
    else {
      const watch=ctx.watches.get(value.id);if(watch)clearTimeout(watch.timer);
      ctx.watches.delete(value.id);
    }
  }
  function watchJob(ctx,job,meta={},count=0){
    if(!valid(ctx)||!activeStatus(job)||ctx.watches.has(job.id))return;
    if(count>=30){ctx.pollPaused.add(job.id);render(ctx);return;}
    const version=ctx.epoch;
    const watch={timer:setTimeout(async()=>{
      ctx.watches.delete(job.id);
      if(!valid(ctx,version)||document.hidden)return;
      try{
        const updated=await request(ctx,"ai/jobs/"+encodeURIComponent(job.id));
        if(!valid(ctx,version))return;
        // Adopt without recursively resetting the bounded poll count.
        if(updated.kind==="summary")ctx.summary=updated;
        else if(updated.kind==="reading")ctx.readingJobs.set(meta.readingId||updated.readingId||updated.result?.readingId||ctx.readingId,updated);
        else if(ctx.conversation?.id===(updated.conversationId||meta.conversationId))ctx.dialogueJob=updated;
        if(activeStatus(updated)){render(ctx);watchJob(ctx,updated,meta,count+1);}
        else await adopt(ctx,updated,meta);
      }catch(error){if(valid(ctx,version)){ctx.pollPaused.add(job.id);ctx.error=errorKey(error);render(ctx);}}
    },2000)};
    ctx.watches.set(job.id,watch);
  }
  async function checkJob(ctx,job,meta={}){
    if(!valid(ctx))return;
    ctx.error=null;ctx.pollPaused.delete(job.id);
    const watch=ctx.watches.get(job.id);if(watch)clearTimeout(watch.timer);ctx.watches.delete(job.id);
    try{await adopt(ctx,await request(ctx,"ai/jobs/"+encodeURIComponent(job.id)),meta);}
    catch(error){if(valid(ctx)){ctx.error=errorKey(error);render(ctx);}}
  }
  async function cancelJob(ctx,job,meta={}){
    if(!valid(ctx)||ctx.posting)return;
    ctx.posting=true;render(ctx);
    try{await adopt(ctx,await request(ctx,"ai/jobs/"+encodeURIComponent(job.id)+"/cancel",{}),meta);}
    catch(error){if(valid(ctx)){ctx.error=errorKey(error);}}
    finally{if(valid(ctx)){ctx.posting=false;render(ctx);}}
  }
  async function sendOperation(ctx,operation){
    if(!valid(ctx)||ctx.posting)return;
    const version=ctx.epoch;
    ctx.operation=operation;ctx.posting=true;ctx.error=null;ctx.notice=null;persist(ctx);render(ctx);
    try{
      const value=await request(ctx,operation.path,operation.body,operation.raw);
      if(!valid(ctx,version))return;
      ctx.operation=null;persist(ctx);ctx.posting=false;ctx.edit=null;stopMedia(ctx);
      await adopt(ctx,value,operation);
    }catch(error){
      if(!valid(ctx,version))return;
      const known=error.status>=400&&error.status<500&&error.status!==408;
      if(error.status===429&&(error.body?.error||error.message)==="ai_preparation_busy"){
        // Admission rejected before reading the audio. Keep this exact clip
        // and operation ID for an explicit status-checked retry.
        operation.checkedMissing=true;ctx.error="queueFull";
      }else if(known){
        ctx.operation=null;persist(ctx);ctx.error=errorKey(error);
        if(error.status===409&&ctx.conversation){ctx.notice="stale";await refreshConversation(ctx);}
      }else ctx.notice="unknown";
    }finally{if(valid(ctx,version)){ctx.posting=false;render(ctx);}}
  }
  function operation(ctx,kind,path,body,raw,meta={}){
    const id=uuid();
    return {id,kind,path:raw?path+(path.includes("?")?"&":"?")+"operationId="+encodeURIComponent(id):path,
      body:body===undefined?undefined:{...body,operationId:id},raw,...meta};
  }
  async function recover(ctx,resend=false){
    const op=ctx.operation;if(!op||ctx.posting||!valid(ctx))return;
    const version=ctx.epoch;ctx.posting=true;ctx.error=null;render(ctx);
    try{
      const result=await request(ctx,"ai/operations/"+encodeURIComponent(op.id));
      if(!valid(ctx,version))return;
      ctx.operation=null;persist(ctx);ctx.posting=false;stopMedia(ctx);ctx.notice=null;
      await adopt(ctx,result,op);
    }catch(error){
      if(!valid(ctx,version))return;
      if(error.status===404){
        op.checkedMissing=true;ctx.notice=op.lostPayload||op.restored?"lostRecording":"missingOperation";
        if(resend&&!op.lostPayload&&!op.restored&&op.path){ctx.posting=false;await sendOperation(ctx,op);}
      }else {ctx.error=errorKey(error);ctx.notice="unknown";}
    }finally{if(valid(ctx,version)){ctx.posting=false;render(ctx);}}
  }
  async function reload(ctx){
    if(!valid(ctx))return;
    const version=ctx.epoch;
    try{
      const options=await request(ctx,"ai/options?"+new URLSearchParams({runId:ctx.runId,lang:ctx.contentLang}));
      if(!valid(ctx,version))return;
      ctx.options=options;ctx.ready=true;ctx.error=null;
      ctx.summary=options.existingSummary||null;
      ctx.readingJobs=new Map((options.readingJobs||[]).map(job=>[job.readingId,job]));
      if(!options.readings.some(x=>x.id===ctx.readingId))ctx.readingId=options.readings[0]?.id||null;
      if(ctx.conversation)ctx.conversation=options.conversations.find(x=>x.id===ctx.conversation.id)||null;
      render(ctx);
      if(activeStatus(ctx.summary))watchJob(ctx,ctx.summary);
      for(const [readingId,job] of ctx.readingJobs)if(activeStatus(job))watchJob(ctx,job,{readingId});
      if(ctx.operation)await recover(ctx);
      else if(ctx.conversation?.pendingJob)await adopt(ctx,await request(ctx,"ai/jobs/"+encodeURIComponent(ctx.conversation.pendingJob)),{conversationId:ctx.conversation.id});
    }catch(error){if(valid(ctx,version)){ctx.error=errorKey(error);ctx.ready=true;render(ctx);}}
  }

  function supportedMime(){
    if(typeof MediaRecorder==="undefined"||!navigator.mediaDevices?.getUserMedia)return null;
    return ["audio/webm;codecs=opus","audio/ogg;codecs=opus","audio/mp4","audio/webm","audio/ogg"]
      .find(mime=>MediaRecorder.isTypeSupported?.(mime))||null;
  }
  async function startRecording(ctx,kind){
    if(!valid(ctx)||busy(ctx))return;
    stopMedia(ctx);ctx.edit=null;ctx.error=null;ctx.notice=null;
    const mime=supportedMime();
    if(!mime||!ctx.caps.audioDecoder){ctx.notice="unsupported";ctx.typed=true;render(ctx);return;}
    const version=ctx.epoch,mediaVersion=ctx.mediaEpoch;
    const limit=Math.min(kind==="reading"?90:45,Number(ctx.caps.limits?.[kind+"Seconds"])||(kind==="reading"?90:45));
    const media={kind,phase:"permission",limit,stream:null,recorder:null,chunks:[],blob:null,url:null,timer:null};
    ctx.media=media;render(ctx);
    try{
      const stream=await navigator.mediaDevices.getUserMedia({audio:true});
      if(!valid(ctx,version)||ctx.mediaEpoch!==mediaVersion){stream.getTracks().forEach(track=>track.stop());return;}
      media.stream=stream;
      const recorder=new MediaRecorder(stream,{mimeType:mime});media.recorder=recorder;media.bytes=0;
      recorder.addEventListener("dataavailable",event=>{
        if(event.data.size){media.chunks.push(event.data);media.bytes+=event.data.size;}
        if(media.bytes>(ctx.caps.limits?.uploadBytes||8*1024*1024)&&recorder.state==="recording")recorder.stop();
      });
      recorder.addEventListener("error",()=>{
        if(valid(ctx,version)){stopMedia(ctx);ctx.error="failed";render(ctx);}
        else stream.getTracks().forEach(track=>track.stop());
      });
      recorder.addEventListener("stop",()=>{
        clearInterval(media.timer);stream.getTracks().forEach(track=>track.stop());media.stream=null;
        if(!valid(ctx,version)||ctx.mediaEpoch!==mediaVersion){media.chunks=[];return;}
        const type=recorder.mimeType||mime;
        media.blob=new Blob(media.chunks,{type});media.chunks=[];
        if(!media.blob.size||media.bytes>(ctx.caps.limits?.uploadBytes||8*1024*1024)){stopMedia(ctx);ctx.error="emptyAudio";render(ctx);return;}
        media.url=URL.createObjectURL(media.blob);media.phase="preview";render(ctx,true);
      });
      recorder.start(250);media.started=Date.now();media.phase="recording";render(ctx,true);
      media.timer=setInterval(()=>{
        const elapsed=Math.min(limit,Math.floor((Date.now()-media.started)/1000));
        ctx.host.querySelector("[data-ai-timer]")?.replaceChildren(document.createTextNode(elapsed+" / "+limit+" s"));
        if(!valid(ctx,version)||document.hidden){suspend(ctx);return;}
        if(elapsed>=limit&&recorder.state==="recording")recorder.stop();
      },250);
    }catch(error){
      if(!valid(ctx,version)||ctx.mediaEpoch!==mediaVersion)return;
      stopMedia(ctx);ctx.error=["NotAllowedError","SecurityError"].includes(error.name)?"permissionDenied":"unsupported";
      if(kind==="dialogue")ctx.typed=true;render(ctx);
    }
  }
  function stopRecording(ctx){
    if(ctx.media?.recorder?.state==="recording"){
      ctx.media.phase="stopping";ctx.media.recorder.stop();render(ctx);
    }
  }
  async function sendAudio(ctx){
    if(!valid(ctx)||busy(ctx)||ctx.media?.phase!=="preview")return;
    const media=ctx.media;
    if(!await consent(ctx,"audio")||!valid(ctx)||ctx.media!==media)return;
    const params=new URLSearchParams({kind:media.kind,runId:ctx.runId,lang:ctx.contentLang});
    const meta={};
    if(media.kind==="reading"){params.set("readingId",ctx.readingId);meta.readingId=ctx.readingId;}
    else{
      if(!ctx.conversation||ctx.conversation.status!=="active")return;
      params.set("conversationId",ctx.conversation.id);params.set("revision",ctx.conversation.revision);meta.conversationId=ctx.conversation.id;
    }
    await sendOperation(ctx,operation(ctx,media.kind,"ai/audio?"+params,undefined,media.blob,meta));
  }
  async function createSummary(ctx){
    if(busy(ctx)||!await consent(ctx,"summary")||!valid(ctx))return;
    await sendOperation(ctx,operation(ctx,"summary","ai/summary",{runId:ctx.runId,lang:ctx.contentLang}));
  }
  async function startDialogue(ctx){
    if(busy(ctx)||!valid(ctx))return;
    const scenarios=ctx.options.dialogues||[],turns=ctx.options.dialogueTurns||ctx.caps.limits?.dialogueTurns||[4,5];
    const scenarioId=ctx.scenarioId||scenarios[0]?.id,number=ctx.turns||turns[0];
    if(!scenarioId||![4,5].includes(number))return;
    await sendOperation(ctx,operation(ctx,"conversation","ai/conversations",{runId:ctx.runId,lang:ctx.contentLang,scenarioId,turns:number}));
  }
  async function sendTyped(ctx){
    if(busy(ctx)||!ctx.typedText?.trim()||!ctx.conversation||!await consent(ctx,"text")||!valid(ctx))return;
    const conversation=ctx.conversation;
    await sendOperation(ctx,operation(ctx,"dialogue","ai/conversations/"+encodeURIComponent(conversation.id)+"/text",
      {revision:conversation.revision,transcript:ctx.typedText.trim()},undefined,{conversationId:conversation.id}));
  }
  async function editTranscript(ctx){
    const edit=ctx.edit;
    if(busy(ctx)||!edit?.text?.trim()||!valid(ctx))return;
    if(edit.kind!=="reading"&&!await consent(ctx,"text"))return;
    if(!valid(ctx))return;
    const revision=edit.kind==="reading"?edit.revision:ctx.conversation?.revision;
    await sendOperation(ctx,operation(ctx,edit.kind==="reading"?"reading":"dialogue_edit",
      "ai/jobs/"+encodeURIComponent(edit.jobId)+"/transcript",
      {transcript:edit.text.trim(),revision},undefined,{readingId:edit.readingId,conversationId:ctx.conversation?.id}));
  }
  async function finishDialogue(ctx){
    if(!ctx.conversation||ctx.posting||ctx.operation||!valid(ctx))return;
    stopMedia(ctx);ctx.posting=true;ctx.error=null;render(ctx);
    try{
      const result=await request(ctx,"ai/conversations/"+encodeURIComponent(ctx.conversation.id)+"/finish",{revision:ctx.conversation.revision});
      if(!valid(ctx))return;
      rememberConversation(ctx,result);ctx.dialogueJob=null;ctx.edit=null;ctx.notice=null;
    }catch(error){
      if(valid(ctx)){ctx.error=errorKey(error);ctx.needsConversationRefresh=true;await refreshConversation(ctx);}
    }finally{if(valid(ctx)){ctx.posting=false;render(ctx);}}
  }
  async function report(ctx,job){
    if(!valid(ctx)||ctx.posting||job.reported)return;
    const reason=await confirmDialog(ctx,{title:t("reportTitle"),message:t("reportText"),confirmLabel:t("report"),
      choices:["incorrect","irrelevant","unclear"].map(k=>[k,t(k)])});
    if(!reason||!valid(ctx))return;
    try{await request(ctx,"ai/jobs/"+encodeURIComponent(job.id)+"/report",{reason});job.reported=true;ctx.reported.add(job.id);render(ctx);}
    catch(error){if(valid(ctx)){ctx.error=errorKey(error);render(ctx);}}
  }
  async function erase(ctx,retry=false){
    if(!valid(ctx)||ctx.posting)return;
    if(!retry&&!await confirmDialog(ctx,{title:t("eraseTitle"),message:t("eraseText"),confirmLabel:t("erase"),destructive:true}))return;
    if(!valid(ctx))return;
    stopMedia(ctx);stopAsync(ctx);ctx.epoch=++epoch;ctx.operation=null;persist(ctx);
    ctx.erasing="pending";ctx.posting=true;ctx.edit=null;ctx.typedText="";render(ctx);
    try{
      const value=await request(ctx,"ai/erase",{confirm:true});
      if(!valid(ctx))return;
      if(value.deleted){ctx.erasing=null;ctx.erased=true;ctx.summary=null;ctx.dialogueJob=null;ctx.conversation=null;ctx.readingJobs.clear();ctx.options={readings:[],dialogues:[],conversations:[]};}
      else ctx.erasing="unknown";
    }catch{if(valid(ctx))ctx.erasing="unknown";}
    finally{if(valid(ctx)){ctx.posting=false;render(ctx);}}
  }
  function changeMode(ctx,mode){
    if(!valid(ctx))return;
    stopMedia(ctx);ctx.edit=null;ctx.mode=mode;ctx.error=null;ctx.notice=null;render(ctx,true);
  }
  function field(label,id,value,onInput){
    const group=el("div",undefined,"lexi-ai-field"),caption=el("label",label),input=el("textarea");
    caption.htmlFor=id;input.id=id;input.value=value||"";input.lang="el";input.dir="ltr";input.maxLength=2000;input.rows=3;
    input.dataset.aiFocus=id;input.addEventListener("input",()=>onInput(input.value));group.append(caption,input);return group;
  }
  function controls(ctx,kind){
    const wrap=el("div",undefined,"lexi-ai-recorder"),media=ctx.media?.kind===kind?ctx.media:null;
    wrap.append(el("p",t("localOnly"),"lexi-ai-muted"));
    if(media?.phase==="permission"){
      const status=el("p",t("permission"),"lexi-ai-status");status.setAttribute("role","status");wrap.append(status);
      wrap.append(button(t("cancel"),()=>{stopMedia(ctx);render(ctx);},"cancel-permission"));return wrap;
    }
    if(media?.phase==="recording"||media?.phase==="stopping"){
      const status=el("p",t("recording"),"lexi-ai-recording");status.setAttribute("role","status");
      const timer=el("span","0 / "+media.limit+" s","lexi-ai-timer");timer.dataset.aiTimer="";timer.dir="ltr";
      const stop=button(t("stop"),()=>stopRecording(ctx),"stop-recording",true);stop.disabled=media.phase!=="recording";
      wrap.append(status,timer,stop);return wrap;
    }
    if(media?.phase==="preview"){
      const audio=document.createElement("audio");audio.controls=true;audio.preload="metadata";audio.src=media.url;audio.setAttribute("aria-label",t("preview"));
      wrap.append(el("p",t("preview")),audio);
      const actions=el("div",undefined,"lexi-ai-actions"),again=button(t("rerecord"),()=>startRecording(ctx,kind),"rerecord");
      const send=button(t("sendAudio"),()=>sendAudio(ctx),"send-audio",true);
      again.disabled=send.disabled=busy(ctx);actions.append(again,send);wrap.append(actions);return wrap;
    }
    const supported=supportedMime()&&ctx.caps.audioDecoder;
    if(!supported){wrap.append(el("p",t("unsupported"),"lexi-ai-muted"));return wrap;}
    const record=button(t("record"),()=>startRecording(ctx,kind),"record-"+kind,true);record.disabled=busy(ctx);
    wrap.append(record,el("p",t("audioLimit",{seconds:kind==="reading"?90:45}),"lexi-ai-muted"));
    return wrap;
  }
  function jobStatus(ctx,job,meta={}){
    const box=el("div",undefined,"lexi-ai-job");
    if(!job)return box;
    if(activeStatus(job)){
      const label=ctx.pollPaused.has(job.id)?"pollPaused":job.result?.stage==="interpreting"?"interpreting":job.status;
      const status=el("p",t(label),"lexi-ai-status");status.setAttribute("role","status");box.append(status);
      const actions=el("div",undefined,"lexi-ai-actions");
      if(ctx.pollPaused.has(job.id))actions.append(button(t("checkStatus"),()=>checkJob(ctx,job,meta),"check-"+job.id));
      const cancel=button(t("cancelJob"),()=>cancelJob(ctx,job,meta),"cancel-"+job.id);cancel.disabled=ctx.posting;actions.append(cancel);box.append(actions);
    }else if(job.status!=="succeeded"){
      const message=job.status==="unknown"?"unknown":job.status==="cancelled"?"cancelled":job.status==="deleted"?"unavailable":errorKey({message:job.error,status:503});
      box.append(el("p",t(message),"lexi-ai-muted"));
      if(job.status==="unknown")box.append(button(t("checkStatus"),()=>checkJob(ctx,job,meta),"check-"+job.id));
    }
    return box;
  }
  function reporting(ctx,job){
    const wrap=el("div",undefined,"lexi-ai-report");
    if(job.reported||ctx.reported.has(job.id))wrap.append(el("span",t("reported"),"lexi-ai-muted"));
    else wrap.append(button(t("report"),()=>report(ctx,job),"report-"+job.id));
    return wrap;
  }
  function editor(ctx){
    const edit=ctx.edit;if(!edit)return null;
    const box=el("section",undefined,"lexi-ai-editor");box.append(el("p",t("edited"),"lexi-ai-muted"));
    box.append(field(t("editTranscript"),"ai-transcript-edit",edit.text,value=>{edit.text=value;box.querySelector("[data-ai-focus='save-transcript']").disabled=!value.trim()||busy(ctx);}));
    const actions=el("div",undefined,"lexi-ai-actions"),save=button(t("saveTranscript"),()=>editTranscript(ctx),"save-transcript",true);
    save.disabled=busy(ctx)||!edit.text?.trim();
    actions.append(save,button(t("cancel"),()=>{ctx.edit=null;render(ctx);},"cancel-edit"));box.append(actions);return box;
  }

  function summaryPanel(ctx){
    const panel=el("section",undefined,"lexi-ai-section");panel.append(el("h3",t("summary")));
    const job=ctx.summary;
    if(!job){
      const create=button(t("createSummary"),()=>createSummary(ctx),"create-summary");create.disabled=busy(ctx);panel.append(create);return panel;
    }
    panel.append(jobStatus(ctx,job));
    if(job.status!=="succeeded"||!job.result)return panel;
    const result=job.result;
    if(result.evidenceComplete===false)panel.append(el("p",t("partialEvidence"),"lexi-ai-notice"));
    const claim=(value,title)=>{
      const section=el("div",undefined,"lexi-ai-claim");section.append(el("h4",title),mixed(value?.text||""));
      if(value?.example){section.append(el("span",t("example"),"lexi-ai-label"));const quote=el("blockquote",value.example);quote.dir="auto";section.append(quote);}
      return section;
    };
    panel.append(claim(result.observation,t("observation")));
    if(Array.isArray(result.improvements)&&result.improvements.length){
      panel.append(el("h4",t("improvements")));
      for(const item of result.improvements.slice(0,2)){
        const box=el("div",undefined,"lexi-ai-claim");box.append(mixed(item.text));
        if(item.example){box.append(el("span",t("example"),"lexi-ai-label"));const quote=el("blockquote",item.example);quote.dir="auto";box.append(quote);}
        panel.append(box);
      }
    }
    if(result.nextStep)panel.append(el("h4",t("nextStep")),mixed(result.nextStep));
    if(result.targetCardId&&app()?.routeToExistingReview){
      panel.append(button(t("existingReview"),()=>{stopMedia(ctx);app().routeToExistingReview(result.targetCardId);},"existing-review"));
      panel.append(el("p",t("reviewNote"),"lexi-ai-muted"));
    }
    panel.append(el("p",t("advisory"),"lexi-ai-muted"),reporting(ctx,job));return panel;
  }
  function readingPanel(ctx){
    const panel=el("section",undefined,"lexi-ai-section"),readings=ctx.options.readings||[];
    panel.append(el("h3",t("reading")),el("p",t("contentOnly"),"lexi-ai-notice"));
    if(!readings.length){panel.append(el("p",t("noReadings")));return panel;}
    const group=el("div",undefined,"lexi-ai-field"),label=el("label",t("chooseReading")),select=el("select");
    select.id="ai-reading-select";label.htmlFor=select.id;select.dataset.aiFocus="reading-select";select.disabled=busy(ctx);
    readings.forEach((reading,index)=>{
      const option=el("option",t("textNumber",{n:index+1,chapter:reading.chapter}));option.value=reading.id;select.append(option);
    });
    select.value=ctx.readingId;
    select.addEventListener("change",()=>{stopMedia(ctx);ctx.readingId=select.value;ctx.edit=null;ctx.focusPhrase=null;ctx.error=null;ctx.notice=null;render(ctx);});
    group.append(label,select);panel.append(group);
    const reading=readings.find(x=>x.id===ctx.readingId)||readings[0];
    panel.append(greek(reading.text));
    if(ctx.focusPhrase){panel.append(el("p",t("focusPhrase"),"lexi-ai-muted"));const focus=greek(ctx.focusPhrase);focus.classList.add("lexi-ai-focus-phrase");panel.append(focus);}
    const job=jobForReading(ctx);
    if(job)panel.append(jobStatus(ctx,job,{readingId:reading.id}));
    if(job?.status==="succeeded"&&job.result){
      const result=job.result,feedback=el("section",undefined,"lexi-ai-feedback");
      feedback.append(el("h4",t("transcript")),greek(result.transcript||""));
      if(result.edited)feedback.append(el("p",t("edited"),"lexi-ai-notice"));
      if(result.originalTranscript!==undefined){
        const details=el("details"),summary=el("summary",t("originalTranscript"));details.append(summary,greek(result.originalTranscript));feedback.append(details);
      }
      if(result.matchingContent)feedback.append(el("p",t("sameContent"),"lexi-ai-positive"));
      else{
        feedback.append(el("h4",t("differences")),el("p",t("asrCaution"),"lexi-ai-muted"));
        for(const difference of (result.comparison||[]).slice(0,2)){
          const box=el("div",undefined,"lexi-ai-comparison");
          box.append(el("span",t("reference"),"lexi-ai-label"),difference.expected?greek(difference.expected):el("p",t("noWords")));
          box.append(el("span",t("recognized"),"lexi-ai-label"),difference.recognized?greek(difference.recognized):el("p",t("noWords")));
          if(difference.expected)box.append(button(t("repeatPhrase"),()=>{stopMedia(ctx);ctx.focusPhrase=difference.expected;ctx.edit=null;render(ctx,true);},"phrase-"+(++uid)));
          feedback.append(box);
        }
        if(result.hasMoreDifferences)feedback.append(el("p",t("moreDifferences"),"lexi-ai-muted"));
      }
      const edit=button(t("editTranscript"),()=>{stopMedia(ctx);ctx.edit={kind:"reading",jobId:job.id,readingId:reading.id,revision:result.revision||0,text:result.transcript||""};render(ctx,true);},"edit-reading");
      edit.disabled=busy(ctx);feedback.append(edit,reporting(ctx,job));panel.append(feedback);
    }
    if(ctx.edit?.kind==="reading")panel.append(editor(ctx));else panel.append(controls(ctx,"reading"));
    return panel;
  }
  function dialogueSetup(ctx){
    const panel=el("section",undefined,"lexi-ai-section");panel.append(el("h3",t("dialogue")));
    const saved=(ctx.options.conversations||[]).filter(x=>x.status!=="deleted");
    if(saved.length){
      panel.append(el("h4",t("savedConversations")));
      const list=el("div",undefined,"lexi-ai-saved");
      for(const conversation of saved){
        const label=t(conversation.status==="active"?"resumeDialogue":"viewDialogue")+" · "+t("turnProgress",{count:conversation.turnCount,total:conversation.targetTurns});
        const select=button(label,async()=>{
          if(!valid(ctx)||busy(ctx))return;
          stopMedia(ctx);ctx.conversation=conversation;ctx.mode="dialogue";ctx.dialogueJob=null;ctx.edit=null;ctx.notice=null;ctx.typedText="";
          await refreshConversation(ctx);
          if(!valid(ctx)||ctx.conversation?.id!==conversation.id)return;
          if(ctx.conversation.pendingJob)await checkJob(ctx,{id:ctx.conversation.pendingJob},{conversationId:conversation.id});
          render(ctx,true);
        },"saved-"+conversation.id);
        select.disabled=busy(ctx);list.append(select);
      }
      panel.append(list);
    }
    const scenarios=ctx.options.dialogues||[],turns=ctx.options.dialogueTurns||ctx.caps.limits?.dialogueTurns||[4,5];
    if(!scenarios.length||!turns.length){panel.append(el("p",t("noDialogue"),"lexi-ai-muted"));return panel;}
    const fields=el("div",undefined,"lexi-ai-setup");
    const scenarioLabel=el("label",t("scenario")),scenario=el("select");scenario.id="ai-scenario";scenarioLabel.htmlFor=scenario.id;
    scenario.lang="el";scenario.dir="ltr";scenario.dataset.aiFocus="scenario";
    for(const value of scenarios){const option=el("option",value.firstQuestion);option.value=value.id;scenario.append(option);}
    scenario.value=ctx.scenarioId||scenarios[0].id;ctx.scenarioId=scenario.value;scenario.disabled=busy(ctx);
    scenario.addEventListener("change",()=>{ctx.scenarioId=scenario.value;});
    const turnLabel=el("label",t("turns")),number=el("select");number.id="ai-turns";turnLabel.htmlFor=number.id;number.dataset.aiFocus="turns";
    for(const value of turns.filter(x=>x===4||x===5)){const option=el("option",value);option.value=value;number.append(option);}
    number.value=String(turns.includes(ctx.turns)?ctx.turns:turns[0]);ctx.turns=Number(number.value);number.disabled=busy(ctx);
    number.addEventListener("change",()=>{ctx.turns=Number(number.value);});fields.append(scenarioLabel,scenario,turnLabel,number);panel.append(fields);
    const start=button(t("startDialogue"),()=>startDialogue(ctx),"start-dialogue",true);start.disabled=busy(ctx);panel.append(start);
    return panel;
  }
  function dialoguePanel(ctx){
    const conversation=ctx.conversation;
    if(!conversation)return dialogueSetup(ctx);
    const panel=el("section",undefined,"lexi-ai-section");
    panel.append(el("h3",t("dialogue")),el("p",t("turnProgress",{count:conversation.turnCount,total:conversation.targetTurns}),"lexi-ai-progress"));
    const history=conversation.history||[];
    for(const [index,turn] of history.entries()){
      const item=el("details",undefined,"lexi-ai-turn");item.open=index===history.length-1;
      item.append(el("summary",t("yourAnswer")+" "+turn.ordinal));
      item.append(el("span",t("question"),"lexi-ai-label"),greek(turn.question?.text||""));
      item.append(el("span",t("yourAnswer"),"lexi-ai-label"),greek(turn.transcript||""));
      if(turn.origin==="typed")item.append(el("p",t("typedOnly"),"lexi-ai-muted"));
      if(turn.edited||turn.origin==="edited_transcript"){
        item.append(el("p",t("edited"),"lexi-ai-notice"));
        if(turn.originalTranscript!==undefined){const original=el("details");original.append(el("summary",t("originalTranscript")),greek(turn.originalTranscript));item.append(original);}
      }
      if(turn.reply)item.append(el("span",t("reply"),"lexi-ai-label"),greek(turn.reply));
      if(turn.correction){item.append(el("span",t("correction"),"lexi-ai-label"),greek(turn.correction));if(turn.explanation)item.append(mixed(turn.explanation));}
      if(turn.finalNote)item.append(mixed(turn.finalNote));
      if(turn.jobId){
        if(index===history.length-1&&["active","completed"].includes(conversation.status)){
          const edit=button(t("editTranscript"),()=>{stopMedia(ctx);ctx.edit={kind:"dialogue",jobId:turn.jobId,text:turn.transcript||""};render(ctx,true);},"edit-turn");
          edit.disabled=busy(ctx);item.append(edit);
        }
        item.append(reporting(ctx,{id:turn.jobId,reported:ctx.reported.has(turn.jobId)}));
      }
      panel.append(item);
    }
    const job=ctx.dialogueJob?.conversationId===conversation.id?ctx.dialogueJob:null;
    if(job)panel.append(jobStatus(ctx,job,{conversationId:conversation.id}));
    if(ctx.needsConversationRefresh)panel.append(button(t("checkStatus"),()=>refreshConversation(ctx),"refresh-dialogue"));
    if(ctx.edit?.kind==="dialogue")panel.append(editor(ctx));
    else if(conversation.status==="active"&&conversation.question){
      const question=el("div",undefined,"lexi-ai-current-question");
      question.append(el("span",t("question")+" "+(conversation.turnCount+1),"lexi-ai-label"),greek(conversation.question.text));
      panel.append(question);
      if(ctx.typed||!supportedMime()||!ctx.caps.audioDecoder){
        panel.append(el("p",t("typedOnly"),"lexi-ai-notice"));
        panel.append(field(t("typeAnswer"),"ai-typed-answer",ctx.typedText,value=>{
          ctx.typedText=value;const send=ctx.host.querySelector("[data-ai-focus='send-text']");if(send)send.disabled=busy(ctx)||!value.trim();
        }));
        const actions=el("div",undefined,"lexi-ai-actions"),send=button(t("sendText"),()=>sendTyped(ctx),"send-text",true);
        send.disabled=busy(ctx)||!ctx.typedText?.trim();actions.append(send);
        if(supportedMime()&&ctx.caps.audioDecoder)actions.append(button(t("voiceButton"),()=>{ctx.typed=false;render(ctx);},"voice-mode"));
        panel.append(actions);
      }else{
        panel.append(controls(ctx,"dialogue"));
        const typed=button(t("typedButton"),()=>{stopMedia(ctx);ctx.typed=true;ctx.edit=null;render(ctx,true);},"typed-mode");typed.disabled=ctx.posting||Boolean(ctx.operation);panel.append(typed);
      }
    }
    if(conversation.status==="active"){
      const finish=button(t("finishDialogue"),()=>finishDialogue(ctx),"finish-dialogue");finish.disabled=ctx.posting||Boolean(ctx.operation);panel.append(finish);
    }else panel.append(el("p",t(conversation.status==="completed"?"completedDialogue":"partialDialogue"),"lexi-ai-positive"));
    return panel;
  }
  function render(ctx,focus=false){
    if(current!==ctx||!ctx.host.isConnected||!ctx.caps?.enabled)return;
    const previous=ctx.host.contains(document.activeElement)?document.activeElement.dataset.aiFocus:null;
    const host=ctx.host;host.hidden=false;host.className="lexi-ai";host.dir=lang()==="ar"?"rtl":"ltr";host.lang=lang();
    const fragment=document.createDocumentFragment(),header=el("header",undefined,"lexi-ai-header"),title=el("h2",t("title"));
    title.tabIndex=-1;title.id="lexi-ai-title";host.setAttribute("aria-labelledby",title.id);
    header.append(el("span",t("optional"),"lexi-ai-kicker"),title,el("p",t("intro"),"lexi-ai-muted"));fragment.append(header);
    if(ctx.erased){fragment.append(el("p",t("erased"),"lexi-ai-positive"));host.replaceChildren(fragment);return;}
    if(ctx.erasing){
      const message=el("p",t(ctx.erasing==="pending"?"erasing":"eraseUnknown"));message.setAttribute("role","status");fragment.append(message);
      if(ctx.erasing==="unknown")fragment.append(button(t("retryErase"),()=>erase(ctx,true),"retry-erase"));
      host.replaceChildren(fragment);return;
    }
    if(ctx.paused){
      fragment.append(el("p",t("stopped"),"lexi-ai-notice"),button(t("resume"),()=>resumeContext(ctx),"resume-ai"));host.replaceChildren(fragment);return;
    }
    if(ctx.contentLang!==lang())fragment.append(el("p",t("contentLanguage",{language:names[ctx.contentLang]}),"lexi-ai-muted"));
    if(ctx.error){const error=el("p",t(ctx.error),"lexi-ai-error");error.setAttribute("role","alert");fragment.append(error);}
    if(ctx.notice){const notice=el("p",t(ctx.notice),"lexi-ai-notice");notice.setAttribute("role","status");fragment.append(notice);}
    if(ctx.posting){const status=el("p",t("sending"),"lexi-ai-status");status.setAttribute("role","status");fragment.append(status);}
    if(ctx.operation){
      const actions=el("div",undefined,"lexi-ai-actions"),check=button(t("checkStatus"),()=>recover(ctx),"recover-operation");check.disabled=ctx.posting;actions.append(check);
      if(ctx.operation.checkedMissing){
        if(ctx.operation.restored||ctx.operation.lostPayload)actions.append(button(t("resetAttempt"),()=>{ctx.operation=null;ctx.notice=null;persist(ctx);render(ctx);},"reset-operation"));
        else {const resend=button(t("retrySend"),()=>recover(ctx,true),"retry-operation");resend.disabled=ctx.posting;actions.append(resend);}
      }
      fragment.append(actions);
    }
    if(!ctx.ready){const load=el("p",t("loading"));load.setAttribute("role","status");fragment.append(load);}
    else if(!ctx.options){
      fragment.append(button(t("checkStatus"),()=>reload(ctx),"reload-options"));
    }else{
      if(ctx.mode!=="overview")fragment.append(button(t("back"),()=>changeMode(ctx,"overview"),"back-options"));
      if(ctx.mode==="reading")fragment.append(readingPanel(ctx));
      else if(ctx.mode==="dialogue")fragment.append(dialoguePanel(ctx));
      else{
        if(ctx.caps.features?.summary)fragment.append(summaryPanel(ctx));
        const choices=el("div",undefined,"lexi-ai-choices");
        if(ctx.caps.features?.reading)choices.append(button(t("reading"),()=>changeMode(ctx,"reading"),"choose-reading"));
        if(ctx.caps.features?.dialogue){
          const dialogue=button(t("dialogue"),()=>{
            if(!valid(ctx))return;
            // Returning to an unresolved conversation is safe; changing its
            // identity would detach its in-flight job from the displayed draft.
            if(busy(ctx)){if(ctx.conversation)changeMode(ctx,"dialogue");return;}
            ctx.conversation=null;ctx.dialogueJob=null;ctx.typedText="";changeMode(ctx,"dialogue");
          },"choose-dialogue");
          dialogue.disabled=busy(ctx)&&!ctx.conversation;choices.append(dialogue);
        }
        fragment.append(choices);
      }
    }
    const privacy=el("details",undefined,"lexi-ai-privacy");privacy.append(el("summary",t("privacy")));
    privacy.append(el("p",t("privacyText",{days:ctx.caps.textRetentionDays,hours:ctx.caps.audioRetentionHours})));
    privacy.append(el("p",t("providerPolicy")),providerLink());
    const eraseButton=button(t("erase"),()=>erase(ctx),"erase-ai");eraseButton.disabled=ctx.posting;privacy.append(eraseButton);fragment.append(privacy);
    host.replaceChildren(fragment);
    if(focus&&!ctx.dialog){const editorInput=ctx.edit?host.querySelector("textarea"):null;(editorInput||title).focus({preventScroll:true});}
    else if(previous&&!ctx.dialog){
      const replacement=[...host.querySelectorAll("[data-ai-focus]")].find(node=>node.dataset.aiFocus===previous&&!node.disabled);replacement?.focus({preventScroll:true});
    }
  }
  async function resumeContext(ctx){
    if(current!==ctx||!ctx.host.isConnected||!app()?.loggedIn?.()||ctx.owner!==app()?.accountKey?.()||document.hidden)return;
    ctx.epoch=++epoch;ctx.paused=false;ctx.notice=null;ctx.error=null;ctx.posting=false;render(ctx);await reload(ctx);
  }
  async function openCompletion(event){
    const detail=event.detail||{},runId=detail.runId||detail.lesson?.runId;
    const host=document.getElementById("lesson-summary-ai");
    if(!host||!runId||!app()?.loggedIn?.())return;
    destroy();host.replaceChildren();host.hidden=true;
    const ctx={host,runId,owner:app()?.accountKey?.(),epoch:++epoch,contentLang:langs.includes(detail.lang)?detail.lang:lang(),caps:null,options:null,
      controllers:new Set(),watches:new Map(),pollPaused:new Set(),reported:new Set(),consents:new Set(),
      mode:"overview",summary:null,readingJobs:new Map(),readingId:null,conversation:null,dialogueJob:null,
      media:null,mediaEpoch:0,paused:false,posting:false,ready:false,error:null,notice:null,edit:null,typed:false,typedText:""};
    current=ctx;restore(ctx);
    try{
      const capabilities=await request(ctx,"ai/capabilities");
      if(!valid(ctx)||!capabilities.enabled){host.hidden=true;return;}
      ctx.caps=capabilities;render(ctx);await reload(ctx);
    }catch{if(current===ctx)host.hidden=true;}
  }
  document.addEventListener("lexi:lesson-complete",openCompletion);
  document.addEventListener("lexi:page-leave",()=>suspend(current));
  document.addEventListener("lexi:page-enter",event=>{if(event.detail?.page==="board"&&current?.host.isConnected&&!current.host.parentElement?.closest("[hidden]"))resumeContext(current);});
  document.addEventListener("lexi:logout",()=>destroy(true));
  document.addEventListener("visibilitychange",()=>{
    if(document.hidden)suspend(current);
    else if(current?.host.isConnected&&!current.host.parentElement?.closest("[hidden]"))resumeContext(current);
  });
  window.addEventListener("pagehide",()=>suspend(current));
  window.addEventListener("beforeunload",()=>suspend(current));
  document.getElementById("lang")?.addEventListener("change",()=>{if(current)render(current);});
  new MutationObserver(()=>{
    if(!current)return;
    if(!app()?.loggedIn?.()||current.owner!==app()?.accountKey?.()){destroy(true);return;}
    if(!current.host.isConnected||current.host.parentElement?.closest("[hidden]"))suspend(current);
  }).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:["hidden"]});
})();
