# Комплексный аудит и верификация мэров муниципалитетов штата Нью-Йорк

**Дата аудита:** 2026-10-15  
**Объект аудита:** Все 14 муниципальных записей мэров Нью-Йорка (`role_code = MAYOR`) в [data/contacts.csv](file:///home/fsociety/Documents/usman/first%20task/data/contacts.csv) и соответствующие строки в [data/coverage.csv](file:///home/fsociety/Documents/usman/first%20task/data/coverage.csv).  
**Методология:** Независимая проверка каждой записи по прямым официальным муниципальным порталам (.gov / официальные городские домены).
- Проверка email, телефонов и LinkedIn проведена строго раздельно: вносятся только данные, прямо опубликованные на официальном городском сайте.
- Никаких домыслов: не использовались шаблоны email, MX/DNS проверки и внешние поисковые выдачи LinkedIn. Синтаксическая валидность формата не является доказательством активности почтового ящика или телефонной линии.

---

## 1. Сводная таблица верификации (14 муниципалитетов)

| Муниципалитет | Импортированное имя | Статус исходных данных | Действующий мэр | Официальный URL приёмной | Опубликованный телефон | Опубликованный Email | LinkedIn на сайте |
|---|---|---|---|---|---|---|---|
| **New York City** | Zohran Mamdani | **Дубликат / Кандидат (`duplicate`)** | Eric Adams / Zohran Kwame Mamdani | [Официальная страница](https://www.nyc.gov/office-of-the-mayor/) | (212) 639-9675 | Не опубликован (веб-форма) | Отсутствует |
| **Buffalo** | Christopher Scanlon | **Бывший и.о. мэра (`former`)** | Sean Ryan | [Официальная страница](https://www.buffalony.gov/490/Mayor) | (716) 851-4183 | MayorRyan@buffalony.gov | Отсутствует |
| **Rochester** | Malik Evans | **Подтверждён (`confirmed`)** | Malik D. Evans | [Официальная страница](https://www.cityofrochester.gov/departments/mayors-office) | (585) 428-7045 | info@cityofrochester.gov | Отсутствует |
| **Mount Vernon** | Shawyn Patterson | **Усечённая фамилия (`confirmed`)** | Shawyn Patterson-Howard | [Официальная страница](https://www.mountvernonny.gov/m/directory/department?did=17) | (914) 665-2362 | Не опубликован (веб-форма) | Отсутствует |
| **Schenectady** | Gary R. McCarthy | **Подтверждён (`confirmed`)** | Gary R. McCarthy | [Официальная страница](https://www.cityofschenectady.gov/210/Mayors-Office) | (518) 382-5000 | gmccarthy@schenectadyny.gov | Отсутствует |
| **Watertown** | Sarah Compo Pierce | **Подтверждён (`confirmed`)** | Sarah V. Compo Pierce | [Официальная страница](https://www.watertown-ny.gov/mayorsoffice) | (315) 785-7720 | spierce@watertown-ny.gov | Отсутствует |
| **Ithaca** | Robert Cantelmo | **Подтверждён (`confirmed`)** | Robert G. Cantelmo | [Официальная страница](https://www.cityofithacany.gov/131/Mayors-Office) | (607) 391-5862 | Не опубликован (веб-форма) | Отсутствует |
| **Freeport** | Robert T. Kennedy | **Подтверждён (`confirmed`)** | Robert T. Kennedy | [Официальная страница](https://www.freeportny.gov/360/Mayor) | (516) 377-2252 | Mayor@freeportny.gov | Отсутствует |
| **Valley Stream** | John Tufarelli | **Вице-мэр / попечитель (`incorrect`)** | Edwin A. Fare | [Официальная страница](https://valleystreamny.gov/mayor) | (516) 825-4200 | Не опубликован | Отсутствует |
| **Binghamton** | Al Libous | **Бывший мэр 1970-х (`former`)** | Jared M. Kraham | [Официальная страница](https://www.binghamton-ny.gov/government/elected-officials/office-of-the-mayor) | (607) 772-7001 | mayor@cityofbinghamton.gov | Отсутствует |
| **Glens Falls** | Roy Akins | **Бывший мэр 2000-х (`former`)** | Dr. Diana Palmer | [Официальная страница](https://www.cityofglensfallsny.gov/Directory.aspx?DID=16) | (518) 761-3805 | mayor@cityofglensfallsny.gov | Отсутствует |
| **Troy** | Edward Murphy | **Бывший мэр XIX века (`former`)** | Carmella Mantello | [Официальная страница](https://www.troyny.gov/318/Mayors-Office) | (518) 279-7156 | carmella.mantello@troyny.gov | Отсутствует |
| **Jamestown** | Samuel Teresi | **Бывший мэр (`former`)** | Kimberly Ecklund | [Официальная страница](https://www.jamestownny.gov/mayors-office/) | (716) 483-7600 | mayor@jamestownny.gov | Отсутствует |
| **Oswego** | John Gosek | **Бывший мэр (`former`)** | Robert A. Corradino | [Официальная страница](https://www.oswegony.gov/government/mayor.php) | (315) 342-8136 | mayor@oswegony.gov | Отсутствует |

---

## 2. Детальные результаты по каждому муниципалитету

### 1. New York City
- **ID записи:** `wb-muni-r0231-mayor-new-york-new-york`
- **Импортированное имя:** Zohran Mamdani
- **Фактический статус:** **Дубликат / кандидат (`duplicate / candidate`)**. В базе уже имеется основная верифицированная запись мэра Нью-Йорка `mayor-new-york-ne` (Eric Adams). Строка `wb-muni-r0231` дублирует муниципалитет. Рекомендуется удалить данный дубликат из импортированных кандидатов, сохранив основную запись `mayor-new-york-ne`.
- **Официальный URL:** [https://www.nyc.gov/office-of-the-mayor/](https://www.nyc.gov/office-of-the-mayor/)
- **Контакты:** (212) 639-9675 / 311.

### 2. Buffalo
- **ID записи:** `wb-muni-r0230-mayor-buffalo-new-york`
- **Импортированное имя:** Christopher Scanlon
- **Фактический статус:** **Бывший и.о. мэра (`former`)**. Кристофер Скэнлон был председателем совета и исполняющим обязанности мэра до 31 декабря 2025 года после отставки Байрона Брауна. Действующий 64-й мэр Буффало с 1 января 2026 года — **Sean Ryan**.
- **Официальный URL:** [https://www.buffalony.gov/490/Mayor](https://www.buffalony.gov/490/Mayor)
- **Контакты:** Телефон `(716) 851-4183`. Email: `MayorRyan@buffalony.gov`. Личный LinkedIn не опубликован.

### 3. Rochester
- **ID записи:** `wb-muni-r0232-mayor-rochester-new-york`
- **Импортированное имя:** Malik Evans
- **Фактический статус:** **Подтверждён (`confirmed`)**. Малик Д. Эванс (Malik D. Evans) — действующий 71-й мэр Рочестера (с января 2022 года).
- **Официальный URL:** [https://www.cityofrochester.gov/departments/mayors-office](https://www.cityofrochester.gov/departments/mayors-office)
- **Контакты:** Телефон `(585) 428-7045`. Email: `info@cityofrochester.gov`. Личный LinkedIn не опубликован.

### 4. Mount Vernon
- **ID записи:** `wb-muni-r1382-mayor-mount-vernon-new-york`
- **Импортированное имя:** Shawyn Patterson
- **Фактический статус:** **Подтверждён (`confirmed / truncated`)**. Фамилия была усечена в исходной таблице; действующий мэр — Шоуин Паттерсон-Говард (**Shawyn Patterson-Howard**).
- **Официальный URL:** [https://www.mountvernonny.gov/m/directory/department?did=17](https://www.mountvernonny.gov/m/directory/department?did=17)
- **Контакты:** Телефон `(914) 665-2362`. Прямой личный email не опубликован (обращения через муниципальную веб-форму). Личный LinkedIn не опубликован.

### 5. Schenectady
- **ID записи:** `wb-muni-r1424-mayor-schenectady-new-york`
- **Импортированное имя:** Gary R. McCarthy
- **Фактический статус:** **Подтверждён (`confirmed`)**. Гэри Р. Маккарти — действующий мэр Скенектади.
- **Официальный URL:** [https://www.cityofschenectady.gov/210/Mayors-Office](https://www.cityofschenectady.gov/210/Mayors-Office)
- **Контакты:** Телефон `(518) 382-5000`. Email: `gmccarthy@schenectadyny.gov`. Личный LinkedIn не опубликован.

### 6. Watertown
- **ID записи:** `wb-muni-r1558-mayor-watertown-new-york`
- **Импортированное имя:** Sarah Compo Pierce
- **Фактический статус:** **Подтверждён (`confirmed`)**. Сара Компо Пирс (Sarah V. Compo Pierce) — действующий мэр Уотертауна (в должности с 1 января 2024 года).
- **Официальный URL:** [https://www.watertown-ny.gov/mayorsoffice](https://www.watertown-ny.gov/mayorsoffice)
- **Контакты:** Телефон `(315) 785-7720`. Email: `spierce@watertown-ny.gov`. Личный LinkedIn не опубликован.

### 7. Ithaca
- **ID записи:** `wb-muni-r1565-mayor-ithaca-new-york`
- **Импортированное имя:** Robert Cantelmo
- **Фактический статус:** **Подтверждён (`confirmed`)**. Роберт Дж. Кантелмо (Robert G. Cantelmo) — действующий мэр Итаки (в должности с 1 января 2024 года).
- **Официальный URL:** [https://www.cityofithacany.gov/131/Mayors-Office](https://www.cityofithacany.gov/131/Mayors-Office)
- **Контакты:** Телефон `(607) 391-5862`. Прямой email не опубликован (обращения через муниципальную форму). Личный LinkedIn не опубликован.

### 8. Freeport
- **ID записи:** `wb-muni-r1801-mayor-freeport-new-york`
- **Импортированное имя:** Robert T. Kennedy
- **Фактический статус:** **Подтверждён (`confirmed`)**. Роберт Т. Кеннеди — действующий мэр деревни Фрипорт.
- **Официальный URL:** [https://www.freeportny.gov/360/Mayor](https://www.freeportny.gov/360/Mayor)
- **Контакты:** Телефон `(516) 377-2252`. Email: `Mayor@freeportny.gov`. Личный LinkedIn не опубликован.

### 9. Valley Stream
- **ID записи:** `wb-muni-r1921-mayor-valley-stream-new-york`
- **Импортированное имя:** John Tufarelli
- **Фактический статус:** **Исправить (`incorrect / trustee`)**. Джон Туфарелли является членом попечительского совета и вице-мэром деревни Долина Стрим. Действующий мэр — Эдвин А. Фэйр (**Edwin A. Fare / Ed Fare**).
- **Официальный URL:** [https://valleystreamny.gov/mayor](https://valleystreamny.gov/mayor)
- **Контакты:** Телефон `(516) 825-4200`. Личный email не опубликован. Личный LinkedIn не опубликован.

### 10. Binghamton
- **ID записи:** `wb-muni-r2177-mayor-binghamton-new-york`
- **Импортированное имя:** Al Libous
- **Фактический статус:** **Исправить (`former / deceased`)**. Альфред Дж. Либоус был мэром Бингемтона в 1969–1981 годах и скончался в 2016 году. Действующий мэр — **Jared M. Kraham** (с 1 января 2022 года).
- **Официальный URL:** [https://www.binghamton-ny.gov/government/elected-officials/office-of-the-mayor](https://www.binghamton-ny.gov/government/elected-officials/office-of-the-mayor)
- **Контакты:** Телефон `(607) 772-7001`. Email: `mayor@cityofbinghamton.gov`. Личный LinkedIn не опубликован.

### 11. Glens Falls
- **ID записи:** `wb-muni-r2224-mayor-glens-falls-new-york`
- **Импортированное имя:** Roy Akins
- **Фактический статус:** **Исправить (`former / deceased`)**. Ле Рой Б. Эйкинс-младший был мэром в 2006–2008 годах и скончался в 2008 году. Действующий мэр Гленс-Фолс — **Dr. Diana Palmer** (с 1 января 2026 года).
- **Официальный URL:** [https://www.cityofglensfallsny.gov/Directory.aspx?DID=16](https://www.cityofglensfallsny.gov/Directory.aspx?DID=16)
- **Контакты:** Телефон `(518) 761-3805`. Email: `mayor@cityofglensfallsny.gov`. Личный LinkedIn не опубликован.

### 12. Troy
- **ID записи:** `wb-muni-r2245-mayor-troy-new-york`
- **Импортированное имя:** Edward Murphy
- **Фактический статус:** **Исправить (`former / 19th century`)**. Эдвард Мерфи-младший был мэром в 1875–1883 годах. Действующий мэр Трои — **Carmella Mantello** (ранее частично внесена агентом Codex в покрытие).
- **Официальный URL:** [https://www.troyny.gov/318/Mayors-Office](https://www.troyny.gov/318/Mayors-Office)
- **Контакты:** Телефон `(518) 279-7156`. Email: `carmella.mantello@troyny.gov`. Личный LinkedIn не опубликован.

### 13. Jamestown
- **ID записи:** `wb-muni-r2258-mayor-jamestown-new-york`
- **Импортированное имя:** Samuel Teresi
- **Фактический статус:** **Исправить (`former`)**. Сэмюэл Терези был мэром до 2019 года. Действующий мэр Джеймстауна — **Kimberly Ecklund** (ранее частично внесена агентом Codex в покрытие).
- **Официальный URL:** [https://www.jamestownny.gov/mayors-office/](https://www.jamestownny.gov/mayors-office/)
- **Контакты:** Телефон `(716) 483-7600`. Email: `mayor@jamestownny.gov`. Личный LinkedIn не опубликован.

### 14. Oswego
- **ID записи:** `wb-muni-r2264-mayor-oswego-new-york`
- **Импортированное имя:** John Gosek
- **Фактический статус:** **Исправить (`former`)**. Джон Госек был мэром в 1992–2005 годах. Действующий мэр Осуиго — **Robert A. Corradino** (ранее частично внесён агентом Codex в покрытие).
- **Официальный URL:** [https://www.oswegony.gov/government/mayor.php](https://www.oswegony.gov/government/mayor.php)
- **Контакты:** Телефон `(315) 342-8136`. Email: `mayor@oswegony.gov` / `mayor@oswegony.org`. Личный LinkedIn не опубликован.
