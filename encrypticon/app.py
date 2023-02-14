import dearpygui.dearpygui as dpg
import pyperclip
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from encrypticon.utils import encrypt_file, generate_key


def add_encrypted_caption_to_filename(filename: str) -> str:
    """Add encrypted caption to filename."""
    return filename.split('.')[0] + '_зашифрован.' + filename.split('.')[1]


def start_app():
    # dearpygui setup
    dpg.create_context()
    dpg.create_viewport(title='Encrypticon', width=1000, height=300)
    dpg.setup_dearpygui()

    with dpg.font_registry():
        with dpg.font(
            './encrypticon/fonts/NotoSans-Regular.ttf', 20
        ) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    with dpg.value_registry():
        dpg.add_string_value(
            default_value='Не задано',
            tag="file_to_encrypt_path")
        dpg.add_string_value(
            default_value='Не задано',
            tag="encrypted_file_path")
        dpg.add_string_value(
            default_value='Не задано',
            tag="key")

    def open_file_dialogue():
        Tk().withdraw()
        filename = askopenfilename()
        dpg.set_value(
            item='file_to_encrypt_path',
            value=filename
        )
        dpg.show_item('save_button')

    def encrypt_selected_file():
        file = open(dpg.get_value('file_to_encrypt_path'), 'rb')
        file_content = file.read()

        key = generate_key()

        dpg.set_value(item='key', value=key.decode("utf-8"))
        pyperclip.copy(key.decode("utf-8"))
        dpg.show_item('key_copied')

        file.close()

        encrypted_content = encrypt_file(key, file_content)

        # dpg.show_item('encrypted_file')
        return encrypted_content

    def download_encrypted_file():
        Tk().withdraw()
        filename = asksaveasfilename(
            initialfile=add_encrypted_caption_to_filename(
                dpg.get_value('file_to_encrypt_path')
            )
        )
        with open(filename, 'wb') as file:
            file.write(encrypt_selected_file())

        dpg.set_value(
            item='encrypted_file_path',
            value=filename
        )
        dpg.show_item('generated_key')
        dpg.show_item('encrypted_file')

    # interface logic
    with dpg.window(label='Зашифровать', width=500, height=300):
        dpg.add_text('Зашифровать файл')

        dpg.add_button(
            label="Выбрать файл для шифровки",
            callback=open_file_dialogue
        )

        with dpg.group(horizontal=True, tag='file_to_encrypt'):
            dpg.add_text('Файл для шифровки: ')
            dpg.add_text(source='file_to_encrypt_path')

        dpg.add_button(
            label="Зашифровать файл",
            callback=download_encrypted_file,
            tag='save_button',
            show=False
        )

        with dpg.group(horizontal=True, tag='encrypted_file', show=False):
            dpg.add_text('Зашифрованный файл: ')
            dpg.add_text(source='encrypted_file_path')

        with dpg.group(horizontal=True, tag='generated_key', show=False):
            dpg.add_text('Ключ: ')
            dpg.add_input_text(source='key', readonly=True)

        dpg.add_text(
            'Ключ скопирован в буфер обмена.',
            color=[0, 255, 0],
            tag='key_copied',
            show=False
        )

        dpg.bind_font(default_font)

    with dpg.window(label='Зашифровать', width=500, height=300, pos=[500, 0]):
        dpg.add_text('Расшифровать файл')
        dpg.bind_font(default_font)

    dpg.bind_theme(global_theme)

    # dearpygui start
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
