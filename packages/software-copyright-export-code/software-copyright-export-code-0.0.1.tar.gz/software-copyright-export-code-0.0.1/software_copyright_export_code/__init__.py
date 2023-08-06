__version__ = '0.0.1'
__author__ = 'Haoyu Pan'
__email__ = 'panhaoyu.china@outlook.com'

# 本脚本用于将文件转换为用于软著申请的脚本
import os
from pathlib import Path


def software_copyright_export_code(
        base_dir: Path,
        skipped_paths: set[Path],
        skipped_suffixes: set[Path],
        output_file: Path,
):
    # 指定一些需要跳过的文件夹，其所有的子文件夹都应当被跳过
    files = []
    for root, sub_dirs, sub_files in os.walk(base_dir):
        root = Path(root)
        if root in skipped_paths:
            continue
        if root.parent in skipped_paths or root.name in ('__pycache__',):
            skipped_paths.add(root)
            continue
        for file_name in sub_files:
            path = root / file_name
            if path in skipped_paths or path.suffix in skipped_suffixes:
                continue
            files.append(path)
    ext = {file.suffix for file in files}
    for f in files:
        print(f.relative_to(base_dir))
    print(ext)
    print(len(files))
    lines = []
    for f in files:
        name = f.name
        with open(f, 'r', encoding='utf-8') as fp:
            lines_of_file = fp.readlines()
        lines_of_file = [line.strip() for line in lines_of_file]
        lines_of_file = [line for line in lines_of_file if line]
        if not lines_of_file:
            continue
        placeholder = '#' * len(name)
        lines.append(f'############{placeholder}######')
        lines.append(f'##### start {name} #####')
        lines.append(f'############{placeholder}######')
        lines.extend(lines_of_file)
        lines.append(f'##########{placeholder}######')
        lines.append(f'##### end {name} #####')
        lines.append(f'##########{placeholder}######')
    words = ('external',)
    lines = [line for line in lines if not any(w in line for w in words)]
    print(len(lines))
    result = '\n'.join(lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
