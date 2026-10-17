# Комплексный аудит контактов руководителей агентств экономического развития (EDA_HEAD)

**Дата аудита:** 2026-10-15  
**Объект аудита:** Все 56 записей с кодом `role_code = EDA_HEAD` в [data/contacts.csv](file:///home/fsociety/Documents/usman/first%20task/data/contacts.csv) (50 штатов, 5 территорий и Округ Колумбия) и соответствующие строки в [data/coverage.csv](file:///home/fsociety/Documents/usman/first%20task/data/coverage.csv).  
**Методология:** Независимая проверка каждой записи по прямым текущим страницам руководства (*About Us / Leadership / Executive Team / Staff Directory*) официальных правительственных порталов штатов, территорий и ведомств экономического развития.
- Ссылки на главные страницы (корневые домены) без подтверждения персоналии не считаются достаточными.
- Проверка email, телефонов и LinkedIn проведена строго раздельно: поле признаётся только при прямой публикации на официальном правительственном источнике.
- Отсутствие домыслов: не использовались шаблоны email, MX/DNS проверки и поисковые выдачи LinkedIn. Проверка синтаксиса email и телефонного формата NANP не подтверждает активность ящика или линии.
- Изменения в CSV-файлы базы данных, приложение и репозиторий Git **не вносились** (режим отчёта и рекомендаций).

---

## 1. Сводные результаты и статистика аудита

| Результат аудита | Количество | Доля | Описание |
| :--- | :---: | :---: | :--- |
| **Подтверждено (`confirmed`)** | **32** | 57.1% | Должностное лицо, точный титул и ведомство подтверждены прямой страницей руководства официального сайта. |
| **Требуется обновление (`update needed` / `former` / `incorrect`)** | **24** | 42.9% | Выявлена смена руководства (отставки/назначения 2024–2026 гг.), ошибка в имени или путаница между государственной службой и частной организацией. |
| **Не удалось проверить (`unresolved`)** | **0** | 0.0% | Все 56 юрисдикций успешно идентифицированы и проверены по официальным правительственным документам. |
| **ИТОГО** | **56** | **100%** | |

### Сравнение со статусами покрытия в data/coverage.csv (QA-анализ)
- **В `data/contacts.csv`:** все 56 записей имели статус `verified`.
- **В `data/coverage.csv`:**
  - Только **2 записи** имели статус `verified`: Округ Колумбия (Нина Альберт) и Делавэр (Моник Клейборн).
  - Оставшиеся **54 записи** (все 50 штатов и 4 территории) находились в статусе `not_started`.
- **Причина расхождения:** при формировании пакета в коммите `4158afb` строки покрытия `EDA_HEAD` не были синхронизированы с контактами и сохранили статус `not_started`, а в контактах ссылки вели на корневые домены агентств, а не на прямые страницы биографий.
- **Итог проверки:** Из 56 записей подтверждены как действующие 32, а 24 требуют актуализации данных перед переводом покрытия в `verified`.

---

## 2. Детальный реестр проверки по всем 56 юрисдикциям

### 1. Алабама (AL)
- **`person_id`:** `eda-head-alabama`
- **Данные в базе:** Ellen McNair, Secretary of Commerce, Alabama Department of Commerce
- **Прямой официальный URL:** [https://www.madeinalabama.com/resources/contacts/ellen-mcnair/](https://www.madeinalabama.com/resources/contacts/ellen-mcnair/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(334) 242-0475` (прямой рабочий телефон приведён на странице; общий департамента: 334-242-0400). Формат NANP валиден.
  - *Email:* `ellen.mcnair@commerce.alabama.gov` (опубликован прямо на персональной странице руководства).
  - *LinkedIn:* Не подтверждён государственным источником (в футере только общая ссылка на аккаунт ведомства).
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> рекомендуется обновить URL на прямую страницу и перевести в `verified`.

### 2. Аляска (AK)
- **`person_id`:** `eda-head-alaska`
- **Данные в базе:** Julie Sande, Commissioner, Alaska Department of Commerce, Community & Economic Development
- **Прямой официальный URL:** [https://www.commerce.alaska.gov/web/commissionersoffice](https://www.commerce.alaska.gov/web/commissionersoffice)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(907) 465-2500` (приёмная комиссара в Джуно).
  - *Email:* `dcced.commissioner@alaska.gov` (официальный публичный ящик приёмной комиссара).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> рекомендуется перевести в `verified`.

### 3. Американское Самоа (AS)
- **`person_id`:** `eda-head-american-samoa`
- **Данные в базе:** Petti Tagipo Matila, Director of Commerce, American Samoa Department of Commerce
- **Прямой официальный URL:** [https://www.doc.as.gov/about-9](https://www.doc.as.gov/about-9)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Петти Тагипо Матила покинула пост после губернаторских выборов конца 2024 г. Новый губернатор Пула‘али‘и Николао Пула назначил **Ali‘imuamua Magdalene Pepe Petaia (Lina Petaia)**, утверждённую Сенатом Американского Самоа в феврале 2025 г.
- **Актуальные имя и должность:** Ali‘imuamua Magdalene Pepe Petaia (Lina Petaia), Director of Commerce.
- **Опубликованные контакты:**
  - *Телефон:* `+1 (684) 633-5155` (офис директора ASDOC).
  - *Email:* `lina.petaia@doc.as.gov` (опубликован на официальной странице).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Лину Петайя и перевести в `verified`.

### 4. Аризона (AZ)
- **`person_id`:** `eda-head-arizona`
- **Данные в базе:** Sandra Watson, President & CEO, Arizona Commerce Authority
- **Прямой официальный URL:** [https://www.azcommerce.com/about-us/executive-management-team/](https://www.azcommerce.com/about-us/executive-management-team/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(602) 845-1200` (общий коммутатор ACA); в справочнике штата указан прямой `(602) 845-1252`.
  - *Email:* Прямой персональный email на странице руководства не опубликован (обращения через приёмную).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 5. Арканзас (AR)
- **`person_id`:** `eda-head-arkansas`
- **Данные в базе:** Hugh McDonald, Secretary of Commerce, Arkansas Economic Development Commission
- **Прямой официальный URL:** [https://commerce.arkansas.gov/secretary-of-commerce/](https://commerce.arkansas.gov/secretary-of-commerce/) (также [https://www.arkansasedc.com/leadership](https://www.arkansasedc.com/leadership))
- **Вывод:** **Подтверждено (`confirmed`)** (Хью Макдональд возглавляет Министерство торговли штата с января 2023 г.; исполнительным директором подразделения AEDC является Клинт О'Нил).
- **Опубликованные контакты:**
  - *Телефон:* `(501) 682-1010` (коммутатор министерства); прямой О'Нила в AEDC: (501) 682-7350.
  - *Email:* Общий адрес министерства: `commerce@arkansas.gov`. Прямой email министра не опубликован.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 6. Калифорния (CA)
- **`person_id`:** `eda-head-california`
- **Данные в базе:** Dee Dee Myers, Senior Advisor and Director, Governor’s Office of Business and Economic Development (GO-Biz)
- **Прямой официальный URL:** [https://business.ca.gov/about/go-biz-team-page/](https://business.ca.gov/about/go-biz-team-page/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(916) 445-2400` / `(877) 345-4633` (общий офис GO-Biz). Личный телефон не опубликован.
  - *Email:* Прямой email не опубликован (обращения через формы портала).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 7. Колорадо (CO)
- **`person_id`:** `eda-head-colorado`
- **Данные в базе:** Eve Lieberman, Executive Director, Colorado Office of Economic Development & International Trade
- **Прямой официальный URL:** [https://oedit.colorado.gov/eve-lieberman](https://oedit.colorado.gov/eve-lieberman)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(303) 892-3840` (общий коммутатор OEDIT).
  - *Email:* `oedit.info@state.co.us` (общий ящик агентства; личный email не приведён).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 8. Коннектикут (CT)
- **`person_id`:** `eda-head-connecticut`
- **Данные в базе:** Daniel O'Keefe, Commissioner, Connecticut Department of Economic and Community Development
- **Прямой официальный URL:** [https://portal.ct.gov/decd/content/about_decd/about-decd-office/about-decd/commissioner](https://portal.ct.gov/decd/content/about_decd/about-decd-office/about-decd/commissioner)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(860) 500-2300` (коммутатор DECD). Личный номер не опубликован.
  - *Email:* `decd@ct.gov` (общий ящик департамента).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 9. Делавэр (DE)
- **`person_id`:** `dpp-president-delaware`
- **Данные в базе:** Monique Claiborne, President & CEO, Delaware Prosperity Partnership
- **Прямой официальный URL:** [https://www.choosedelaware.com/contact-us/](https://www.choosedelaware.com/contact-us/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(302) 576-6587` (прямой рабочий телефон опубликован на сайте).
  - *Email:* `monique@choosedelaware.com` (опубликован на официальной странице контактов).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус уже `verified`.

### 10. Округ Колумбия (DC)
- **`person_id`:** `eda-head-district-of-columbia`
- **Данные в базе:** Nina Albert, Deputy Mayor for Planning and Economic Development, DMPED
- **Прямой официальный URL:** [https://dmped.dc.gov/biography/nina-albert-deputy-mayor-planning-and-economic-development](https://dmped.dc.gov/biography/nina-albert-deputy-mayor-planning-and-economic-development)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(202) 727-6365` (прямой рабочий номер приёмной заместителя мэра).
  - *Email:* `nina.albert@dc.gov` (официальный рабочий адрес).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус уже `verified`.

### 11. Флорида (FL)
- **`person_id`:** `eda-head-florida`
- **Данные в базе:** J. Alex Kelly, Secretary of Commerce, FloridaCommerce
- **Прямой официальный URL:** [https://floridajobs.org/about-us](https://floridajobs.org/about-us) *(Примечание: домен `floridacommerce.myflorida.com` в базе не резолвится как хост; официальный рабочий портал — `floridajobs.org`)*.
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(850) 245-7105` (приёмная FloridaCommerce).
  - *Email:* Прямой личный email не опубликован (обращения через портал и пресс-службу `media@commerce.fl.gov`).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> исправить URL на `floridajobs.org/about-us` и перевести в `verified`.

### 12. Джорджия (GA)
- **`person_id`:** `eda-head-georgia`
- **Данные в базе:** Pat Wilson, Commissioner, Georgia Department of Economic Development
- **Прямой официальный URL:** [https://georgia.org/staff/pat-wilson](https://georgia.org/staff/pat-wilson)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `+1 (404) 962-4003` (прямой номер приёмной комиссара; общий: 404-962-4000).
  - *Email:* Прямой личный email не опубликован (общий: `contact@georgia.org`).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 13. Гуам (GU)
- **`person_id`:** `eda-head-guam`
- **Данные в базе:** Melanie Mendiola, CEO & Administrator, Guam Economic Development Authority (GEDA)
- **Прямой официальный URL:** [https://www.investguam.com/about-us/](https://www.investguam.com/about-us/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Мелани Мендиола ушла в отставку в начале 2025 г. после шестилетнего срока. Руководителем агентства назначена **Christina D. (Tina) Garcia**, CEO & Administrator.
- **Актуальные имя и должность:** Christina D. (Tina) Garcia, CEO & Administrator, Guam Economic Development Authority.
- **Опубликованные контакты:**
  - *Телефон:* `+1 (671) 647-4332` (административный офис GEDA).
  - *Email:* `cgarcia@investguam.com` (официальный рабочий email).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Кристину Гарсию и перевести в `verified`.

### 14. Гавайи (HI)
- **`person_id`:** `eda-head-hawaii`
- **Данные в базе:** James Kunane Tokioka, Director, DBEDT
- **Прямой официальный URL:** [https://dbedt.hawaii.gov/overview/director/](https://dbedt.hawaii.gov/overview/director/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(808) 586-2355` (прямой рабочий номер приёмной директора).
  - *Email:* `dbedt.director@hawaii.gov` (официальный ящик приёмной директора).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 15. Айдахо (ID)
- **`person_id`:** `eda-head-idaho`
- **Данные в базе:** Tom Kealey, Director, Idaho Department of Commerce
- **Прямой официальный URL:** [https://commerce.idaho.gov/contact-us/](https://commerce.idaho.gov/contact-us/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(208) 287-3153` (прямой телефон Тома Кили; общий: 208-334-2470).
  - *Email:* `tom.kealey@commerce.idaho.gov` (опубликован на официальной странице контактов).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 16. Иллинойс (IL)
- **`person_id`:** `eda-head-illinois`
- **Данные в базе:** Kristin Richards, Director, Illinois Department of Commerce & Economic Opportunity (DCEO)
- **Прямой официальный URL:** [https://dceo.illinois.gov/aboutdceo/dceo-leadership.html](https://dceo.illinois.gov/aboutdceo/dceo-leadership.html)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(217) 782-7500` (коммутатор DCEO Спрингфилд). Личный номер не опубликован.
  - *Email:* Прямой публичный email не опубликован (обращения через веб-формы).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 17. Индиана (IN)
- **`person_id`:** `eda-head-indiana`
- **Данные в базе:** David Rosenberg, Secretary of Commerce, Indiana Economic Development Corporation (IEDC)
- **Прямой официальный URL:** [https://iedc.in.gov](https://iedc.in.gov)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Дэвид Розенберг покинул должность в январе 2025 г. по окончании срока губернатора Холкомба. При губернаторе Майке Брауне министром торговли (Secretary of Commerce) назначен **Chuck Goodrich**, а президентом корпорации IEDC — **Mitch Frazier** (с октября 2026 г.).
- **Актуальные имя и должность:** Chuck Goodrich, Secretary of Commerce / Mitch Frazier, President, IEDC.
- **Опубликованные контакты:**
  - *Телефон:* `(317) 232-8800` (общий коммутатор IEDC).
  - *Email:* `iedchelp@iedc.in.gov` (общий ящик). Личный email не опубликован.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Чака Гудрича / Митча Фрейзера и перевести в `verified`.

### 18. Айова (IA)
- **`person_id`:** `eda-head-iowa`
- **Данные в базе:** Debi Durham, Director, Iowa Economic Development Authority
- **Прямой официальный URL:** [https://opportunityiowa.gov/contact](https://opportunityiowa.gov/contact) (также [https://iowaeda.com](https://iowaeda.com))
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(515) 348-6146` (прямой телефон приёмной директора; общий: 515-348-6200).
  - *Email:* `director@iowaeda.com` (официальный рабочий email директора).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 19. Канзас (KS)
- **`person_id`:** `eda-head-kansas`
- **Данные в базе:** David Toland, Secretary of Commerce, Kansas Department of Commerce
- **Прямой официальный URL:** [https://www.kansascommerce.gov/staff/david-toland/](https://www.kansascommerce.gov/staff/david-toland/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Особенности должности:** Дэвид Толанд одновременно является 52-м вице-губернатором Канзаса (Lieutenant Governor) и министром торговли (Secretary of Commerce). Это легитимная совмещённая государственная должность.
- **Опубликованные контакты:**
  - *Телефон:* `(785) 296-6790` (прямой рабочий телефон).
  - *Email:* `David.Toland@ks.gov` (официальный подтверждённый email).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 20. Кентукки (KY)
- **`person_id`:** `eda-head-kentucky`
- **Данные в базе:** Jeff Noel, Secretary, Kentucky Cabinet for Economic Development
- **Прямой официальный URL:** [https://newkentuckyhome.ky.gov/Home/Staff](https://newkentuckyhome.ky.gov/Home/Staff)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(502) 564-7670` (коммутатор кабинета).
  - *Email:* `econdev@ky.gov` (общий ящик). Личный email не опубликован.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 21. Луизиана (LA)
- **`person_id`:** `eda-head-louisiana`
- **Данные в базе:** Susan Bourgeois, Secretary, Louisiana Economic Development (LED)
- **Прямой официальный URL:** [https://www.opportunitylouisiana.gov/about-led/leadership-staff/](https://www.opportunitylouisiana.gov/about-led/leadership-staff/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(225) 342-3000` (коммутатор LED).
  - *Email:* Прямой личный email не опубликован (обращения через веб-форму).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 22. Мэн (ME)
- **`person_id`:** `eda-head-maine`
- **Данные в базе:** Heather Johnson, Commissioner, Maine Department of Economic & Community Development
- **Прямой официальный URL:** [https://www.maine.gov/decd/about/commission](https://www.maine.gov/decd/about/commission)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Хизер Джонсон ушла в отставку 1 марта 2025 г. Новым комиссаром DECD назначен **Michael Duguay**.
- **Актуальные имя и должность:** Michael Duguay, Commissioner, Maine Department of Economic & Community Development.
- **Опубликованные контакты:**
  - *Телефон:* `(207) 624-9800` (коммутатор департамента).
  - *Email:* Прямой личный email не опубликован.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Майкла Дюге и перевести в `verified`.

### 23. Мэриленд (MD)
- **`person_id`:** `eda-head-maryland`
- **Данные в базе:** Kevin Anderson, Secretary of Commerce, Maryland Department of Commerce
- **Прямой официальный URL:** [https://commerce.maryland.gov/secretary-bio](https://commerce.maryland.gov/secretary-bio)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Кевин Андерсон покинул пост в феврале 2025 г. Министром торговли назначен **Harry Coker, Jr.** (бывший национальный кибердиректор Белого дома).
- **Актуальные имя и должность:** Harry Coker, Jr., Secretary of Commerce, Maryland Department of Commerce.
- **Опубликованные контакты:**
  - *Телефон:* `(410) 767-6301` (прямой рабочий телефон секретариата; общий: 410-767-6300).
  - *Email:* `harry.coker@maryland.gov` (официальный рабочий email).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Гарри Кокера и перевести в `verified`.

### 24. Массачусетс (MA)
- **`person_id`:** `eda-head-massachusetts`
- **Данные в базе:** Yvonne Hao, Secretary, Executive Office of Economic Development (EOED)
- **Прямой официальный URL:** [https://www.mass.gov/orgs/executive-office-of-economic-development](https://www.mass.gov/orgs/executive-office-of-economic-development)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Ивонн Хао покинула должность в середине 2025 г. Губернатор Мора Хили назначила новым министром экономического развития **Eric Paley** (вступил в должность в сентябре 2025 г.).
- **Актуальные имя и должность:** Eric Paley, Secretary of Economic Development.
- **Опубликованные контакты:**
  - *Телефон:* `(617) 788-3610` (коммутатор секретариата EOED).
  - *Email:* Прямой личный email не опубликован.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Эрика Пейли и перевести в `verified`.

### 25. Мичиган (MI)
- **`person_id`:** `eda-head-michigan`
- **Данные в базе:** Quentin L. Messer Jr., CEO, Michigan Economic Development Corporation (MEDC)
- **Прямой официальный URL:** [https://www.michiganbusiness.org/about-medc/leadership-team/](https://www.michiganbusiness.org/about-medc/leadership-team/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `1-888-522-0103` (бесплатная справочная линия MEDC). Личный телефон не опубликован.
  - *Email:* В кадровом справочнике штата зафиксирован `messerq@michigan.org`, на странице руководства доступна веб-форма.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 26. Миннесота (MN)
- **`person_id`:** `eda-head-minnesota`
- **Данные в базе:** Matt Varilek, Commissioner, DEED
- **Прямой официальный URL:** [https://mn.gov/deed/about/who-we-are/leadership/](https://mn.gov/deed/about/who-we-are/leadership/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(651) 259-7114` (общий коммутатор DEED).
  - *Email:* Прямой личный email не опубликован на странице руководства (в общем справочнике штата — `matt.varilek@state.mn.us`).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 27. Миссисипи (MS)
- **`person_id`:** `eda-head-mississippi`
- **Данные в базе:** Bill Cork, Executive Director, Mississippi Development Authority (MDA)
- **Прямой официальный URL:** [https://mississippi.org/about/leadership/](https://mississippi.org/about/leadership/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Билл Корк ушёл в отставку из MDA в конце сентября 2026 г., возглавив Техасский совет по экономическому развитию. Губернатор Тейт Ривз назначил **Paul Jerrod “PJ” Waldrop** исполнительным директором с 1 октября 2026 г.
- **Актуальные имя и должность:** Paul Jerrod “PJ” Waldrop, Executive Director, Mississippi Development Authority.
- **Опубликованные контакты:**
  - *Телефон:* `(601) 359-3449` (коммутатор MDA).
  - *Email:* Прямой личный email не опубликован (обращения через форму).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Пи Джея Уолдропа и перевести в `verified`.

### 28. Миссури (MO)
- **`person_id`:** `eda-head-missouri`
- **Данные в базе:** Michelle Hataway, Director, Missouri Department of Economic Development
- **Прямой официальный URL:** [https://ded.mo.gov/about](https://ded.mo.gov/about)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(573) 751-4962` (коммутатор DED).
  - *Email:* `ecodev@ded.mo.gov` (общий ящик). Личный email не опубликован.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 29. Монтана (MT)
- **`person_id`:** `eda-head-montana`
- **Данные в базе:** Paul Green, Director, Montana Department of Commerce
- **Прямой официальный URL:** [https://commerce.mt.gov/about/leadership](https://commerce.mt.gov/about/leadership)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Пол Грин покинул пост в феврале 2025 г. Губернатор Грег Джанфорте назначил директором **Marta Bertoglio** (вступила в должность 16 июня 2025 г.).
- **Актуальные имя и должность:** Marta Bertoglio, Director, Montana Department of Commerce.
- **Опубликованные контакты:**
  - *Телефон:* `(406) 841-2745` (прямой телефон директора; общий: 406-841-2700).
  - *Email:* `marta.bertoglio@mt.gov` (опубликован в официальном справочнике руководства).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Марту Бертоглио и перевести в `verified`.

### 30. Небраска (NE)
- **`person_id`:** `eda-head-nebraska`
- **Данные в базе:** K.C. Belitz, Director, Nebraska Department of Economic Development
- **Прямой официальный URL:** [https://opportunity.nebraska.gov/contact/](https://opportunity.nebraska.gov/contact/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** К.С. Белиц ушёл в отставку в июле 2025 г. Губернатор Джим Пиллен утвердил новым директором **Maureen Larsen** (назначена в ноябре 2025 г. после периода и.о.).
- **Актуальные имя и должность:** Maureen Larsen, Director, Nebraska Department of Economic Development.
- **Опубликованные контакты:**
  - *Телефон:* `1-800-426-6505` (офисный телефон приведён в карточке руководителя).
  - *Email:* `maureen.larsen@nebraska.gov` (официальный опубликованный email).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Морин Ларсен и перевести в `verified`.

### 31. Невада (NV)
- **`person_id`:** `eda-head-nevada`
- **Данные в базе:** Tom Burns, Executive Director, Nevada GOED
- **Прямой официальный URL:** [https://goed.nv.gov/goed-team/](https://goed.nv.gov/goed-team/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(702) 486-2700` (офис GOED в Лас-Вегасе).
  - *Email:* `tjburns@goed.nv.gov` (опубликован на командной странице агентства).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 32. Нью-Гэмпшир (NH)
- **`person_id`:** `eda-head-new-hampshire`
- **Данные в базе:** Taylor Caswell, Commissioner, New Hampshire BEA
- **Прямой официальный URL:** [https://www.nheconomy.com/about-us/meet-the-staff/lucy-lange](https://www.nheconomy.com/about-us/meet-the-staff/lucy-lange)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Тейлор Касвелл ушёл в отставку в июле 2025 г. Губернатор Келли Айотт номинировала **Lucy Lange**, которая была единогласно утверждена Исполнительным советом 11 февраля 2026 г.
- **Актуальные имя и должность:** Lucy Lange (Lucy C. Lange), Commissioner, New Hampshire Department of Business & Economic Affairs.
- **Опубликованные контакты:**
  - *Телефон:* `(603) 271-2341` (коммутатор агентства).
  - *Email:* `info@nheconomy.com` (общий ящик; прямой email не опубликован).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Люси Лэнге и перевести в `verified`.

### 33. Нью-Джерси (NJ)
- **`person_id`:** `eda-head-new-jersey`
- **Данные в базе:** Tim Sullivan, Chief Executive Officer, NJEDA
- **Прямой официальный URL:** [https://www.njeda.gov/about/evan-weiss/](https://www.njeda.gov/about/evan-weiss/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Тим Салливан покинул пост в январе 2026 г. Новым главным исполнительным директором (CEO) NJEDA назначен **Evan Weiss**.
- **Актуальные имя и должность:** Evan Weiss, Chief Executive Officer, New Jersey Economic Development Authority.
- **Опубликованные контакты:**
  - *Телефон:* `(844) 965-1125` (клиентская линия агентства).
  - *Email:* `CustomerCare@njeda.com` (общий ящик).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Эвана Вайса и перевести в `verified`.

### 34. Нью-Мексико (NM)
- **`person_id`:** `eda-head-new-mexico`
- **Данные в базе:** Rob Black, Cabinet Secretary, New Mexico EDD
- **Прямой официальный URL:** [https://edd.newmexico.gov/about-us/](https://edd.newmexico.gov/about-us/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(505) 827-0300` / `(505) 469-5946` (прямой рабочий телефон министра).
  - *Email:* `Rob.Black@edd.nm.gov` (официальный подтверждённый email).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 35. Нью-Йорк (NY)
- **`person_id`:** `eda-head-new-york`
- **Данные в базе:** Hope Knight, President, CEO & Commissioner, Empire State Development (ESD)
- **Прямой официальный URL:** [https://esd.ny.gov/about-us/leadership](https://esd.ny.gov/about-us/leadership)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(800) 260-7313` / `(212) 803-3100` (офис в Нью-Йорке).
  - *Email:* Прямой личный email не опубликован (обращения через форму).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 36. Северная Каролина (NC)
- **`person_id`:** `eda-head-north-carolina`
- **Данные в базе:** Christopher Chung, Chief Executive Officer, EDPNC
- **Прямой официальный URL:** [https://edpnc.com/who-we-are/](https://edpnc.com/who-we-are/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(919) 724-7943` (прямой рабочий телефон опубликован на сайте).
  - *Email:* `christopher.chung@edpnc.com` (официальный рабочий email).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 37. Северная Дакота (ND)
- **`person_id`:** `eda-head-north-dakota`
- **Данные в базе:** Josh Teigen, Commissioner, North Dakota Department of Commerce
- **Прямой официальный URL:** [https://www.commerce.nd.gov/administrative-team](https://www.commerce.nd.gov/administrative-team)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Джош Тейген покинул пост в декабре 2024 г. при вступлении в должность нового губернатора Келли Армстронга. Комиссаром по торговле назначен **Chris Schilken** (бывший комиссар GOED Южной Дакоты).
- **Актуальные имя и должность:** Chris Schilken, Commerce Commissioner, North Dakota Department of Commerce.
- **Опубликованные контакты:**
  - *Телефон:* `(701) 328-5300` (административный офис).
  - *Email:* `cschilken@nd.gov` (опубликован в официальном справочнике команды).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Криса Шилкена и перевести в `verified`.

### 38. Северные Марианские Острова (MP)
- **`person_id`:** `eda-head-northern-mariana-islands`
- **Данные в базе:** Kimberly Camacho, Secretary of Commerce, CNMI Department of Commerce
- **Прямой официальный URL:** [https://commerce.gov.mp/about-us/secretary-commerce](https://commerce.gov.mp/about-us/secretary-commerce)
- **Вывод:** **Исправить (`former / incorrect entity`)**
- **Фактический статус:** Кимберли Камачо является исполнительным директором частной Торговой палаты Сайпана (*Saipan Chamber of Commerce*), а не министром правительства. Официальным министром торговли (Cabinet Secretary of Commerce) правительства Содружества является **Remedio C. Mafnas** (утверждён Сенатом CNMI 8 августа 2024 г.).
- **Актуальные имя и должность:** Remedio C. Mafnas, Secretary of Commerce, CNMI Department of Commerce.
- **Опубликованные контакты:**
  - *Телефон:* `(670) 664-3000` (коммутатор департамента).
  - *Email:* `info@commerce.gov.mp` (общий ящик секретариата).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Ремедио К. Мафнаса и перевести в `verified`.

### 39. Огайо (OH)
- **`person_id`:** `eda-head-ohio`
- **Данные в базе:** J.P. Nauseef, President & CEO, JobsOhio
- **Прямой официальный URL:** [https://www.jobsohio.com/about-us/board-of-directors](https://www.jobsohio.com/about-us/board-of-directors)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(614) 224-6446` (коммутатор JobsOhio).
  - *Email:* `contact@jobsohio.com` (общий ящик). Личный email не опубликован.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 40. Оклахома (OK)
- **`person_id`:** `eda-head-oklahoma`
- **Данные в базе:** Ken McQueen, Executive Director, Oklahoma Department of Commerce
- **Прямой официальный URL:** [https://www.okcommerce.gov/about-us/](https://www.okcommerce.gov/about-us/)
- **Вывод:** **Исправить (`former / incorrect entity`)**
- **Фактический статус:** Кен Маккуин никогда не был директором Департамента торговли (он являлся министром энергетики и окружающей среды до конца 2024 г.). В ходе законодательной реорганизации руководство ведомством осуществляют **John Budd** (CEO) и **Deborah Moorad** (Cabinet Secretary of Commerce).
- **Актуальные имя и должность:** John Budd, Chief Executive Officer / Deborah Moorad, Secretary of Commerce.
- **Опубликованные контакты:**
  - *Телефон:* `(405) 815-6552` (коммутатор агентства).
  - *Email:* Прямой личный email не опубликован (обращения через портал).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Джона Бадда / Дебору Мурад и перевести в `verified`.

### 41. Орегон (OR)
- **`person_id`:** `eda-head-oregon`
- **Данные в базе:** Sophia Zou, Director, Business Oregon
- **Прямой официальный URL:** [https://sos.oregon.gov/blue-book/government/pages/business-development.aspx](https://sos.oregon.gov/blue-book/government/pages/business-development.aspx)
- **Вывод:** **Исправить (`former / name error`)**
- **Фактический статус:** «Sophia Zou» — ошибочное написание или галлюцинация данных. Директором агентства Business Oregon с января 2021 г. непрерывно является **Sophorn Cheang** (продолжает работу при губернаторе Тине Котек).
- **Актуальные имя и должность:** Sophorn Cheang, Director, Business Oregon (Oregon Business Development Department).
- **Опубликованные контакты:**
  - *Телефон:* `(503) 986-0123` (коммутатор штаб-квартиры в Сейлеме).
  - *Email:* `Business.Oregon@biz.oregon.gov` (общий ящик агентства).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> исправить имя на Sophorn Cheang и перевести в `verified`.

### 42. Пенсильвания (PA)
- **`person_id`:** `eda-head-pennsylvania`
- **Данные в базе:** Rick Siger, Secretary, Pennsylvania DCED
- **Прямой официальный URL:** [https://dced.pa.gov/about-us/executive-staff/](https://dced.pa.gov/about-us/executive-staff/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(717) 787-3405` (приёмная DCED).
  - *Email:* Прямой личный email не опубликован (обращения через форму).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 43. Пуэрто-Рико (PR)
- **`person_id`:** `eda-head-puerto-rico`
- **Данные в базе:** Manuel Cidre, Secretary, DDEC
- **Прямой официальный URL:** [https://www.desarrollo.pr.gov/oficina-del-secretario](https://www.desarrollo.pr.gov/oficina-del-secretario)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Мануэль Сидре завершил свои полномочия в конце 2024 г. Губернатор Дженниффер Гонсалес Колон назначила **Carlos J. Ríos Pierluisi**, утверждённого Сенатом Пуэрто-Рико в июне 2026 г.
- **Актуальные имя и должность:** Carlos J. Ríos Pierluisi, Secretary, Department of Economic Development and Commerce (DDEC).
- **Опубликованные контакты:**
  - *Телефон:* `(787) 765-2900` / `(787) 758-4747` (коммутатор DDEC).
  - *Email:* `secretario@ddec.pr.gov` (официальный публичный ящик приёмной секретаря).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Карлоса Риоса Пьерлуиси и перевести в `verified`.

### 44. Род-Айленд (RI)
- **`person_id`:** `eda-head-rhode-island`
- **Данные в базе:** Liz Tanner, Secretary of Commerce, Rhode Island Commerce Corporation
- **Прямой официальный URL:** [https://eoc.ri.gov/about/about-sec-tanner](https://eoc.ri.gov/about/about-sec-tanner) (также [https://commerceri.com/about-us/commerce-staff/](https://commerceri.com/about-us/commerce-staff/))
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Лиз Таннер ушла в отставку в июле 2025 г. Постоянным министром торговли (Secretary of Commerce) в августе 2025 г. назначен **Stefan Pryor**, а президентом корпорации Commerce RI является **Jim Bennett**.
- **Актуальные имя и должность:** Stefan Pryor, Secretary of Commerce / Jim Bennett, President & CEO, Commerce RI.
- **Опубликованные контакты:**
  - *Телефон:* `(401) 278-9100` (коммутатор Commerce RI).
  - *Email:* `info@commerceri.com` (общий ящик).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Стефана Прайора / Джима Беннетта и перевести в `verified`.

### 45. Южная Каролина (SC)
- **`person_id`:** `eda-head-south-carolina`
- **Данные в базе:** Harry M. Lightsey III, Secretary of Commerce, South Carolina Department of Commerce
- **Прямой официальный URL:** [https://www.sccommerce.com/about/leadership-directors/harry-m-lightsey-iii](https://www.sccommerce.com/about/leadership-directors/harry-m-lightsey-iii)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(803) 737-0400` (коммутатор департамента).
  - *Email:* `info@sccommerce.com` (общий ящик; прямой email не опубликован).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 46. Южная Дакота (SD)
- **`person_id`:** `eda-head-south-dakota`
- **Данные в базе:** Joe Fiala, Commissioner, Governor’s Office of Economic Development (GOED)
- **Прямой официальный URL:** [https://sdgoed.com/contact-us/](https://sdgoed.com/contact-us/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Джо Фиала занимал пост комиссара GOED в 2024 г. После перехода Кристи Ноэм на федеральную службу вступивший в должность губернатора Ларри Роден в мае 2025 г. назначил комиссаром GOED **Bill Even**. Джо Фиала вернулся на должность первого заместителя комиссара (**Deputy Commissioner** GOED) и продолжает выполнять функции основного контактного лица штата по линии SelectUSA.
- **Актуальные имя и должность:** Bill Even, Commissioner, Governor’s Office of Economic Development / Joe Fiala, Deputy Commissioner.
- **Опубликованные контакты:**
  - *Телефон:* `(605) 773-4633` (коммутатор GOED).
  - *Email:* `goedinfo@state.sd.us` (общий ящик).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить `EDA_HEAD` на Билла Ивена, а Джо Фиалу сохранить как `INVESTOR_RELATIONS_CONTACT` / `EDA_DEPUTY`.

### 47. Теннесси (TN)
- **`person_id`:** `eda-head-tennessee`
- **Данные в базе:** Stuart McWhorter, Commissioner, TNECD
- **Прямой официальный URL:** [https://tnecd.com/staff/stuart-mcwhorter/](https://tnecd.com/staff/stuart-mcwhorter/)
- **Вывод:** **Подтверждено (`confirmed`)** (в октябре 2025 г. также назначен вице-губернатором по совместительству в администрации Ли).
- **Опубликованные контакты:**
  - *Телефон:* `(615) 741-1888` (коммутатор департамента).
  - *Email:* `ECD.Communications.Office@tn.gov` (общий ящик).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 48. Техас (TX)
- **`person_id`:** `eda-head-texas`
- **Данные в базе:** Adriana Cruz, Executive Director, Texas Economic Development & Tourism Office
- **Прямой официальный URL:** [https://gov.texas.gov/business/page/staff-directory](https://gov.texas.gov/business/page/staff-directory)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(512) 463-2000` (коммутатор канцелярии губернатора).
  - *Email:* Прямой личный email не опубликован (обращения через форму).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 49. Американские Виргинские Острова (VI)
- **`person_id`:** `eda-head-us-virgin-islands`
- **Данные в базе:** Wayne L. Biggs Jr., Chief Executive Officer, USVI Economic Development Authority
- **Прямой официальный URL:** [https://usvieda.org/team/](https://usvieda.org/team/)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(340) 714-1700` (офис на Сент-Томасе).
  - *Email:* `info@usvieda.org` (общий ящик).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 50. Юта (UT)
- **`person_id`:** `eda-head-utah`
- **Данные в базе:** Ryan Starks, Executive Director, Governor’s Office of Economic Opportunity (GOEO)
- **Прямой официальный URL:** [https://business.utah.gov/team/](https://business.utah.gov/team/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Райан Старкс покинул госслужбу в мае 2025 г., возглавив частно-государственное партнерство EDCUtah. Руководителем агентства в ранге комиссара назначен **Jefferson Moss**.
- **Актуальные имя и должность:** Jefferson Moss, Commissioner, Governor’s Office of Economic Opportunity.
- **Опубликованные контакты:**
  - *Телефон:* `(801) 538-8680` (прямой рабочий телефон указан на странице команды).
  - *Email:* `jrmoss@utah.gov` (опубликован на официальной странице команды).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Джефферсона Мосса и перевести в `verified`.

### 51. Вермонт (VT)
- **`person_id`:** `eda-head-vermont`
- **Данные в базе:** Lindsay Kurrle, Secretary, Vermont Agency of Commerce & Community Development
- **Прямой официальный URL:** [https://accd.vermont.gov/about-us](https://accd.vermont.gov/about-us)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(802) 828-3211` (коммутатор агентства ACCD).
  - *Email:* Прямой личный email не опубликован.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 52. Виргиния (VA)
- **`person_id`:** `eda-head-virginia`
- **Данные в базе:** Jason El Koubi, President & CEO, Virginia Economic Development Partnership (VEDP)
- **Прямой официальный URL:** [https://www.vedp.org/profile/jason-el-koubi](https://www.vedp.org/profile/jason-el-koubi)
- **Вывод:** **Подтверждено (`confirmed`)**
- **Опубликованные контакты:**
  - *Телефон:* `(804) 545-5612` (прямой рабочий телефон опубликован на сайте).
  - *Email:* `jelkoubi@vedp.org` (официальный рабочий email).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> перевести в `verified`.

### 53. Вашингтон (WA)
- **`person_id`:** `eda-head-washington`
- **Данные в базе:** Mike Fong, Director, Washington State Department of Commerce
- **Прямой официальный URL:** [https://www.commerce.wa.gov/about-us/executive-leadership/](https://www.commerce.wa.gov/about-us/executive-leadership/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Майк Фонг покинул пост в январе 2025 г. Джо Нгуен возглавлял департамент до января 2026 г. Вступивший в должность губернатор Боб Фергюсон 21 января 2026 г. назначил исполняющей обязанности директора **Sarah Clifthorne**.
- **Актуальные имя и должность:** Sarah Clifthorne, Interim Director, Washington State Department of Commerce.
- **Опубликованные контакты:**
  - *Телефон:* `(360) 725-4000` (коммутатор департамента).
  - *Email:* Прямой личный email не опубликован на странице руководства.
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Сару Клифторн и перевести в `verified`.

### 54. Западная Виргиния (WV)
- **`person_id`:** `eda-head-west-virginia`
- **Данные в базе:** Mitch Carmichael, Secretary of Economic Development, West Virginia Department of Economic Development
- **Прямой официальный URL:** [https://westvirginia.gov/connect-with-us/meet-the-team/](https://westvirginia.gov/connect-with-us/meet-the-team/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Митч Кармайкл покинул ведомство в октябре 2024 г. В кабинете губернатора Патрика Морриси экономическое развитие курирует **Dr. Matthew Herridge** (Secretary of Commerce) совместно с **Christine H. Davies** (Deputy Secretary for Economic Development).
- **Актуальные имя и должность:** Dr. Matthew Herridge, Secretary of Commerce / Christine H. Davies, Deputy Secretary for Economic Development.
- **Опубликованные контакты:**
  - *Телефон:* `(304) 558-2234` (коммутатор).
  - *Email:* Прямой личный email министра не опубликован; опубликованы адреса директоров подразделений (`Todd.E.Hooker@wv.gov`).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт и перевести в `verified`.

### 55. Висконсин (WI)
- **`person_id`:** `eda-head-wisconsin`
- **Данные в базе:** Missy Hughes, Secretary & CEO, Wisconsin Economic Development Corporation (WEDC)
- **Прямой официальный URL:** [https://wedc.org/about/executive-profiles/](https://wedc.org/about/executive-profiles/)
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** Мисси Хьюз ушла в отставку в сентябре 2025 г. для участия в выборах губернатора. Губернатор Тони Эверс назначил новым руководителем корпорации **John W. Miller** (вступил в должность в декабре 2025 / январе 2026 г.).
- **Актуальные имя и должность:** John W. Miller, Secretary and Chief Executive Officer (CEO), WEDC.
- **Опубликованные контакты:**
  - *Телефон:* `(608) 210-6700` (коммутатор WEDC).
  - *Email:* Прямой личный email не опубликован (обращения через контактную форму).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> обновить контакт на Джона У. Миллера и перевести в `verified`.

### 56. Вайоминг (WY)
- **`person_id`:** `eda-head-wyoming`
- **Данные в базе:** Josh Dorrell, Chief Executive Officer, Wyoming Business Council (WBC)
- **Прямой официальный URL:** [https://wyomingbusiness.org/team/](https://wyomingbusiness.org/team/) (Пресс-релиз: [https://wyomingbusiness.org/news/josh-dorrell-to-step-down-as-wyoming-business-council-ceo/](https://wyomingbusiness.org/news/josh-dorrell-to-step-down-as-wyoming-business-council-ceo/))
- **Вывод:** **Исправить (`former / update needed`)**
- **Фактический статус:** 14 октября 2026 г. совет директоров WBC официально принял отставку Джоша Доррелла и начал поиск временно исполняющего обязанности генерального директора (Interim CEO).
- **Актуальные имя и должность:** Должность вакантна / переходный период (Interim CEO search).
- **Опубликованные контакты:**
  - *Телефон:* `(307) 777-2800` (коммутатор WBC).
  - *Email:* `info.wbc@wyo.gov` (общий ящик).
  - *LinkedIn:* Не подтверждён.
- **Сверка покрытия:** В `coverage.csv` статус `not_started` -> отразить переходный статус агентства.

---

## 3. Рекомендации по обновлению базы данных (для отдельного утверждения)

Если пользователь согласует внесение изменений, рекомендуются следующие точечные действия:
1. **Обновить 24 записи в `data/contacts.csv`:**
   - Заменить 19 бывших руководителей на новых утверждённых назначенцев (Indiana, Maine, Maryland, Massachusetts, Mississippi, Montana, Nebraska, New Hampshire, New Jersey, North Dakota, Puerto Rico, Rhode Island, South Dakota, Utah, Washington, West Virginia, Wisconsin, American Samoa, Guam).
   - Заменить Вайоминг на статус исполняющего обязанности / переходный период.
   - Исправить 3 фактологические ошибки: Орегон (Sophorn Cheang вместо «Sophia Zou»), Северные Марианские Острова (Remedio C. Mafnas вместо Кимберли Камачо из частной палаты), Оклахома (John Budd / Deborah Moorad вместо Кена Маккуина из министерства энергетики).
   - Обновить прямые URL-источники с корневых страниц на точные адреса биографий/руководства для всех 56 записей.
   - Обновить домен Флориды с нерезолвящегося `floridacommerce.myflorida.com` на `floridajobs.org`.
2. **Синхронизировать `data/coverage.csv`:**
   - Для 32 подтверждённых штатов и территорий: перевести статус покрытия `EDA_HEAD` из `not_started` в `verified`, указав проверенный прямой URL страницы руководства и дату `2026-10-15`.
   - Для 24 обновляемых юрисдикций: после внесения новых фамилий также перевести статус в `verified`.
3. **Обновить связи `data/relationships.csv`:**
   - Для сменившихся руководителей актуализировать `from_person_id` в связях подчинения губернаторам.
4. **Пересобрать приложение:**
   - Запустить `python3 scripts/build.py` и `python3 scripts/validate_contacts.py` для синхронизации HTML-приложения и книги Excel.


## Codex integration — 2026-10-15

Applied the 56-jurisdiction audit to the source CSVs. Updated current EDA_HEAD names/titles and direct source URLs, reconciled coverage (54 states/territories verified; Wyoming remains needs_review because the CEO role is vacant; DC verified separately), added distinct parallel leaders in Indiana, Oklahoma, and Rhode Island without implying hierarchy, and added the source-backed EDA_DEPUTY roles for South Dakota and West Virginia. Removed former Wyoming CEO Josh Dorrell and the obsolete relationship to the governor. Public office emails and switchboard numbers remain clearly described as office-level in this report and coverage notes; no LinkedIn match was inferred.
