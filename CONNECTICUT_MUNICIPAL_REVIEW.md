# Комплексный аудит и верификация мэров муниципалитетов Коннектикута

**Дата аудита:** 2026-10-15  
**Объект аудита:** Все 10 муниципальных записей мэров Коннектикута (`role_code = MAYOR`) в [data/contacts.csv](file:///home/fsociety/Documents/usman/first%20task/data/contacts.csv) и соответствующие строки в [data/coverage.csv](file:///home/fsociety/Documents/usman/first%20task/data/coverage.csv).  
**Методология:** Независимая проверка каждой записи по прямым официальным муниципальным порталам (.gov / официальные городские домены).
- Проверка email, телефонов и LinkedIn проведена строго раздельно: вносятся только данные, прямо опубликованные на официальном городском сайте.
- Никаких домыслов: не использовались шаблоны email, MX/DNS проверки и внешние поисковые выдачи LinkedIn. Синтаксическая валидность формата не является доказательством активности почтового ящика или телефонной линии.

---

## 1. Сводная таблица верификации (10 муниципалитетов)

| Муниципалитет | Импортированное имя | Статус исходных данных | Действующий мэр | Официальный URL приёмной | Опубликованный телефон | Опубликованный Email | LinkedIn на сайте |
|---|---|---|---|---|---|---|---|
| **New Haven** | Justin Elicker | **Подтверждён (`confirmed`)** | Justin Elicker | [Официальная страница](https://www.newhavenct.gov/government/office-of-the-mayor) | (203) 946-8200 | Не опубликован (веб-форма) | Отсутствует |
| **Norwalk** | Barbara Smyth | **Подтверждён (`confirmed`)** | Barbara C. Smyth | [Официальная страница](https://www.norwalkct.gov/155/Mayors-Office) | (203) 854-7701 | bsmyth@norwalkct.gov | Отсутствует |
| **New Britain** | Francisco Santiago | **Член горсовета (`incorrect`)** | Robert "Bobby" Sanchez | [Официальная страница](https://www.newbritainct.gov/gov/mayors-office/mayors-office) | (860) 826-3300 | Mayor@NewBritainCT.gov | Отсутствует |
| **Bristol** | Ellen Zoppo | **Усечённая фамилия (`confirmed`)** | Ellen Zoppo-Sassu | [Официальная страница](https://www.bristolct.gov/149/Mayors-Office) | (860) 584-6250 | mayorsoffice@bristolct.gov | Отсутствует |
| **Middletown** | Jeanette Blackwell | **Президент совета (`incorrect`)** | Gene Nocera | [Официальная страница](https://www.middletownct.gov/212/Mayors-Office) | (860) 638-4801 | mayor@middletownct.gov | Отсутствует |
| **Shelton** | Mark A. Lauretti | **Подтверждён (`confirmed`)** | Mark A. Lauretti | [Официальная страница](https://cityofshelton.org/p/office-of-the-mayor) | (203) 924-1555 ext. 1504 | shelton01@cityofshelton.org | Отсутствует |
| **Torrington** | Chris Beyus | **Член горсовета (`incorrect`)** | Molly Spino | [Официальная страница](https://www.torringtonct.gov/departments/administration___mayor_s_office/index.php) | (860) 489-2228 | Molly_Spino@torringtonct.org | Отсутствует |
| **Naugatuck** | N. Warren "Pete" Hess | **Подтверждён (`confirmed`)** | N. Warren "Pete" Hess III | [Официальная страница](https://www.naugatuck-ct.gov/mayor) | (203) 720-7009 | nwhess@naugatuck-ct.gov | Отсутствует |
| **Waterbury** | "Gets Prison Term" | **Сбой парсинга (`corrupted`)** | Paul K. Pernerewski Jr. | [Официальная страница](https://www.waterburyct.gov/administration/mayor) | (203) 574-6712 | Не опубликован (веб-форма) | Отсутствует |
| **West Haven** | Robert Johnson | **Бывший мэр 1970-х (`former`)** | Dorinda Borer | [Официальная страница](https://www.cityofwesthaven.com/151/Mayors-Office) | (203) 937-3510 | dborer@westhaven-ct.gov | Отсутствует |

---

## 2. Детальные результаты по каждому муниципалитету

### 1. New Haven
- **ID записи:** `wb-muni-r0769-mayor-new-haven-connecticut`
- **Импортированное имя:** Justin Elicker
- **Фактический статус:** **Подтверждён (`confirmed`)**. Джастин Эликер является действующим 51-м мэром Нью-Хейвена.
- **Официальный URL:** [https://www.newhavenct.gov/government/office-of-the-mayor](https://www.newhavenct.gov/government/office-of-the-mayor)
- **Контакты:** Телефон приёмной `(203) 946-8200`. Личный прямой email не опубликован (обращения через городскую форму обратной связи). Личный LinkedIn не опубликован.

### 2. Norwalk
- **ID записи:** `wb-muni-r1200-mayor-norwalk-connecticut`
- **Импортированное имя:** Barbara Smyth
- **Фактический статус:** **Подтверждён (`confirmed`)**. Барбара Смит (Barbara C. Smyth) избрана мэром Норволка 5 ноября 2025 года (ранее президент городского совета).
- **Официальный URL:** [https://www.norwalkct.gov/155/Mayors-Office](https://www.norwalkct.gov/155/Mayors-Office)
- **Контакты:** Телефон приёмной `(203) 854-7701`. Email: `bsmyth@norwalkct.gov`. Личный LinkedIn не опубликован.

### 3. New Britain
- **ID записи:** `wb-muni-r1342-mayor-new-britain-connecticut`
- **Импортированное имя:** Francisco Santiago
- **Фактический статус:** **Исправить (`incorrect / council member`)**. Франсиско Сантьяго является вице-президентом городского совета (Common Council President Pro Tempore), а не мэром. Действующий 41-й мэр Нью-Бритене с 12 ноября 2025 года — **Robert "Bobby" Sanchez**.
- **Официальный URL:** [https://www.newbritainct.gov/gov/mayors-office/mayors-office](https://www.newbritainct.gov/gov/mayors-office/mayors-office) (Биография мэра: [honorable-robert-bobby-sanchez](https://www.newbritainct.gov/gov/mayors-office/honorable-robert-bobby-sanchez))
- **Контакты:** Телефон `(860) 826-3300`. Email: `Mayor@NewBritainCT.gov`. Личный LinkedIn не опубликован.

### 4. Bristol
- **ID записи:** `wb-muni-r1489-mayor-bristol-connecticut`
- **Импортированное имя:** Ellen Zoppo
- **Фактический статус:** **Подтверждён (`confirmed / truncated`)**. В импортированных данных фамилия была усечена. Действующий мэр — Эллен Зоппо-Сассу (**Ellen Zoppo-Sassu**), вернувшаяся на пост мэра в 2025 году.
- **Официальный URL:** [https://www.bristolct.gov/149/Mayors-Office](https://www.bristolct.gov/149/Mayors-Office)
- **Контакты:** Телефон `(860) 584-6250`. Email: `mayorsoffice@bristolct.gov`. Личный LinkedIn не опубликован.

### 5. Middletown
- **ID записи:** `wb-muni-r1737-mayor-middletown-connecticut`
- **Импортированное имя:** Jeanette Blackwell
- **Фактический статус:** **Исправить (`incorrect / council president`)**. Джанетт Блэкуэлл — президент городского совета Мидлтауна. Действующий мэр — **Gene Nocera**.
- **Официальный URL:** [https://www.middletownct.gov/212/Mayors-Office](https://www.middletownct.gov/212/Mayors-Office)
- **Контакты:** Телефон `(860) 638-4801`. Email: `mayor@middletownct.gov`. Личный LinkedIn не опубликован.

### 6. Shelton
- **ID записи:** `wb-muni-r1845-mayor-shelton-connecticut`
- **Импортированное имя:** Mark A. Lauretti
- **Фактический статус:** **Подтверждён (`confirmed`)**. Марк А. Лауретти занимает пост мэра Шелтона непрерывно с 1991 года. В базе содержался неработающий домен `sheltonct.gov` — официальный сайт города `cityofshelton.org`.
- **Официальный URL:** [https://cityofshelton.org/p/office-of-the-mayor](https://cityofshelton.org/p/office-of-the-mayor)
- **Контакты:** Телефон `(203) 924-1555 ext. 1504`. Email: `shelton01@cityofshelton.org`. Личный LinkedIn не опубликован.

### 7. Torrington
- **ID записи:** `wb-muni-r1857-mayor-torrington-connecticut`
- **Импортированное имя:** Chris Beyus
- **Фактический статус:** **Исправить (`incorrect / council member`)**. Крис Бейюс — член городского совета Торрингтона. Действующий мэр — **Molly Spino**.
- **Официальный URL:** [https://www.torringtonct.gov/departments/administration___mayor_s_office/index.php](https://www.torringtonct.gov/departments/administration___mayor_s_office/index.php)
- **Контакты:** Телефон `(860) 489-2228`. Email: `Molly_Spino@torringtonct.org`. Личный LinkedIn не опубликован.

### 8. Naugatuck
- **ID записи:** `wb-muni-r2099-mayor-naugatuck-connecticut`
- **Импортированное имя:** N. Warren "Pete" Hess
- **Фактический статус:** **Подтверждён (`confirmed`)**. Действующий мэр боро Ногатак — N. Warren "Pete" Hess III. В базе был нерезолвящийся домен `naugatuckct.gov`, официальный сайт — `naugatuck-ct.gov`.
- **Официальный URL:** [https://www.naugatuck-ct.gov/mayor](https://www.naugatuck-ct.gov/mayor)
- **Контакты:** Телефон `(203) 720-7009`. Email: `nwhess@naugatuck-ct.gov`. Личный LinkedIn не опубликован.

### 9. Waterbury
- **ID записи:** `wb-muni-r2168-mayor-waterbury-connecticut`
- **Импортированное имя:** "Gets Prison Term"
- **Фактический статус:** **Исправить (`corrupted / scraping artifact`)**. Строка "Gets Prison Term" попала в исходную таблицу из криминальной хроники осуждения бывшего мэра Филипа Джордано. Действующий мэр Уотербери — **Paul K. Pernerewski Jr.** (в должности с 2023 года).
- **Официальный URL:** [https://www.waterburyct.gov/administration/mayor](https://www.waterburyct.gov/administration/mayor)
- **Контакты:** Телефон `(203) 574-6712`. Прямой личный email мэра не опубликован. Личный LinkedIn не опубликован.

### 10. West Haven
- **ID записи:** `wb-muni-r2237-mayor-west-haven-connecticut`
- **Импортированное имя:** Robert Johnson
- **Фактический статус:** **Исправить (`former / deceased`)**. Роберт Джонсон был мэром в 1975–1983 гг. и скончался в 2014 г. Действующий 13-й мэр Вест-Хейвена — **Dorinda Borer** (в должности с декабря 2023 года). В базе был недействительный домен `westhavenct.gov`, официальный сайт — `cityofwesthaven.com`.
- **Официальный URL:** [https://www.cityofwesthaven.com/151/Mayors-Office](https://www.cityofwesthaven.com/151/Mayors-Office)
- **Контакты:** Телефон `(203) 937-3510`. Email: `dborer@westhaven-ct.gov`. Личный LinkedIn не опубликован.
