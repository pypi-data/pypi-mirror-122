import os
import shutil
# --- 初始化环境 ---


def create_dir_if_not_exist(dirpath: str):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        return False
    return True


def run():
    src1 = os.path.join(os.path.dirname(__file__), os.path.join(os.path.join('templates', 'admin'), 'csv_form.html'))
    dst1 = os.path.join('templates', 'admin')

    src = os.path.join(os.path.dirname(__file__), os.path.join(os.path.join('templates', 'entities'), 'mychange_list.html'))
    dst = os.path.join('templates', 'entities')

    if os.path.exists(dst1) and os.path.exists(dst):
        return

    print('--- 首次引入bddjango, 初始化templates中...')
    create_dir_if_not_exist('templates')
    create_dir_if_not_exist(os.path.join('templates', 'admin'))
    create_dir_if_not_exist(os.path.join('templates', 'entities'))

    shutil.copy2(src1, dst1)
    shutil.copy2(src, dst)


if __name__ == '__main__':
    run()