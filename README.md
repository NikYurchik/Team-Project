# First Team-Project

<!--
This is a bot-assistant.
Bot implemented as a console application.

Executes commands:

'hello' - responds to 'How can I help you?', goes into interactive mode and displays the invitation '>>'.
    The bot goes into interactive mode at startup without any parameters at all.

'add [--<key>] [<Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]]' - saves
    a new contact / phone / birthday / email / address / fullname in the phonebook.
    <key>: {contact | name} | phone | birthday | email | address | fullname

'change [--<key>] <Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]' - saves
    the new phone number / birthday / email / address / fullname of an existing contact in the phonebook.
    <key>: phone | birthday | email | address | fullname

'delete [--<key>] <Name> | <Phone>' - deleting a contact by name from the phone book / phone from a contact by name.
    <key>: {contact | name} | phone

'search <mask>' - search for contacts by fragment of name or by fragment of phone number.

'show [--<key>] [<Name>]' - displays the phone number for the specified contact / displays all saved contacts with phone numbers and birthday.
    <key>: {contact | name} | [all]
    With the --setting key, the bot displays all of its current settings.

'exit' - outputs 'Good bye!' and completes its work interactively.

'setting --<key> <value>' - set the value of the settings key.
    <key>: settings keys.
        request_missing_details - whether to request in the command mode the missing details of the contact;
        display_upcoming_birthdays - whether to display, when starting the bot, a list of contacts whose birthday falls within a specified period from the current day;
        number_of_days - number of days from the current day to display the list of contacts whose birthday falls within this period.
    First, the current value of the key is displayed, then confirmation of the change is requested.

If the bot is launched with the key and parameters, then it performs the specified operation and exits.
If the request for missing contact details is set in the settings,
then in the process of performing add and change operations, the bot will interactively request the missing details.
-->

<!--
Это бот-помощник.
Бот реализован в виде консольного приложения.

Выполняет команды:

'hello' - отвечает 'How can I help you?', переходит в интерактивный режим и отображает приглашение '>>'.
    В интерактивный режим бот переходит при запуске вообще без параметров.

'add [--<key>] [<Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]]' - сохраняет
    новый контакт / телефон / день рождения / электронная почта / адрес / полное имя в телефонной книге.
    <key>: {contact | name} | phone | birthday | email | address | fullname

'change [--<key>] <Name> [<Phone> | <BirthDay> | <Email> | <Address> | <FullName>]' - сохраняет
    новый номер телефона / день рождения / электронная почта / адрес / полное имя существующего контакта в телефонной книге.
    <key>: phone | birthday | email | address | fullname

'delete [--<key>] <Name> | <Phone>' - удаление контакта по имени из телефонной книги или телефона из контакта по имени.
    <key>: {contact | name} | phone

'search <mask>' - поиск контактов по фрагменту имени / номера телефона / дня рождения / электронной почты / адреса / полнго имени.

'show [--<key>] [<Name>]' - отображает номер телефона, день рождения, электронную почту, адрес, полное имя для указанного контакта
    или отображает все сохраненные контакты со всеми заполненными реквизитами.
    <key>: {contact | name} | [all] | setting
    С ключём --setting бот отображает все свои текущие настройки.

'exit' - в интерактивном режиме выводит 'Good bye!' и завершает свою работу.

'setting --<key> <value>' - установить значение ключа настроек.
    <key>: ключи настроек.
        request_missing_details - запрашивать ли в командном режиме недостающие реквизиты контакта;
        display_upcoming_birthdays - выводить ли при запуске бота список контактов, у которых день рождения попадает в заданный период от текущего дня;
        number_of_days - количество дней от текущего дня для вывода списка контактов, у которых день рождения приходится на этот период.
    Сначала выводится текущее значения ключа, затем запрашивается подтверждение изменения.

Если бот запускается с ключём и параметрами, то он выполняет заданную операцию и завершает работу.
Если в настройках задан запрос недостающих реквизит контакта,
то в процессе выполнения операций add и change бот в интерактивном режиме запросит недостающие реквизиты.
-->
