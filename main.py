from notebook_1 import Note
from time import sleep

filename = 'note.bin'


def main():
    assistant = Note()

    try:
        load = assistant.load_from_bin(filename)
    except FileNotFoundError:
        pass

    while True:

        commands = input(
            'Пожалуйста введите команду из списка доступных команд.\n>>>> ')

        if commands.lower() == 'help':
            func = assistant.hello()
            print(func)

        elif commands.lower() == 'add':
            tags = input(
                'Введите тег, или несколько тегов через кому.\n>>> ')
            tags = tags.split(',')
            note_text = input('Введите информацию по данному тегу.\n>>> ')
            assistant.add_note(note_text, tags)
            save = assistant.save_to_bin(filename)

        elif commands.lower() == 'find':
            keyword = input('Введите тег для поиска.\n>>> ')
            assistant.search_notes(keyword)

        elif commands.lower() == 'edit':
            inp = input(
                'Введите <<note>> если хотите редактировать заметку или <<tag>> если тег/\n>>> ')
            if inp == 'note':
                keyword = input('Введите тег для изменения заметки.\n>>> ')
                new_text = input('Введите новый текст заметки.\n>>> ')
                assistant.edit_note(keyword, new_text)

            elif inp == 'tag':
                keyword = input('Введите тег для изменения заметки.\n>>> ')
                new_text = input('Введите новый текст заметки.\n>>> ')
                new_text = new_text.split(',')
                assistant.edit_tag(keyword, new_text)

        elif commands.lower() == 'delete':
            keyword = input('Введите тег для удаления заметки.\n>>> ')
            assistant.delete_note(keyword)

        elif commands.lower() == 'del all':
            comm = assistant.delete_all()
            print(comm)

        elif commands.lower() == 'sort':
            tag = input('Введите тег для сортировки.\n>>> ')
            assistant.sort_notes_by_tag(tag)

        elif commands == 'show all':
            note_print = assistant.show()
            print(note_print)

        elif commands.lower() == 'show num':
            inp = input('Введите количество выведенных заметок\n>>> ')
            notes_generator = assistant.note_generator(inp)
            for two_notes in notes_generator:
                for note in two_notes:
                    print(note)
                print('')

        elif commands.lower() == 'close':
            save = assistant.save_to_bin(filename)
            print('Досвидания!!!')
            break

        else:
            delay = 2
            print('Неизвестная команда, пожалуйста введите команду повторно')
            sleep(delay)


if __name__ == '__main__':
    main()
