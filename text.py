class Errors:
    er_in_db = 'Произошла ошибка при работе с БД, обратитесь в дурку.'
    
    def no_in_bd(name):
        sticker_id = 'CAACAgIAAxkBAAKFSWcaHD1wuD1hDX9OV32FoGKihgHgAAK6XgACss_hS2W6UCZcul39NgQ'
        error_text = f'Извините {name}, мы кажется незнакомы.'
        return error_text, sticker_id


class Buttons:
    pass


class Registration:
    successful_name = 'Допустим, будем знакомы'
    error_name_sticker = 'CAACAgIAAxkBAAKFQ2caGS6ev6eXUwq2iUQdSWPE_AxwAALeJQAC4t4RSKM1yvvWC1DmNgQ'
    error_name_text = 'что насчет русских буков и 2+ слов?'
    successful_group = 'Ааааа..., та самая группа'
    error_group_sticker = 'CAACAgIAAxkBAAKFXWcbpfSU8_oIUeG0EYKKZGzEFhHLAAKDQAAC1YIBSEfrXWbqHIFjNgQ'


class Debug:
    clear_states_sticker = 'CAACAgIAAxkBAAKFWmcbeRat3RWROyArsNln2OrKecIxAAKYIgACHuMRSHuQUoy3_lq1NgQ'


def generate_points_text(tech_points, art_points):
    if tech_points == 0:
        result = 'У вас нет инженерных баллов.\n'
    else:
        result = f'Количество инженерных баллов: {tech_points}.\n'
    
    if art_points == 0:
        result += 'У вас нет творческих баллов.'
    else:
        result += f'Количество творческих баллов: {art_points}.'
    
    return result


if __name__ == '__main__':
    pass