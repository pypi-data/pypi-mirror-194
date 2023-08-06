import os
import datetime
import textwrap
from typing import Tuple

from TimetableToImage import Timetable
from PIL import Image, ImageDraw, ImageFont


def get_multiline_text_size(text_string: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    """
    Calculate size (width, height) of multiline text by text and font

    :param text_string:
    :param font:
    :return: Tuple of width and height
    """
    # https://stackoverflow.com/a/46220683/9263761
    strings = text_string.split('\n')
    text_width = 0
    ascent, descent = font.getmetrics()
    for line in strings:
        text_width = max(font.getmask(line).getbbox()[2], text_width)
    text_height = (ascent + descent) * len(strings)
    return text_width, text_height


def get_shifts_to_place_center(text: str, font: ImageFont.FreeTypeFont,
                               place_width: int = None, place_height: int = None) -> Tuple[int, int]:
    """
    Returns shift for draw text center of place

    :param text:
    :param font:
    :param place_width:
    :param place_height:
    :return: tuple of shifts
    """
    text_width, text_height = get_multiline_text_size(text, font)

    shift_x = None
    shift_y = None

    if place_width is not None:
        shift_x = (place_width - text_width) / 2
    if place_height is not None:
        shift_y = (place_height - text_height) / 2

    return shift_x, shift_y


def get_splitted_string(lesson: Timetable.Lesson, limit: int) -> str:
    """
    Return lesson text splitted by symbols limit in string

    :param lesson:
    :param limit:
    :return:
    """
    room = ""
    for letter in lesson.room:
        if letter != ' ':
            room += letter

    teacher = lesson.teacher
    teacher_words = teacher.split()
    teacher_flag = True
    if len(teacher_words) != 2:
        teacher_flag = False

    name = lesson.name
    if teacher_flag:
        t = ', '.join([name, teacher, room])
    else:
        t = name

    if teacher_flag:
        return textwrap.fill(text=t, width=limit)

    t_lines = textwrap.wrap(text=t, width=limit)

    last_line = t_lines[-1]

    t_last_line = last_line + ', ' + teacher
    t_wrap = textwrap.wrap(text=t_last_line, width=limit)
    if len(t_wrap) > 1:
        if len(textwrap.wrap(text=teacher + ',', width=limit)) == 1:
            t_lines[-1] += ','
            t_lines.append(teacher)

    else:
        t_lines.pop()
        t_lines += t_wrap

    last_line = t_lines[-1]
    t_last = last_line + ', ' + room
    if len(textwrap.wrap(text=t_last, width=limit)) == 1:
        t_lines[-1] = t_last
    else:
        t_lines[-1] += ',\n' + room

    string = '\n'.join(t_lines)

    return string


def get_table_row_letters_count(font, column_width):
    text_width = 0
    letters_count = 0
    while text_width < column_width:
        letters_count += 1
        text_width, _ = get_multiline_text_size("д" * letters_count, font)
    return letters_count - 1


def generate_from_timetable_week(
        timetable_week: Timetable.Week,
        timetable_bells: Timetable.Bells = None,
        inverted: bool = False,
        text_promotion: str = None,
        eng_lang: bool = False,
        font_path: str = None,
        resolution: Tuple[int, int] = (1920, 1080)) -> Image:
    """
    Generate FULL-HD image of timetable

    :param resolution: resolution of result image (default FullHD: 1920x1080)
    :param font_path: path to font
    :param timetable_week: Timetable.Week object
    :param timetable_bells: Timetable.Bells object
    :param inverted: set night theme of image
    :param text_promotion: promotion text on image
    :param eng_lang: set English language of headers and articles
    :return:
    """
    width, height = resolution
    full_hd = True if resolution == (1920, 1080) else False
    #
    have_bells = False
    if timetable_bells is not None:
        have_bells = True
    #
    font_size_article = 28 if not full_hd else 38
    font_size_header = 18 if not full_hd else 30
    font_size_table_large = 13 if not full_hd else 21
    font_size_table_small = 12 if not full_hd else 20
    #
    color_white = (255, 255, 255)
    color_black = (0, 0, 0)
    content_color = color_black
    background_color = color_white
    table_lines_width = 2 if not full_hd else 4
    if inverted:
        content_color = (202, 202, 232)
        background_color = (23, 33, 43)
        table_lines_width = 1 if not full_hd else 2
    #
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    #
    font_path_regular = os.path.join(os.path.dirname(__file__), "fonts", "Golos-UI",
                                     "font_regular.ttf")
    font_path_medium = os.path.join(os.path.dirname(__file__), "fonts", "Golos-UI",
                                    "font_medium.ttf")
    font_path_bold = os.path.join(os.path.dirname(__file__), "fonts", "Golos-UI",
                                  "font_bold.ttf")
    #
    font_exist = True
    if not (os.path.exists(font_path_regular) and
            os.path.exists(font_path_medium) and
            os.path.exists(font_path_bold)):
        font_exist = False
        print(font_path_regular, font_path_medium, font_path_bold)
    #
    if font_path is not None or not font_exist:
        if font_path is not None:
            if not os.path.exists(font_path):
                font_path = "calibri.ttf"
        else:
            font_path = "calibri.ttf"
        font_path_regular = font_path
        font_path_medium = font_path
        font_path_bold = font_path
    #
    font_regular_article = ImageFont.truetype(
        font_path_regular, font_size_article)
    font_bold_article = ImageFont.truetype(
        font_path_bold, font_size_article)
    #
    font_regular_header = ImageFont.truetype(
        font_path_regular, font_size_header)
    font_medium_header = ImageFont.truetype(
        font_path_medium, font_size_header)
    font_bold_header = ImageFont.truetype(
        font_path_bold, font_size_header)
    #
    font_regular_table_large = ImageFont.truetype(
        font_path_regular, font_size_table_large)
    #
    font_regular_table_small = ImageFont.truetype(
        font_path_regular,
        font_size_table_small)
    #
    article_height_k = 1.5
    table_header_row_height_k = 1.4
    table_header_rows_count = 2
    table_rows_count = 6
    table_left_header_width = get_multiline_text_size("00.00", font_bold_header)[0] + 20  # 60
    table_cols_count = 8
    x_left_text_article = 5
    y_top_table_header = font_size_article * article_height_k
    y_top_text_article = y_top_table_header / 5
    # article promotion
    if text_promotion is not None:
        text_width, _ = get_multiline_text_size(text_promotion, font_regular_article)
        shift_x, shift_y = get_shifts_to_place_center(
            text_promotion, font_regular_article,
            place_width=width, place_height=y_top_table_header)
        draw.text((shift_x, shift_y), text_promotion,
                  font=font_regular_article,
                  fill=content_color)

    if timetable_week.group:
        text_timetable_for_group = "Расписание группы: "
        if eng_lang:
            text_timetable_for_group = "Timetable for group: "
        # article "Timetable group: "
        _, shift_y = get_shifts_to_place_center(text_timetable_for_group, font_regular_article,
                                                place_height=y_top_table_header)
        draw.text((x_left_text_article, shift_y), text_timetable_for_group,
                  font=font_regular_article,
                  fill=content_color)
        # article group name
        x_left_text_group_name, _ = get_multiline_text_size(text_timetable_for_group,
                                                            font_regular_article)
        _, shift_y = get_shifts_to_place_center(timetable_week.group, font_bold_article,
                                                place_height=y_top_table_header)
        draw.text((x_left_text_article + x_left_text_group_name + 20, shift_y), timetable_week.group,
                  font=font_bold_article,
                  fill=content_color)

    # article week number
    if timetable_week.number is not None:
        text_week = "Неделя:"
        if eng_lang:
            text_week = "Week:"
        _, shift_y = get_shifts_to_place_center(text_week, font_regular_article,
                                                place_height=y_top_table_header)
        t_w, t_h = get_multiline_text_size(text_week, font_regular_article)
        x_left_text_week = width - 10 - 10 - get_multiline_text_size("99", font_bold_article)[
            0] - t_w
        draw.text((x_left_text_week, shift_y), text_week,
                  font=font_regular_article,
                  fill=content_color)
        shift_x, shift_y = get_shifts_to_place_center(
            str(timetable_week.number), font_bold_article,
            place_width=10 + 10 + get_multiline_text_size("99", font_bold_article)[0],
            place_height=y_top_table_header)
        t_w, t_h = get_multiline_text_size(str(timetable_week.number), font_bold_article)
        draw.text((width - t_w - shift_x, shift_y), str(timetable_week.number),
                  font=font_bold_article,
                  fill=content_color)

    # article week dates
    if timetable_week.begin is not None and timetable_week.end is not None:
        week_begin = timetable_week.begin.strftime("%d.%m")
        week_end = timetable_week.end.strftime("%d.%m")
        text_period = f"{week_begin} - {week_end}"
        text_period_width, _ = get_multiline_text_size(text_period, font_bold_article)
        _, shift_y = get_shifts_to_place_center(text_period, font_bold_article,
                                                place_height=y_top_table_header)
        draw.text((x_left_text_week - 20 - text_period_width, shift_y), text_period,
                  font=font_bold_article,
                  fill=content_color)

    # horizontal header
    for i in range(table_header_rows_count):
        draw.line((0, y_top_table_header + font_size_header * table_header_row_height_k * i, width,
                   y_top_table_header + font_size_header * table_header_row_height_k * i),
                  fill=content_color, width=table_lines_width)

    # horizontal table
    y_top_table = y_top_table_header + \
                  font_size_header * table_header_row_height_k * table_header_rows_count
    table_row_height = (height - y_top_table) / table_rows_count
    for i in range(table_rows_count):
        draw.line((0, y_top_table + table_row_height * i, width, y_top_table + table_row_height * i),
                  fill=content_color, width=table_lines_width)

    # vertical header + table
    x_left_table = table_left_header_width
    table_col_width = (width - table_left_header_width) / table_cols_count
    for i in range(table_cols_count):
        draw.line((x_left_table + table_col_width * i, y_top_table_header,
                   x_left_table + table_col_width * i, height), fill=content_color,
                  width=table_lines_width)

    table_row_letters_count_large = get_table_row_letters_count(font_regular_table_large,
                                                                table_col_width - table_lines_width)
    table_row_letters_count_small = get_table_row_letters_count(font_regular_table_small,
                                                                table_col_width - table_lines_width)

    # text pair
    text_pair = "Пара"
    if eng_lang:
        text_pair = "Pair"
    shift_x, shift_y = get_shifts_to_place_center(
        text_pair, font_regular_header,
        place_width=x_left_table,
        place_height=font_size_header * table_header_row_height_k)
    draw.text((shift_x - table_lines_width / 2, y_top_table_header + shift_y), text_pair,
              font=font_regular_header, fill=content_color)

    # text time
    text_time = "Время"
    if eng_lang:
        text_time = "Time"
    shift_x, shift_y = get_shifts_to_place_center(
        text_time, font_regular_header,
        place_width=x_left_table,
        place_height=font_size_header * table_header_row_height_k)
    draw.text((shift_x - table_lines_width / 2,
               y_top_table_header + font_size_header * table_header_row_height_k + shift_y),
              text_time,
              font=font_regular_header, fill=content_color)

    # pair number and time
    for i in range(table_cols_count):
        shift_x, shift_y = get_shifts_to_place_center(
            str(i + 1), font_regular_header,
            place_width=table_col_width,
            place_height=font_size_header * table_header_row_height_k)
        draw.text((x_left_table + table_col_width * i + shift_x, y_top_table_header + shift_y),
                  str(i + 1),
                  font=font_regular_header, fill=content_color)
        if have_bells:
            bell = timetable_bells.bells[i]
            bell: Timetable.Bell
            text_time = f"{bell.begin.strftime('%H:%M')}-{bell.end.strftime('%H:%M')}"
            shift_x, shift_y = get_shifts_to_place_center(
                text_time, font_regular_header,
                place_width=table_col_width,
                place_height=font_size_header * table_header_row_height_k)
            draw.text((x_left_table + table_col_width * i + shift_x,
                       y_top_table_header + font_size_header * table_header_row_height_k + shift_y),
                      text_time,
                      font=font_regular_header, fill=content_color)
    DAYS_NAME = Timetable.Week.DAYS_NAME_RU
    if eng_lang:
        DAYS_NAME = Timetable.Week.DAYS_NAME_EN
    # pairs by days
    for i in range(len(timetable_week.days)):
        timetable_day = timetable_week.days[i]
        timetable_day: Timetable.Day
        text_day = DAYS_NAME[i]
        # if date set - write it
        if timetable_day.date is not None:
            day_date = timetable_day.date
            day_date: datetime.date
            text_date = day_date.strftime("%d.%m")
            text_day += "\n" + text_date
        # write day of week
        x_shift, y_shift = get_shifts_to_place_center(
            text_day,
            font_bold_header,
            place_width=x_left_table,
            place_height=int(table_row_height)
        )
        draw.text((x_shift - table_lines_width, y_top_table + y_shift + table_row_height * i),
                  text_day, font=font_bold_header, fill=content_color, align="center")
        # write timetable
        x_left_pair = x_left_table
        for j, timetable_pair in enumerate(timetable_day.pairs):
            timetable_pair: Timetable.Pair
            y_top_pair = y_top_table + table_row_height * i
            lesson_font = font_regular_table_large
            row_split = table_row_letters_count_large
            single_lesson = True
            if len(timetable_pair.lessons) > 1:
                single_lesson = False
                lesson_font = font_regular_table_small
                row_split = table_row_letters_count_small
            for v, lesson in enumerate(timetable_pair.lessons):
                lesson: Timetable.Lesson
                text_lesson = get_splitted_string(lesson, row_split)
                text_width, text_height = get_multiline_text_size(text_lesson, lesson_font)
                # try to write text into cell
                target_height = table_row_height - table_lines_width
                if not single_lesson:
                    target_height = table_row_height / 2 - table_lines_width
                if text_height > target_height:
                    # if it doesn't fit, then change the font until it fits.
                    new_text_font = lesson_font
                    ind = 0
                    while text_height > target_height:
                        ind += 1
                        new_text_font = ImageFont.truetype(
                            font_path_regular,
                            new_text_font.size - 1)
                        new_limit = get_table_row_letters_count(new_text_font,
                                                                table_col_width - table_lines_width)
                        text_lesson = get_splitted_string(lesson, new_limit)
                        text_width, text_height = get_multiline_text_size(text_lesson,
                                                                          new_text_font)

                        lesson_font = new_text_font

                x_shift = (table_col_width - text_width) / 2
                if single_lesson:
                    y_shift = (table_row_height - text_height) / 2
                else:
                    y_shift = (table_row_height / 2 - text_height) / 2
                    if v == 1:
                        y_shift = (table_row_height / 2 - text_height) / 2 + table_row_height / 2

                draw.multiline_text(
                    (
                        x_left_pair + x_shift + table_col_width * j,
                        y_top_pair + y_shift
                    ),
                    text_lesson,
                    font=lesson_font,
                    fill=content_color,
                    align="center"
                )
    #
    return image
